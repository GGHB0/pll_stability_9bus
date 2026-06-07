---
name: numpy-pandas-plotly-pipeline
description: Pipeline de análise de sinais temporais com NumPy/Pandas/Plotly — padrões usados no src/ deste projeto
---

# NumPy · Pandas · Plotly — Pipeline de Sinais

> **Contexto**: padrões específicos usados em `src/loader.py`, `src/chart.py`, `src/renderer.py`
> para análise dos sinais exportados do Simulink.

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

## Subplots Plotly multi-painel

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

n = 5   # número de painéis
fig = make_subplots(rows=n, cols=1, shared_xaxes=True, vertical_spacing=0.05)

fig.add_trace(
    go.Scatter(x=t, y=np.degrees(theta_err),
               name="Erro (°)", mode="lines",
               line=dict(width=1.8, color="#2563eb")),
    row=1, col=1,
)

# Linha horizontal de tolerância
fig.add_hline(y=np.degrees(TOL_RAD),
              line=dict(color="rgba(220,50,50,0.45)", width=1.1, dash="dash"),
              row=1, col=1)

# Linha vertical da falta
fig.add_vline(x=T_FAULT,
              line=dict(color="rgba(100,100,100,0.25)", width=1.1, dash="dot"),
              row=1, col=1)
```

## Tema light/dark via JSON + JS

Estratégia usada em `src/renderer.py`: exportar a figura como JSON e injetar
no HTML — o JS faz `Plotly.relayout` + `Plotly.restyle` por traço.

```python
import json

fig_json   = fig.to_json()                              # string JSON da figura
light_cols = json.dumps(["#2563eb", "#dc2626", ...])    # cores por traço
dark_cols  = json.dumps(["#60a5fa", "#f87171", ...])
trace_idx  = json.dumps([0, 1, 2, ...])                 # índices dos traços
```

No JS:
```javascript
var figData = /* JSON injetado pelo Python */;
Plotly.newPlot(gd, figData.data, figData.layout, {responsive: true});

function toggleTheme() {
  Plotly.relayout(gd, isDark ? LAYOUT_DARK : LAYOUT_LIGHT);
  traceIdx.forEach(function(ti, i) {
    Plotly.restyle(gd, {"line.color": [cols[i]]}, [ti]);
  });
}
```

## trace_map — rastreamento de cores por traço

```python
trace_map: list[tuple[int, str, str]] = []
# (índice do traço na fig, cor light, cor dark)

def add(trace, row, lc, dc):
    fig.add_trace(trace, row=row, col=1)
    trace_map.append((len(fig.data) - 1, lc, dc))
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

Definidas em `src/config.py` como `LIGHT_COLORS` / `DARK_COLORS`.

## See Also

- [File Parser](file-parser.md) — padrão geral de leitura de arquivos
- [Clean Architecture](clean-architecture.md) — estrutura do pacote `src/`
- `src/loader.py`, `src/chart.py`, `src/renderer.py` — implementação real
