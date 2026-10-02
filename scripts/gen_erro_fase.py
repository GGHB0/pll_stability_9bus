"""
Gera os graficos de erro de fase do Cap. 5 do TCC em assets/charts/ -- pedidos
do Oscar nos comentarios 173, 189, 195, 212 e 216 do V10 ("porque nao estao
apresentando os graficos de erro angular?").

Definicao do erro de fase = a mesma do texto do Cap. 5, NAO o theta_err do
dashboard: atan2(vq_rede_pu, vd_rede_pu) em graus, no PCC. Pico medido a
partir do 1o ciclo apos a aplicacao da falta (o 1o ciclo e transitorio de
comutacao); t_s = ultimo instante com |erro| > 2 graus, contado de t_clear.
Receita fechada em .claude/kb/tcc-word/revisao-fragmento/
revisao_fragmento_cap5_metricas.md -- os numeros anotados nas figuras saem
daqui, calculados na hora, para nao divergirem do texto a cada re-simulacao.

Figuras (SVG + PNG):
  erro_fase_regime          -- 5.1: energizacao, nominal x inadequada
  erro_fase_simetricas      -- 5.2: trifasica nominal nos 4 pontos (2x2)
  erro_fase_assimetricas    -- 5.3: pares nominal x inadequada (2x2)
  erro_fase_perda_sincronismo -- 5.4: trifasica na Barra 7, nominal x inadequada

Eixo x em tempo relativo a aplicacao da falta: os cenarios com sintonia
inadequada de safras diferentes nao aplicam a falta no mesmo instante
(ver kb/simulation/cenarios_simulados.md).
"""
import json
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from gen_fault_waveforms import (  # noqa: E402  (estilo e paleta comuns ao Cap. 5)
    AZUL, LARANJA, NAVY, VERDE, VERMELHO, LEGEND_KW, ROOT, save, style_axes,
)
from validar_cenarios import cenario_ok, pasta_inadequada  # noqa: E402

CICLO_S = 1 / 60
TOL_DEG = 2.0
PRE_MS, POS_MS = 20, 200       # janela: 20 ms antes da falta ate 200 ms apos a eliminacao
CINZA = "#64748b"

NOMINAL = dict(color=AZUL, label="Sintonia nominal")
INADEQ = dict(color=LARANJA, label="Sintonia inadequada")


