# -*- coding: utf-8 -*-
"""Nota tecnica: sintonia do SRF-PLL, projeto de kp_pll e ki_pll."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pdfnote import Note, render_preview, XI, SQ, AP, AR, DL, TAU, WN, W0, MINUS  # noqa: E402

n = Note(
    title="Sintonia do SRF-PLL",
    subtitle="Projeto dos ganhos k<sub>p,pll</sub> e k<sub>i,pll</sub> do filtro de la&#231;o",
    out=ROOT / "output" / "sintonia_srf_pll_nota_tecnica.pdf",
    meta_left="Trabalho de Conclus&#227;o de Curso &#183; Engenharia El&#233;trica &#183; UERJ<br/>"
              "Comportamento din&#226;mico do SRF-PLL em inversores conectados &#224; rede",
    meta_right="Nota t&#233;cnica<br/>2 de agosto de 2026",
    running_head="Sintonia do SRF-PLL",
)

n.h("1. Por que esta nota")
n.p("Os ganhos do PLL nunca foram calculados dentro do reposit&#243;rio. Eles entram como "
    "constantes literais nos blocos proporcionais do netlist do PSIM, migram fixos para "
    "dentro do bloco de PLL do Simulink e chegam ao <i>params.m</i> sem nenhuma "
    "justificativa escrita. Esta nota reconstr&#243;i o projeto, conferido contra as fontes "
    "originais, e fecha exatamente nos valores gravados.")

n.h("2. N&#227;o confundir os dois pares de ganhos")
n.p("O <i>params.m</i> carrega dois pares distintos, dimensionados por m&#233;todos "
    "diferentes. Confundi-los &#233; o erro mais f&#225;cil de cometer aqui.")
n.table(["Vari&#225;vel", "Valor", "Malha", "Metodologia"],
        [["k<sub>p,pll</sub> / k<sub>i,pll</sub>", "460 / 105&#160;820",
          "PI do la&#231;o do SRF-PLL", "esta nota"],
         ["K<sub>p</sub> / K<sub>i</sub>",
          f"29,4815/4 {AP} 7,370<br/>7075,56/4 {AP} 1768,9", "controlador de corrente",
          "K<sub>p</sub> = 8&#183;f<sub>g</sub>&#183;L<sub>est</sub> (Tese AGP)"]],
        [3.1, 3.3, 3.9, 4.4])
n.gap(4)
n.note("S&#243; k<sub>p,pll</sub> e k<sub>i,pll</sub> alimentam o bloco de sincronismo.")

n.h("3. Modelo linearizado")
n.p(f"Para pequenos desvios de fase, a cadeia Park {AR} PI {AR} VCO se lineariza: o detector "
    f"de fase vira um ganho igual &#224; magnitude <i>U</i> da tens&#227;o de entrada, o filtro "
    f"de la&#231;o &#233; o PI e o VCO &#233; um integrador. A malha fechada resulta de segunda "
    f"ordem:")
n.eq("G(s) = (K<sub>p</sub>&#183;s + K<sub>i</sub>) / "
     "(s<super>2</super> + K<sub>p</sub>&#183;s + K<sub>i</sub>)", "1")
n.gap(8)
n.p("Comparando com a forma can&#244;nica de um sistema de segunda ordem:")
n.eq(f"G(s) = (2{XI}{WN}&#183;s + {WN}<super>2</super>) / "
     f"(s<super>2</super> + 2{XI}{WN}&#183;s + {WN}<super>2</super>)", "2")
n.gap(8)
n.eq(f"K<sub>i</sub> = {WN}<super>2</super>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;"
     f"K<sub>p</sub> = 2{XI}{WN}", "3")

n.h("4. A condi&#231;&#227;o para (3): la&#231;o normalizado")
n.p("A equa&#231;&#227;o caracter&#237;stica geral do SRF-PLL carrega a magnitude da entrada, "
    "s<super>2</super> + K<sub>p</sub>&#183;U&#183;s + K<sub>i</sub>&#183;U = 0. As formas de "
    "(3) s&#243; valem sem o <i>U</i> se o la&#231;o estiver normalizado em pu, isto &#233;, se "
    "<i>U</i> = 1. O netlist confirma que est&#225;:")
n.table(["Etapa", "Ganho", "Efeito"],
        [["Sensor de tens&#227;o", "1 / 16&#160;329,93",
          f"16&#160;329,93 = 20&#160;000&#183;{SQ}(2/3) = tens&#227;o de pico de fase da base "
          f"de 20 kV"],
         ["Clarke", f"0,816497 ({SQ}2/3) e 0,707107", f"A {AR} 1,224745&#183;A"],
         ["Park", f"{MINUS}0,816497", f"1,224745&#183;A {AR} A"]],
        [3.4, 3.6, 7.7])
n.gap(6)
n.p("O m&#243;dulo do vetor <i>dq</i> sai igual &#224; entrada normalizada, logo <b>U = 1 pu no "
    "nominal</b>. Teodorescu confirma pelo outro lado: a equa&#231;&#227;o de sintonia dele "
    "sup&#245;e explicitamente entrada unit&#225;ria, e manda dividir os ganhos pela amplitude "
    "caso contr&#225;rio.")
n.note("<b>Consequ&#234;ncia pr&#225;tica:</b> se a base de tens&#227;o do modelo mudar, os "
       "ganhos do PLL precisam ser reescalados junto. Eles n&#227;o s&#227;o independentes da base.")

n.h("5. Os dois par&#226;metros de projeto")
n.p(f"Fixadas as rela&#231;&#245;es (3), restam apenas duas escolhas: o amortecimento {XI} e o "
    f"tempo de acomoda&#231;&#227;o t<sub>s</sub>.")
n.table(["Par&#226;metro", "Valor", "Justificativa"],
        [[XI, "0,707",
          "Conven&#231;&#227;o de segunda ordem: resposta transit&#243;ria &#243;tima, sobressinal "
          "de cerca de 5%. &#201; o <i>qsi</i> j&#225; gravado no <i>params.m</i>."],
         ["t<sub>s</sub>", "20 ms",
          f"Crit&#233;rio de 1%: t<sub>s</sub> = 4,6/({XI}{WN}). Faixa recomendada na "
          f"literatura: de um a dois per&#237;odos da fundamental, ou seja 16,7 a 33,3 ms "
          f"em 60 Hz."]],
        [2.4, 2.2, 10.1])
n.gap(8)
n.p(f"<b>De onde vem o 4,6.</b> N&#227;o tem rela&#231;&#227;o com a malha do PLL: &#233; o "
    f"crit&#233;rio de acomoda&#231;&#227;o. A resposta ao degrau de um sistema de segunda ordem "
    f"subamortecido decai dentro de um envelope exponencial exp({MINUS}{XI}{WN}&#183;t). O "
    f"t<sub>s</sub> &#233; o instante em que esse envelope entra na faixa de toler&#226;ncia {DL}:")
n.eq(f"exp({MINUS}{XI}{WN}&#183;t<sub>s</sub>) = {DL}&#160;&#160;&#160;&#160;{AR}"
     f"&#160;&#160;&#160;&#160;t<sub>s</sub> = ln(1/{DL}) / ({XI}{WN})", "4")
n.gap(8)
n.p(f"O numerador &#233; apenas ln(1/{DL}), arredondado por conven&#231;&#227;o:")
n.table([f"Toler&#226;ncia {DL}", f"ln(1/{DL})", "Numerador", "Onde aparece"],
        [["5%", "2,996", "3", "Ogata"],
         ["2%", "3,912", "4", "Ogata; Alves, equa&#231;&#227;o (11)"],
         ["1%", "4,605", "<b>4,6</b>", "Franklin; Teodorescu, equa&#231;&#227;o (4.38)"]],
        [2.6, 2.2, 2.4, 7.5])
n.gap(6)
n.p(f"Leitura equivalente: 1/({XI}{WN}) &#233; a <b>constante de tempo {TAU} do envelope</b>, e "
    f"acomodar dentro de 1% custa <b>4,6 constantes de tempo</b>. Aqui {TAU} = 1/230 = 4,35 ms, "
    f"e 4,6&#183;{TAU} = 20 ms. O 9,2 que aparece na se&#231;&#227;o 6 &#233; 2 &#215; 4,6, "
    f"porque K<sub>p</sub> = 2{XI}{WN}.")
n.note(f"<b>Precis&#227;o:</b> o envelope exato da resposta ao degrau &#233; "
       f"exp({MINUS}{XI}{WN}&#183;t)/{SQ}(1{MINUS}{XI}<super>2</super>). Incluir esse fator "
       f"daria 4,95 em vez de 4,6 para {XI} = 0,707. A conven&#231;&#227;o de controle despreza "
       f"o 1/{SQ}(1{MINUS}{XI}<super>2</super>): os numeradores 3, 4 e 4,6 s&#227;o "
       f"aproxima&#231;&#245;es padronizadas, n&#227;o valores exatos.")
n.p("O t<sub>s</sub> &#233; a <b>&#250;nica grandeza escolhida por julgamento</b> em todo o "
    "projeto. A faixa de um a dois per&#237;odos tem limite f&#237;sico dos dois lados:")
n.table(["Limite", "Raz&#227;o"],
        [["Piso, cerca de 1 per&#237;odo",
          "N&#227;o existe informa&#231;&#227;o de fase de um sinal de 60 Hz em menos de um "
          "ciclo. Abaixo disso o modelo linearizado deixa de valer, porque ele sup&#245;e a "
          "malha lenta em rela&#231;&#227;o &#224; portadora, e o PLL vira amplificador de "
          "ru&#237;do em vez de ficar mais r&#225;pido."],
         ["Teto, cerca de 2 per&#237;odos",
          "O controlador de corrente opera no referencial <i>dq</i> entregue pelo PLL. "
          "Enquanto o PLL n&#227;o reconverge, i<sub>d</sub> e i<sub>q</sub> s&#227;o projetados "
          "em eixo errado, o que aparece como inje&#231;&#227;o de reativo indevida e, no "
          "limite, perda de sincronismo."]],
        [3.6, 11.1])
n.gap(6)
n.p("20 ms equivalem a 1,20 per&#237;odo, logo no in&#237;cio da faixa: reconverge dentro do "
    "primeiro ciclo p&#243;s-falta sem descer ao regime onde a lineariza&#231;&#227;o se quebra.")

n.h("6. O c&#225;lculo")
n.p(f"Combinando (3) com o crit&#233;rio de 1% resulta a forma direta "
    f"K<sub>p</sub> = 2{XI}{WN} = 9,2/t<sub>s</sub>:")
n.eq(f"{XI}{WN} = 4,6 / t<sub>s</sub> = 4,6 / 0,020 = 230 rad/s<br/>"
     f"<b>K<sub>p</sub> = 2{XI}{WN} = 9,2 / 0,020 = 460</b><br/>"
     f"{WN} = 230 / 0,707 {AP} 325,3 rad/s&#160;&#160;(51,8 Hz)<br/>"
     f"<b>K<sub>i</sub> = {WN}<super>2</super> {AP} 105&#160;820</b>", "5")
n.gap(8)
n.note(f"<b>Arredondamento.</b> {XI} = 0,707 tem tr&#234;s casas decimais. Levando a "
       f"divis&#227;o adiante sem arredondar d&#225; {WN} = 325,32 rad/s e K<sub>i</sub> = "
       f"105&#160;832, cerca de 0,01% acima do valor gravado. O {XI} exato que fecha em "
       f"K<sub>p</sub> = 460 e K<sub>i</sub> = 105&#160;820 &#233; 0,70704 &#8212; a diferen&#231;a "
       f"&#233; do arredondamento de entrada, n&#227;o do m&#233;todo.")
n.p(f"Os dois ganhos fecham nos valores gravados dentro dessa precis&#227;o. Na "
    f"dire&#231;&#227;o inversa, partindo do que est&#225; no <i>params.m</i>:")
n.eq(f"{WN} = {SQ}(105&#160;820) = 325,30 rad/s<br/>"
     f"{XI} = 460 / (2&#183;325,30) = 0,7070", "6")

n.h(f"7. O pre&#231;o: banda alta demais para rejeitar 2{W0}")
n.p(f"{WN} = 325,3 rad/s equivale a 51,8 Hz, logo abaixo da pr&#243;pria fundamental. Sob falta "
    f"assim&#233;trica, a componente de sequ&#234;ncia negativa aparece em v<sub>q</sub> como um "
    f"ripple em 2{W0} = 754 rad/s, ou seja 120 Hz, a apenas <b>2,32 vezes {WN}</b>. Um PI "
    f"simples n&#227;o tem zeros em &#177;j2{W0} e n&#227;o atenua esse dist&#250;rbio.")
n.p(f"O mesmo t<sub>s</sub> curto que garante reconverg&#234;ncia r&#225;pida &#233; o que deixa "
    f"o PLL exposto no cen&#225;rio de falta assim&#233;trica. Esse compromisso entre banda de "
    f"rastreamento e rejei&#231;&#227;o do ripple de 2{W0} &#233; o eixo central do trabalho.")

n.h("8. O cen&#225;rio BAD_PLL")
n.p(f"A flag <i>BAD_PLL</i> escala os <b>dois</b> ganhos por 0,2, o que preserva a raz&#227;o "
    f"K<sub>i</sub>/K<sub>p</sub> e move o par no plano {XI}&#8211;{WN} assim:")
n.eq(f"{WN}' = {SQ}(0,2)&#183;{WN} = 0,447&#183;325,3 = 145,5 rad/s<br/>"
     f"{XI}' = 0,707&#183;{SQ}(0,2) = 0,3162", "7")
n.gap(8)
n.p("Ou seja, o cen&#225;rio degrada <b>banda e amortecimento ao mesmo tempo</b>, n&#227;o s&#243; "
    "a velocidade de rastreamento. Ao descrever a sintonia inadequada no texto, vale dizer "
    "isso: o PLL n&#227;o fica apenas mais lento, fica tamb&#233;m subamortecido.")

n.h("9. Antes de simular")
n.table(["Conferir", "Valor esperado"],
        [["<i>qsi</i>", "0,707"],
         ["<i>kp_pll</i>", "460"],
         ["<i>ki_pll</i>", "105820"],
         ["<i>BAD_PLL</i>",
          "<i>false</i> para o caso nominal; <i>true</i> aplica o fator 0,2 nos dois ganhos"],
         ["Base de tens&#227;o",
          "20 kV linha-linha. Se mudar, os ganhos do PLL precisam ser reescalados junto, "
          "ver se&#231;&#227;o 4"]],
        [3.4, 11.3])

n.refs([
    "ALVES, Andr&#233; G. P.; DIAS, Robson F. S.; ROLIM, Lu&#237;s G. B. A Smooth "
    "Synchronization Methodology for the Reconnection of Autonomous Microgrids. "
    "<i>Journal of Control, Automation and Electrical Systems</i>, v. 31, p. 665-674, 2020. "
    "DOI 10.1007/s40313-020-00576-x.",
    "TEODORESCU, Remus; LISERRE, Marco; RODR&#205;GUEZ, Pedro. <i>Grid Converters for "
    "Photovoltaic and Wind Power Systems</i>. Chichester: John Wiley &amp; Sons, Ltd, 2011. "
    "ISBN 978-0-470-05751-3.",
    "OGATA, Katsuhiko. <i>Modern Control Engineering</i>. 5. ed. London: Pearson, 2009.",
    "FRANKLIN, Gene F.; POWELL, J. David; EMAMI-NAEINI, Abbas. <i>Feedback Control of "
    "Dynamic Systems</i>. 4. ed. Upper Saddle River: Prentice Hall, 2002. ISBN 0-13-032393-4.",
    "KARIMI-GHARTEMANI, Masoud. <i>Enhanced Phase-Locked Loop Structures for Power and "
    "Energy Applications</i>. Hoboken: John Wiley &amp; Sons / IEEE Press, 2014. "
    "ISBN 978-1-118-79502-6.",
])
n.gap(6)
n.note("As equa&#231;&#245;es (1) a (3) est&#227;o em Alves, Dias &amp; Rolim (2020), se&#231;&#227;o "
       "4.1, equa&#231;&#245;es (7) a (11). A forma K<sub>p</sub> = 9,2/t<sub>s</sub> usada aqui, "
       "com o crit&#233;rio de 1%, est&#225; em Teodorescu, Liserre &amp; Rodr&#237;guez (2011), "
       "se&#231;&#227;o 4.2.2.3, p. 56, equa&#231;&#245;es (4.35) a (4.38). A equa&#231;&#227;o "
       "caracter&#237;stica com a magnitude <i>U</i> est&#225; em Karimi-Ghartemani (2014), "
       "equa&#231;&#227;o (6.4), p. 135.")

out = n.build()
if "--preview" in sys.argv:
    render_preview(out, Path(sys.argv[sys.argv.index("--preview") + 1]))
