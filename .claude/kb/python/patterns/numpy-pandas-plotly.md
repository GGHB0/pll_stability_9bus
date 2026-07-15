---
name: numpy-pandas-plotly-pipeline
description: Pipeline de análise de sinais temporais com NumPy/Pandas/Plotly — padrões usados no src/ deste projeto
---

# NumPy · Pandas · Plotly — Pipeline de Sinais

> **Contexto**: padrões específicos usados em `src/pipeline/loader.py`, `src/pipeline/chart.py`,
> `src/report/renderer.py` para análise dos sinais exportados do Simulink.

## Leitura de CSV com Pandas

```python
from pathlib import Path
import pandas as pd
import numpy as np

df = pd.read_csv(Path("output/sim_data.csv"))
cols = set(df.columns)

# Detecção de formato (8 ou 10 colunas)
has_ref = {"id_ref_pu", "iq_ref_pu"} <= cols

# Array NumPy a partir de coluna
t = df["t_s"].to_numpy()
P = df["P_pu"].to_numpy()
```

## Máscara temporal (janela pós-falta)

```python
T_FAULT = 0.5
mask = t >= T_FAULT          # array booleano
t_pf  = t[mask]
e_pf  = theta_err[mask]
```

## Integração numérica — `np.trapezoid`

> ⚠️ `np.trapz` foi **removido** no NumPy 2.0. Usar `np.trapezoid`.

```python
IAE = float(np.trapezoid(np.abs(e_pf), t_pf))   # ∫|e| dt
ISE = float(np.trapezoid(e_pf ** 2,    t_pf))   # ∫e² dt
```

## Tempo de acomodação (settling time)

```python
TOL_RAD = 0.02   # ±1.15°
fora = t_pf[np.abs(e_pf) > TOL_RAD]
ts   = float(fora[-1]) if len(fora) else float(t_pf[0])
```

## Subplots Plotly — layout misto (single / pair)

`ChartBuilder.build_sections()` retorna `(fig_inv, fig_sys, tm_inv, tm_sys)` — duas
figuras separadas (Inversor UFV e Sistema 9-Bus), cada uma com layout de 2 colunas
onde linhas podem ser full-width (`_S`) ou par lado-a-lado (`_P`, não usado atualmente).

```python
_S = "single"   # linha inteira — colspan 2
_P = "pair"     # dois subplots lado a lado

specs = [
    [{"type": "scatter", "colspan": 2}, None] if r[0] == _S
    else [{"type": "scatter"}, {"type": "scatter"}]
    for r in rows
]
fig = make_subplots(rows=n, cols=2, shared_xaxes=True,
                    vertical_spacing=0.07, specs=specs)
```

Painéis combinados (múltiplas curvas no mesmo subplot):
- `dq_combined` — id med, id ref, iq med, iq ref  
- `vdq_combined` — Vd Rede, Vq Rede, Vd Inv, Vq Inv  
- `pq_combined` — P UFV, Q UFV

Contador de eixos `ax` incrementa +1 por linha `_S`, +2 por linha `_P`.

## Multi-legenda (uma por subplot)

Cada traço recebe `trace.legend = "legend{n}"` antes de ser adicionado.
`_place_legends()` posiciona cada legenda:
- Linhas `_S`: fora à direita (`x=1.01`, `xanchor="left"`)
- Linhas `_P`: dentro do subplot, canto superior-direito

```python
key = "legend" if ax == 1 else f"legend{ax}"
fig.update_layout(**{key: dict(x=1.01, y=y_mid, ...)})
```

## Tema light/dark — duas figuras

Exportar cada figura como JSON e injetar no HTML:

```python
fig_json = fig.to_json()  # string JSON
```

No JS, `axisUpdates()` itera `Object.keys(figData.layout)` para encontrar
todos os eixos dinamicamente (robusto a qualquer configuração):

```javascript
function axisUpdates(figData, isDarkMode) {
  var upd = {};
  Object.keys(figData.layout).forEach(function(k) {
    if (k.startsWith("xaxis") || k.startsWith("yaxis")) {
      upd[k+".gridcolor"]     = isDarkMode ? "#1f2937" : "#f1f5f9";
      upd[k+".zerolinecolor"] = isDarkMode ? "#374151" : "#e5e7eb";
    }
  });
  return upd;
}
function applyTheme(gd, figData, lightC, darkC, tIdx, isDark) {
  Plotly.relayout(gd, Object.assign({}, isDark ? BASE_DARK : BASE_LIGHT,
                                    axisUpdates(figData, isDark)));
  tIdx.forEach(function(ti, i) {
    Plotly.restyle(gd, {"line.color": [(isDark ? darkC : lightC)[i]]}, [ti]);
  });
}
// toggleTheme() re-tema a figura da aba ativa (as demais ficam "sujas")
```

## trace_map — rastreamento de cores por traço

```python
trace_map: list[tuple[int, str, str]] = []
# (índice do traço na fig, cor light, cor dark)
# adicionado em ChartBuilder._add() a cada go.Scatter inserido
```

## Encoding no Windows

```python
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

Necessário para caracteres como `Δ`, `θ`, `·` no PowerShell/cmd.

## Paletas de cor do projeto

| Variável | Light | Dark |
|---|---|---|
| azul | `#2563eb` | `#60a5fa` |
| vermelho | `#dc2626` | `#f87171` |
| verde | `#16a34a` | `#4ade80` |
| laranja | `#ea580c` | `#fb923c` |
| violeta | `#9333ea` | `#c084fc` |
| ciano | `#0891b2` | `#22d3ee` |

Definidas em `src/config/settings.py` como `LIGHT_COLORS` / `DARK_COLORS`.

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

## See Also

- [File Parser](file-parser.md) — padrão geral de leitura de arquivos
- [Clean Architecture](clean-architecture.md) — estrutura do pacote `src/`
- `src/pipeline/loader.py`, `src/pipeline/chart.py`, `src/report/renderer.py` — implementação real
