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
                      # (FFT, IAE/ISE/ts). Medido nos dados (bus6/1phase):
                      # pior sinal é |V| Bus 2, que acomoda em 0.078 s
TOL_RAD  = 0.02       # ±1.15° — critério de acomodação do PLL (rad)

# Limiares de classificação: (bom_máx, moderado_máx); acima → crítico
IAE_THRESH      = (0.05,  0.15)   # rad·s — erro de fase pós-falta
ISE_THRESH      = (0.005, 0.020)  # rad²·s
TS_DELTA_THRESH = (0.10,  0.30)   # s após t_fault
PEAK_ERR_DEG_THRESH = (20.0, 60.0)  # ° — pico de |erro de fase| pós-falta
ERR_SS_DEG_THRESH   = (0.5,  1.0)   # ° — erro de fase SUSTENTADO em regime permanente
                                    # (média de |e| após a acomodação; PLL bem
                                    # sintonizado tende a ~0°)
SYNC_LOSS_DEG    = 90.0           # ° — acima disso: perda de sincronismo do PLL
VBUS_AVG_THRESH  = (0.90,  0.50)  # pu — severidade do afundamento (LVRT IEEE 1547);
                                  # aplicado à tensão MÉDIA (regime: período
                                  # inteiro; falta: só a janela t_fault–t_clear)
LVRT_THRESHOLD   = 0.88           # pu — linha de referência no gráfico

# ── Espectro de Fourier ─────────────────────────────────────────────────────
SPEC_FMAX_HZ   = 2000.0   # Hz — limite superior do espectro calculado/exibido
SPEC_XRANGE_HZ = 1500.0   # Hz — range default do eixo x: cobre harmônicas e f_res LCL
                          # (duplo-clique revela até FMAX)
F_FUND_HZ      = 60.0     # Hz — fundamental no abc; seq. negativa da falta cai aqui
F_2H_HZ        = 120.0    # Hz — fundamental de seq. negativa refletida no dq
                          # (n=1 negativa → -(n+1)f₁); NÃO é a 2ª harmônica
F_RES_LCL_HZ   = 1443.4   # Hz — ressonância do filtro LCL (ω_res = 9068.99 rad/s)

# Frequências marcadas no espectro abc (vline tracejada + rótulo): fundamental,
# harmônicas ímpares características do inversor e ressonância do filtro LCL.
SPEC_MARKERS = (
    (F_FUND_HZ,      "f<sub>1</sub>"),
    (3 * F_FUND_HZ,  "3f<sub>1</sub>"),
    (5 * F_FUND_HZ,  "5f<sub>1</sub>"),
    (7 * F_FUND_HZ,  "7f<sub>1</sub>"),
    (F_RES_LCL_HZ,   "f<sub>res</sub> LCL"),
)

# Frequências marcadas no espectro dq: a fundamental (n=1 positiva) vira DC e sai
# com a média; a fundamental de seq. negativa da falta reflete em 2f₁; as ordens
# 5ª/7ª colidem em 6f₁ e 11ª/13ª em 12f₁ — ver
# kb/standards/harmonic_dq_frame_mapping.md.
SPEC_MARKERS_DQ = (
    (F_2H_HZ,        "2f<sub>1</sub>"),
    (6 * F_FUND_HZ,  "6f<sub>1</sub>"),
    (12 * F_FUND_HZ, "12f<sub>1</sub>"),
    (F_RES_LCL_HZ,   "f<sub>res</sub> LCL"),
)

# Cores por segmento temporal: {segmento: (light, dark)}. No espectro abc há
# três segmentos (pré-falta/durante a falta/pós-falta); cenários em regime
# permanente (sem falta) usam só "Regime".
SPEC_SEG_COLORS = {
    "Pré-falta":       ("#64748b", "#94a3b8"),  # cinza
    "Durante a falta": ("#dc2626", "#f87171"),  # vermelho
    "Pós-falta":       ("#2563eb", "#60a5fa"),  # azul
    "Regime":          ("#2563eb", "#60a5fa"),
}

# Segmentos isentos de checagem normativa na tabela de harmônicas: os limites
# do IEEE 519/1547 são critérios de regime permanente — aplicá-los durante o
# curto-circuito em si geraria falsos positivos triviais (distorção alta
# durante falta é esperada, não é o que a norma mede).
SPEC_SEG_NO_NORM = ("Durante a falta",)

# ── Limites normativos de harmônico — IEEE 519-2014 / IEEE 1547-2018 ────────
# Unidade geradora conectada à Barra 2 (20 kV, classe 1 kV<V≤69 kV), linha
# Isc/IL<20 obrigatória para geração (IEEE 519-2014 Tab.2, nota "c"); ver
# kb/standards/harmonic_significance_criteria.md.
# Corrente, harmônicos ímpares h<11 (mesmo valor no IEEE 1547-2018 §7.3):
CURR_ODD_LIMIT_PU   = 0.04
# Corrente, pares h<11 — escala progressiva "Relaxed Evens" do IEEE 1547-2018
# (Tabela 15; o 519-2014 usa 25% flat do ímpar em vez disso, ver KB):
CURR_EVEN_LIMITS_PU = {2: 0.01, 4: 0.02, 6: 0.03}
# Tensão, IEEE 519-2014 Tabela 1, classe 1 kV<V≤69 kV — limite individual
# flat (a norma não varia o limite de TENSÃO por ordem, só o de corrente):
VOLT_INDIVIDUAL_LIMIT_PU = 0.03
# Desequilíbrio dq (h=2ª/120 Hz = sequência negativa) — patamar empírico da
# TeseAGP §5.2.2 (~2-3% já tratado como "distúrbio"; sem base normativa):
DQ_UNBALANCE_WARN_PU = 0.02
DQ_UNBALANCE_HIGH_PU = 0.03

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
