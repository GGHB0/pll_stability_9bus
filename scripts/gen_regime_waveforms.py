"""
Gera os graficos dos cenarios 'regime' e 'regime_bad_pll' (regime permanente,
sem falta -- PLL nominal e sintonia inadequada) em assets/charts/ -- um SVG +
PNG por grafico, sem Plotly, matplotlib puro, com a paleta do projeto
(src/config/settings.py) e as mesmas convencoes de serie do dashboard (dq:
medido solido + ref tracejado; vdq: Rede solido + Inversor pontilhado -- ver
src/pipeline/chart.py kind="dq_combined"/"vdq_combined").

Por cenario, 5 graficos (prefixo = SCENARIOS[i]["prefix"]):
  <prefixo>_correntes_abc.svg  -- i_a, i_b, i_c            (janela final, 3 ciclos)
  <prefixo>_tensoes_abc.svg    -- v_a, v_b, v_c             (mesma janela)
  <prefixo>_potencia_pq.svg    -- P, Q                      (0-t_end completo)
  <prefixo>_corrente_dq.svg    -- i_d/i_q medido + ref       (0-t_end completo)
  <prefixo>_tensao_dq.svg      -- v_d/v_q Rede + Inversor    (0-t_end completo)

O cenario 'regime_bad_pll' (Kp/Ki_pll x0,2, ver [[project_bad_pll]] na KB)
assenta muito mais devagar que o nominal -- empiricamente ~0,55 s (ultima vez
que P/Q se afastam >0,08 pu do valor final), nao os T_SETTLE=0,1 s do
dashboard (medido p/ o caso nominal, ver src/config/settings.py). O marcador
de assentamento de cada cenario e por isso especifico, nao o T_SETTLE global.

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
# tons mais saturados/escuros -- usados na serie "alvo" de cada par medido/alvo
# (referencia em corrente dq, Rede em tensao dq), sempre desenhada por cima
# (zorder maior) do medido/Inversor para destaca-la -- ver assets/charts/README.md
AZUL_REF, VERMELHO_REF = "#1d4ed8", "#b91c1c"
# cinza neutro p/ a serie "medido" quando ela precisa ficar por cima (pontilhada)
# de uma serie quase coincidente -- azul/vermelho mais claro nao rende contraste
# suficiente contra o proprio azul/vermelho escuro por baixo (ver tensao dq)
CINZA_MEDIDO = "#334155"
NAVY = "#0B132B"
GRID_COLOR = "#e2e8f0"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Segoe UI", "Arial"],
    "font.size": 10,
    "axes.edgecolor": "#94a3b8",
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": "#334155",
    "ytick.color": "#334155",
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "svg.fonttype": "none",   # mantem texto editavel no SVG (nao vira path)
})

LEGEND_KW = dict(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9)
fase_cores = [("Fase a", AZUL), ("Fase b", VERMELHO), ("Fase c", VERDE)]

SCENARIOS = [
    dict(folder="regime", prefix="regime", t_end=0.6, window=(0.55, 0.60),
         settle_t=0.1, title_suffix=" -- regime permanente",
         settle_label="transitório de partida excluído dos cálculos\n(T_settle = 0,1 s)"),
    dict(folder="regime_bad_pll", prefix="regime_bad_pll", t_end=1.0, window=(0.95, 1.00),
         settle_t=0.55, title_suffix=" -- sintonia inadequada",
         settle_label="assentamento mais lento (sintonia inadequada)\n≈0,55 s vs 0,1 s no caso nominal"),
]


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def new_fig():
    fig, ax = plt.subplots(figsize=(7.0, 3.4), dpi=150)
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.12, right=0.97)
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


def mark_settle(ax, settle_t, label):
    ax.axvspan(0, settle_t, color="#94a3b8", alpha=0.15, zorder=0)
    ax.axvline(settle_t, color="#94a3b8", linewidth=1.0, linestyle="--", zorder=1)
    ax.text(settle_t, ax.get_ylim()[1], "  " + label.replace("\n", "\n  "),
            fontsize=7.5, color="#64748b", va="top", ha="left")


def gen_scenario(sc):
    d_pq = pd.read_csv(ROOT / f"output/results/{sc['folder']}/sim_data.csv")
    d_abc = pd.read_csv(ROOT / f"output/results/{sc['folder']}/sim_data_abc.csv")
    t0, t1 = sc["window"]
    win = d_abc[(d_abc.t_s >= t0) & (d_abc.t_s <= t1)].iloc[::8].copy()
    win["t_ms"] = win.t_s * 1000
    prefix, suf, t_end = sc["prefix"], sc["title_suffix"], sc["t_end"]

    # 1. correntes abc -------------------------------------------------
    fig, ax = new_fig()
    for col, (_, color) in zip(["ia_ufv_pu", "ib_ufv_pu", "ic_ufv_pu"], fase_cores):
        ax.plot(win.t_ms, win[col], color=color, linewidth=1.4)
    style_axes(ax)
    ax.set_ylabel("Corrente (pu)")
    ax.set_xlabel("Tempo (ms)")
    ax.set_title("Correntes trifásicas do inversor" + suf, pad=32)
    legend_above(ax, [plt.Line2D([0], [0], color=c) for _, c in fase_cores],
                 [l for l, _ in fase_cores], ncol=3)
    save(fig, f"{prefix}_correntes_abc")

    # 2. tensoes abc ------------------------------------------------------
    fig, ax = new_fig()
    for col, (_, color) in zip(["va_ufv_pu", "vb_ufv_pu", "vc_ufv_pu"], fase_cores):
        ax.plot(win.t_ms, win[col], color=color, linewidth=1.4)
    style_axes(ax)
    ax.set_ylabel("Tensão (pu)")
    ax.set_xlabel("Tempo (ms)")
    ax.set_title("Tensões trifásicas do inversor" + suf, pad=32)
    legend_above(ax, [plt.Line2D([0], [0], color=c) for _, c in fase_cores],
                 [l for l, _ in fase_cores], ncol=3)
    save(fig, f"{prefix}_tensoes_abc")

    # 3. potencia P/Q ---------------------------------------------------
    fig, ax = new_fig()
    ax.plot(d_pq.t_s, d_pq.P_ufv_pu, color=AZUL, linewidth=0.7, label="P")
    ax.plot(d_pq.t_s, d_pq.Q_ufv_pu, color=LARANJA, linewidth=0.7, label="Q")
    style_axes(ax)
    ax.set_ylabel("Potência (pu)")
    ax.set_xlabel("Tempo (s)")
    ax.set_title("Potência ativa e reativa do inversor" + suf)
    ax.set_xlim(0, t_end)
    mark_settle(ax, sc["settle_t"], sc["settle_label"])
    ax.legend(loc="lower right", fontsize=9, **LEGEND_KW)
    save(fig, f"{prefix}_potencia_pq")

    # 4. corrente dq ------------------------------------------------------
    fig, ax = new_fig()
    ln_id  = ax.plot(d_pq.t_s, d_pq.id_ufv_pu, color=AZUL, linewidth=0.6, zorder=2)[0]
    ln_idr = ax.plot(d_pq.t_s, d_pq.id_ufv_ref_pu, color=AZUL_REF, linewidth=0.9, linestyle="--", zorder=3)[0]
    ln_iq  = ax.plot(d_pq.t_s, d_pq.iq_ufv_pu, color=VERMELHO, linewidth=0.6, zorder=2)[0]
    ln_iqr = ax.plot(d_pq.t_s, d_pq.iq_ufv_ref_pu, color=VERMELHO_REF, linewidth=0.9, linestyle="--", zorder=3)[0]
    style_axes(ax)
    ax.set_ylabel("Corrente (pu)")
    ax.set_xlabel("Tempo (s)")
    ax.set_title("Corrente do inversor no referencial dq" + suf)
    ax.set_xlim(0, t_end)
    mark_settle(ax, sc["settle_t"], sc["settle_label"])
    ax.legend([ln_id, ln_idr, ln_iq, ln_iqr],
              ["i_d med.", "i_d ref.", "i_q med.", "i_q ref."],
              loc="lower right", ncol=2, fontsize=9, **LEGEND_KW)
    save(fig, f"{prefix}_corrente_dq")

    # 5. tensao dq --------------------------------------------------------
    fig, ax = new_fig()
    ln_vdr = ax.plot(d_pq.t_s, d_pq.vd_rede_pu, color=AZUL_REF, linewidth=0.8, zorder=2)[0]
    ln_vqr = ax.plot(d_pq.t_s, d_pq.vq_rede_pu, color=VERMELHO_REF, linewidth=0.8, zorder=2)[0]
    ln_vdi = ax.plot(d_pq.t_s, d_pq.vd_ufv_pu, color=CINZA_MEDIDO, linewidth=0.55, linestyle=":", zorder=3)[0]
    ln_vqi = ax.plot(d_pq.t_s, d_pq.vq_ufv_pu, color=CINZA_MEDIDO, linewidth=0.55, linestyle=(0, (1, 1.4)), zorder=3)[0]
    style_axes(ax)
    ax.axhline(0.0, color="#94a3b8", linewidth=1.0, linestyle=":", zorder=0)
    ax.set_ylabel("Tensão (pu)")
    ax.set_xlabel("Tempo (s)")
    ax.set_title("Tensão no referencial dq" + suf)
    ax.set_xlim(0, t_end)
    mark_settle(ax, sc["settle_t"], sc["settle_label"])
    ax.legend([ln_vdr, ln_vqr, ln_vdi, ln_vqi],
              ["v_d Rede", "v_q Rede", "v_d Inversor", "v_q Inversor"],
              loc="lower right", ncol=2, fontsize=9, **LEGEND_KW)
    save(fig, f"{prefix}_tensao_dq")


if __name__ == "__main__":
    for sc in SCENARIOS:
        gen_scenario(sc)
