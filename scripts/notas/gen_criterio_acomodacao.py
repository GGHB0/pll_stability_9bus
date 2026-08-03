# -*- coding: utf-8 -*-
"""Nota tecnica: o criterio de acomodacao do SRF-PLL (de onde vem o 4,6)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pdfnote import Note, render_preview, XI, SQ, AR, DL, TAU, WN, W0, MINUS  # noqa: E402

TH = "θ"

n = Note(
    title="O crit&#233;rio de acomoda&#231;&#227;o do SRF-PLL",
    subtitle="Por que 4,6, o que ele custa e como defender a escolha",
    out=ROOT / "output" / "criterio_acomodacao_srf_pll.pdf",
    meta_left="Trabalho de Conclus&#227;o de Curso &#183; Engenharia El&#233;trica &#183; UERJ<br/>"
              "Complemento &#224; nota de sintonia do SRF-PLL",
    meta_right="Nota t&#233;cnica<br/>2 de agosto de 2026",
    running_head="Crit&#233;rio de acomoda&#231;&#227;o do SRF-PLL",
)

n.h("1. A pergunta")
n.p(f"O 4,6 &#233; ln(100). Ele vem do <b>crit&#233;rio de acomoda&#231;&#227;o</b>, n&#227;o da malha "
    f"do PLL. N&#227;o existe argumento t&#233;cnico que o torne mais correto que o 4 do "
    f"crit&#233;rio de 2%: os dois descrevem o mesmo envelope exponencial, mudando apenas "
    f"onde se desenha a faixa de toler&#226;ncia. Qualquer defesa precisa ser sobre o "
    f"<b>resultado</b>, {XI}{WN} = 230 rad/s, e n&#227;o sobre a constante.")

n.h("2. A escolha n&#227;o &#233; gratuita")
n.p("Fixado t<sub>s</sub> = 20 ms, trocar o crit&#233;rio muda os ganhos:")
n.table(["Crit&#233;rio", "K<sub>p</sub> = 2&#183;ln(1/" + DL + ")/t<sub>s</sub>",
         WN, "K<sub>i</sub> = " + WN + "<super>2</super>"],
        [["1% &#8212; numerador 4,6", "<b>460</b>", "325,3 rad/s", "<b>105&#160;820</b>"],
         ["2% &#8212; numerador 4", "400", "282,9 rad/s", "80&#160;000"]],
        [4.3, 4.6, 2.8, 3.0])
n.gap(6)
n.note(f"K<sub>i</sub> arredondado &#224; centena mais pr&#243;xima do valor gravado no "
       f"projeto; ({XI}{WN})<super>2</super> exato d&#225; 105&#160;832 e 80&#160;024 "
       f"respectivamente &#8212; diferen&#231;as de 0,01&#8211;0,03% que n&#227;o afetam "
       f"nenhuma conclus&#227;o desta nota.")
n.p("S&#227;o 15% de diferen&#231;a no ganho proporcional. A escolha do crit&#233;rio n&#227;o &#233; "
    "cosm&#233;tica: ela muda o sistema que vai para a simula&#231;&#227;o.")

n.h("3. O argumento a favor do crit&#233;rio mais apertado")
n.p("O PLL n&#227;o &#233; uma malha qualquer. Ele &#233; o <b>gerador da refer&#234;ncia angular</b> "
    "que define o eixo <i>dq</i> do controlador de corrente. Erro residual de &#226;ngulo n&#227;o "
    "fica contido no PLL: propaga-se multiplicativamente para i<sub>d</sub> e i<sub>q</sub> "
    "como acoplamento cruzado entre pot&#234;ncia ativa e reativa. Para um dispositivo cuja "
    "sa&#237;da &#233; refer&#234;ncia de outro la&#231;o, exigir a faixa mais apertada &#233; a "
    "escolha conservadora, e &#233; um argumento de engenharia leg&#237;timo.")
n.p("Isso &#233; coerente com a divis&#227;o da literatura: Franklin adota 1% ao tratar de "
    "acomoda&#231;&#227;o, enquanto Ogata apresenta 2% e 5% como caracteriza&#231;&#227;o "
    "gen&#233;rica da resposta ao degrau.")

n.h(f"4. O argumento contra, que vale conhecer antes da banca")
n.p(f"Ganho maior alarga a banda, e banda mais larga deixa passar mais ripple de "
    f"2{W0}. No la&#231;o linearizado, a transfer&#234;ncia do ripple de v<sub>q</sub> para "
    f"{TH} &#233; a mesma G(s) do rastreamento de fase:")
n.eq(f"{TH}(s) / v<sub>q</sub>(s) = (K<sub>p</sub>&#183;s + K<sub>i</sub>) / "
     f"(s<super>2</super> + K<sub>p</sub>&#183;s + K<sub>i</sub>)", "1")
n.gap(8)
n.p(f"Avaliada em 2{W0} = 754 rad/s, ou seja 120 Hz:")
n.table(["Ganhos", "Crit&#233;rio", "|G(j2" + W0 + ")|"],
        [["K<sub>p</sub> = 460, K<sub>i</sub> = 105&#160;820", "1%", "<b>0,627</b>"],
         ["K<sub>p</sub> = 400, K<sub>i</sub> = 80&#160;000", "2%", "0,543"]],
        [6.2, 3.0, 5.5])
n.gap(6)
n.p(f"Cerca de <b>15% mais ripple</b> atravessa com o crit&#233;rio de 1% &#8212; um c&#225;lculo "
    f"independente do 15% da tabela anterior, que coincide em ordem de grandeza mas n&#227;o "
    f"&#233; a mesma raz&#227;o se propagando pela malha. Se o eixo do "
    f"trabalho &#233; mostrar que o SRF-PLL &#233; vulner&#225;vel sob falta assim&#233;trica, "
    f"convém levantar isso por conta pr&#243;pria: o crit&#233;rio mais apertado piorou "
    f"marginalmente o pr&#243;prio fen&#244;meno investigado. N&#227;o invalida o projeto, mas "
    f"&#233; melhor apresentar do que ser perguntado.")

n.h("5. Como redigir no TCC")
n.p(f"N&#227;o defenda o 4,6. Defenda o {XI}{WN} = 230 rad/s, isto &#233;, reconverg&#234;ncia "
    f"dentro de aproximadamente um ciclo da fundamental. O crit&#233;rio entra como "
    f"<b>conven&#231;&#227;o adotada</b>, com cita&#231;&#227;o, e t<sub>s</sub> entra como a "
    f"escolha de projeto. &#201; a forma como a literatura apresenta, e evita pedir "
    f"justificativa para uma constante que &#233; ln(100).")

n.h("6. Crit&#233;rio de projeto n&#227;o &#233; crit&#233;rio de avalia&#231;&#227;o")
n.p("Os dois convivem no trabalho e s&#227;o coisas diferentes. Vale uma frase no texto "
    "separando um do outro:")
n.table(["", "Crit&#233;rio de projeto", "Crit&#233;rio de avalia&#231;&#227;o"],
        [["Natureza", "relativo ao degrau", "absoluto"],
         ["Valor", "1% (numerador 4,6)", "&#177;0,02 rad = &#177;1,15&#176;"],
         ["Onde entra", "sintonia de k<sub>p,pll</sub> e k<sub>i,pll</sub>",
          "m&#233;trica t<sub>s</sub> do dashboard e das simula&#231;&#245;es"]],
        [2.6, 5.6, 6.5])
n.gap(6)
n.p("N&#227;o se convertem um no outro sem fixar a amplitude do degrau de fase. Deixar "
    "impl&#237;cito que s&#227;o o mesmo crit&#233;rio &#233; o tipo de detalhe que vira "
    "pergunta na defesa.")

n.h("7. Resumo")
n.p(f"O 4,6 &#233; ln(100) e &#233; conven&#231;&#227;o. O que se defende &#233; "
    f"{XI}{WN} = 230 rad/s: r&#225;pido o bastante para reconvergir no primeiro ciclo "
    f"p&#243;s-falta, ao custo de 15% mais ripple de 2{W0} do que a alternativa de 2%.")

n.refs([
    "FRANKLIN, Gene F.; POWELL, J. David; EMAMI-NAEINI, Abbas. <i>Feedback Control of "
    "Dynamic Systems</i>. 4. ed. Upper Saddle River: Prentice Hall, 2002. ISBN 0-13-032393-4.",
    "OGATA, Katsuhiko. <i>Modern Control Engineering</i>. 5. ed. London: Pearson, 2009.",
    "TEODORESCU, Remus; LISERRE, Marco; RODR&#205;GUEZ, Pedro. <i>Grid Converters for "
    "Photovoltaic and Wind Power Systems</i>. Chichester: John Wiley &amp; Sons, Ltd, 2011. "
    "ISBN 978-0-470-05751-3.",
    "ALVES, Andr&#233; G. P.; DIAS, Robson F. S.; ROLIM, Lu&#237;s G. B. A Smooth "
    "Synchronization Methodology for the Reconnection of Autonomous Microgrids. "
    "<i>Journal of Control, Automation and Electrical Systems</i>, v. 31, p. 665-674, 2020. "
    "DOI 10.1007/s40313-020-00576-x.",
])

out = n.build()
if "--preview" in sys.argv:
    render_preview(out, Path(sys.argv[sys.argv.index("--preview") + 1]))
