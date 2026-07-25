---
name: dark-mode-legend-title-fixes
description: Continuação de dark-mode-theming — legenda invisível no dark (chaves dotted) e barra de título de painel re-temada por engano (cinza em vez de branco)
---

# Tema Escuro: Legendas e Barra de Título (renderer.py)

Continuação de [[dark-mode-theming]] (fragmentado pelo limite de 200
linhas). Fix 1-3 (annotations/shapes/eixos) estão lá; aqui vão Fix 4 e 5.

## Fix 4 (2026-07-05): legenda invisível no dark — mesmas chaves dotted

Usuário reportou "legenda no modo dark não aparece". Mesma classe de bug do
Fix 2, em outras vítimas: `BASE_DARK`/`BASE_LIGHT` ainda carregavam
`"font.color"`, `"legend.bgcolor"` e `"hoverlabel.*"` como chaves dotted —
ignoradas pelo `Plotly.react`. O `layout.font.color` ficava preso no
`#111827` gravado pelo `chart.py`: texto de legenda `#111827` sobre paper
`#111827` = literalmente invisível.

Agravante: as legendas são **múltiplas e nomeadas** (`legend`, `legend2`, …
— uma por painel, ver [[construcao-graficos]]), então um único
`"legend.bgcolor"` nunca cobriria as demais; e as legendas internas dos
painéis pareados têm `bgcolor: rgba(255,255,255,0.8)` fixo (branco no dark).

Fix (`themedLayout`): `BASE_*` viraram paletas planas (`{paper, plot, font,
legendInnerBg, hoverBg, hoverBorder}`) aplicadas **aninhadas**:

```javascript
var base = {
  paper_bgcolor: C.paper, plot_bgcolor: C.plot,
  font: Object.assign({}, figData.layout.font, { color: C.font }),
  hoverlabel: Object.assign({}, figData.layout.hoverlabel,
                            { bgcolor: C.hoverBg, bordercolor: C.hoverBorder }),
};
// no mesmo loop dos eixos:
if (k.startsWith("legend")) {
  var lg = figData.layout[k] || {};
  var upd = { font: Object.assign({}, lg.font, { color: C.font }) };
  if (lg.bgcolor && lg.bgcolor !== "rgba(0,0,0,0)") upd.bgcolor = C.legendInnerBg;
  axUpd[k] = Object.assign({}, lg, upd);
}
```

Só a bgcolor das legendas **internas** (semi-opacas) é re-temada
(`rgba(26,36,54,0.85)` no dark); as externas seguem transparentes.
Verificado via `gd._fullLayout.legendN.font.color` nos dois temas.

## Fix 5 (2026-07-25): barra de título do painel ficava cinza em vez de branca

Usuário reportou que a fonte do título dos gráficos deveria ser branca —
já era, em `chart.py`/`spectrum.py` (`_label` grava `font.color="#ffffff"`
na annotation da barra). O bug estava só no JS: desde o redesign de títulos
(`b2bbb2a`, 2026-07-21) `_label` passou a usar `xref="paper"` **igual**
ao `_group_title`, mas o `isGroupTitle` do Fix 1 checava só `a.xref ===
"paper"` — os dois tipos de annotation caíam no mesmo ramo e a barra de
título também levava a cor cinza/slate do `_group_title`, sobrescrevendo o
branco gravado no Python.

A distinção real entre os dois hoje: `_label` usa `yref="paper"` (a barra
é posicionada em coordenadas de página); `_group_title` usa `yref="y...
domain"` (ancorado ao domínio do eixo Y daquela linha). Fix — checar os
dois refs e **não tocar** na cor da barra de título (deixar `a` como veio,
já com o branco certo do Python):

```javascript
var annotations = (figData.layout.annotations || []).map(function(a) {
  var isGroupTitle = a.xref === "paper" && a.yref !== "paper";
  if (!isGroupTitle) return a;   // barra de título: cor fixa, não re-temar
  var color = isDarkMode ? "#cbd5e1" : "#334155";
  return Object.assign({}, a, { font: Object.assign({}, a.font, { color: color }) });
});
```

Mesmo padrão do Fix 3 (shapes): ao re-temar uma coleção em massa, sempre
filtrar pelo subconjunto certo — `xref` sozinho não bastava mais depois que
duas features passaram a compartilhar o mesmo valor.
