"""
Gera os graficos dos cenarios 'regime' e 'regime_bad_pll' (regime permanente,
sem falta -- PLL nominal e sintonia inadequada) em assets/charts/ -- um SVG +
PNG por grafico, sem Plotly, matplotlib puro, com a paleta do projeto
(src/config/settings.py). Corrente dq segue a convencao do dashboard (medido
solido + ref tracejado, mesmos eixos -- ver src/pipeline/chart.py
kind="dq_combined"). Tensao dq foge dessa convencao de proposito: Rede e
Inversor vao em arquivos separados (ver comentario na secao 5), nao
sobrepostos como no dashboard (kind="vdq_combined") -- a pedido do usuario,
depois de repetidos problemas de legibilidade com as duas series quase
coincidentes na mesma figura.

Por cenario, 6 graficos (prefixo = SCENARIOS[i]["prefix"]):
  <prefixo>_correntes_abc.svg       -- i_a, i_b, i_c            (janela final, 3 ciclos)
  <prefixo>_tensoes_abc.svg         -- v_a, v_b, v_c             (mesma janela)
  <prefixo>_potencia_pq.svg         -- P, Q                      (0-t_end completo)
  <prefixo>_corrente_dq.svg         -- i_d/i_q medido + ref       (0-t_end completo)
  <prefixo>_tensao_dq_rede.svg      -- v_d/v_q do lado da Rede     (0-t_end completo)
  <prefixo>_tensao_dq_inversor.svg  -- v_d/v_q do lado do Inversor (0-t_end completo)

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
import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── paleta do projeto (src/config/settings.py, LIGHT_COLORS) ────────────────
AZUL, VERMELHO, VERDE, LARANJA = "#2563eb", "#dc2626", "#16a34a", "#ea580c"
# tom mais saturado/escuro -- usado na serie de referencia em corrente dq
# (medido e alvo ficam na mesma figura, precisam de contraste entre si),
# desenhado primeiro (zorder menor); o medido e tracejado e desenhado por
# cima, pra suas lacunas revelarem o traco solido por baixo -- ver
# assets/charts/README.md. Tensao dq nao usa mais esse par: Rede e Inversor
# viraram arquivos separados (secao 5), entao cada um usa AZUL/VERMELHO puro.
AZUL_REF, VERMELHO_REF = "#1d4ed8", "#b91c1c"
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
    # "path": glifos viram contorno vetorial no SVG. Foi "none" (texto editavel)
    # antes, mas mathtext (subscritos $v_d$ etc.) exporta cada glifo com x fixo
    # e font-family sem fallback -- se o visualizador nao tiver a fonte exata
    # instalada (raro fora do matplotlib), as letras "esticam". "path" elimina
    # a dependencia de fonte por completo (sempre renderiza identico), ao custo
    # de o texto nao ser mais selecionavel/editavel dentro do SVG.
    "svg.fonttype": "path",
})

LEGEND_KW = dict(frameon=True, facecolor="white", edgecolor="none", framealpha=0.9)
fase_cores = [("Fase a", AZUL), ("Fase b", VERMELHO), ("Fase c", VERDE)]

SCENARIOS = [
    dict(folder="regime", prefix="regime", t_end=0.6, window=(0.55, 0.60),
         settle_t=0.1, title_suffix=" -- regime permanente",
         settle_label="transitório de partida excluído dos cálculos\n(T$_{settle}$ = 0,1 s)"),
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


def decimate_envelope(t, y, target_points=4000):
    """Decimacao por envelope (min+max por bin) em vez de subamostragem
    ingenua (pegar 1 a cada N amostras). Sinais com ondulacao mais rapida que
    a taxa decimada -- caso do batimento em v_q/v_d durante a "barriga" de
    sintonia inadequada -- aliasavam em zigue-zague artificial quando so 1
    amostra por bin sobrevivia (pontos escolhidos caiam em fases aleatorias
    da oscilacao real). Manter o min E o max de cada bin preserva o envelope
    verdadeiro sem cortar picos nem inventar ruido; em trechos suaves (sem
    ondulacao dentro do bin) degrada para o mesmo efeito de 1 amostra por
    bin, sem alargar a linha -- ver assets/charts/README.md.
    """
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
    swap = imin > imax  # mantem ordem cronologica dentro do bin
    t_lo, y_lo = np.where(swap, t_max, t_min), np.where(swap, y_max, y_min)
    t_hi, y_hi = np.where(swap, t_min, t_max), np.where(swap, y_min, y_max)
    t_out, y_out = np.empty(n_bins * 2), np.empty(n_bins * 2)
    t_out[0::2], t_out[1::2] = t_lo, t_hi
    y_out[0::2], y_out[1::2] = y_lo, y_hi
    return t_out, y_out


def mark_settle(ax, settle_t, label):
    ax.axvspan(0, settle_t, color="#94a3b8", alpha=0.15, zorder=0)
    ax.axvline(settle_t, color="#94a3b8", linewidth=1.0, linestyle="--", zorder=1)
    ax.text(settle_t, ax.get_ylim()[1], "  " + label.replace("\n", "\n  "),
            fontsize=7.5, color="#64748b", va="top", ha="left")


def gen_scenario(sc):
    d_pq_full = pd.read_csv(ROOT / f"output/results/{sc['folder']}/sim_data.csv")
    d_abc = pd.read_csv(ROOT / f"output/results/{sc['folder']}/sim_data_abc.csv")
    t0, t1 = sc["window"]
    win = d_abc[(d_abc.t_s >= t0) & (d_abc.t_s <= t1)].iloc[::8].copy()
    win["t_ms"] = win.t_s * 1000
    prefix, suf, t_end = sc["prefix"], sc["title_suffix"], sc["t_end"]

    # sim_data.csv vem a 5 us (dt do export, ver kb/simulation/export_workflow.md)
    # -- 120 mil amostras numa janela de 0,6-1,0 s plotadas em ~430px de largura
    # da ~280 amostras/pixel. Decima por envelope (min+max por bin, ver
    # decimate_envelope acima) para ~4000 pontos/traco, igual ao teto do
    # dashboard (_MAX_POINTS, src/pipeline/chart.py), mas cada coluna e
    # decimada independentemente -- um stride unico por linha do CSV (como
    # antes) escolhe a MESMA fase de amostragem p/ todo mundo, o que aliasa
    # em zigue-zague qualquer coluna cuja ondulacao seja mais rapida que a
    # taxa decimada (visivel sobretudo em v_q durante a "barriga" de batimento
    # da sintonia inadequada).
    t_full = d_pq_full.t_s.values

    def dec(col):
        return decimate_envelope(t_full, d_pq_full[col].values)

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
    t_p, y_p = dec("P_ufv_pu")
    t_q, y_q = dec("Q_ufv_pu")
    ax.plot(t_p, y_p, color=AZUL, linewidth=1.2, label="P")
    ax.plot(t_q, y_q, color=LARANJA, linewidth=1.2, label="Q")
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
    ln_id  = ax.plot(*dec("id_ufv_pu"), color=AZUL, linewidth=0.6, zorder=2)[0]
    ln_idr = ax.plot(*dec("id_ufv_ref_pu"), color=AZUL_REF, linewidth=0.9, linestyle="--", zorder=3)[0]
    ln_iq  = ax.plot(*dec("iq_ufv_pu"), color=VERMELHO, linewidth=0.6, zorder=2)[0]
    ln_iqr = ax.plot(*dec("iq_ufv_ref_pu"), color=VERMELHO_REF, linewidth=0.9, linestyle="--", zorder=3)[0]
    style_axes(ax)
    ax.set_ylabel("Corrente (pu)")
    ax.set_xlabel("Tempo (s)")
    ax.set_title("Corrente do inversor no referencial dq" + suf)
    ax.set_xlim(0, t_end)
    mark_settle(ax, sc["settle_t"], sc["settle_label"])
    ax.legend([ln_id, ln_idr, ln_iq, ln_iqr],
              [r"$i_d$ med.", r"$i_d$ ref.", r"$i_q$ med.", r"$i_q$ ref."],
              loc="lower right", ncol=2, fontsize=9, **LEGEND_KW)
    save(fig, f"{prefix}_corrente_dq")

    # 5. tensao dq -- Rede e Inversor em arquivos separados ---------------
    # Ao contrario de corrente dq (medido/ref sobrepostos), aqui as duas
    # series ficam quase coincidentes o tempo todo (sem falta, PCC ~= tensao
    # de rede) -- sobrepor na mesma figura exigia truque de cor/zorder pra
    # não virar uma mancha, e mesmo assim ficava dificil de ler (pedido do
    # usuario p/ separar). Cada arquivo usa AZUL/VERMELHO puro (sem par
    # claro/escuro, que so fazia sentido pra diferenciar series sobrepostas).
    t_vdr, y_vdr = dec("vd_rede_pu")
    t_vqr, y_vqr = dec("vq_rede_pu")
    t_vdi, y_vdi = dec("vd_ufv_pu")
    t_vqi, y_vqi = dec("vq_ufv_pu")

    # eixo Y compartilhado entre os dois arquivos, p/ poderem ser comparados
    # lado a lado no TCC na mesma escala
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
        ax.set_title(f"Tensão no referencial dq ({label})" + suf)
        ax.set_xlim(0, t_end)
        ax.set_ylim(*ylim)
        mark_settle(ax, sc["settle_t"], sc["settle_label"])
        ax.legend(loc="lower right", fontsize=9, **LEGEND_KW)
        save(fig, f"{prefix}_tensao_dq_{suf_name}")


if __name__ == "__main__":
    for sc in SCENARIOS:
        gen_scenario(sc)
