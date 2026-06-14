"""
config.py — Constantes globais do projeto PLL-IEEE9Bus.
"""

from pathlib import Path

# ── Caminhos ────────────────────────────────────────────────────────────────
PROJ_ROOT  = Path(__file__).resolve().parent.parent
CSV_PATH   = PROJ_ROOT / "output" / "sim_data.csv"
HTML_OUT   = PROJ_ROOT / "output" / "pll_metrics.html"

# ── Parâmetros de simulação ─────────────────────────────────────────────────
T_FAULT  = 0.5        # instante da falta (s)
TOL_RAD  = 0.02       # ±1.15° — critério de acomodação do PLL (rad)

# Limiares de classificação: (bom_máx, moderado_máx); acima → crítico
IAE_THRESH      = (0.05,  0.15)   # rad·s
ISE_THRESH      = (0.005, 0.020)  # rad²·s
TS_DELTA_THRESH = (0.10,  0.30)   # s após T_FAULT
DP_THRESH       = (0.10,  0.30)   # pu
DQ_THRESH       = (0.15,  0.40)   # pu

# ── Paletas de traços ────────────────────────────────────────────────────────
# Light mode
LIGHT_COLORS = [
    "#2563eb",  # azul
    "#dc2626",  # vermelho
    "#16a34a",  # verde
    "#ea580c",  # laranja
    "#9333ea",  # violeta
    "#0891b2",  # ciano
    "#ca8a04",  # âmbar
    "#db2777",  # rosa
]

# Dark mode (versões pastel para fundo escuro)
DARK_COLORS = [
    "#60a5fa",
    "#f87171",
    "#4ade80",
    "#fb923c",
    "#c084fc",
    "#22d3ee",
    "#fbbf24",
    "#f472b6",
]
