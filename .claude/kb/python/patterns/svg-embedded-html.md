---
name: python-svg-embedded-html
description: SVG interativo embutido no HTML gerado em Python — onclick, f-strings e o bug crítico de aspas dentro de f-string
aliases: [python-svg-embedded-html]
---

# SVG interativo embutido no HTML

Fragmentado de [[numpy-pandas-plotly-pipeline]]. Uso no dashboard em [[estrutura-html]].

## SVG interativo embutido no HTML

`assets/diagrams/ieee9bus_unifilar.svg` é embutido inline via `_svg_section_html()` no renderer.
Cada elemento clicável é um `<g data-loc="busN">` ou `<g data-loc="lineA_B">` com:
- `<rect class="hit">` — área de clique transparente com `pointer-events:all`
- `<rect class="hlr">` — highlight ring azul (opacity 0 → 1 via CSS `.svg-active`)

O JS adiciona `.has-data` nos grupos cujo `data-loc` aparece em `SCENARIOS` como prefixo.
`highlightSVG(key)` remove `.svg-active` global e aplica no grupo do cenário ativo.
É chamado ao final de `switchScenario()` para sincronizar diagrama ↔ `<select>`.

```javascript
// Mapeamento loc → [key1, key2, ...] construído no load
var svgLocMap = {};
Object.keys(SCENARIOS).forEach(function(k) {
  var loc = (k === "regime") ? "regime" : k.split("/")[0];
  if (!svgLocMap[loc]) svgLocMap[loc] = [];
  svgLocMap[loc].push(k);
});
```

Clique com 1 cenário → `switchScenario()` direto. Múltiplos → tooltip via DOM.

### ⚠️ Bug crítico: onclick em string dentro de f-string Python

**NUNCA** montar atributo `onclick="..."` com aspas duplas dentro de string JS
que está dentro de f-string Python `f"""..."""`. O `\"` não escapa dentro de
triple-quoted strings — produz `\"` literal no JS, gerando syntax error silencioso
que impede o script inteiro de executar.

```javascript
// ERRADO (syntax error no JS): onclick com aspas duplas dentro de string JS
html += "<button onclick=\"_fn('" + k + "')\">label</button>"
// CORRETO — criar elemento via DOM e atribuir .onclick como função
var btn = document.createElement("button");
btn.onclick = (function(key) { return function() { _fn(key); }; })(k);
```

O `<style>` do SVG inline torna-se CSS global — usar seletores específicos
(`.svg-node`, `.svg-active`) para não vazar estilos para o resto da página.

