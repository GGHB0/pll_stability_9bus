---
name: dashboard-zoom-export
description: Controles do dashboard — botão de zoom na janela de falta (sincronizado entre figuras) e export PNG hi-res do modebar
---

# Zoom na Falta e Export PNG (renderer.py)

Adicionados em 2026-07 junto com [[chart-analysis-overlays]].

> **Overlay fantasma removido (2026-07-25)**: o botão "Comparar PLL"
> (`#ghost-toggle`) sobrepunha os traces do cenário equivalente do outro modo
> PLL — removido a pedido do usuário por não estar sendo usado. Saíram
> `ghostMode`, `_exactEquiv`, `_ghostData`, `toggleGhost` e o bloco `gbtn` em
> `_syncCtrlButtons`; o toggle nominal/sintonia inadequada
> ([[bad-pll-dashboard-filter]]) é uma feature separada e não foi afetado.

## Zoom na falta

Botão `#zoom-fault` na filter-bar. `_applyZoom()` usa `Plotly.relayout` com
dotted-path (**válido em relayout**, ao contrário de `Plotly.react` — ver
[[dark-mode-theming]]):

```javascript
var upd = (zoomFault && sc.tFault != null)
  ? { "xaxis.range": [...], "xaxis.autorange": false }
  : { "xaxis.autorange": true };
TIME_TABS.forEach(function(t) {          // ["inv","sys"] — res sem gráfico, spec fora (Hz)
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

Inversor/Sistema são gráficos Plotly separados (Resumo não tem gráfico
desde 2026-07-24); `matches` não cruza figuras. `_bridgeZoom(srcWhich)`
escuta `plotly_relayout` de cada gd de
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

## Sincronização de estado (`_syncCtrlButtons`)

Chamado no início de `switchScenario` e no toggle de zoom. Regras:

- Cenário sem falta (`tFault == null`): zoom desliga e desabilita.
- Label segue a regra de [[header-branding]]: o texto descreve a **próxima
  ação** ("Zoom na falta" ↔ "Visão completa"), com classe `.active` para o
  estado ligado (CSS `.diag-btn.active` / `:disabled`).

## 📸 Export PNG hi-res

`PLOTLY_CFG.toImageButtonOptions = { format: "png", scale: 3 }` (era svg).
`_renderChart` seta o filename dinâmico por cenário/seção:

```javascript
PLOTLY_CFG.toImageButtonOptions.filename =
  "pll_" + currentKey.split("/").join("_") + "_" + which;
```

O botão de câmera do modebar exporta a figura 3× — resolução pronta para as
figuras do TCC DOCX. O fundo exportado segue o tema ativo (paper_bgcolor).