def num(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")


def load(folder):
    base = ROOT / "output" / "results" / folder
    fi = json.loads((base / "fault_info.json").read_text())
    d = pd.read_csv(base / "sim_data.csv")
    t = d.t_s.to_numpy()
    e = np.degrees(np.arctan2(d.vq_rede_pu.to_numpy(), d.vd_rede_pu.to_numpy()))
    return fi, t, e


def metrics(fi, t, e):
    tf, tc = fi["t_fault"], fi["t_clear"]
    pico = float(np.abs(e[(t >= tf + CICLO_S) & (t <= tc)]).max())
    pos = t >= tc
    fora = t[pos][np.abs(e[pos]) > TOL_DEG]
    if len(fora) == 0:
        ts = 0.0
    elif fora[-1] >= t[-1] - 2e-3:
        ts = None                      # nao volta a faixa dentro da janela simulada
    else:
        ts = (fora[-1] - tc) * 1000
    return pico, ts


def thin(x, y, step=10):
    """Decima por passo fixo (dt = 10 us) e quebra a linha nos saltos de +-180
    graus do atan2, que senao viram riscos verticais atravessando o grafico."""
    x, y = x[::step], y[::step].copy()
    y[1:][np.abs(np.diff(y)) > 180] = np.nan
    return x, y


def rel_window(fi, t, e):
    tf, tc = fi["t_fault"], fi["t_clear"]
    m = (t >= tf - PRE_MS / 1000) & (t <= tc + POS_MS / 1000)
    return thin((t[m] - tf) * 1000, e[m])


def mark_fault_rel(ax, dur_ms, labels=True):
    ax.axvspan(0, CICLO_S * 1000, color=CINZA, alpha=0.18, zorder=0, lw=0)
    ax.axvspan(CICLO_S * 1000, dur_ms, color=VERMELHO, alpha=0.07, zorder=0, lw=0)
    ax.axvline(0, color=VERMELHO, lw=1.1, ls="--", alpha=0.8, zorder=1)
    ax.axvline(dur_ms, color=VERDE, lw=1.1, ls="--", alpha=0.7, zorder=1)
    ax.axhspan(-TOL_DEG, TOL_DEG, color=VERDE, alpha=0.25, zorder=0, lw=0)
    ax.axhline(0, color="#94a3b8", lw=0.8, ls=":", zorder=0)
    if labels:
        y = ax.get_ylim()[1]
        ax.text(2, y, "falta", fontsize=9, color=VERMELHO, va="top", ha="left")
        ax.text(dur_ms + 2, y, "eliminação", fontsize=9, color=VERDE, va="top", ha="left")


def fault_legend_handles():
    return [plt.Rectangle((0, 0), 1, 1, color=CINZA, alpha=0.3),
            plt.Rectangle((0, 0), 1, 1, color=VERDE, alpha=0.35)], \
           ["1º ciclo (comutação, fora do pico)", "faixa de ±2°"]


def ts_txt(ts):
    return "não retorna na janela" if ts is None else f"{num(ts, 0)} ms"


def resumo(rotulo, pico, ts):
    volta = "não retorna a ±2°" if ts is None else f"±2° em {num(ts, 0)} ms"
    return f"{rotulo}: pico {num(pico)}° · {volta}"


def sym_ylim(*arrays, minimo=10):
    m = max(np.nanmax(np.abs(a)) for a in arrays)
    m = max(m * 1.08, minimo)
    return -m, m


# ── 5.1: energizacao ────────────────────────────────────────────────────────
def fig_regime():
    fig, ax = plt.subplots(figsize=(7.0, 3.4), dpi=150)
    fig.subplots_adjust(top=0.84, bottom=0.16, left=0.11, right=0.97)
    YLIM, T_MAX = 65, 200
    for folder, st in (("regime", NOMINAL), ("regime_bad_pll", INADEQ)):
        fi, t, e = load(folder)
        x, y = thin(t * 1000, e)
        m = x <= T_MAX
        ax.plot(x[m], np.clip(y[m], -YLIM, YLIM), color=st["color"], lw=1.0, label=st["label"])
        fora = t[np.abs(e) > TOL_DEG]
        t_in = fora[-1] * 1000
        ax.axvline(t_in, color=st["color"], lw=1.0, ls=":", zorder=1)
        ax.annotate(f"entra em ±2° em {num(t_in, 0)} ms", xy=(t_in, TOL_DEG),
                    xytext=(t_in + 8, 30 if folder == "regime" else 46),
                    fontsize=9, color=st["color"],
                    arrowprops=dict(arrowstyle="-", color=st["color"], lw=0.8))
    ax.axhspan(-TOL_DEG, TOL_DEG, color=VERDE, alpha=0.25, zorder=0, lw=0)
    ax.axhline(0, color="#94a3b8", lw=0.8, ls=":", zorder=0)
    style_axes(ax)
    ax.set_xlim(0, T_MAX)
    ax.set_ylim(-YLIM, YLIM)
    ax.set_xlabel("Tempo desde a energização (ms)")
    ax.set_ylabel("Erro de fase (°)")
    ax.text(T_MAX, -YLIM * 0.93, "nos primeiros ms a tensão ainda é nula e o erro sai da escala",
            fontsize=8, color=CINZA, ha="right", va="bottom")
    h, l = ax.get_legend_handles_labels()
    h.append(plt.Rectangle((0, 0), 1, 1, color=VERDE, alpha=0.35)); l.append("faixa de ±2°")
    ax.legend(h, l, loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=3, fontsize=9, **LEGEND_KW)
    save(fig, "erro_fase_regime")


# ── 5.2: gradiente de localizacao, nominal ──────────────────────────────────
SIMETRICAS = [("bus7/3phase", "Barra 7 (PCC)"), ("line7_8/3phase", "Linha 7-8"),
              ("line8_9/3phase", "Linha 8-9"), ("bus6/3phase", "Barra 6")]


def fig_simetricas():
    fig, axs = plt.subplots(2, 2, figsize=(8.0, 5.4), dpi=150, sharex=True, sharey=True)
    fig.subplots_adjust(top=0.88, bottom=0.10, left=0.09, right=0.98, hspace=0.32, wspace=0.08)
    dados = [(rot,) + load(f) for f, rot in SIMETRICAS]
    lim = sym_ylim(*[rel_window(fi, t, e)[1] for _, fi, t, e in dados])
    for ax, (rot, fi, t, e) in zip(axs.flat, dados):
        dur = (fi["t_clear"] - fi["t_fault"]) * 1000
        x, y = rel_window(fi, t, e)
        ax.set_ylim(*lim)
        style_axes(ax)
        mark_fault_rel(ax, dur)
        ax.plot(x, y, color=AZUL, lw=0.9)
        pico, ts = metrics(fi, t, e)
        ax.set_title(rot, fontsize=10.5)
        ax.text(0.98, 0.05, f"pico na falta: {num(pico)}°\nretorno a ±2°: {ts_txt(ts)}",
                transform=ax.transAxes, fontsize=9.5, ha="right", va="bottom",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#cbd5e1"))
    for ax in axs[1]:
        ax.set_xlabel("Tempo desde a aplicação da falta (ms)")
    for ax in axs[:, 0]:
        ax.set_ylabel("Erro de fase (°)")
    h, l = fault_legend_handles()
    fig.legend(h, l, loc="upper center", ncol=2, fontsize=9, **LEGEND_KW)
    save(fig, "erro_fase_simetricas")


# ── 5.3 e 5.4: pares nominal x inadequada ───────────────────────────────────
ASSIMETRICAS = [("bus6/2phase", "Bifásica na Barra 6"), ("bus7/1phase", "Monofásica na Barra 7"),
                ("bus6/1phase", "Monofásica na Barra 6"), ("bus7/2phase", "Bifásica na Barra 7")]


def plot_par(ax, folder, lim=None):
    linhas = []
    assert cenario_ok(folder), f"{folder} reprovado em validar_cenarios.py"
    bad = pasta_inadequada(folder)   # None: dado reprovado/ausente, so o nominal
    pares = [(folder, NOMINAL)] + ([(bad, INADEQ)] if bad else [])
    dados = [(st,) + load(f) for f, st in pares]
    if lim is None:
        lim = sym_ylim(*[rel_window(fi, t, e)[1] for _, fi, t, e in dados])
    ax.set_ylim(*lim)
    style_axes(ax)
    fi0 = dados[0][1]
    mark_fault_rel(ax, (fi0["t_clear"] - fi0["t_fault"]) * 1000)
    for st, fi, t, e in dados:
        x, y = rel_window(fi, t, e)
        ax.plot(x, y, color=st["color"], lw=0.9, alpha=0.9 if st is NOMINAL else 1.0)
        pico, ts = metrics(fi, t, e)
        linhas.append((st, pico, ts))
    # numeros acima do eixo, nunca em caixa sobre o traco: com escorregamento
    # de ciclo a curva da sintonia inadequada ocupa o eixo inteiro
    for k, (st, p, ts) in enumerate(reversed(linhas)):
        rot = "nominal" if st is NOMINAL else "inadequada"
        ax.text(0.0, 1.02 + 0.085 * (k + (bad is None)), resumo(rot, p, ts), transform=ax.transAxes,
                fontsize=9.5, color=st["color"], ha="left", va="bottom")
    if bad is None:
        ax.text(0.0, 1.02, "inadequada: fora da comparação", transform=ax.transAxes,
                fontsize=9.5, color=INADEQ["color"], ha="left", va="bottom", style="italic")
    return linhas


def legend_pares(fig):
    h = [plt.Line2D([0], [0], color=NOMINAL["color"]), plt.Line2D([0], [0], color=INADEQ["color"])]
    l = [NOMINAL["label"], INADEQ["label"]]
    h2, l2 = fault_legend_handles()
    ncol = 4 if fig.get_figwidth() >= 8 else 2
    fig.legend(h + h2, l + l2, loc="upper center", ncol=ncol, fontsize=9, **LEGEND_KW)


def fig_assimetricas():
    fig, axs = plt.subplots(2, 2, figsize=(8.0, 6.4), dpi=150, sharex=True, sharey=True)
    fig.subplots_adjust(top=0.85, bottom=0.09, left=0.09, right=0.98, hspace=0.50, wspace=0.08)
    for ax, (folder, rot) in zip(axs.flat, ASSIMETRICAS):
        plot_par(ax, folder, lim=(-190, 190))
        ax.set_title(rot, fontsize=10.5, pad=34)
        ax.set_yticks([-180, -90, 0, 90, 180])
    for ax in axs[1]:
        ax.set_xlabel("Tempo desde a aplicação da falta (ms)")
    for ax in axs[:, 0]:
        ax.set_ylabel("Erro de fase (°)")
    legend_pares(fig)
    save(fig, "erro_fase_assimetricas")


def fig_perda_sincronismo():
    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=150)
    fig.subplots_adjust(top=0.74, bottom=0.13, left=0.11, right=0.97)
    plot_par(ax, "bus7/3phase", lim=(-190, 190))
    ax.set_yticks([-180, -90, 0, 90, 180])
    ax.set_xlabel("Tempo desde a aplicação da falta (ms)")
    ax.set_ylabel("Erro de fase (°)")
    legend_pares(fig)
    save(fig, "erro_fase_perda_sincronismo")


if __name__ == "__main__":
    fig_regime()
    fig_simetricas()
    fig_assimetricas()
    fig_perda_sincronismo()
