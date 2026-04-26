# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TCC (Trabalho de Conclusão de Curso) em Engenharia Elétrica — UERJ 2025. Investigates the dynamic behavior of the **SRF-PLL** (Synchronous Reference Frame Phase-Locked Loop) algorithm in grid-tied inverters under severe network contingencies, motivated by the August 15, 2023 Brazilian grid disturbance that disconnected 22,547 MW (~31% of national load).

## Repository Contents

| File | Purpose |
|---|---|
| `pll_stability_9bus_analysis.ipynb` | Analytical parameter calculation (Ybarra/Zbarra, Thevenin impedance, LCL filter sizing, PLL and current controller gains) |
| `pll_stability_9bus.slx` | MATLAB/Simulink EMT model — grid-tied VSI with SRF-PLL on IEEE 9-bus system |
| `GridTiedInverterOptimalI2.slx` | Secondary Simulink model (grid-tied inverter variant) |

## Running the Notebook

```bash
jupyter notebook pll_stability_9bus_analysis.ipynb
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
