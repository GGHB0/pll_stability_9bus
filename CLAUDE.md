# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TCC (Trabalho de Conclusão de Curso) em Engenharia Elétrica — UERJ 2025. Investigates the dynamic behavior of the **SRF-PLL** (Synchronous Reference Frame Phase-Locked Loop) algorithm in grid-tied inverters under severe network contingencies, motivated by the August 15, 2023 Brazilian grid disturbance that disconnected 22,547 MW (~31% of national load).

## Repository Layout

```
pll_stability_9bus/
├── pll_stability_9bus.slx              ← main Simulink model (root)
├── params.m                            ← MATLAB workspace setup for the main model
├── pll_stability_9bus_faultInfo.xml    ← Fault Analyzer metadata for the main model
├── notebooks/
│   └── pll_stability_9bus_analysis.ipynb   ← analytical parameter calculation
├── simulink/                           ← auxiliary Simulink models
│   ├── pll_stability_9bus_FaultModel.slx
│   ├── GridTiedInverterOptimalI2.slx   ← MathWorks reference example
│   ├── GridTiedInverterOptimalIData.m  ← params for the reference example
│   ├── teste_isolado.slx               ← isolated sandbox
│   └── archive/
│       └── pll_stability_9bus.slx.original   ← backup of pre-modification model
├── scripts/                            ← Python analysis scripts
├── assets/                             ← diagrams, banner, figures
└── .claude/                            ← knowledge base + skills (see below)
```

Before simulating the main model, run `params.m` in MATLAB to populate the workspace. Auxiliary models in `simulink/` are standalone (not referenced by the main model).

## Running the Notebook

```bash
jupyter notebook notebooks/pll_stability_9bus_analysis.ipynb
# or
jupyter lab
```

Dependencies: `numpy`, `pandas`, `math` (standard library). No `requirements.txt` exists — install manually if needed:

```bash
pip install numpy pandas jupyter
```

Run all cells top-to-bottom; cells are sequentially dependent (variables defined in earlier cells are reused throughout).

## Simulink Models

Open `.slx` files in **MATLAB/Simulink** (R202x). The model simulates EMT (Electromagnetic Transient) scenarios for four contingency types: symmetric voltage sag, asymmetric voltage sag (introduces negative sequence → 2nd harmonic oscillations in PLL), phase-angle jump, and high RoCoF.

## System Parameters (key values used across notebook and model)

- Base: 20 kV / 100 MVA / 60 Hz
- IEEE 9-bus network; inverter connected at Bus 2
- Thevenin impedance computed as `Z_ii` diagonal of `inv(Ybarra)` at the connection bus
- LCL filter resonance: `ω_res = 9068.99 rad/s`, damping `ξ = 0.707`, switching freq `fs = 5 kHz`
- PLL gains derived from: `Kp = 8·60·(L1+L2+Lest)`, `Ki = 32·60²·(L1+L2+Lest)`

## Notebook Architecture

The notebook follows a linear calculation pipeline:

1. **Network construction** — builds `Ybarra` via `montar_Ybarra()`, inverts to get `Zbarra`
2. **Thevenin equivalent** — extracts `Z22` (diagonal element at connection bus)
3. **LCL filter sizing** — computes `L1`, `L2`, `Cf`, damping resistors `Rd1`/`Rd2`
4. **Controller design** — PLL gains `Kp`/`Ki` and current controller tuning (pole-zero cancellation)

The `montar_Ybarra(n_barras, entrebarras, impedancias_barra, retornar)` function is the core utility: pass `retornar="Y"` for admittance matrix, `retornar="Z"` for impedance matrix (inverts internally).

## Performance Metrics

Results are evaluated by: IAE (Integral Absolute Error of phase angle), ISE (Integral Square Error), phase error settling time, active/reactive power oscillations, and LVRT compliance per IEEE 1547-2018.

## Knowledge Base (.claude/)

The `.claude/` directory contains the project's persistent knowledge system:

```
.claude/
├── kb/                        ← knowledge bases (Markdown, max 200 lines each)
│   ├── project-scope.md       ← full TCC scope, chapter status, contingency table
│   ├── pll/                   ← SRF-PLL theory, Kp/Ki methodology, contingency scenarios
│   ├── inverter/              ← LCL filter, Simulink model architecture
│   ├── power-system/          ← IEEE 9-bus topology, Thevenin methodology
│   ├── simulation/            ← notebook↔params.m workflow, Vcc override, runtime config
│   └── standards/             ← LVRT, IEEE 1547-2018
├── commands/
│   └── git.yaml               ← project git workflow conventions
├── rules/
│   └── limits.md              ← file size limits and kb folder map
└── skills/
    └── slx-explorer/          ← skill for inspecting .slx files via Python/XML
```

### Inspecting the Simulink Model Without MATLAB

`.slx` files are ZIP archives containing XML. Use Python to read them directly:

```python
import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile('pll_stability_9bus.slx', 'r') as z:
    xml = z.read('simulink/blockdiagram.xml').decode('utf-8', errors='replace')
```

Key system SIDs: root network (`system_root`), UFV Model/VSI (`3896`), Optimal Controller (`3963`), PWM Control/PI+Notch (`3974`), PWM comparator (`3997`). See `kb/inverter/simulink_model.md` for full map.

### Kp/Ki Gain Note

Gains are divided by 4 **twice**: once in the notebook (pu conversion, Z_base = 4 Ω) and once inside the Simulink Gain blocks. The double division compensates for a ~6× mismatch between V_base_LN and Vcc/2 in the SPWM normalization, combined with a ×2 factor from the notebook formula using `(L1+L2+Lest)` instead of `Lest`.
