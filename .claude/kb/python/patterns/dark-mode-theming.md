---
name: dark-mode-theming
description: Gotcha do tema escuro no dashboard HTML — annotations/shapes com cor fixa, bug de chave "eixo.propriedade" flat no axUpd, e plot_bgcolor sem contraste com o card
---

# Tema Escuro: Annotations e Shapes de `chart.py`

## Contexto

Reportado em 2026-07: "os gráficos no dark mode ficaram horríveis de enxergar".
Causa: `_label` e `_group_title` em
[chart.py](../../../../src/pipeline/chart.py) desenham texto via
`fig.add_annotation(..., font=dict(color="#fixo"))` — cor hardcoded pensada
só para fundo claro. Diferente de `layout.font.color` (que cascade pros eixos
e legendas), a cor de uma annotation **não herda** do tema global; fica presa
no valor gravado no JSON da figura.

`themedLayout()` (JS, em `renderer.py`) só reaplicava `paper_bgcolor`,
`font.color` e `gridcolor`/`zerolinecolor` por eixo — nunca tocava em
`layout.annotations` nem `layout.shapes`. Resultado no dark mode:
`_group_title` (`#334155`, cinza-ardósia escuro) ficava quase invisível sobre
o fundo `#111827`; `_label` (`#6b7280`) também com contraste baixo.

## Fix (`renderer.py`, `themedLayout`)

Como Plotly não expõe uma "classe" para annotation, a distinção usa um campo
que já existe e é estável: `xref`.

- `_label` (rótulo de painel, ex. "P Bus 1 (pu)") sempre usa
  `xref = "x domain"` ou `f"x{{n}} domain"` — nunca `"paper"`.
- `_group_title` (subtítulo "BARRA N") sempre usa `xref="paper"`.

```javascript
var annotations = (figData.layout.annotations || []).map(function(a) {
  var isGroupTitle = a.xref === "paper";
  var color = isDarkMode
    ? (isGroupTitle ? "#cbd5e1" : "#9ca3af")
    : (isGroupTitle ? "#334155" : "#6b7280");
  return Object.assign({}, a, { font: Object.assign({}, a.font, { color: color }) });
});
var shapes = (figData.layout.shapes || []).map(function(s) {
  return Object.assign({}, s, {
    line: Object.assign({}, s.line, { color: isDarkMode ? "#374151" : "#e2e8f0" })
  });
});
return Object.assign({}, figData.layout, base, axUpd, { annotations: annotations, shapes: shapes });
```

`shapes` só contém a linha divisória do `_group_title` (único `add_shape` em
`chart.py`) — por isso dá pra reaplicar cor uniformemente em todos os shapes
sem precisar diferenciar por tipo.

## Gotcha ⚠️ se adicionar nova annotation/shape em `chart.py`

Qualquer novo `add_annotation`/`add_shape` com cor fixa em `chart.py` **não**
vai se re-temar sozinho — precisa entrar explicitamente em `themedLayout()`.
Se o novo elemento não puder ser distinguido por `xref`, usar outro campo
estável (ex. `font.size`) como critério, seguindo o mesmo padrão.

## Fix 2 (2026-07): bug real era outro — chave "eixo.propriedade" nunca aplicava

Usuário reportou que **continuava** ruim de enxergar mesmo após o fix acima.
Investigação revelou a causa raiz de verdade: `axUpd` construía chaves flat
tipo `"xaxis.gridcolor"` (string com ponto) e mesclava tudo com um único
`Object.assign` no nível raiz do layout:

```javascript
// bug: cria uma propriedade literal chamada "xaxis.gridcolor" no objeto,
// NÃO faz layout.xaxis.gridcolor = ... (Plotly.react não entende dotted-path
// em layout novo — isso só funciona em Plotly.relayout/restyle)
axUpd[k + ".gridcolor"] = isDarkMode ? "#1f2937" : "#f1f5f9";
...
return Object.assign({}, figData.layout, base, axUpd, {...});
```

Resultado: `gridcolor`/`zerolinecolor` **nunca foram sobrescritos** em nenhum
tema — todo eixo ficava preso no valor claro gravado pelo `chart.py`
(`gridcolor: "#f0f2f5"`, quase branco), invisível sobre qualquer fundo escuro.
Confirmado inspecionando `gd._fullLayout.xaxis.gridcolor` (retornava o valor
claro) vs. `gd.layout["xaxis.gridcolor"]` (a chave malformada existia, mas
solta, sem efeito).

Fix — construir o objeto do eixo aninhado corretamente, com spread das
props originais:

```javascript
var axUpd = {};
Object.keys(figData.layout).forEach(function(k) {
  if (k.startsWith("xaxis") || k.startsWith("yaxis")) {
    axUpd[k] = Object.assign({}, figData.layout[k], {
      gridcolor:     isDarkMode ? "#31425c" : "#f1f5f9",
      zerolinecolor: isDarkMode ? "#4b5d7a" : "#e5e7eb",
    });
  }
});
```

Aproveitado para também clarear `plot_bgcolor` no dark mode — antes era
idêntico ao `paper_bgcolor` (`#111827`, igual ao `--card-bg` do CSS), então a
área de plotagem não tinha nenhuma separação visual do card ao redor.
Agora `BASE_DARK.plot_bgcolor = "#1a2436"` (um tom acima), com grid/zeroline
recalibrados para contraste com esse novo fundo.

### Gotcha ⚠️ geral sobre `Plotly.react`

Nunca usar chaves `"eixo.propriedade"` (dotted string) num objeto de layout
passado para `Plotly.react`/`Plotly.newPlot` — isso só é válido em
`Plotly.relayout(gd, {"xaxis.gridcolor": ...})`. Para atualizar uma
propriedade de eixo dentro de um layout completo, sempre aninhar:
`layout.xaxis = Object.assign({}, layout.xaxis, { prop: valor })`.

## Fix 3 (2026-07): re-tema de shapes engolia as linhas de falta/LVRT

O map de `shapes` do Fix 1 repintava **todas** as shapes com o cinza da
divisória — mas `add_vline`/`add_hline`/`add_vrect` do `chart.py` também
viram entradas em `layout.shapes`. Resultado: as vlines vermelhas de falta,
os limites LVRT e a banda de tolerância eram repintados de cinza claro a
cada `Plotly.react` (troca de tema OU de cenário), nos DOIS temas.

Fix — filtrar pela mesma chave estável usada nas annotations: só a divisória
do `_group_title` tem `xref === "paper"`:

```javascript
var shapes = (figData.layout.shapes || []).map(function(s) {
  if (s.xref !== "paper") return s;  // shapes de dados mantêm cor semântica
  return Object.assign({}, s, { line: ... });
});
```

Corolário do gotcha do Fix 1: ao re-temar coleções (`annotations`, `shapes`)
em massa, **sempre filtrar pelo subconjunto que realmente precisa** — o
Plotly joga vlines/hlines/vrects na mesma lista que shapes manuais.
