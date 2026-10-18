"""Figuras dedicadas do deck da defesa: mesmos dados e curvas das figuras do
Cap. 5 do TCC, redesenhadas no tamanho da caixa da imagem no slide.

Os dados e as métricas vêm das funções dos geradores do TCC (scripts/
gen_erro_fase.py, gen_espectro_vd.py); aqui só muda o desenho. Sai anotação
cujo número já está na tabela ou nos cartões do slide; nunca muda dado, eixo
ou curva. Regras em casos/figura_dedicada.md.

Uso: python gen_figs_defesa.py [5.3,5.7,...]   (sem argumento: todas)
Saída: assets/charts/defesa/fig_<N_M>.svg/.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estilo as E  # noqa: E402  (põe ROOT e ROOT/scripts no path)
import numpy as np  # noqa: E402
import gen_erro_fase as EF  # noqa: E402
import gen_espectro_vd as EV  # noqa: E402
from validar_cenarios import pasta_inadequada  # noqa: E402

E.aplica()

# caixa da imagem no slide (in): slide 13, 15 (moldura alargada), 16 esq./dir.
CAIXA = {"5.3": (6.26, 3.04), "5.7": (5.52, 3.05), "5.10": (5.15, 2.79), "5.18": (4.89, 2.79)}
NOMINAL = dict(color=E.AZUL, label="Sintonia nominal")
INADEQ = dict(color=E.LARANJA, label="Sintonia inadequada")
FAIXA = (lambda: E.plt.Rectangle((0, 0), 1, 1, color=E.VERDE, alpha=0.35), "faixa de ±2°")


def marca_falta(ax, dur_ms, rotulos="fora"):
    """rotulos: "fora" (acima do eixo), "base" (dentro, embaixo) ou None."""
    EF.mark_fault_rel(ax, dur_ms, labels=False)
    if rotulos:
        lo, hi = ax.get_ylim()
        y, va = (hi, "bottom") if rotulos == "fora" else (lo, "bottom")
        for x, txt, cor in ((3, "falta", E.VERMELHO), (dur_ms + 3, "eliminação", E.VERDE)):
            ax.text(x, y, txt, color=cor, va=va, ha="left", clip_on=False)


def fig_5_3():
    """Energização, nominal x inadequada (Fig. 5.3). Ficam as marcas de 40 e 79 ms."""
    fig, ax = E.figura(CAIXA["5.3"])
    YLIM, T_MAX = 65, 200
    for folder, st, y_txt in (("regime", NOMINAL, 30), ("regime_bad_pll", INADEQ, 50)):
        fi, t, e = EF.load(folder)
        x, y = EF.thin(t * 1000, e)
        m = x <= T_MAX
        ax.plot(x[m], np.clip(y[m], -YLIM, YLIM), color=st["color"], label=st["label"])
        t_in = t[np.abs(e) > EF.TOL_DEG][-1] * 1000
        ax.axvline(t_in, color=st["color"], lw=1.2, ls=":", zorder=1)
        ax.annotate(f"±2° em {EF.num(t_in, 0)} ms", xy=(t_in, EF.TOL_DEG), xytext=(t_in + 8, y_txt),
                    fontsize=E.PT_ROTULO, color=st["color"], fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=st["color"], lw=1.0))
    ax.axhspan(-EF.TOL_DEG, EF.TOL_DEG, color=E.VERDE, alpha=0.25, zorder=0, lw=0)
    E.eixos(ax)
    ax.set_xlim(0, T_MAX)
    ax.set_ylim(-YLIM, YLIM)
    ax.set_yticks([-60, -30, 0, 30, 60])
    ax.set_xlabel("Tempo desde a energização (ms)")
    ax.set_ylabel("Erro de fase (°)")
    h, l = ax.get_legend_handles_labels()
    fig.legend(h + [FAIXA[0]()], l + [FAIXA[1]], loc="outside upper center", ncol=3, **E.LEGENDA)
    E.salva(fig, "fig_5_3")


def fig_5_7():
    """Trifásica nominal nos 4 pontos (Fig. 5.7). Pico e retorno estão na tabela do slide."""
    fig, axs = E.figura(CAIXA["5.7"], 2, 2, sharex=True, sharey=True)
    dados = [(rot,) + EF.load(f) for f, rot in EF.SIMETRICAS]
    lim = EF.sym_ylim(*[EF.rel_window(fi, t, e)[1] for _, fi, t, e in dados])
    for k, (ax, (rot, fi, t, e)) in enumerate(zip(axs.flat, dados)):
        x, y = EF.rel_window(fi, t, e)
        ax.set_ylim(*lim)
        E.eixos(ax)
        marca_falta(ax, (fi["t_clear"] - fi["t_fault"]) * 1000, rotulos="base" if k == 0 else None)
        ax.plot(x, y, color=E.AZUL, lw=1.3)
        ax.set_title(rot.replace(" (PCC)", ""), color=E.LARANJA if k == 0 else E.TEXTO)
        ax.set_yticks([-100, 0, 100])
        ax.set_xticks([0, 100, 200, 300])
    fig.supxlabel("Tempo desde a aplicação da falta (ms)", fontsize=E.PT_ROTULO)
    fig.supylabel("Erro de fase (°)", fontsize=E.PT_ROTULO)
    E.salva(fig, "fig_5_7")


def fig_5_10():
    """Espectro de vd na falta, nominal (Fig. 5.10). A nota das trifásicas está na faixa do slide 15."""
    fig, ax = E.figura(CAIXA["5.10"])
    cores = {"bus7/2phase": E.VERMELHO, "bus7/1phase": E.LARANJA, "bus6/2phase": E.AZUL,
             "bus6/1phase": E.ROXO, "bus7/3phase": E.MARINHO, "bus6/3phase": E.CINZA}
    ax.axvspan(112.5, 127.5, color=E.VERMELHO, alpha=0.07, zorder=0, lw=0)
    for folder, rot, _, ls in EV.CASOS:
        f, a = EV.espectro(folder)
        ax.plot(f, a, color=cores[folder], ls=ls, lw=1.6, marker="o", ms=3.5, label=rot)
    E.eixos(ax)
    ax.set_xlim(0, EV.F_MAX)
    ax.set_ylim(0, None)
    ax.set_xticks(np.arange(0, EV.F_MAX + 1, 120))
    ax.set_xlabel("Frequência (Hz)")
    ax.set_ylabel(r"Amplitude em $v_d$ (pu)")
    ax.text(128, ax.get_ylim()[1] * 0.97, "120 Hz", fontsize=E.PT_ROTULO, fontweight="bold",
            color=E.VERMELHO, va="top", ha="left")
    ax.legend(loc="upper right", ncol=1, fontsize=E.PT - 0.5, **E.LEGENDA)
    E.salva(fig, "fig_5_10")


def fig_5_18():
    """Trifásica na Barra 7, nominal x inadequada (Fig. 5.18). O 98 ms está no cartão do slide."""
    fig, ax = E.figura(CAIXA["5.18"])
    folder = "bus7/3phase"
    pares = [(folder, NOMINAL), (pasta_inadequada(folder), INADEQ)]
    ax.set_ylim(-190, 190)
    E.eixos(ax)
    fi0 = EF.load(folder)[0]
    marca_falta(ax, (fi0["t_clear"] - fi0["t_fault"]) * 1000)
    for f, st in pares:
        fi, t, e = EF.load(f)
        x, y = EF.rel_window(fi, t, e)
        ax.plot(x, y, color=st["color"], lw=1.3, label=st["label"])
    ax.set_yticks([-180, -90, 0, 90, 180])
    ax.set_xlabel("Tempo desde a aplicação da falta (ms)")
    ax.set_ylabel("Erro de fase (°)")
    h, l = ax.get_legend_handles_labels()
    fig.legend(h, l, loc="outside upper center", ncol=2, **E.LEGENDA)
    E.salva(fig, "fig_5_18")


FIGS = {"5.3": fig_5_3, "5.7": fig_5_7, "5.10": fig_5_10, "5.18": fig_5_18}

if __name__ == "__main__":
    for n in (sys.argv[1].split(",") if len(sys.argv) > 1 else FIGS):
        FIGS[n]()
