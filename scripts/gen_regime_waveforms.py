"""
Gera os graficos do cenario 'regime' (regime permanente, sem falta, PLL
nominal) em assets/charts/ -- um SVG + PNG por grafico, sem Plotly, matplotlib
puro, com a paleta do projeto (src/config/settings.py) e as mesmas convencoes
de series do dashboard (dq: medido solido + ref tracejado; vdq: Rede solido +
Inversor pontilhado -- ver src/pipeline/chart.py kind="dq_combined"/"vdq_combined").

Graficos:
  regime_correntes_abc.svg  -- i_a, i_b, i_c            (janela 0,55-0,60 s, 3 ciclos)
  regime_tensoes_abc.svg    -- v_a, v_b, v_c             (mesma janela)
  regime_potencia_pq.svg    -- P, Q                      (0-0,6 s completo)
  regime_corrente_dq.svg    -- i_d/i_q medido + ref       (0-0,6 s completo)
  regime_tensao_dq.svg      -- v_d/v_q Rede + Inversor    (0-0,6 s completo)

Requer matplotlib (nao listado em requirements.txt -- so usado por este
gerador de figura, nao pelo pipeline principal do dashboard).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── paleta do projeto (src/config/settings.py, LIGHT_COLORS) ────────────────
AZUL, VERMELHO, VERDE, LARANJA = "#2563eb", "#dc2626", "#16a34a", "#ea580c"
NAVY = "#0B132B"
GRID_COLOR = "#e2e8f0"
T_SETTLE = 0.1

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Segoe UI", "Arial"],
    "font.size": 10,
    "axes.edgecolor": "#94a3b8",
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": "#334155",
    "ytick.color": "#334155",
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "svg.fonttype": "none",   # mantem texto editavel no SVG (nao vira path)
})

LEGEND_KW = dict(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9)


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def new_fig():
    fig, ax = plt.subplots(figsize=(6.4, 3.4), dpi=150)
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.13, right=0.97)
    return fig, ax


def legend_above(ax, handles, labels, ncol):
    """Legenda fora da area de plot, entre o titulo e o topo do eixo --
    evita cobrir as ondas trifasicas (nao ha canto livre nelas)."""
    ax.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 1.02),
              ncol=ncol, fontsize=9, **LEGEND_KW)


def save(fig, name):
    svg_path = OUT_DIR / f"{name}.svg"
    png_path = OUT_DIR / f"{name}.png"
    fig.savefig(svg_path, format="svg")
    fig.savefig(png_path, format="png", dpi=220, facecolor="white")
    plt.close(fig)
    print("OK", svg_path)


def mark_settle(ax):
    """Sombreia e marca o transitorio de partida (T_SETTLE), excluido de
    todo calculo do dashboard -- mesma convencao de src/config/settings.py."""
    ax.axvspan(0, T_SETTLE, color="#94a3b8", alpha=0.15, zorder=0)
    ax.axvline(T_SETTLE, color="#94a3b8", linewidth=1.0, linestyle="--", zorder=1)
    ax.text(T_SETTLE, ax.get_ylim()[1],
             "  transitório de partida excluído dos cálculos (T$_{settle}$ = 0,1 s)",
             fontsize=7.5, color="#64748b", va="top", ha="left")


# ── dados ─────────────────────────────────────────────────────────────────
d_pq = pd.read_csv(ROOT / "output/results/regime/sim_data.csv")
d_abc = pd.read_csv(ROOT / "output/results/regime/sim_data_abc.csv")

win = d_abc[(d_abc.t_s >= 0.55) & (d_abc.t_s <= 0.60)].iloc[::8].copy()
win["t_ms"] = win.t_s * 1000

fase_cores = [("Fase a", AZUL), ("Fase b", VERMELHO), ("Fase c", VERDE)]

# 1. correntes abc ------------------------------------------------------
fig, ax = new_fig()
for col, (_, color) in zip(["ia_ufv_pu", "ib_ufv_pu", "ic_ufv_pu"], fase_cores):
    ax.plot(win.t_ms, win[col], color=color, linewidth=1.4)
style_axes(ax)
ax.set_ylabel("Corrente (pu)")
ax.set_xlabel("Tempo (ms)")
ax.set_title("Correntes trifásicas do inversor -- regime permanente", pad=32)
legend_above(ax, [plt.Line2D([0], [0], color=c) for _, c in fase_cores],
             [l for l, _ in fase_cores], ncol=3)
save(fig, "regime_correntes_abc")

# 2. tensoes abc ----------------------------------------------------------
fig, ax = new_fig()
for col, (_, color) in zip(["va_ufv_pu", "vb_ufv_pu", "vc_ufv_pu"], fase_cores):
    ax.plot(win.t_ms, win[col], color=color, linewidth=1.4)
style_axes(ax)
ax.set_ylabel("Tensão (pu)")
ax.set_xlabel("Tempo (ms)")
ax.set_title("Tensões trifásicas do inversor -- regime permanente", pad=32)
legend_above(ax, [plt.Line2D([0], [0], color=c) for _, c in fase_cores],
             [l for l, _ in fase_cores], ncol=3)
save(fig, "regime_tensoes_abc")

# 3. potencia P/Q -----------------------------------------------------------
fig, ax = new_fig()
ax.plot(d_pq.t_s, d_pq.P_ufv_pu, color=AZUL, linewidth=1.2, label="$P$")
ax.plot(d_pq.t_s, d_pq.Q_ufv_pu, color=LARANJA, linewidth=1.2, label="$Q$")
style_axes(ax)
ax.set_ylabel("Potência (pu)")
ax.set_xlabel("Tempo (s)")
ax.set_title("Potência ativa e reativa do inversor")
ax.set_xlim(0, 0.6)
mark_settle(ax)
ax.legend(loc="lower right", fontsize=9, **LEGEND_KW)
save(fig, "regime_potencia_pq")

# 4. corrente dq (medido solido + ref tracejado, como no dashboard) ---------
fig, ax = new_fig()
ax.plot(d_pq.t_s, d_pq.id_ufv_pu, color=AZUL, linewidth=1.3, label=r"$i_d$ med.")
ax.plot(d_pq.t_s, d_pq.id_ufv_ref_pu, color=AZUL, linewidth=1.6, linestyle="--", label=r"$i_d$ ref")
ax.plot(d_pq.t_s, d_pq.iq_ufv_pu, color=VERMELHO, linewidth=1.3, label=r"$i_q$ med.")
ax.plot(d_pq.t_s, d_pq.iq_ufv_ref_pu, color=VERMELHO, linewidth=1.6, linestyle="--", label=r"$i_q$ ref")
style_axes(ax)
ax.set_ylabel("Corrente (pu)")
ax.set_xlabel("Tempo (s)")
ax.set_title("Corrente do inversor no referencial dq")
ax.set_xlim(0, 0.6)
mark_settle(ax)
ax.legend(loc="lower right", ncol=2, fontsize=9, **LEGEND_KW)
save(fig, "regime_corrente_dq")

# 5. tensao dq (Rede solido + Inversor pontilhado, como no dashboard) -------
fig, ax = new_fig()
ax.plot(d_pq.t_s, d_pq.vd_rede_pu, color=AZUL, linewidth=1.4, label=r"$v_d$ Rede")
ax.plot(d_pq.t_s, d_pq.vq_rede_pu, color=VERMELHO, linewidth=1.4, label=r"$v_q$ Rede")
ax.plot(d_pq.t_s, d_pq.vd_ufv_pu, color=AZUL, linewidth=1.3, linestyle=":", label=r"$v_d$ Inversor")
ax.plot(d_pq.t_s, d_pq.vq_ufv_pu, color=VERMELHO, linewidth=1.3, linestyle=":", label=r"$v_q$ Inversor")
style_axes(ax)
ax.axhline(0.0, color="#94a3b8", linewidth=1.0, linestyle=":", zorder=0)
ax.set_ylabel("Tensão (pu)")
ax.set_xlabel("Tempo (s)")
ax.set_title("Tensão no referencial dq")
ax.set_xlim(0, 0.6)
mark_settle(ax)
ax.legend(loc="lower right", ncol=2, fontsize=9, **LEGEND_KW)
save(fig, "regime_tensao_dq")
