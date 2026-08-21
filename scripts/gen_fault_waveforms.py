"""
Gera os graficos de cenarios de falta (curto-circuito) em assets/charts/ -- um
SVG + PNG por grafico, mesma base visual de gen_regime_waveforms.py (matplotlib
puro, paleta do projeto), mas com duas diferencas de estrutura:

1. Fonte dos dados: output/results/<bus ou linha>/<tipo_falta>/ (com
   fault_info.json), nao output/results/regime/. t_fault/t_clear vem do JSON
   de cada pasta -- ver .claude/kb/simulation/cenarios_simulados.md (params.m
   nao e fonte confiavel do que cada cenario exportado usou).
2. Janela dos graficos de linha do tempo completa (P/Q, corrente dq, tensao
   dq): comeca no instante de assentamento do cenario em vez de 0 -- o
   fenomeno de interesse aqui e a falta, nao o transitorio de partida do
   PLL, entao o trecho anterior e simplesmente cortado (nao so sombreado
   como em gen_regime_waveforms.py). Esse instante depende do modelo (campo
   "bad_pll" do fault_info.json, ver cenarios_simulados.md):
     - Nominal: T_SETTLE = 0,1 s (constante oficial, src/config/settings.py).
       t_fault = 0,3 s cai sempre depois.
     - Sintonia inadequada (Kp/Ki_pll x0,2): energizacao muito mais lenta e
       oscilatoria (xi=0,316) -- mesmo instante empirico ~0,55 s usado em
       gen_regime_waveforms.py, nao T_SETTLE global (medido so p/ o caso
       nominal). t_fault = 0,6 s cai sempre depois.

Por cenario, 6 graficos (prefixo = SCENARIOS[i]["prefix"]):
  <prefixo>_correntes_abc.svg       -- i_a, i_b, i_c   (janela em torno da falta)
  <prefixo>_tensoes_abc.svg         -- v_a, v_b, v_c    (mesma janela)
  <prefixo>_potencia_pq.svg         -- P, Q             (settle_t-t_end, falta marcada)
  <prefixo>_corrente_dq.svg         -- i_d/i_q medido+ref (settle_t-t_end, falta marcada)
  <prefixo>_tensao_dq_rede.svg      -- v_d/v_q Rede      (settle_t-t_end, falta marcada)
  <prefixo>_tensao_dq_inversor.svg  -- v_d/v_q Inversor  (settle_t-t_end, falta marcada)

Marcador de falta: sombreado vermelho + vline tracejada vermelha em t_fault +
vline tracejada verde em t_clear -- mesma convencao do dashboard
(src/pipeline/chart.py, metodo _vline).

Requer matplotlib (nao listado em requirements.txt, ver gen_regime_waveforms.py).
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── paleta do projeto (src/config/settings.py, LIGHT_COLORS) ────────────────
AZUL, VERMELHO, VERDE, LARANJA = "#2563eb", "#dc2626", "#16a34a", "#ea580c"
AZUL_REF, VERMELHO_REF = "#1d4ed8", "#b91c1c"
NAVY = "#0B132B"
GRID_COLOR = "#e2e8f0"

# T_SETTLE = 0,1 s -- transitorio de partida do PLL, excluido de todo calculo
# (src/config/settings.py). So vale para o modelo NOMINAL. Cenarios de falta
# nominais aplicam a falta em 0,3 s, sempre depois -- ver cenarios_simulados.md.
T_SETTLE = 0.1
# Sintonia inadequada assenta muito mais devagar (xi=0,316) -- mesmo valor
# empirico usado em gen_regime_waveforms.py (regime_bad_pll), nao T_SETTLE
# global. Cenarios de falta com sintonia inadequada aplicam a falta em
# 0,6 s, sempre depois.
BAD_PLL_SETTLE = 0.55
CICLO_S = 1 / 60  # 60 Hz

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
    "svg.fonttype": "path",  # ver gen_regime_waveforms.py -- evita glifo esticado
})

LEGEND_KW = dict(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9)
fase_cores = [("Fase a", AZUL), ("Fase b", VERMELHO), ("Fase c", VERDE)]

FAULT_TYPE_LABEL = {"1phase": "monofásica", "2phase": "bifásica", "3phase": "trifásica"}

SCENARIOS = [
    dict(folder="bus7/3phase", prefix="bus7_3phase", bus="Barra 7", fault_type="3phase"),
    dict(folder="bus7/3phase_bad_pll", prefix="bus7_3phase_bad_pll", bus="Barra 7", fault_type="3phase"),
    dict(folder="bus6/3phase", prefix="bus6_3phase", bus="Barra 6", fault_type="3phase"),
    dict(folder="bus6/3phase_bad_pll", prefix="bus6_3phase_bad_pll", bus="Barra 6", fault_type="3phase"),
    dict(folder="bus7/1phase", prefix="bus7_1phase", bus="Barra 7", fault_type="1phase"),
    dict(folder="bus7/1phase_bad_pll", prefix="bus7_1phase_bad_pll", bus="Barra 7", fault_type="1phase"),
    dict(folder="bus6/2phase", prefix="bus6_2phase", bus="Barra 6", fault_type="2phase"),
    dict(folder="bus6/2phase_bad_pll", prefix="bus6_2phase_bad_pll", bus="Barra 6", fault_type="2phase"),
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
    ax.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 1.02),
              ncol=ncol, fontsize=9, **LEGEND_KW)


def set_title(ax, text, pad=None):
    """Titulo com fonte reduzida conforme o comprimento -- os cenarios de
    sintonia inadequada acrescentam "(sintonia inadequada)" ao sufixo, e no
    fontsize padrao (11, bold) o texto ficava mais largo que a figura e
    cortava na borda direita do PNG/SVG."""
    if len(text) > 78:
        fontsize = 8.3
    elif len(text) > 62:
        fontsize = 9.5
    else:
        fontsize = 11
    kw = dict(fontsize=fontsize)
    if pad is not None:
        kw["pad"] = pad
    ax.set_title(text, **kw)


def save(fig, name):
    svg_path = OUT_DIR / f"{name}.svg"
    png_path = OUT_DIR / f"{name}.png"
    fig.savefig(svg_path, format="svg")
    fig.savefig(png_path, format="png", dpi=220, facecolor="white")
    plt.close(fig)
    print("OK", svg_path)


def decimate_envelope(t, y, target_points=4000):
    """Ver gen_regime_waveforms.py -- min+max por bin evita aliasing de
    subamostragem ingenua em sinais com ondulacao rapida."""
    t = np.asarray(t)
    y = np.asarray(y)
    n = len(y)
    n_bins = max(1, target_points // 2)
    bin_size = n // n_bins
    if bin_size < 2:
        return t, y
    n_used = n_bins * bin_size
    t_b = t[:n_used].reshape(n_bins, bin_size)
    y_b = y[:n_used].reshape(n_bins, bin_size)
    rows = np.arange(n_bins)
    imin = np.argmin(y_b, axis=1)
    imax = np.argmax(y_b, axis=1)
    t_min, y_min = t_b[rows, imin], y_b[rows, imin]
    t_max, y_max = t_b[rows, imax], y_b[rows, imax]
    swap = imin > imax
    t_lo, y_lo = np.where(swap, t_max, t_min), np.where(swap, y_max, y_min)
    t_hi, y_hi = np.where(swap, t_min, t_max), np.where(swap, y_min, y_max)
    t_out, y_out = np.empty(n_bins * 2), np.empty(n_bins * 2)
    t_out[0::2], t_out[1::2] = t_lo, t_hi
    y_out[0::2], y_out[1::2] = y_lo, y_hi
    return t_out, y_out


def mark_fault(ax, t_fault, t_clear):
    """Sombreado + vlines tracejadas da janela de falta -- mesma convencao
    visual do dashboard (src/pipeline/chart.py, _vline): vermelho translucido
    entre inicio/eliminacao, vline vermelha em t_fault, verde em t_clear."""
    ax.axvspan(t_fault, t_clear, color=VERMELHO, alpha=0.07, zorder=0)
    ax.axvline(t_fault, color=VERMELHO, linewidth=1.3, linestyle="--", zorder=1, alpha=0.8)
    ax.axvline(t_clear, color=VERDE, linewidth=1.3, linestyle="--", zorder=1, alpha=0.7)
    ax.text(t_fault, ax.get_ylim()[1], "  falta aplicada",
            fontsize=7.5, color=VERMELHO, va="top", ha="left")
    ax.text(t_clear, ax.get_ylim()[1], "  falta eliminada",
            fontsize=7.5, color=VERDE, va="top", ha="left")


def gen_scenario(sc):
    folder = ROOT / "output" / "results" / sc["folder"]
    fault_info = json.loads((folder / "fault_info.json").read_text())
    t_fault, t_clear = fault_info["t_fault"], fault_info["t_clear"]

    d_pq_full = pd.read_csv(folder / "sim_data.csv")
    d_abc_full = pd.read_csv(folder / "sim_data_abc.csv")
    t_end = float(d_pq_full.t_s.max())
    prefix = sc["prefix"]
    bad_pll = bool(fault_info.get("bad_pll", False))
    settle_t = BAD_PLL_SETTLE if bad_pll else T_SETTLE
    suf = f" -- falta {FAULT_TYPE_LABEL[sc['fault_type']]} na {sc['bus']}"
    if bad_pll:
        suf += " (sintonia inadequada)"

    # janelas de linha do tempo completa comecam no assentamento do modelo
    # (settle_t), nao em 0 (ver docstring do modulo) -- filtra antes de
    # decimar p/ nao gastar pontos no trecho cortado.
    d_settle = d_pq_full[d_pq_full.t_s >= settle_t]
    t_full = d_settle.t_s.values

    def dec(col):
        return decimate_envelope(t_full, d_settle[col].values)

    # janela abc: cobre a transicao pre-falta -> durante -> pos-falta
    t0, t1 = t_fault - 2 * CICLO_S, t_clear + 3 * CICLO_S
    win = d_abc_full[(d_abc_full.t_s >= t0) & (d_abc_full.t_s <= t1)].iloc[::8].copy()
    win["t_ms"] = win.t_s * 1000

    # 1. correntes abc ---------------------------------------------------
    fig, ax = new_fig()
    for col, (_, color) in zip(["ia_ufv_pu", "ib_ufv_pu", "ic_ufv_pu"], fase_cores):
        ax.plot(win.t_ms, win[col], color=color, linewidth=1.0)
    style_axes(ax)
    ax.set_ylabel("Corrente (pu)")
    ax.set_xlabel("Tempo (ms)")
    set_title(ax, "Correntes trifásicas do inversor" + suf, pad=32)
    ax.axvspan(t_fault * 1000, t_clear * 1000, color=VERMELHO, alpha=0.07, zorder=0)
    ax.axvline(t_fault * 1000, color=VERMELHO, linewidth=1.3, linestyle="--", zorder=1, alpha=0.8)
    ax.axvline(t_clear * 1000, color=VERDE, linewidth=1.3, linestyle="--", zorder=1, alpha=0.7)
    legend_above(ax, [plt.Line2D([0], [0], color=c) for _, c in fase_cores],
                 [l for l, _ in fase_cores], ncol=3)
    save(fig, f"{prefix}_correntes_abc")

    # 2. tensoes abc ------------------------------------------------------
    fig, ax = new_fig()
    for col, (_, color) in zip(["va_ufv_pu", "vb_ufv_pu", "vc_ufv_pu"], fase_cores):
        ax.plot(win.t_ms, win[col], color=color, linewidth=1.0)
    style_axes(ax)
    ax.set_ylabel("Tensão (pu)")
    ax.set_xlabel("Tempo (ms)")
    set_title(ax, "Tensões trifásicas do inversor" + suf, pad=32)
    ax.axvspan(t_fault * 1000, t_clear * 1000, color=VERMELHO, alpha=0.07, zorder=0)
    ax.axvline(t_fault * 1000, color=VERMELHO, linewidth=1.3, linestyle="--", zorder=1, alpha=0.8)
    ax.axvline(t_clear * 1000, color=VERDE, linewidth=1.3, linestyle="--", zorder=1, alpha=0.7)
    legend_above(ax, [plt.Line2D([0], [0], color=c) for _, c in fase_cores],
                 [l for l, _ in fase_cores], ncol=3)
    save(fig, f"{prefix}_tensoes_abc")

    # 3. potencia P/Q -------------------------------------------------------
    fig, ax = new_fig()
    t_p, y_p = dec("P_ufv_pu")
    t_q, y_q = dec("Q_ufv_pu")
    ax.plot(t_p, y_p, color=AZUL, linewidth=1.0, label="P")
    ax.plot(t_q, y_q, color=LARANJA, linewidth=1.0, label="Q")
    style_axes(ax)
    ax.set_ylabel("Potência (pu)")
    ax.set_xlabel("Tempo (s)")
    set_title(ax, "Potência ativa e reativa do inversor" + suf)
    ax.set_xlim(settle_t, t_end)
    mark_fault(ax, t_fault, t_clear)
    ax.legend(loc="lower right", fontsize=9, **LEGEND_KW)
    save(fig, f"{prefix}_potencia_pq")

    # 4. corrente dq ----------------------------------------------------
    fig, ax = new_fig()
    ln_id  = ax.plot(*dec("id_ufv_pu"), color=AZUL, linewidth=0.6, zorder=2)[0]
    ln_idr = ax.plot(*dec("id_ufv_ref_pu"), color=AZUL_REF, linewidth=0.9, linestyle="--", zorder=3)[0]
    ln_iq  = ax.plot(*dec("iq_ufv_pu"), color=VERMELHO, linewidth=0.6, zorder=2)[0]
    ln_iqr = ax.plot(*dec("iq_ufv_ref_pu"), color=VERMELHO_REF, linewidth=0.9, linestyle="--", zorder=3)[0]
    style_axes(ax)
    ax.set_ylabel("Corrente (pu)")
    ax.set_xlabel("Tempo (s)")
    set_title(ax, "Corrente do inversor no referencial dq" + suf)
    ax.set_xlim(settle_t, t_end)
    mark_fault(ax, t_fault, t_clear)
    ax.legend([ln_id, ln_idr, ln_iq, ln_iqr],
              [r"$i_d$ med.", r"$i_d$ ref.", r"$i_q$ med.", r"$i_q$ ref."],
              loc="lower right", ncol=2, fontsize=9, **LEGEND_KW)
    save(fig, f"{prefix}_corrente_dq")

    # 5. tensao dq -- Rede e Inversor em arquivos separados (ver
    # gen_regime_waveforms.py p/ o motivo da separacao) ---------------------
    t_vdr, y_vdr = dec("vd_rede_pu")
    t_vqr, y_vqr = dec("vq_rede_pu")
    t_vdi, y_vdi = dec("vd_ufv_pu")
    t_vqi, y_vqi = dec("vq_ufv_pu")

    y_all = np.concatenate([y_vdr, y_vqr, y_vdi, y_vqi])
    pad = 0.05 * (y_all.max() - y_all.min())
    ylim = (y_all.min() - pad, y_all.max() + pad)

    for suf_name, label, (t_d, y_d), (t_q, y_q) in [
        ("rede", "Rede", (t_vdr, y_vdr), (t_vqr, y_vqr)),
        ("inversor", "Inversor", (t_vdi, y_vdi), (t_vqi, y_vqi)),
    ]:
        fig, ax = new_fig()
        ax.plot(t_d, y_d, color=AZUL, linewidth=0.7, label=r"$v_d$")
        ax.plot(t_q, y_q, color=VERMELHO, linewidth=0.7, label=r"$v_q$")
        style_axes(ax)
        ax.axhline(0.0, color="#94a3b8", linewidth=1.0, linestyle=":", zorder=0)
        ax.set_ylabel("Tensão (pu)")
        ax.set_xlabel("Tempo (s)")
        set_title(ax, f"Tensão no referencial dq ({label})" + suf)
        ax.set_xlim(settle_t, t_end)
        ax.set_ylim(*ylim)
        mark_fault(ax, t_fault, t_clear)
        ax.legend(loc="lower right", fontsize=9, **LEGEND_KW)
        save(fig, f"{prefix}_tensao_dq_{suf_name}")


if __name__ == "__main__":
    for sc in SCENARIOS:
        gen_scenario(sc)
