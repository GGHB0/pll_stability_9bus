---
name: dark-mode-theming
description: Gotcha do tema escuro no dashboard HTML — annotations/shapes de chart.py têm cor fixa e precisam de override manual no JS
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
