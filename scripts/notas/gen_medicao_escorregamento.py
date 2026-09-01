# -*- coding: utf-8 -*-
"""Nota tecnica: como (vd, vq) viram 19,2 voltas - arctan2, unwrap e Delta-theta."""
import sys
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pdfnote import Note, render_preview, MINUS  # noqa: E402

TH = "θ"      # theta
DE = "Δ"      # Delta maiusculo
CASO = ROOT / "output" / "results" / "bus7" / "3phase_bad_pll"
CSV = CASO / "sim_data.csv"
CSV_ANG = CASO / "sim_data_angles.csv"
T_CLEAR = 0.700
_ACCENT, _GREY, _WARM = "#1A4A6E", "#B0BEC9", "#B4531C"


def _br_axis(ax, which="both"):
    """Formata os rotulos de eixo em padrao pt-BR (virgula decimal)."""
    from matplotlib.ticker import FuncFormatter
    fmt = FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))
    if which in ("x", "both"):
        ax.xaxis.set_major_formatter(fmt)
    if which in ("y", "both"):
        ax.yaxis.set_major_formatter(fmt)


def _v(x, casas=2, sinal=True, mil=False):
    """Numero no padrao pt-BR: virgula decimal, milhar com espaco fixo, menos
    tipografico. `sinal=True` forca o '+' explicito nos positivos."""
    fmt = f"{{:{',' if mil else ''}.{casas}f}}"
    s = fmt.format(abs(x)).replace(",", "\x00").replace(".", ",").replace("\x00", "&#160;")
    if x < 0:
        return MINUS + s
    return ("+" if sinal else "") + s


def _load():
    df = pd.read_csv(CSV)
    seg = df[df["t_s"] >= T_CLEAR].reset_index(drop=True)
    t = seg["t_s"].to_numpy()
    vd = seg["vd_rede_pu"].to_numpy()
    vq = seg["vq_rede_pu"].to_numpy()
    raw = np.degrees(np.arctan2(vq, vd))
    unw = np.degrees(np.unwrap(np.arctan2(vq, vd)))
    return t, vd, vq, raw, unw


def _fig_plano(t, vd, vq, i1, i2, path):
    """Plano d-q com duas amostras reais de mesma razao vq/vd em quadrantes opostos.
    A reta tracejada e o lugar geometrico dessa razao: as duas amostras caem sobre
    ela, em sentidos opostos, e e por isso que o arco-tangente nao as distingue."""
    from matplotlib.patches import Arc
    plt.rcParams["font.family"] = "Times New Roman"
    fig, ax = plt.subplots(figsize=(5.2, 4.8), dpi=220)
    lim = 1.05
    ax.axhline(0, color="#9AA7B0", lw=0.9)
    ax.axvline(0, color="#9AA7B0", lw=0.9)

    m = vq[i1] / vd[i1]                       # inclinacao comum as duas amostras
    xr = np.array([-lim, lim])
    ax.plot(xr, m * xr, color="#8899A6", lw=0.9, ls="--", zorder=1,
            label="reta de mesma razão " r"$v_q/v_d$")

    for i, cor in ((i1, _ACCENT), (i2, _WARM)):
        ax.annotate("", xy=(vd[i], vq[i]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=cor, lw=2.2,
                                    shrinkA=0, shrinkB=0), zorder=3)
        ax.plot([vd[i]], [vq[i]], "o", color=cor, ms=4.5, zorder=4)

    ax.add_patch(Arc((0, 0), 0.62, 0.62, theta1=0.0, theta2=58.23,
                     color=_ACCENT, lw=1.1, zorder=2))
    ax.add_patch(Arc((0, 0), 0.98, 0.98, theta1=-121.79, theta2=0.0,
                     color=_WARM, lw=1.1, ls=":", zorder=2))
    ax.text(0.25, 0.20, r"$+58{,}23^\circ$", color=_ACCENT, fontsize=9.5)
    ax.text(0.10, -0.62, r"$-121{,}79^\circ$", color=_WARM, fontsize=9.5)

    ax.plot([], [], color=_ACCENT, lw=2.2,
            label=f"t = {t[i1] * 1000:.1f} ms".replace(".", ","))
    ax.plot([], [], color=_WARM, lw=2.2,
            label=f"t = {t[i2] * 1000:.1f} ms".replace(".", ","))
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.set_xticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    ax.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])
    _br_axis(ax)
    ax.set_xlabel(r"$v_d$ (pu)")
    ax.set_ylabel(r"$v_q$ (pu)")
    ax.legend(frameon=False, fontsize=8.2, loc="upper left",
              handlelength=1.6, borderpad=0.1, labelspacing=0.25)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, transparent=True)
    plt.close(fig)


