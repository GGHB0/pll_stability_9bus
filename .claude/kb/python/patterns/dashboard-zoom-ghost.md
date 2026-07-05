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
function _zoomUpd(figData, range) {
  var upd = {};
  Object.keys(figData.layout).forEach(function(k) {
    if (k.indexOf("xaxis") === 0) {
      if (range) { upd[k + ".range"] = range; upd[k + ".autorange"] = false; }
      else       { upd[k + ".autorange"] = true; }
    }
  });
  return upd;
}
Plotly.relayout(gdInv, _zoomUpd(sc.invData, range));
if (sc.hasSys) Plotly.relayout(gdSys, _zoomUpd(sc.sysData, range));
```

### Gotcha ⚠️ `shared_xaxes` não cobre a coluna 2

`shared_xaxes=True` no make_subplots liga os eixos por `matches` **por
coluna**: setar só `"xaxis.range"` zooma a cadeia da coluna 1, mas os painéis
pareados (P/Q Bus na coluna 2) têm cadeia própria e ficam de fora. Por isso
`_zoomUpd` varre **todas** as chaves `xaxis*` do layout da figura.

Como `Plotly.react` reseta o range, `_applyZoom()` é chamado **depois** dos
reacts em `switchScenario` e `toggleTheme` — o zoom persiste entre cenários
e temas.

## 👻 Fantasma nominal × BAD_PLL

Botão `#ghost-toggle` (renderizado só se `has_bad_pll`). Sobrepõe os traces
do cenário equivalente do outro modo PLL no mesmo gráfico:

- `_exactEquiv(key)`: par exato `key ↔ key + "_bad_pll"` — **sem** fallback
  para `_firstOfMode` (diferente de `_findEquiv`); sem par → botão disabled.
- `_ghostData(which)`: mapeia só os índices de `invIdx`/`sysIdx` (traces de
  dados — exclui marcador tₛ e envelope LVRT) com **a mesma cor** do trace
  principal + `dash:"dot"`, `width:1.2`, `opacity:0.5`, `showlegend:false`,
  `hoverinfo:"skip"` (o hover unificado ficaria ilegível em dobro).
- Injetado em `reactThemedChart` via `.concat(_ghostData(which))` — o
  parâmetro `which` ("inv"/"sys") foi adicionado à assinatura.

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
`reactThemedChart` seta o filename dinâmico por cenário/seção:

```javascript
PLOTLY_CFG.toImageButtonOptions.filename =
  "pll_" + currentKey.split("/").join("_") + "_" + which;
```

O botão de câmera do modebar exporta a figura 3× — resolução pronta para as
figuras do TCC DOCX. O fundo exportado segue o tema ativo (paper_bgcolor).
