"""
config.py — Constantes globais do projeto PLL-IEEE9Bus.
"""

from pathlib import Path

# ── Caminhos ────────────────────────────────────────────────────────────────
PROJ_ROOT  = Path(__file__).resolve().parent.parent.parent
CSV_PATH   = PROJ_ROOT / "output" / "sim_data.csv"
HTML_OUT   = PROJ_ROOT / "output" / "pll_metrics.html"

# ── Parâmetros de simulação ─────────────────────────────────────────────────
T_FAULT  = 0.2        # fallback (s) se fault_info.json não existir
T_SETTLE = 0.1        # s — transitório de partida do PLL, excluído de TODO cálculo
                      # (FFT, IAE/ISE/ts, ΔP/ΔQ). Medido nos dados (bus6/1phase):
                      # pior sinal é |V| Bus 2, que acomoda em 0.078 s
TOL_RAD  = 0.02       # ±1.15° — critério de acomodação do PLL (rad)

# Limiares de classificação: (bom_máx, moderado_máx); acima → crítico
IAE_THRESH      = (0.05,  0.15)   # rad·s — erro de fase pós-falta
ISE_THRESH      = (0.005, 0.020)  # rad²·s
TS_DELTA_THRESH = (0.10,  0.30)   # s após t_fault
DP_THRESH       = (0.10,  0.50)   # pu — excursão de P na janela pós-clear
DQ_THRESH       = (0.15,  0.60)   # pu — excursão de Q na janela pós-clear
PEAK_ERR_DEG_THRESH = (20.0, 60.0)  # ° — pico de |erro de fase| pós-falta
SYNC_LOSS_DEG    = 90.0           # ° — acima disso: perda de sincronismo do PLL
VBUS2_MIN_THRESH = (0.90,  0.50)  # pu — severidade do afundamento (LVRT IEEE 1547)
LVRT_THRESHOLD   = 0.88           # pu — linha de referência no gráfico

# ── Espectro de Fourier ─────────────────────────────────────────────────────
SPEC_FMAX_HZ   = 2000.0   # Hz — limite superior do espectro calculado/exibido
SPEC_XRANGE_HZ = 1500.0   # Hz — range default do eixo x: cobre harmônicas e f_res LCL
                          # (duplo-clique revela até FMAX)
F_2H_HZ        = 120.0    # Hz — 2ª harmônica no dq (sequência negativa da falta)
F_RES_LCL_HZ   = 1443.4   # Hz — ressonância do filtro LCL (ω_res = 9068.99 rad/s)

# Cores por segmento temporal: {segmento: (light, dark)}
SPEC_SEG_COLORS = {
    "Pré-falta": ("#64748b", "#94a3b8"),
    "Falta":     ("#dc2626", "#f87171"),
    "Pós-falta": ("#2563eb", "#60a5fa"),
    "Regime":    ("#2563eb", "#60a5fa"),
}

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
