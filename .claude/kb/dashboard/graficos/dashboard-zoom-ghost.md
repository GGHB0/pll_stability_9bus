---
name: dashboard-zoom-ghost
description: Controles novos do dashboard — botão de zoom na janela de falta, overlay fantasma nominal×BAD_PLL e export PNG hi-res do modebar
---

# Zoom na Falta, Fantasma PLL e Export PNG (renderer.py)

Adicionados em 2026-07 junto com [[chart-analysis-overlays]].

## 🔍 Zoom na falta

Botão `#zoom-fault` na filter-bar. `_applyZoom()` usa `Plotly.relayout` com
dotted-path (**válido em relayout**, ao contrário de `Plotly.react` — ver
[[dark-mode-theming]]):

```javascript
var upd = (zoomFault && sc.tFault != null)
  ? { "xaxis.range": [...], "xaxis.autorange": false }
  : { "xaxis.autorange": true };
TIME_TABS.forEach(function(t) {          // ["res","inv","sys"] — spec fora (Hz)
  if (_plotted(t)) Plotly.relayout(gd[t], upd);
});
```

Desde as abas ([[tabs-navegacao]]), só gráficos `_plotted(t)` (div com
`.data` e flag `_dirty` limpa) recebem relayout — um gráfico sujo é
renderizado do zero ao abrir a aba e ganha o zoom vigente na sequência.

### Gotcha ⚠️ `shared_xaxes` não cobre a coluna 2

`shared_xaxes=True` no make_subplots liga os eixos por `matches` **por
coluna**: os painéis pareados (P/Q Bus na coluna 2) têm cadeia própria e não
seguem zoom feito na coluna 1 — nem por botão, nem por arrasto. Fix na
origem (`chart.py::_apply_layout`): linkar todo eixo não-raiz ao raiz:

```python
for ax_name in self._fig.layout:
    if ax_name.startswith("xaxis") and ax_name != "xaxis":
        self._fig.layout[ax_name].matches = "x"
```

Com isso basta atualizar `"xaxis.range"` que a figura inteira segue — e o
zoom **manual** (arrasto) em qualquer painel também move os demais.

### Sincronização entre figuras (`_bridgeZoom`)

Resumo/Inversor/Sistema são gráficos Plotly separados; `matches` não cruza
figuras. `_bridgeZoom(srcWhich)` escuta `plotly_relayout` de cada gd de
`TIME_TABS` e replica o range nas demais figuras plotadas. Detalhes:

- `_extractXZoom(ev)` aceita os três formatos de payload: `"xaxisN.range"`
  (array), `"xaxisN.range[0]"/"[1]"` (arrasto real do usuário) e
  `"xaxisN.autorange"` (duplo-clique).
- Trava `_syncingZoom` evita loop infinito (o relayout replicado dispararia a
  ponte de volta); `_applyZoom` também usa a trava.
- `.on` só existe após o 1º plot do div — `_ensureBridges()` registra sob
  demanda em `switchTab` (com lazy render, um gd pode nunca ter sido plotado).
- Handlers `.on` sobrevivem a `Plotly.react` (ficam no elemento DOM).

Como `Plotly.react` reseta o range, `_applyZoom()` é chamado **depois** dos
reacts em `switchScenario` e `toggleTheme` — o zoom do botão persiste entre
cenários e temas (o zoom manual não persiste: react restaura autorange).

## 👻 Fantasma nominal × BAD_PLL

Botão `#ghost-toggle` (renderizado só se `has_bad_pll`). Sobrepõe os traces
do cenário equivalente do outro modo PLL no mesmo gráfico:

- `_exactEquiv(key)`: par exato `key ↔ key + "_bad_pll"` — **sem** fallback
  para `_firstOfMode` (diferente de `_findEquiv`); sem par → botão disabled.
- `_ghostData(which)`: mapeia só os índices de `invIdx`/`sysIdx`/`specIdx`
  (traces de dados — exclui marcador tₛ e envelope LVRT) com **a mesma cor**
  do trace principal + `dash:"dot"`, `width:1.2`, `opacity:0.5`,
  `showlegend:false`, `hoverinfo:"skip"` (o hover unificado ficaria ilegível
  em dobro).
- Injetado em `_renderChart` via `.concat(_ghostData(which))` — o
  parâmetro `which` ("res"/"inv"/"sys"/"spec") seleciona a figura pelo
  acesso genérico `o[which + "Data"]`. No espectro
  ([[espectro-fourier]]) o ghost compara direto o pico de 120 Hz
  nominal × PLL com sintonia inadequada.

Mesma cor + pontilhado/esmaecido = "mesmo sinal, outro PLL" — a degradação
aparece lado a lado sem alternar o toggle de memória.

## Sincronização de estado (`_syncCtrlButtons`)

Chamado no início de `switchScenario` e nos toggles. Regras:

- Cenário sem falta (`tFault == null`): zoom desliga e desabilita.
- Sem par exato: fantasma desliga e desabilita.
- Labels seguem a regra de [[header-branding]]: o texto descreve a **próxima
  ação** ("Zoom na falta" ↔ "Visão completa"; "Comparar PLL" ↔ "Ocultar
  comparação"), com classe `.active` para o estado ligado
  (CSS `.diag-btn.active` / `:disabled`).

## 📸 Export PNG hi-res

`PLOTLY_CFG.toImageButtonOptions = { format: "png", scale: 3 }` (era svg).
`_renderChart` seta o filename dinâmico por cenário/seção:

```javascript
PLOTLY_CFG.toImageButtonOptions.filename =
  "pll_" + currentKey.split("/").join("_") + "_" + which;
```

O botão de câmera do modebar exporta a figura 3× — resolução pronta para as
figuras do TCC DOCX. O fundo exportado segue o tema ativo (paper_bgcolor).