def _fig_serra(t, raw, unw, path):
    """Painel de cima: arctan2 cru (dente de serra). Embaixo: depois do unwrap."""
    plt.rcParams["font.family"] = "Times New Roman"
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 4.4), dpi=220, sharex=True)
    ms = (t - T_CLEAR) * 1000
    a1.plot(ms, raw, color=_GREY, lw=0.8)
    a1.set_ylabel("Cru (graus)")
    a1.set_yticks([-180, -90, 0, 90, 180])
    a1.set_ylim(-215, 215)
    a2.plot(ms, unw, color=_ACCENT, lw=1.4)
    a2.set_ylabel("Desenrolado (graus)")
    a2.set_xlabel("Tempo após a eliminação da falta (ms)")
    a2.set_xlim(0, 300)
    for ax in (a1, a2):
        ax.axhline(0, color="#9AA7B0", lw=0.7, zorder=0)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, transparent=True)
    plt.close(fig)


def _fig_zoom(t, raw, unw, iw, path):
    """Zoom de 0,4 ms em torno do primeiro wrap."""
    plt.rcParams["font.family"] = "Times New Roman"
    a, b = iw - 40, iw + 40
    ms = (t[a:b] - T_CLEAR) * 1000
    fig, ax = plt.subplots(figsize=(6.2, 3.0), dpi=220)
    ax.plot(ms, raw[a:b], color=_GREY, lw=1.6, marker="o", ms=2.2,
            markevery=4, label="arctan2 cru")
    ax.plot(ms, unw[a:b], color=_ACCENT, lw=1.6, label="depois do unwrap")
    ax.axvline((t[iw] - T_CLEAR) * 1000, color="#9AA7B0", lw=0.9, ls="--", zorder=0)
    ax.annotate("salto de +359,94°\n(artefato da borda)",
                xy=((t[iw] - T_CLEAR) * 1000, 0), xytext=(0.60, 0.50),
                textcoords="axes fraction", fontsize=8.5, color="#5A6B78",
                ha="left", arrowprops=dict(arrowstyle="->", color="#8899A6", lw=0.9))
    ax.set_yticks([-180, -90, 0, 90, 180])
    ax.set_ylim(-215, 215)
    _br_axis(ax, which="x")
    ax.set_xlabel("Tempo após a eliminação da falta (ms)")
    ax.set_ylabel("Ângulo (graus)")
    ax.legend(frameon=False, fontsize=9, loc="center left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, transparent=True)
    plt.close(fig)


t, vd, vq, raw, unw = _load()
dt = float(t[1] - t[0])
d_raw = np.diff(raw)
IW = int(np.where(np.abs(d_raw) > 180)[0][0]) + 1   # primeira amostra ja enrolada
N_WRAP = int((np.abs(d_raw) > 180).sum())
DELTA = float(unw[-1] - unw[0])
VOLTAS = DELTA / 360.0
passo = np.abs(np.diff(unw))
MAG = np.hypot(vd, vq)
N_STR = f"{len(t):,}".replace(",", "&#160;")
I_Q1, I_Q3 = 2738, 35187                            # par de mesma razao, lados opostos

# rota alternativa: o erro de fase que o proprio modelo ja registra
_ang = pd.read_csv(CSV_ANG)
_ang = _ang[_ang["t_s"] >= T_CLEAR].reset_index(drop=True)
A_DT = float(_ang["t_s"][1] - _ang["t_s"][0])
A_RAW = np.degrees(_ang["theta_err_rad"].to_numpy())
A_UNW = np.degrees(np.unwrap(_ang["theta_err_rad"].to_numpy()))
A_DELTA = float(A_UNW[-1] - A_UNW[0])
A_VOLTAS = A_DELTA / 360.0
A_WRAP = int((np.abs(np.diff(A_RAW)) > 180).sum())
A_PASSO = np.abs(np.diff(A_UNW))
DIF_REL = abs(A_DELTA - abs(DELTA)) / abs(DELTA) * 100.0

tmp = Path(tempfile.mkdtemp(prefix="pll_note_slip_"))
p_plano, p_serra, p_zoom = tmp / "plano.png", tmp / "serra.png", tmp / "zoom.png"
_fig_plano(t, vd, vq, I_Q1, I_Q3, p_plano)
_fig_serra(t, raw, unw, p_serra)
_fig_zoom(t, raw, unw, IW, p_zoom)

n = Note(
    title="Como se mede a perda de sincronismo do SRF-PLL",
    subtitle="Do par (v<sub>d</sub>, v<sub>q</sub>) &#224;s 19,2 voltas: arctan2, "
             "unwrap e os n&#250;meros do caso da Barra 7",
    out=ROOT / "output" / "medicao_escorregamento_srf_pll.pdf",
    meta_left="Trabalho de Conclus&#227;o de Curso &#183; Engenharia El&#233;trica &#183; UERJ<br/>"
              "Falta trif&#225;sica na Barra 7, sintonia inadequada &#183; Se&#231;&#227;o 5.4",
    meta_right="Nota t&#233;cnica<br/>25 de agosto de 2026",
    running_head="Medi&#231;&#227;o da perda de sincronismo do SRF-PLL",
)

n.h("1. O que se quer medir")
n.p("A Se&#231;&#227;o 5.4 afirma que, depois da elimina&#231;&#227;o do curto-circuito, o "
    "erro de fase do SRF-PLL acumula <b>6&#160;916&#176;</b>, ou <b>19,2 voltas completas "
    "em 300 ms</b>, e que a taxa de rota&#231;&#227;o se estabiliza em torno de <b>70 Hz</b>. "
    "Esta nota mostra de onde vem cada um desses n&#250;meros, partindo das duas colunas "
    "medidas na simula&#231;&#227;o e chegando ao valor escrito no texto.")
n.p("A cadeia tem quatro elos, e cada um deles &#233; assunto de uma se&#231;&#227;o adiante:")
n.table(["Elo", "O que faz", "Sa&#237;da"],
        [["Par medido", "duas colunas do arquivo de resultados",
          "v<sub>d</sub>(t), v<sub>q</sub>(t) em pu"],
         ["arctan2", "converte o par no &#226;ngulo do vetor",
          f"{TH}<sub>cru</sub>(t), de {MINUS}180&#176; a +180&#176;"],
         ["unwrap", "remove os saltos de 360&#176; da borda",
          f"{TH}(t) cont&#237;nuo, sem limite"],
         ["diferen&#231;a e inclina&#231;&#227;o", "acumulado total e taxa instant&#226;nea",
          f"{DE}{TH} e f<sub>escorr</sub>"]],
        [3.0, 6.5, 5.2])
n.gap(6)
n.note("Cen&#225;rio: falta trif&#225;sica franca na Barra 7, aplicada em 0,600 s e "
       "eliminada em 0,700 s, com o SRF-PLL na sintonia inadequada. Janela de an&#225;lise: "
       "da elimina&#231;&#227;o ao fim da simula&#231;&#227;o, ou seja de 0,700 s a "
       f"1,000 s. S&#227;o {N_STR} amostras a passo fixo de {dt * 1e6:.0f} &#181;s.")

n.h("2. O par (v<sub>d</sub>, v<sub>q</sub>) &#233; um vetor, n&#227;o dois sinais soltos")
n.p("O SRF-PLL projeta a tens&#227;o trif&#225;sica da rede em um referencial girante cujo "
    "&#226;ngulo ele mesmo estima. O resultado dessa proje&#231;&#227;o s&#227;o as duas "
    "componentes v<sub>d</sub> e v<sub>q</sub>. Tomadas no mesmo instante, elas n&#227;o "
    "s&#227;o duas grandezas independentes: s&#227;o as <b>coordenadas cartesianas de um "
    "&#250;nico vetor</b> no plano <i>dq</i>, o vetor da tens&#227;o da rede visto de dentro "
    "do referencial estimado.")
n.eq_tex(r"v_d = |V|\,\cos\theta \qquad\qquad v_q = |V|\,\sin\theta", "1")
n.gap(8)
n.p("Duas leituras saem da&#237;. O <b>m&#243;dulo</b> |V| &#233; a amplitude da "
    f"tens&#227;o, e o <b>&#226;ngulo</b> {TH} &#233; o erro de fase: o quanto o referencial "
    "estimado est&#225; adiantado ou atrasado em rela&#231;&#227;o &#224; tens&#227;o real "
    "da rede. Com o SRF-PLL travado, o vetor aponta ao longo do eixo direto, ou seja "
    f"v<sub>q</sub> &#8776; 0 e {TH} &#8776; 0. N&#227;o &#233; coincid&#234;ncia: zerar "
    "v<sub>q</sub> &#233; exatamente o objetivo do controlador PI do SRF-PLL, e por isso "
    "v<sub>q</sub> j&#225; &#233;, por constru&#231;&#227;o, o sinal de erro que ele "
    "realimenta.")
n.note(f"Enquanto o erro &#233; pequeno, v<sub>q</sub> sozinho serve de aproxima&#231;&#227;o "
       f"do erro de fase, porque |V|&#183;sen{TH} &#8776; |V|&#183;{TH} para {TH} pequeno. "
       "Essa lineariza&#231;&#227;o &#233; a base do modelo de segunda ordem usado no "
       "projeto dos ganhos, mas ela deixa de valer justamente no cen&#225;rio desta nota, "
       "em que o erro percorre o c&#237;rculo inteiro.")

n.h("3. Por que arctan2, e n&#227;o o arco-tangente da raz&#227;o")
n.p("O caminho ing&#234;nuo para extrair o &#226;ngulo seria calcular arctg(v<sub>q</sub> / "
    "v<sub>d</sub>). Ele falha, e a falha n&#227;o &#233; sutil: a fun&#231;&#227;o tangente "
    "tem per&#237;odo de <b>180&#176;</b>, e n&#227;o de 360&#176;. Inverter o sinal das duas "
    "coordenadas ao mesmo tempo n&#227;o muda a raz&#227;o entre elas, de modo que dois "
    "vetores apontando para lados exatamente opostos produzem a mesma raz&#227;o e, "
    "portanto, o mesmo arco-tangente. O par abaixo &#233; real, medido nesta pr&#243;pria "
    "simula&#231;&#227;o:")
n.table(["Instante", "v<sub>d</sub> (pu)", "v<sub>q</sub> (pu)",
         "v<sub>q</sub>/v<sub>d</sub>", "arctg da raz&#227;o", "arctan2"],
        [[_v(t[I_Q1] * 1000, 1, sinal=False) + " ms", _v(vd[I_Q1], 4), _v(vq[I_Q1], 4),
          _v(vq[I_Q1] / vd[I_Q1], 4),
          _v(np.degrees(np.arctan(vq[I_Q1] / vd[I_Q1])), 2) + "&#176;",
          "<b>" + _v(raw[I_Q1], 2) + "&#176;</b>"],
         [_v(t[I_Q3] * 1000, 1, sinal=False) + " ms", _v(vd[I_Q3], 4), _v(vq[I_Q3], 4),
          _v(vq[I_Q3] / vd[I_Q3], 4),
          _v(np.degrees(np.arctan(vq[I_Q3] / vd[I_Q3])), 2) + "&#176;",
          "<b>" + _v(raw[I_Q3], 2) + "&#176;</b>"]],
        [2.3, 2.4, 2.4, 2.5, 2.6, 2.5])
n.gap(6)
n.p("As duas raz&#245;es coincidem at&#233; a terceira casa, e o arco-tangente devolve "
    "praticamente o mesmo valor para ambas. Mas os vetores apontam para lados opostos, "
    "separados por 180&#176;: o primeiro tem as duas coordenadas positivas, o segundo tem "
    "as duas negativas. Um &#226;ngulo de +58&#176; para o segundo caso estaria "
    "simplesmente errado.")
n.image(p_plano, width_cm=10.2,
        caption="Figura 1 &#8212; As duas amostras reais da tabela acima, no plano "
                "<i>dq</i>. Mesma raz&#227;o v<sub>q</sub>/v<sub>d</sub>, dire&#231;&#245;es "
                "opostas: o arco-tangente da raz&#227;o n&#227;o distingue uma da outra.")
n.p("&#201; esse o problema que a fun&#231;&#227;o arctan2 resolve. Ela recebe as duas "
    "coordenadas <b>separadamente</b>, e n&#227;o a raz&#227;o entre elas, o que lhe permite "
    "usar o <b>sinal de cada uma</b> para identificar o quadrante antes de decidir o "
    "&#226;ngulo:")
n.table(["Sinais medidos", "Quadrante", "arctan2(v<sub>q</sub>, v<sub>d</sub>)"],
        [["v<sub>d</sub> &gt; 0", "1&#186; ou 4&#186;", "arctg(v<sub>q</sub>/v<sub>d</sub>)"],
         ["v<sub>d</sub> &lt; 0 e v<sub>q</sub> &#8805; 0", "2&#186;",
          "arctg(v<sub>q</sub>/v<sub>d</sub>) + 180&#176;"],
         ["v<sub>d</sub> &lt; 0 e v<sub>q</sub> &lt; 0", "3&#186;",
          "arctg(v<sub>q</sub>/v<sub>d</sub>) " + MINUS + " 180&#176;"],
         ["v<sub>d</sub> = 0", "eixo q", "&#177;90&#176; conforme o sinal de v<sub>q</sub>"]],
        [5.0, 3.2, 6.5])
n.gap(6)
n.note("Vale desfazer uma confus&#227;o comum: arctan2 <b>n&#227;o</b> &#233; o "
       "arco-tangente de cada coordenada separadamente. &#201; um &#250;nico &#226;ngulo, "
       "calculado do par, em que as coordenadas entram separadas apenas para que os seus "
       "sinais resolvam o quadrante. A terceira linha da tabela acima explica o "
       f"{MINUS}121,79&#176; da amostra de 875,9 ms: arctg(+1,6132) = +58,21&#176;, e como "
       "v<sub>d</sub> e v<sub>q</sub> s&#227;o ambos negativos, subtraem-se 180&#176;.")

n.h("4. O limite de &#177;180&#176; e o salto na borda")
n.p("Resolvido o quadrante, sobra um limite estrutural: arctan2 devolve sempre um valor "
    f"entre {MINUS}180&#176; e +180&#176;. Ele responde <b>onde no c&#237;rculo</b> o vetor "
    "est&#225; agora, e nada mais. N&#227;o tem como saber, nem tem onde registrar, quantas "
    "voltas j&#225; foram dadas. Quando o vetor cruza o eixo direto negativo, o valor "
    f"devolvido salta de perto de {MINUS}180&#176; para perto de +180&#176;.")
n.p("O trecho abaixo &#233; o primeiro cruzamento desse tipo na janela analisada. As seis "
    "amostras s&#227;o consecutivas, separadas por 5 &#181;s:")
n.table(["Amostra", "t (ms)", "v<sub>d</sub> (pu)", "v<sub>q</sub> (pu)",
         f"{TH}<sub>cru</sub>", "Varia&#231;&#227;o"],
        [[str(i), _v((t[i] - T_CLEAR) * 1000, 3, sinal=False),
          _v(vd[i], 4), _v(vq[i], 6), _v(raw[i], 4) + "&#176;",
          ("&#8212;" if i == IW - 3 else
           ("<b>" + _v(d_raw[i - 1], 2) + "&#176;</b>" if abs(d_raw[i - 1]) > 180
            else _v(d_raw[i - 1], 4) + "&#176;"))]
         for i in range(IW - 3, IW + 3)],
        [1.9, 2.1, 2.4, 2.9, 2.9, 2.5])
n.gap(6)
n.p("Duas coisas saltam da tabela. Primeiro, o que o sinal medido faz &#233; banal: "
    "v<sub>d</sub> permanece negativo o tempo todo, e v<sub>q</sub> apenas atravessa o zero, "
    "passando de &#8722;34 &#215; 10<super>&#8722;6</super> para +304 &#215; "
    "10<super>&#8722;6</super> pu. O vetor mal se moveu. Segundo, o &#226;ngulo cru registra "
    f"nesse instante uma varia&#231;&#227;o de <b>{_v(d_raw[IW - 1], 2)}&#176;</b>, quando o "
    f"passo t&#237;pico nas amostras vizinhas &#233; de "
    f"{_v(d_raw[IW - 2], 4)}&#176;. O salto &#233; um artefato do intervalo de "
    "sa&#237;da da fun&#231;&#227;o, e n&#227;o um evento f&#237;sico: o &#226;ngulo real "
    f"continuou caindo suavemente, cruzou {MINUS}180&#176; e deveria ter chegado a "
    f"{MINUS}180,05&#176;, valor que simplesmente n&#227;o existe na sa&#237;da do arctan2.")
n.image(p_zoom, width_cm=13.0,
        caption="Figura 2 &#8212; Zoom de 0,4 ms em torno do primeiro cruzamento. O "
                "&#226;ngulo cru salta a largura inteira do intervalo; o desenrolado "
                "atravessa a borda sem descontinuidade.")

n.h("5. O unwrap: contando as voltas")
n.p("O <i>unwrap</i> reconstr&#243;i o &#226;ngulo cont&#237;nuo a partir do &#226;ngulo "
    "recortado. A regra &#233; simples e se aplica amostra a amostra, comparando cada valor "
    "com o anterior:")
n.eq_tex(r"\theta[i] \;=\; \theta_{cru}[i] \;+\; 360^{\circ}\,k[i]", "2")
n.gap(8)
n.p("O contador inteiro k come&#231;a em zero e s&#243; muda quando a diferen&#231;a entre "
    "duas amostras consecutivas do &#226;ngulo cru ultrapassa meia volta: diferen&#231;a "
    "acima de +180&#176; faz k diminuir uma unidade, diferen&#231;a abaixo de "
    f"{MINUS}180&#176; faz k aumentar uma unidade. O ponto decisivo &#233; que <b>k n&#227;o "
    "retorna ao valor anterior</b>: a corre&#231;&#227;o vale dali em diante, e por isso as "
    "voltas se acumulam em vez de se cancelarem.")
n.p(f"No cruzamento da se&#231;&#227;o anterior, a diferen&#231;a bruta foi de "
    f"{_v(d_raw[IW - 1], 2)}&#176;, maior que +180&#176;. O contador passa a {MINUS}1, e a "
    f"amostra deixa de valer {_v(raw[IW], 4)}&#176; para valer {_v(raw[IW], 4)}&#176; "
    f"{MINUS} 360&#176; = {_v(unw[IW], 4)}&#176;, que &#233; a continua&#231;&#227;o "
    f"natural dos {_v(raw[IW - 1], 4)}&#176; da amostra imediatamente anterior. Na janela "
    f"inteira isso acontece <b>{N_WRAP} vezes</b>, uma por volta completa.")
n.image(p_serra, width_cm=13.4,
        caption="Figura 3 &#8212; Os 300 ms de janela. Em cima, o &#226;ngulo cru: um dente "
                "de serra que se repete e nunca deixa ver o acumulado. Embaixo, o mesmo "
                "sinal ap&#243;s o unwrap: uma rampa que desce sem parar.")

n.h("6. Por que o unwrap n&#227;o se engana neste caso")
n.p("A regra do unwrap carrega uma premissa: ela sup&#245;e que uma varia&#231;&#227;o "
    "maior que 180&#176; entre amostras vizinhas s&#243; pode ser recorte, nunca movimento "
    "real. Se o &#226;ngulo verdadeiro chegasse a variar mais que meia volta em um passo de "
    "amostragem, o algoritmo interpretaria movimento como recorte e a contagem de voltas "
    "sairia errada. Vale, portanto, verificar a margem:")
n.table(["Estat&#237;stica do passo angular", "Valor", "Margem at&#233; 180&#176;"],
        [["M&#233;dia", _v(passo.mean(), 3, sinal=False) + "&#176;/amostra",
          f"{180 / passo.mean():.0f}&#215;"],
         ["Percentil 99", _v(np.percentile(passo, 99), 3, sinal=False) + "&#176;/amostra",
          f"{180 / np.percentile(passo, 99):.0f}&#215;"],
         ["M&#225;ximo absoluto", _v(passo.max(), 3, sinal=False) + "&#176;/amostra",
          f"{180 / passo.max():.0f}&#215;"]],
        [6.4, 4.3, 4.0])
n.gap(6)
n.p("O pior caso da janela inteira fica <b>21 vezes</b> abaixo do limiar, e apenas 13 das "
    f"{N_STR} amostras chegam a variar mais de 1&#176;. Vale notar onde est&#225; esse "
    "m&#225;ximo: exatamente no instante da elimina&#231;&#227;o da falta, quando o "
    f"m&#243;dulo do vetor vale apenas {_v(MAG.min(), 3, sinal=False)} pu, o menor da "
    "janela. &#201; o "
    "comportamento esperado, j&#225; que com o vetor pr&#243;ximo da origem uma "
    "varia&#231;&#227;o absoluta pequena nas coordenadas gira bastante a "
    "dire&#231;&#227;o. Ainda assim a margem permanece larga.")
n.note("A raiz da folga &#233; o passo de amostragem. A 5 &#181;s, uma rota&#231;&#227;o de "
       "130 Hz avan&#231;a 360&#176; &#215; 130 &#215; 5&#215;10<super>&#8722;6</super> "
       "&#8776; 0,23&#176; por amostra. Seria preciso reduzir a taxa de amostragem em quase "
       "tr&#234;s ordens de grandeza para p&#244;r a medi&#231;&#227;o em risco. O "
       "escorregamento medido n&#227;o &#233; artefato de amostragem.")

n.h(f"7. O acumulado: {DE}{TH} e as voltas")
n.p("Com a s&#233;rie j&#225; cont&#237;nua, o acumulado &#233; a diferen&#231;a entre o "
    "&#250;ltimo e o primeiro valor da janela:")
n.eq_tex(r"\Delta\theta \;=\; \theta[N-1] - \theta[0] \;=\; "
         r"\int_{t_{elim}}^{t_{fim}} \frac{d\theta}{dt}\,dt", "3", fontsize=19)
n.gap(8)
n.p(f"A segunda igualdade &#233; a leitura f&#237;sica: como d{TH}/dt &#233; a "
    "diferen&#231;a instant&#226;nea entre a velocidade do referencial estimado e a da "
    f"rede, {DE}{TH} &#233; a integral do <b>erro de frequ&#234;ncia</b> ao longo da janela. "
    "Os valores medidos:")
n.table(["Grandeza", "Valor medido"],
        [[f"{TH} no in&#237;cio da janela (t = 0,700 s)", _v(unw[0], 2) + "&#176;"],
         [f"{TH} no fim da janela (t = 1,000 s), j&#225; desenrolado",
          _v(unw[-1], 2, mil=True) + "&#176;"],
         [f"Acumulado {DE}{TH}", "<b>" + _v(DELTA, 2, mil=True) + "&#176;</b>"],
         [f"Voltas completas, {DE}{TH} &#247; 360&#176;", "<b>" + _v(VOLTAS, 2) + "</b>"]],
        [8.7, 6.0])
n.gap(6)
n.p("Da&#237; sai o n&#250;mero do texto. O sinal negativo indica o sentido: o &#226;ngulo "
    "decresce de forma monot&#244;nica ao longo dos 300 ms inteiros, ou seja o referencial "
    "estimado gira mais r&#225;pido que a tens&#227;o da rede. A Se&#231;&#227;o 5.4 relata "
    "o m&#243;dulo, 6&#160;916&#176; e 19,2 voltas, porque a afirma&#231;&#227;o de "
    "interesse &#233; a exist&#234;ncia do escorregamento, e n&#227;o o seu sentido, que "
    "depende da conven&#231;&#227;o de sinal adotada na medi&#231;&#227;o.")
n.note(f"Confer&#234;ncia cruzada independente: o unwrap acionou o contador {N_WRAP} "
       f"vezes na janela, uma por travessia da borda. S&#227;o {N_WRAP} travessias contra "
       f"{_v(abs(VOLTAS), 2, sinal=False)} voltas calculadas pelo acumulado, ou seja as "
       "duas contagens fecham. A fra&#231;&#227;o de 0,21 &#233; a volta incompleta em que "
       "a simula&#231;&#227;o termina.")

n.h("8. A taxa de escorregamento")
n.p("O acumulado responde <i>quanto</i> girou no total. A taxa responde <i>com que "
    "velocidade</i> gira em cada momento, e sai da inclina&#231;&#227;o da mesma curva "
    "desenrolada, por ajuste linear de primeira ordem em janelas curtas de 20 ms:")
n.eq_tex(r"f_{escorr} \;=\; \frac{1}{360^{\circ}}\,\frac{d\theta}{dt}", "4", fontsize=19)
n.gap(8)
_rows = []
for _t0 in (0.70, 0.74, 0.78, 0.82, 0.90, 0.98):
    _i0 = int(round((_t0 - T_CLEAR) / dt))
    _i1 = min(_i0 + int(round(0.020 / dt)), len(t) - 1)
    _sl = float(np.polyfit(t[_i0:_i1], unw[_i0:_i1], 1)[0])
    _rows.append([_v(_t0, 2, sinal=False) + " a " + _v(t[_i1], 2, sinal=False),
                  _v(_sl, 0, mil=True) + "&#176;/s",
                  "<b>" + _v(_sl / 360, 1) + " Hz</b>"])
n.table(["Janela de 20 ms (s)", "Inclina&#231;&#227;o", "Escorregamento"],
        _rows, [5.4, 4.6, 4.7])
n.gap(6)
n.p("A leitura &#233; direta: a taxa <b>cresce</b> ao longo dos primeiros 60 a 80 ms "
    "ap&#243;s a elimina&#231;&#227;o, de cerca de 20 Hz at&#233; um patamar, e depois "
    "oscila em regime, sem se fixar em um &#250;nico valor. Uma varredura mais fina, com "
    "janelas de 20 ms deslizando de 5 em 5 ms a partir de 0,76 s, mostra essa "
    "oscila&#231;&#227;o entre aproximadamente <b>65 e 81 Hz</b>, com m&#233;dia em torno "
    "de 72 Hz; as seis janelas da tabela acima s&#227;o uma amostra dessa faixa, n&#227;o "
    "o intervalo inteiro. &#201; esse regime, arredondado, que o texto da Se&#231;&#227;o "
    "5.4 reporta como 70 Hz. Em termos absolutos, o referencial estimado passa a girar a "
    "aproximadamente 130 Hz enquanto a rede segue em 60 Hz.")
n.p("Os dois n&#250;meros da Se&#231;&#227;o 5.4 medem coisas distintas, e um n&#227;o "
    "substitui o outro. O acumulado de 19,2 voltas prova a <b>persist&#234;ncia</b>: o erro "
    "n&#227;o oscila em torno de zero, ele cresce sem limite at&#233; o fim da "
    "simula&#231;&#227;o, e o SRF-PLL nunca reencontra o sincronismo. A taxa de 70 Hz "
    "quantifica o <b>regime</b> em que essa perda se estabiliza, em uma unidade "
    "fisicamente compar&#225;vel com as demais grandezas do trabalho. O primeiro &#233; a "
    "integral, o segundo &#233; a derivada da mesma curva.")

n.h("9. A rota direta: o &#226;ngulo que o modelo j&#225; registra")
n.p("Toda a cadeia acima parte das componentes de tens&#227;o, mas o modelo tamb&#233;m "
    "registra os &#226;ngulos diretamente: o &#226;ngulo estimado pelo SRF-PLL e o "
    "&#226;ngulo da tens&#227;o da rede s&#227;o gravados em uma s&#233;rie pr&#243;pria, "
    "e a rotina de exporta&#231;&#227;o j&#225; entrega a diferen&#231;a entre os dois. "
    "Cabe portanto a pergunta: com o erro de fase j&#225; dispon&#237;vel, o arctan2 seria "
    "dispens&#225;vel? A resposta &#233; sim para o arctan2, e <b>n&#227;o</b> para o "
    "unwrap.")
n.table(["", "Rota pelas componentes", "Rota pelo &#226;ngulo registrado"],
        [["Entrada", "v<sub>d</sub> e v<sub>q</sub> da rede no ponto de "
                     "conex&#227;o", "&#226;ngulo do SRF-PLL menos &#226;ngulo da rede"],
         ["Passo de amostragem", f"{dt * 1e6:.0f} &#181;s", f"{A_DT * 1e6:.0f} &#181;s"],
         ["Amostras na janela", N_STR, f"{len(A_UNW):,}".replace(",", "&#160;")],
         ["Precisa de arctan2", "<b>sim</b>", "n&#227;o"],
         ["Precisa de unwrap", "<b>sim</b>", "<b>sim</b>"],
         ["Travessias de borda", str(N_WRAP), str(A_WRAP)],
         [f"Acumulado {DE}{TH}", _v(DELTA, 2, mil=True) + "&#176;",
          _v(A_DELTA, 2, mil=True) + "&#176;"],
         ["Voltas", "<b>" + _v(VOLTAS, 2) + "</b>", "<b>" + _v(A_VOLTAS, 2) + "</b>"]],
        [3.8, 5.5, 5.4])
n.gap(6)
n.p("O ponto decisivo est&#225; na quinta linha. A rotina de exporta&#231;&#227;o aplica "
    "um recorte para o intervalo de meia volta antes de gravar a diferen&#231;a entre os "
    f"&#226;ngulos, e por isso a coluna pronta chega com o mesmo problema: {A_WRAP} "
    "travessias de borda, exatamente as mesmas que aparecem pelo outro caminho. Pular o "
    "arctan2 economiza um passo; pular o unwrap continuaria devolvendo um erro de fase "
    "que oscila entre limites fixos e esconde o acumulado, que &#233; justamente o que se "
    "quer medir. O <b>unwrap n&#227;o &#233; consequ&#234;ncia do arctan2</b>: ele &#233; "
    "consequ&#234;ncia de qualquer &#226;ngulo gravado em intervalo finito.")
n.p("Feita a ressalva, as duas rotas concordam. A diferen&#231;a entre os acumulados "
    f"&#233; de {_v(abs(A_DELTA) - abs(DELTA), 1, sinal=False)}&#176;, ou "
    f"{_v(DIF_REL, 2, sinal=False)}% do total, o que em voltas significa "
    f"{_v(abs(A_VOLTAS), 2, sinal=False)} contra {_v(abs(VOLTAS), 2, sinal=False)}. "
    "Nenhuma conclus&#227;o do trabalho muda com isso: a diferen&#231;a &#233; "
    "compat&#237;vel com a resolu&#231;&#227;o temporal. No passo t&#237;pico, a "
    f"s&#233;rie de &#226;ngulos avan&#231;a {_v(A_PASSO.mean(), 2, sinal=False)}&#176; "
    f"por amostra contra {_v(passo.mean(), 3, sinal=False)}&#176; pela rota das "
    f"componentes, quarenta vezes menos; no pior caso de cada uma, "
    f"{_v(A_PASSO.max(), 1, sinal=False)}&#176; contra {_v(passo.max(), 3, sinal=False)}"
    "&#176;, o mesmo instante de m&#243;dulo m&#237;nimo da Se&#231;&#227;o 6 domina "
    "os dois.")
n.note("O sinal aparece invertido entre as duas rotas, e isso &#233; conven&#231;&#227;o, "
       "n&#227;o discrep&#226;ncia. A diferen&#231;a entre &#226;ngulos mede o quanto o "
       "referencial estimado est&#225; adiantado em rela&#231;&#227;o &#224; rede, e sai "
       "positiva. O arctan2 das componentes mede o &#226;ngulo do vetor da rede visto de "
       "dentro do referencial estimado, que &#233; a mesma grandeza com o sinal trocado. "
       "As duas dizem a mesma coisa: o referencial gira mais r&#225;pido que a rede. Por "
       "isso a Se&#231;&#227;o 5.4 reporta o m&#243;dulo.")
n.p("Para o texto do trabalho ficou a rota das componentes, por dois motivos. Ela mede o "
    "erro sobre a mesma tens&#227;o do ponto de conex&#227;o que alimenta as demais "
    "m&#233;tricas do cap&#237;tulo, o que mant&#233;m todas as grandezas ancoradas na "
    "mesma s&#233;rie, e o faz com quarenta vezes mais resolu&#231;&#227;o temporal, "
    "margem que sustenta a verifica&#231;&#227;o da Se&#231;&#227;o 6. A rota direta "
    "serve como <b>confer&#234;ncia independente</b>, e nessa fun&#231;&#227;o ela fecha.")

n.h("10. Como reproduzir")
n.p("A receita fechada, para que qualquer n&#250;mero desta nota possa ser reconferido:")
n.table(["Passo", "Defini&#231;&#227;o"],
        [["Fonte", "colunas de tens&#227;o de eixo direto e de quadratura da rede, no ponto "
                   "de conex&#227;o, do cen&#225;rio de falta trif&#225;sica na Barra 7 com "
                   "sintonia inadequada"],
         ["Janela", "do instante de elimina&#231;&#227;o (0,700 s) ao fim da "
                    "simula&#231;&#227;o (1,000 s)"],
         [f"{TH}<sub>cru</sub>", "arctan2 do par (quadratura, direto), convertido a graus"],
         [f"{TH}", "unwrap sobre a s&#233;rie em radianos, convertida a graus em seguida"],
         [f"{DE}{TH}", "&#250;ltimo valor menos o primeiro"],
         ["Voltas", f"{DE}{TH} dividido por 360&#176;"],
         ["Escorregamento", f"ajuste linear de primeira ordem sobre {TH}, em janelas de "
                            "20 ms, dividido por 360&#176;"]],
        [3.4, 11.3])
n.gap(6)
n.note("A ordem dos argumentos importa e &#233; uma fonte cl&#225;ssica de erro: a "
       "componente de <b>quadratura vem primeiro</b>, e a de eixo direto vem em segundo. A "
       "conven&#231;&#227;o segue a do plano cartesiano, em que a coordenada vertical "
       "precede a horizontal na chamada. Trocar a ordem devolve o &#226;ngulo "
       "complementar, medido a partir do eixo q.")

n.refs([
    "HARRIS, Charles R. et al. Array programming with NumPy. Nature, v. 585, p. 357-362, "
    "2020. DOI: 10.1038/s41586-020-2649-2.",
    "KARIMI-GHARTEMANI, Masoud. Enhanced Phase-Locked Loop Structures for Power and Energy "
    "Applications. Hoboken: John Wiley &amp; Sons / IEEE Press, 2014. "
    "ISBN 978-1-118-79502-6.",
    "TEODORESCU, Remus; LISERRE, Marco; RODR&#205;GUEZ, Pedro. Grid Converters for "
    "Photovoltaic and Wind Power Systems. Chichester: John Wiley &amp; Sons, Ltd, 2011. "
    "ISBN 978-0-470-05751-3.",
    "YAZDANI, Amirnaser; IRAVANI, Reza. Voltage-Sourced Converters in Power Systems: "
    "Modeling, Control, and Applications. Hoboken: John Wiley &amp; Sons / IEEE Press, "
    "2010. ISBN 978-0-470-52156-4.",
])

out = n.build()
print("PDF:", out)
if "--preview" in sys.argv:
    render_preview(out, Path(sys.argv[sys.argv.index("--preview") + 1]))
