# -*- coding: utf-8 -*-
"""Nota tecnica: o vazamento espectral por desalinhamento de frequencia na
FFT de harmonicas, achado em 2026-08-10 e corrigido em 2026-08-11.

Os dois graficos (Figura 1/2) e o f1 medido no exemplo numerico sao
recalculados a partir do cenario Regime real a cada geracao — nao sao
numeros colados a mao — para que a nota nunca fique dessincronizada do
codigo em spectrum.py. Ver .claude/kb/standards/harmonic_frequency_leakage.md."""
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pdfnote import Note, render_preview  # noqa: E402
from src.pipeline.loader import SimData  # noqa: E402
from src.pipeline.spectrum import _amplitude_spectrum, _measure_f1, _harmonics  # noqa: E402
from src.config import T_SETTLE, F_FUND_HZ  # noqa: E402

DF = "&#916;f"
DTH = "&#916;&#952;"
PI = "&#960;"

_ACCENT, _GREY, _INK = "#1A4A6E", "#B0BEC9", "#14232E"


def _build_evidence(tmp_dir: Path):
    """Recalcula o espectro do cenario Regime (mesma fonte dos numeros do KB)
    e gera os dois PNGs de evidencia. Retorna (fig_espectro, fig_barras,
    f1_medido, harm_antes, harm_depois)."""
    d = SimData(ROOT / "output" / "results" / "regime" / "sim_data.csv")
    t, y = d.t_abc, d.ia_ufv
    mask = (t >= T_SETTLE) & (t <= float(t[-1]))
    tm, ym = t[mask], y[mask]
    f1 = _measure_f1(tm, ym)

    f_b, amp_b, dc_b = _amplitude_spectrum(tm, ym, window="rect", f1=F_FUND_HZ)
    f_a, amp_a, dc_a = _amplitude_spectrum(tm, ym, window="rect", f1=f1)
    h_before = _harmonics(f_b, amp_b, dc_b, f1=F_FUND_HZ)
    h_after = _harmonics(f_a, amp_a, dc_a, f1=f1)

    plt.rcParams["font.family"] = "Times New Roman"

    fig, ax = plt.subplots(figsize=(6.4, 3.5), dpi=220)
    fm_b = (f_b >= 90) & (f_b <= 260)
    fm_a = (f_a >= 90) & (f_a <= 260)
    ax.plot(f_b[fm_b], amp_b[fm_b] * 100, color=_GREY, lw=1.8,
            label="Antes (janela por 60,000 Hz fixo)")
    ax.plot(f_a[fm_a], amp_a[fm_a] * 100, color=_ACCENT, lw=1.8,
            label=f"Depois (janela por f₁={f1:.3f} Hz medido)")
    for freq in (120, 180, 240):
        ax.axvline(freq, color="#9AA7B0", lw=0.9, ls="--", zorder=0)
    ax.set_xlabel("Frequência (Hz)")
    ax.set_ylabel("Amplitude (% da fundamental)")
    ax.legend(frameon=False, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    p_spec = tmp_dir / "leak_spectrum.png"
    fig.savefig(p_spec, transparent=True)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.0, 3.3), dpi=220)
    cats = ["2ª", "3ª", "4ª"]
    antes = [h_before[k] * 100 for k in (2, 3, 4)]
    depois = [h_after[k] * 100 for k in (2, 3, 4)]
    x = np.arange(len(cats))
    ax.bar(x - 0.18, antes, width=0.36, color=_GREY, label="Antes (60 Hz fixo)")
    ax.bar(x + 0.18, depois, width=0.36, color=_ACCENT, label="Depois (f₁ medido)")
    for xi, v in zip(x - 0.18, antes):
        ax.text(xi, v + 0.03, f"{v:.2f}", ha="center", fontsize=8.5, color=_INK)
    for xi, v in zip(x + 0.18, depois):
        ax.text(xi, v + 0.03, f"{v:.2f}", ha="center", fontsize=8.5, color=_INK)
    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    ax.set_ylabel("Vazamento (%)")
    ax.legend(frameon=False, fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    p_bars = tmp_dir / "leak_bars.png"
    fig.savefig(p_bars, transparent=True)
    plt.close(fig)

    return p_spec, p_bars, f1, h_before, h_after


tmp_dir = Path(tempfile.mkdtemp(prefix="pll_note_leakage_"))
p_spec, p_bars, F1_MEAS, H_BEFORE, H_AFTER = _build_evidence(tmp_dir)


def pct(v):
    return f"{v * 100:.2f}%".replace(".", ",")


n = Note(
    title="Vazamento espectral na FFT de harm&#244;nicas",
    subtitle="Por que a 2&#170; harm&#244;nica saia alta no pr&#233;-falta, e o que foi corrigido",
    out=ROOT / "output" / "vazamento_espectral_harmonicos.pdf",
    meta_left="Trabalho de Conclus&#227;o de Curso &#183; Engenharia El&#233;trica &#183; UERJ<br/>"
              "Complemento &#224; nota de normas de harm&#244;nicos",
    meta_right="Nota t&#233;cnica<br/>11 de agosto de 2026",
    running_head="Vazamento espectral na FFT de harm&#244;nicas",
)

n.h("1. O achado")
n.p("A tabela de harm&#244;nicas do dashboard mostrava, no segmento pr&#233;-falta de "
    "<b>todo</b> cen&#225;rio, uma 2&#170; harm&#244;nica de corrente entre 1,3% e 2,1% &#8212; "
    "acima do limite de 1,0% do IEEE 519-2014/1547-2018. N&#227;o &#233; distor&#231;&#227;o real "
    "do inversor: &#233; <b>vazamento espectral</b>, causado por dois fatores combinados.")
n.p("<b>Primeiro</b>, a rede simulada nunca fecha em 60,000&#160;Hz exatos. A frequ&#234;ncia "
    "instant&#226;nea (medida por cruzamento de zero em i<sub>a</sub> ou no &#226;ngulo do "
    "gerador) parte de &#8776;59,88&#160;Hz e continua caindo ao longo de toda a janela de "
    "regime dispon&#237;vel &#8212; resposta prim&#225;ria de droop dos geradores s&#237;ncronos "
    "G1/G3 sem AGC, fechando sozinhos o balan&#231;o de pot&#234;ncia ap&#243;s o G2 ter sido "
    "substitu&#237;do pelo inversor (fonte de corrente, n&#227;o participa de regula&#231;&#227;o "
    "de frequ&#234;ncia). <b>Segundo</b>, a rotina de espectro (<i>spectrum.py</i>) truncava a "
    "janela da FFT assumindo essa frequ&#234;ncia nominal fixa &#8212; nunca a real.")

n.h("2. A matem&#225;tica do vazamento")
n.p(f"Seja o sinal real y(t) = A&#183;sen(2{PI}f<sub>1</sub>t), com f<sub>1</sub> a frequ&#234;ncia "
    f"verdadeira do trecho &#8212; n&#227;o os 60,000&#160;Hz assumidos. O c&#243;digo decidia o "
    f"tamanho da janela por")
n.eq_tex(r"n_{\mathrm{ciclos}} = \mathrm{trunc}(T_{\mathrm{seg}}\cdot 60)", tag="1a")
n.eq_tex(r"T_{\mathrm{janela}} = \dfrac{n_{\mathrm{ciclos}}}{60}", tag="1b")
n.gap(4)
n.p(f"Como T<sub>janela</sub> raramente &#233; m&#250;ltiplo inteiro do per&#237;odo real "
    f"1/f<sub>1</sub>, a DFT &#8212; que trata a janela como se repetisse periodicamente "
    f"&#8212; enxerga um salto de fase na emenda:")
n.eq_tex(r"\Delta\theta = 2\pi\,(60 - f_1)\,T_{\mathrm{janela}}", tag="2")
n.gap(4)
n.p("Esse salto n&#227;o &#233; uma descontinuidade pequena: ele espalha a energia do tom "
    "puro por todos os bins, seguindo o n&#250;cleo de Dirichlet de uma janela retangular "
    "&#8212; a envolt&#243;ria cai devagar, como um sinc:")
n.eq_tex(r"|X(f)| \approx A\left|\dfrac{\sin(\pi\,\Delta f\,T)}{\pi\,\Delta f\,T}\right|"
         r",\quad \Delta f = f - f_1", tag="3")
n.gap(4)
n.p(f"&#201; essa envolt&#243;ria em ~1/{DF} que produz o piso decrescente do espectro "
    f"&#8212; maior perto da fundamental, caindo devagar pelo resto da faixa &#8212; em "
    f"vez de picos isolados s&#243; nas ordens reais. E &#233; onde essa curva cruza os bins "
    f"nominais de 120/180/240&#160;Hz que a tabela l&#234; &#8220;2&#170;/3&#170;/4&#170; harm&#244;nica&#8221;.")
n.image(p_spec,
        caption="Figura 1 &#8212; Regime, corrente i<sub>a</sub>: piso decrescente ao redor de "
                "120/180/240&#160;Hz com janela por 60&#160;Hz fixo (cinza) contra picos isolados "
                "junto ao ru&#237;do com a janela por f&#8321; medido (azul).")
n.note(f"Exemplo num&#233;rico &#8212; Regime, corrente i<sub>a</sub>, janela pr&#233;-falta de "
       f"0,5&#160;s: f<sub>1</sub> medido &#233; {F1_MEAS:.3f}&#160;Hz. Com T<sub>janela</sub>=0,5&#160;s "
       f"fixo (30 ciclos assumidos a 60&#160;Hz &#8212; a l&#243;gica ANTES da corre&#231;&#227;o, "
       f"Eq.&#160;1a/1b), o sinal real completa apenas 29,84 ciclos &#8212; d&#233;ficit de 0,16 "
       f"ciclo, {DTH}&#8776;1,03&#160;rad pela Eq.&#160;2. A envolt&#243;ria da Eq.&#160;3 &#8212; "
       f"limite superior, j&#225; que o valor exato oscila com a fase residual sen({PI}{DF}T) "
       f"&#8212; no bin de 120&#160;Hz ({DF}=120&#8722;{F1_MEAS:.3f}&#8776;60,3&#160;Hz, T=0,5&#160;s "
       f"&#8594; {PI}{DF}T&#8776;94,8): |X|/A &#8804; 1/94,8&#8776;1,1% num &#250;nico bin. O "
       f"{pct(H_BEFORE[2])} medido antes da corre&#231;&#227;o (Se&#231;&#227;o&#160;5) usa outra "
       f"metodologia &#8212; RMS dos 3 bins vizinhos (118/120/122&#160;Hz), como pede o "
       f"IEEE&#160;519-2014&#160;&#167;4.1 &#8212; e por somar energia de mais de um bin fica maior "
       f"que a cota de bin &#250;nico, mas na mesma ordem de grandeza: confirma que a origem "
       f"&#233; vazamento, n&#227;o conte&#250;do harm&#244;nico real.")

n.h("3. Evid&#234;ncia independente: tom sint&#233;tico")
n.p("Reproduzido processando um <b>seno puro</b> de 59,67337&#160;Hz (zero harm&#244;nico "
    "real, por constru&#231;&#227;o) pela mesma l&#243;gica de janela do c&#243;digo antigo:")
n.table(["Ordem", "Sint&#233;tico (zero distor&#231;&#227;o)", "Observado no dashboard (Regime)"],
        [["2&#170;", "0,976%", "1,35 &#8211; 2,09%"],
         ["3&#170;", "0,526%", "0,55 &#8211; 0,67%"],
         ["4&#170;", "0,369%", "&#8776; 0,32%"]],
        [3.2, 5.8, 5.7])
n.gap(6)
n.p("A ordem de grandeza bate: o &#8220;harm&#244;nico&#8221; reportado era majoritariamente "
    "vazamento da fundamental, n&#227;o conte&#250;do real de alta ordem. O espectro de "
    "0&#8211;600&#160;Hz confirmava isso visualmente &#8212; em vez de um pico isolado em "
    "120&#160;Hz, um piso decrescente suave a partir de 60&#160;Hz (mesma assinatura da "
    "Figura&#160;1, curva cinza).")

n.h("4. A corre&#231;&#227;o implementada")
n.p(f"<i>spectrum.py</i> ganhou <b>_measure_f1</b>: mede a frequ&#234;ncia real do trecho por "
    f"cruzamento de zero ascendente (interpolado linearmente entre amostras), com fallback "
    f"para 60,000&#160;Hz se houver menos de 3 cruzamentos ou o resultado fugir de uma faixa "
    f"s&#227; (50&#8211;70&#160;Hz). A janela passa a truncar por essa frequ&#234;ncia medida:")
n.eq_tex(r"T_{\mathrm{janela}} = \dfrac{n_{\mathrm{ciclos}}}{f_{1,\,\mathrm{medido}}}", tag="4")
n.gap(4)
n.p("Escopo: s&#243; o modo <b>abc</b>, onde a fundamental realmente oscila perto de "
    "60&#160;Hz. O modo <b>dq</b> mant&#233;m 60,000&#160;Hz fixo &#8212; ali a fundamental "
    "vira componente DC, e cruzamento de zero n&#227;o se aplica. O r&#243;tulo da linha na "
    "tabela do relat&#243;rio continua pela <b>ordem nominal</b> (&#8220;120&#160;Hz&#8221; para "
    "a 2&#170;): s&#243; a janela de busca do bin se desloca para perto da frequ&#234;ncia real.")

n.h("5. Resultado: reduz, mas n&#227;o elimina &#8212; e por um motivo f&#237;sico")
n.p("Regime, corrente, fase a, antes e depois da corre&#231;&#227;o:")
n.table(["Ordem", "Antes (60&#160;Hz fixo)", "Depois (f&#8321; medido)"],
        [["2&#170;", pct(H_BEFORE[2]), pct(H_AFTER[2])],
         ["3&#170;", pct(H_BEFORE[3]), pct(H_AFTER[3])],
         ["4&#170;", pct(H_BEFORE[4]), pct(H_AFTER[4])]],
        [3.2, 5.7, 5.8])
n.gap(6)
n.image(p_bars,
        caption="Figura 2 &#8212; mesmos dados da tabela acima: a 3&#170;/4&#170; quase "
                "zeram, a 2&#170; cai bem menos.")
n.p(f"A 3&#170;/4&#170; quase zeraram &#8212; confirma que o realinhamento funciona. A 2&#170; "
    f"caiu s&#243; &#8776;17% porque a causa raiz <b>n&#227;o &#233; um deslocamento fixo de "
    f"60,000 para {F1_MEAS:.3f}&#160;Hz</b>: &#233; um <b>chirp cont&#237;nuo</b> &#8212; a frequ&#234;ncia "
    f"segue caindo <i>dentro</i> da pr&#243;pria janela de 0,5&#160;s (a mesma resposta de "
    f"droop da Se&#231;&#227;o&#160;1). Uma &#250;nica f<sub>1</sub> m&#233;dia alinha o in&#237;cio e "
    f"o fim da janela, mas n&#227;o cancela o alargamento espectral que a varia&#231;&#227;o "
    f"de frequ&#234;ncia dentro dela produz &#8212; alargamento maior perto da fundamental, "
    f"por isso a 2&#170; sofre mais que a 3&#170;/4&#170;, mais distantes.")
n.p("O mecanismo tem funda&#231;&#227;o formal: Carvalho et al. (2014) mostra que, com "
    "amostragem s&#237;ncrona, a sa&#237;da da DFT &#233; um &#250;nico fasor est&#225;vel; com "
    "f&#160;=&#160;f&#8320;&#8314;&#916;f, onde &#916;f &#233; a varia&#231;&#227;o real da rede "
    "(&#8220;the operating frequency is prone to small variations (&#916;f) due to the "
    "dynamic power balance&#8221;, p.75), um segundo termo deixa de ser cancelado e a amplitude "
    "passa a oscilar dentro da pr&#243;pria janela. O artigo trata &#916;f como "
    "quase-est&#225;tico <i>por</i> janela; o achado aqui &#8212; &#916;f variando "
    "<i>dentro</i> de uma &#250;nica janela &#8212; &#233; extens&#227;o direta do mesmo "
    "mecanismo, n&#227;o algo que o artigo demonstre literalmente.")
n.note("Confirmado nos 26 cen&#225;rios: pr&#233;-falta fica sistematicamente em 1,3&#8211;1,6% "
       "ap&#243;s a corre&#231;&#227;o (os cen&#225;rios BAD_PLL ca&#237;ram abaixo de 1%, "
       "0,88&#8211;1,19% &#8212; plaus&#237;vel, ganhos de PLL mais lentos geram menos ripple "
       "no pr&#243;prio sinal medido). Reduzir mais exigiria encurtar a janela &#8212; menos "
       "ciclos acumulam menos chirp &#8212; &#224;s custas da resolu&#231;&#227;o de 5&#160;Hz que "
       "o IEEE 519-2014 &#167;4.1 pede; limita&#231;&#227;o j&#225; declarada.")

n.h("6. Como ler a c&#233;lula vermelha na banca")
n.p("Se o professor apontar a 2&#170; harm&#244;nica do pr&#233;-falta/Regime ainda acima de "
    "1%: n&#227;o &#233; problema do inversor em regime permanente. &#201; res&#237;duo de "
    "medi&#231;&#227;o &#8212; a rede simulada ainda est&#225; em transit&#243;rio prim&#225;rio de "
    "frequ&#234;ncia quando a janela de an&#225;lise &#233; capturada, e nenhuma janela de "
    "frequ&#234;ncia &#250;nica consegue representar perfeitamente um sinal cuja frequ&#234;ncia "
    "est&#225; mudando continuamente dentro dela. A causa raiz &#233; a aus&#234;ncia de AGC "
    "nos geradores substitutos (G1/G3), n&#227;o o controlador do inversor sob teste.")

n.refs([
    "IEEE. IEEE Recommended Practice and Requirements for Harmonic Control in Electric "
    "Power Systems. IEEE Std 519-2014, 2014.",
    "IEEE. IEEE Application Guide for IEEE Std 1547-2018, IEEE Standard for Interconnection "
    "and Interoperability of Distributed Energy Resources with Associated Electric Power "
    "Systems Interfaces. IEEE Std 1547.2-2023, 2023.",
    "CARVALHO, Janison R. de; DUQUE, Carlos A.; LIMA, Marcelo A. A.; COURY, Denis V.; "
    "RIBEIRO, Paulo F. A novel DFT-based method for spectral analysis under time-varying "
    "frequency conditions. Electric Power Systems Research, v. 108, p. 74-81, 2014. "
    "DOI: 10.1016/j.epsr.2013.10.017.",
])

out = n.build()
if "--preview" in sys.argv:
    render_preview(out, Path(sys.argv[sys.argv.index("--preview") + 1]))
