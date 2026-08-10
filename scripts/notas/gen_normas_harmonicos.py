# -*- coding: utf-8 -*-
"""Nota tecnica: IEEE 519-2014 e IEEE 1547-2018 e sua aplicacao no dashboard."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pdfnote import Note, render_preview  # noqa: E402

LE = "&lt;"
LEQ = "&#8804;"
X = "&#215;"

n = Note(
    title="Os limites de harm&#244;nico do IEEE 519 e do IEEE 1547",
    subtitle="O que cada norma exige, onde achar cada n&#250;mero e como isso vira "
             "a tabela de harm&#244;nicas do dashboard",
    out=ROOT / "output" / "normas_harmonicos.pdf",
    meta_left="Trabalho de Conclus&#227;o de Curso &#183; Engenharia El&#233;trica &#183; UERJ<br/>"
              "Estabilidade do SRF-PLL em inversores conectados &#224; rede",
    meta_right="Nota t&#233;cnica<br/>9 de agosto de 2026",
    running_head="Limites de harm&#244;nico &#8212; IEEE 519 e IEEE 1547",
)

# ── 1 ────────────────────────────────────────────────────────────────────────
n.h("1. Do que trata esta nota")
n.p("O relat&#243;rio HTML gerado pelo projeto tem, abaixo do espectro de Fourier, uma "
    "tabela de harm&#244;nicas em que algumas c&#233;lulas aparecem destacadas em vermelho "
    "ou amarelo. Esta nota explica <b>de onde vem cada um desses limites</b>, o que "
    "as duas normas de fato exigem, e quais s&#227;o os limites de validade da "
    "compara&#231;&#227;o que o dashboard faz.")
n.p("As duas normas n&#227;o competem: o <b>IEEE 519-2014</b> &#233; uma <i>recommended "
    "practice</i> geral, escrita para qualquer usu&#225;rio da rede, e &#233; a origem "
    "hist&#243;rica dos n&#250;meros. O <b>IEEE 1547-2018</b> &#233; um <i>standard</i> "
    "espec&#237;fico para recursos energ&#233;ticos distribu&#237;dos (DER), e adapta os "
    "limites do 519 &#224; realidade de um inversor. O guia de aplica&#231;&#227;o do 1547 "
    "chega a mandar, explicitamente, estimar os harm&#244;nicos da DER <i>pelo IEEE 519</i>.")
n.p("O sistema em quest&#227;o &#233; uma unidade fotovoltaica conectada &#224; <b>Barra 2</b> "
    "da rede IEEE de 9 barras, em <b>20 kV</b>, base de 100 MVA e 60 Hz. Toda a "
    "sele&#231;&#227;o de linhas e tabelas abaixo decorre desses dois dados: a classe de "
    "tens&#227;o e o fato de ser <b>equipamento de gera&#231;&#227;o</b>.")

# ── 2 ────────────────────────────────────────────────────────────────────────
n.h("2. Onde encontrar cada coisa nos PDFs")
n.p("Os dois documentos t&#234;m capa e p&#225;ginas preliminares, ent&#227;o o n&#250;mero da "
    "p&#225;gina no leitor de PDF <b>n&#227;o coincide</b> com o n&#250;mero impresso no "
    "rodap&#233;. Abaixo v&#227;o os dois, para evitar procura desnecess&#225;ria.")
n.gap(2)
n.p("<b>IEEE 519-2014</b> &#8212; p&#225;gina do PDF = p&#225;gina impressa + 12.")
n.table(["Conte&#250;do", "Impressa", "PDF"],
        [["Cl&#225;usula 3 &#8212; defini&#231;&#245;es (PCC, TDD, THD)", "3&#8211;4", "15&#8211;16"],
         ["<b>Cl&#225;usula 4 &#8212; medi&#231;&#227;o de harm&#244;nicos</b>", "<b>4&#8211;5</b>", "<b>16&#8211;17</b>"],
         ["5.1 e Tabela 1 &#8212; distor&#231;&#227;o de tens&#227;o", "6", "18"],
         ["5.2 e Tabela 2 &#8212; corrente, 120 V a 69 kV", "7", "19"],
         ["5.3 e Tabela 3 &#8212; corrente, 69 a 161 kV", "8", "20"],
         ["5.4 e Tabela 4 &#8212; corrente, acima de 161 kV", "9", "21"],
         ["5.5 e Tabela 5 &#8212; multiplicadores", "9&#8211;10", "21&#8211;22"],
         ["Anexos A a D", "11+", "23+"]],
        [8.7, 3.0, 3.0])
n.gap(6)
n.p("<b>IEEE 1547.2-2023</b> &#8212; p&#225;gina do PDF = p&#225;gina impressa + 1.")
n.table(["Conte&#250;do", "Impressa", "PDF"],
        [["Tabela 15 &#8212; mudan&#231;as de QEE 2003 &#8594; 2018", "137", "138"],
         ["7.1 &#8212; inje&#231;&#227;o CC (e os n&#250;meros em texto corrido)", "137&#8211;140", "138&#8211;141"],
         ["7.2 &#8212; RVC e flicker (Tabela 16)", "140&#8211;144", "141&#8211;145"],
         ["<b>7.3 &#8212; distor&#231;&#227;o de corrente (Tabelas 17 e 18)</b>", "<b>144&#8211;146</b>", "<b>145&#8211;147</b>"],
         ["7.4 &#8212; sobretens&#227;o", "146&#8211;148", "147&#8211;149"],
         ["7.5 &#8212; roteiro de estudo de QEE", "148", "149"]],
        [8.7, 3.0, 3.0])
n.gap(4)
n.note("O arquivo cujo nome sugere ser o IEEE 1547-2018 &#233;, na verdade, o <b>IEEE "
       "Std 1547.2-2023</b> &#8212; o <i>Application Guide</i>. Ele serve para quase tudo: "
       "cita literalmente o texto normativo do 1547-2018 entre aspas e ainda explica a "
       "origem de cada n&#250;mero. A &#250;nica limita&#231;&#227;o est&#225; registrada na "
       "se&#231;&#227;o 4.3 desta nota.")

# ── 3 ────────────────────────────────────────────────────────────────────────
n.h("3. IEEE 519-2014")

n.p("<b>3.1 A l&#243;gica da norma.</b> A abertura da Cl&#225;usula 5 estabelece que "
    "controlar harm&#244;nico &#233; responsabilidade conjunta: o <b>usu&#225;rio limita a "
    "corrente que injeta</b> e o <b>dono do sistema limita a tens&#227;o resultante</b>. "
    "A premissa &#233; que, se todos respeitarem o limite de corrente, a distor&#231;&#227;o "
    "de tens&#227;o fica aceit&#225;vel por consequ&#234;ncia. Por isso h&#225; uma tabela de "
    "tens&#227;o e tr&#234;s de corrente: s&#227;o os dois lados do mesmo contrato, n&#227;o "
    "alternativas.")
n.p("Dois avisos de escopo valem para todas as tabelas. Primeiro, os limites se aplicam "
    "<b>somente no PCC</b> &#8212; a norma &#233; expl&#237;cita ao dizer que n&#227;o devem "
    "ser aplicados a equipamentos individuais nem a pontos internos &#224; instala&#231;&#227;o, "
    "onde os valores s&#227;o legitimamente maiores por falta de diversidade e cancelamento. "
    "Segundo, todas as tabelas tratam apenas de <b>m&#250;ltiplos inteiros da "
    "fundamental</b>; inter-harm&#244;nicos saem para o Anexo A, caso a caso.")

n.p("<b>3.2 Cl&#225;usula 4 &#8212; como medir.</b> Esta &#233; a metade da norma que "
    "costuma passar despercebida, e &#233; a que fala diretamente de FFT. Ela remete &#224;s "
    "normas IEC 61000-4-7 e IEC 61000-4-30, e resume:")
n.table(["Item", "Exig&#234;ncia"],
        [["4.1 Janela", "12 ciclos (&#8776; 200 ms) em 60 Hz, o que d&#225; resolu&#231;&#227;o "
                        "espectral de 5 Hz. A magnitude da harm&#244;nica &#233; o bin central "
                        "<b>combinado em RMS com os dois bins vizinhos</b> de 5 Hz."],
         ["4.2 <i>Very short</i>", "agrega&#231;&#227;o RMS de 15 janelas consecutivas &#8594; 3 s"],
         ["4.3 <i>Short</i>", "agrega&#231;&#227;o RMS de 200 valores <i>very short</i> &#8594; 10 min"],
         ["4.4 Estat&#237;stica", "compara-se <b>percentil</b>, n&#227;o valor: 99&#186; percentil "
                                 "di&#225;rio dos valores de 3 s; 95&#186; e 99&#186; percentis "
                                 "semanais dos de 10 min"]],
        [3.2, 11.5])
n.gap(4)
n.note("A consequ&#234;ncia disso est&#225; na se&#231;&#227;o 7: os limites do 519 s&#227;o "
       "estat&#237;sticos, medidos em campo ao longo de <b>semanas</b>. Isso muda o que se "
       "pode afirmar a partir de uma simula&#231;&#227;o de segundos.")

n.p("<b>3.3 Cl&#225;usula 5 &#8212; as tabelas.</b> A <b>Tabela 1</b> trata de distor&#231;&#227;o "
    "de tens&#227;o, em porcentagem da tens&#227;o nominal no PCC:")
n.table(["Tens&#227;o V no PCC", "Individual (%)", "THD (%)"],
        [["V " + LEQ + " 1,0 kV", "5,0", "8,0"],
         ["<b>1 kV " + LE + " V " + LEQ + " 69 kV</b>", "<b>3,0</b>", "<b>5,0</b>"],
         ["69 kV " + LE + " V " + LEQ + " 161 kV", "1,5", "2,5"],
         ["161 kV " + LE + " V", "1,0", "1,5"]],
        [6.7, 4.0, 4.0])
n.gap(4)
n.p("A Barra 2, em 20 kV, cai na segunda linha: <b>3,0% por ordem individual</b>. Note "
    "que o limite de tens&#227;o &#233; <b>constante por ordem</b> &#8212; a norma n&#227;o "
    "escalona tens&#227;o por ordem harm&#244;nica, s&#243; corrente.")
n.p("A <b>Tabela 2</b> trata de corrente para sistemas de 120 V a 69 kV. As linhas s&#227;o "
    "escolhidas pela raz&#227;o entre a corrente de curto dispon&#237;vel e a corrente de "
    "demanda m&#225;xima (I<sub>sc</sub>/I<sub>L</sub>):")
n.table(["I<sub>sc</sub>/I<sub>L</sub>", "3&#8211;10", "11&#8211;16", "17&#8211;22",
         "23&#8211;34", "35&#8211;50", "TDD"],
        [["<b>" + LE + " 20</b>", "<b>4,0</b>", "<b>2,0</b>", "<b>1,5</b>", "<b>0,6</b>",
          "<b>0,3</b>", "<b>5,0</b>"],
         ["20&#8211;50", "7,0", "3,5", "2,5", "1,0", "0,5", "8,0"],
         ["50&#8211;100", "10,0", "4,5", "4,0", "1,5", "0,7", "12,0"],
         ["100&#8211;1000", "12,0", "5,5", "5,0", "2,0", "1,0", "15,0"],
         ["&#62;&#160;1000", "15,0", "7,0", "6,0", "2,5", "1,4", "20,0"]],
        [2.7, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0])
n.gap(4)
n.p("Valores em % de I<sub>L</sub>, a corrente de demanda m&#225;xima, definida logo abaixo "
    "da tabela como <b>a soma das demandas m&#225;ximas dos doze meses anteriores dividida "
    "por doze</b>. As faixas de ordem est&#227;o escritas na norma como "
    "3 " + LEQ + " h " + LE + " 11 e assim por diante; acima elas aparecem como intervalos "
    "de ordens inteiras, que &#233; como o dashboard as usa.")
n.p("A tabela tem tr&#234;s notas de rodap&#233;, e a terceira &#233; a que decide o caso "
    "deste projeto:")
n.table(["Nota", "Conte&#250;do"],
        [["a", "harm&#244;nicos pares limitados a <b>25% do limite &#237;mpar</b> correspondente"],
         ["b", "distor&#231;&#245;es que resultem em <i>offset</i> CC (por exemplo conversores "
               "de meia onda) <b>n&#227;o s&#227;o permitidas</b> &#8212; &#233; proibi&#231;&#227;o, "
               "n&#227;o limite num&#233;rico"],
         ["<b>c</b>", "<b>todo equipamento de gera&#231;&#227;o fica limitado a estes valores "
                      "independentemente da rela&#231;&#227;o I<sub>sc</sub>/I<sub>L</sub> real</b>"]],
        [1.6, 13.1])
n.gap(4)
n.p("A nota <b>c</b> elimina qualquer c&#225;lculo de curto-circuito: por ser unidade "
    "geradora, o inversor est&#225; obrigado &#224; linha " + LE + "&#160;20, a mais "
    "restritiva da tabela. &#201; a mesma filosofia da Tabela 16 do guia do 1547, que "
    "adota o limite mais estrito de RVC por se aplicar a instala&#231;&#245;es individuais: "
    "quando o alvo &#233; um agente isolado, a norma reserva a folga do sistema para os demais.")
n.p("As <b>Tabelas 3 e 4</b> repetem a estrutura para classes de tens&#227;o mais altas, "
    "com valores progressivamente menores &#8212; a Tabela 3 (69 a 161 kV) &#233; a Tabela 2 "
    "pela metade. O padr&#227;o tem sentido f&#237;sico: em transmiss&#227;o a imped&#226;ncia "
    "&#233; menor, e a mesma corrente harm&#244;nica produz distor&#231;&#227;o de tens&#227;o "
    "que se propaga para muito mais gente. Nenhuma das duas se aplica a 20 kV.")
n.p("A <b>Tabela 5</b> &#233; a &#250;nica que afrouxa limites: concede multiplicadores de "
    "1,4 a 2,2 a quem reduzir as ordens baixas. A equa&#231;&#227;o (3) revela a origem &#8212; "
    "o multiplicador &#233; a raiz de p/6, com p o n&#250;mero de pulsos de um retificador "
    "trif&#225;sico. &#201; um b&#244;nus pensado para conversores multipulso comutados pela "
    "rede, n&#227;o para inversores PWM, e n&#227;o se aplica aqui. Vale registrar porque "
    "evidencia para que tipo de equipamento o 519 foi escrito &#8212; e explica por que o "
    "1547 precisou de uma cl&#225;usula pr&#243;pria para DER.")

# ── 4 ────────────────────────────────────────────────────────────────────────
n.h("4. IEEE 1547-2018, lido pelo guia 1547.2-2023")

n.p("<b>4.1 A Tabela 15.</b> O guia abre a Cl&#225;usula 7 resumindo o que mudou em "
    "qualidade de energia entre a vers&#227;o de 2003 e a de 2018:")
n.table(["Item de QEE", "1547-2003", "1547-2018"],
        [["Inje&#231;&#227;o CC", "0,5% da corrente", "sem mudan&#231;a"],
         ["RVC", "n&#227;o existia", "novo: 3% em MT, 5% em BT"],
         ["Flicker", "&#8220;n&#227;o deve causar&#8221;", "novo: P<sub>st</sub> " + LE +
          " 0,35, P<sub>lt</sub> " + LE + " 0,25"],
         ["<b>Harm&#244;nico de corrente</b>", "<b>" + LE + " 5% TDD</b>",
          "<b>" + LE + " 5% TRD, pares relaxados</b>"],
         ["<b>Harm&#244;nico de tens&#227;o</b>", "<b>nenhum</b>", "<b>nenhum</b>"],
         ["Sobretens&#227;o tempor&#225;ria", "&#8220;n&#227;o causar GFO perturbadora&#8221;",
          "novo: at&#233; 138% V<sub>l-g</sub>"],
         ["Sobretens&#227;o instant&#226;nea", "n&#227;o existia", "novo: 2 pu em 1,5 ms; 1,4 pu em 16 ms"]],
        [5.1, 4.2, 5.4])
n.gap(4)
n.p("Duas leituras imediatas. A linha de <b>harm&#244;nico de tens&#227;o permanece "
    "&#8220;nenhum&#8221;</b>: o 1547 n&#227;o imp&#245;e limite de distor&#231;&#227;o de "
    "tens&#227;o, porque isso &#233; responsabilidade do operador da rede, n&#227;o da DER. "
    "Logo, o limite de tens&#227;o usado no dashboard s&#243; pode vir da Tabela 1 do 519 "
    "&#8212; n&#227;o h&#225; alternativa. E a troca de <b>TDD por TRD</b>, com pares "
    "relaxados, s&#227;o as &#250;nicas duas mudan&#231;as de harm&#244;nico entre as duas "
    "vers&#245;es.")

n.p("<b>4.2 A mudan&#231;a de &#237;ndice, e por que ela importa aqui.</b> O TDD do 519 "
    "&#233; medido em porcentagem de I<sub>L</sub>, a m&#233;dia de doze meses de demanda "
    "m&#225;xima real. O <b>TRD</b> do 1547 usa <b>I<sub>rated</sub></b>, a corrente nominal "
    "do inversor &#8212; um dado de projeto. A diferen&#231;a &#233; decisiva para este "
    "trabalho: I<sub>L</sub> simplesmente n&#227;o existe numa simula&#231;&#227;o "
    "eletromagn&#233;tica de poucos segundos, enquanto I<sub>rated</sub> &#233; conhecido. "
    "&#201; por isso que <b>todos os limites de corrente do dashboard s&#227;o expressos em "
    "porcentagem da corrente nominal do inversor</b>, mesmo quando o valor num&#233;rico "
    "coincide com o do 519.")

n.p("<b>4.3 O texto do 7.3 e as duas tabelas em imagem.</b> O requisito citado "
    "literalmente diz que, com a DER servindo <b>cargas lineares equilibradas</b>, a "
    "inje&#231;&#227;o de corrente harm&#244;nica no PCC n&#227;o pode exceder as Tabelas 17 e "
    "18, e que essa inje&#231;&#227;o deve ser <b>exclusiva de qualquer harm&#244;nico j&#225; "
    "presente na tens&#227;o da rede sem a DER conectada</b>. S&#227;o duas condicionantes "
    "importantes: vale sob carga equilibrada, e mede-se a <b>contribui&#231;&#227;o da "
    "DER</b>, n&#227;o a distor&#231;&#227;o total do sistema.")
n.p("As Tabelas 17 e 18 est&#227;o no PDF como <b>imagem</b>, n&#227;o como texto. Elas "
    "podem ser lidas na tela, na p&#225;gina impressa 144, mas nenhuma extra&#231;&#227;o "
    "autom&#225;tica recupera seus n&#250;meros. Os valores usados no dashboard v&#234;m de "
    "uma frase em <b>texto corrido</b>, na se&#231;&#227;o de inje&#231;&#227;o CC "
    "(p&#225;gina impressa 138), que enumera os limites de baixa ordem: <b>4% nos "
    "&#237;mpares individuais; 1%, 2%, 3% e 4% na 2&#170;, 4&#170;, 6&#170; e 8&#170; ordens; "
    "e 5% de TRD</b>.")

n.p("<b>4.4 As duas notas de rodap&#233;.</b> A nota 118 introduz uma toler&#226;ncia "
    "transit&#243;ria que n&#227;o aparece em nenhuma tabela: os limites s&#227;o valores de "
    "projeto para <b>opera&#231;&#227;o normal com dura&#231;&#227;o superior a uma hora</b>, "
    "e em <b>partidas ou condi&#231;&#245;es incomuns podem ser excedidos em 50%</b>. J&#225; "
    "a nota 119 fala em TDD e demanda de 15 ou 30 minutos, contradizendo a Tabela 15 e o "
    "pr&#243;prio t&#237;tulo das Tabelas 17 e 18; &#233; res&#237;duo editorial herdado do "
    "519, e prevalece o texto normativo: <b>TRD sobre I<sub>rated</sub></b>.")

n.p("<b>4.5 O par&#225;grafo que sustenta a metodologia.</b> A se&#231;&#227;o 7.3.1 "
    "esclarece que o requisito se aplica &#224; corrente no PCC com a DER servindo cargas "
    "lineares, isto &#233;, <b>num sistema sem outras fontes de harm&#244;nico</b>. E "
    "acrescenta que, na pr&#225;tica, isso <b>n&#227;o &#233; realiz&#225;vel em campo</b>, "
    "servindo como base para <b>ensaio de tipo em laborat&#243;rio</b>. Uma simula&#231;&#227;o "
    "eletromagn&#233;tica com um &#250;nico inversor e sem outras fontes harm&#244;nicas "
    "&#233; exatamente essa condi&#231;&#227;o idealizada. Isso torna o crit&#233;rio do 1547 "
    "<b>metodologicamente compat&#237;vel</b> com o que se simula aqui &#8212; ao contr&#225;rio "
    "do 519, que &#233; estat&#237;stico e de campo.")
n.p("Na mesma linha, a se&#231;&#227;o 7.5 do guia descreve o roteiro de um estudo de "
    "qualidade de energia e recomenda, entre outros passos, <b>construir os modelos da "
    "rede e da DER em um programa de transit&#243;rios eletromagn&#233;ticos</b>, "
    "<b>simular opera&#231;&#245;es de falta e elimina&#231;&#227;o</b> em diversas "
    "condi&#231;&#245;es, e <b>estimar os harm&#244;nicos contribu&#237;dos pela DER segundo "
    "o IEEE 519-2014</b>. &#201; a metodologia deste trabalho, descrita pelo guia da "
    "pr&#243;pria norma.")
n.gap(2)
n.note("A cl&#225;usula 7.3.3 acrescenta uma condicionante que raramente se menciona: os "
       "limites das Tabelas 17 e 18 <b>s&#243; s&#227;o permiss&#237;veis</b> se o "
       "transformador de conex&#227;o n&#227;o for submetido a mais de 5% da sua corrente "
       "nominal em harm&#244;nico. Acima disso, aplica-se a metodologia do IEEE C57.110 e o "
       "transformador pode precisar ser reavaliado.")

# ── 5 ────────────────────────────────────────────────────────────────────────
n.h("5. As duas normas lado a lado")
n.table(["", "IEEE 519-2014", "IEEE 1547-2018"],
        [["Natureza", "<i>recommended practice</i>", "<i>standard</i> (requisito)"],
         ["Sujeito", "qualquer usu&#225;rio da rede", "a DER especificamente"],
         ["Base do percentual", "I<sub>L</sub>: demanda m&#233;dia de 12 meses",
          "I<sub>rated</sub>: corrente nominal de projeto"],
         ["&#205;ndice agregado", "TDD, 5,0%", "TRD, 5%"],
         ["&#205;mpar de ordem baixa", "4,0%", "4% &#8212; id&#234;ntico"],
         ["Pares de ordem baixa", "25% do &#237;mpar, ou seja 1,0%",
          "1%, 2%, 3%, 4% na 2&#170;, 4&#170;, 6&#170;, 8&#170;"],
         ["Limite de tens&#227;o", "3,0% individual; THD 5,0%", "nenhum"],
         ["Condi&#231;&#227;o de medi&#231;&#227;o", "percentis sobre dias e semanas",
          "ensaio de tipo, carga linear equilibrada"],
         ["Toler&#226;ncia transit&#243;ria", "n&#227;o trata",
          "limites " + X + "1,5 em partida ou condi&#231;&#227;o incomum"],
         ["<b>Compat&#237;vel com simula&#231;&#227;o?</b>", "<b>n&#227;o</b>", "<b>sim</b>"]],
        [4.5, 5.1, 5.1])
n.gap(4)
n.p("A leitura pr&#225;tica &#233;: <b>os n&#250;meros nasceram no 519, mas o crit&#233;rio "
    "que se pode legitimamente aplicar a uma simula&#231;&#227;o &#233; o do 1547</b>. Onde "
    "os dois divergem, o dashboard segue o 1547, com uma exce&#231;&#227;o obrigat&#243;ria: "
    "o limite de tens&#227;o, que s&#243; existe no 519.")

# ── 6 ────────────────────────────────────────────────────────────────────────
n.pagebreak()
n.h("6. Aplica&#231;&#227;o no dashboard")
n.p("<b>6.1 Os limites efetivamente aplicados.</b> Cada c&#233;lula da tabela de "
    "harm&#244;nicas &#233; comparada, por ordem, aos valores abaixo:")
n.table(["Grandeza e ordem", "Limite", "Fonte"],
        [["Corrente, &#237;mpares de ordem 3 a 10", "4%",
          "1547-2018 7.3, texto direto; coincide com o 519"],
         ["Corrente, &#237;mpares de ordem 11 a 16", "2%",
          "519-2014 Tabela 2, linha " + LE + "&#160;20 &#8212; <b>infer&#234;ncia, ver 8</b>"],
         ["Corrente, 2&#170;/4&#170;/6&#170;/8&#170; ordem", "1 / 2 / 3 / 4%",
          "1547-2018 7.3, texto direto (pares relaxados)"],
         ["Tens&#227;o, qualquer ordem individual", "3%",
          "519-2014 Tabela 1, classe 1 a 69 kV"],
         ["Desequil&#237;brio em 120 Hz (eixos <i>dq</i>)", "2% e 3%",
          "<b>emp&#237;rico</b>, tese de doutorado do coorientador &#8212; sem base normativa"]],
        [5.5, 2.4, 6.8])
n.gap(4)
n.p("Todos os limites de corrente s&#227;o percentuais da <b>corrente nominal do "
    "inversor</b>, que vale 1,0 pu nas condi&#231;&#245;es de refer&#234;ncia do modelo. "
    "Como a base &#233; unit&#225;ria, os percentuais traduzem-se diretamente para os "
    "valores em pu exibidos no espectro: 4% correspondem a 0,04 pu. O limite de tens&#227;o "
    "&#233; percentual da tens&#227;o nominal da Barra 2.")

n.p("<b>6.2 Por que a checagem por ordem s&#243; vale no dom&#237;nio abc.</b> O relat&#243;rio "
    "mostra o espectro em duas representa&#231;&#245;es: as fases <i>a</i>, <i>b</i>, <i>c</i> "
    "e os eixos <i>d</i>, <i>q</i> do referencial s&#237;ncrono. A transformada para o "
    "referencial s&#237;ncrono desloca cada componente em uma vez a frequ&#234;ncia "
    "fundamental, para cima ou para baixo conforme a sequ&#234;ncia, de modo que "
    "<b>duas ordens diferentes caem no mesmo ponto do espectro</b>: a 5&#170; e a 7&#170; "
    "se somam em 360 Hz, a 11&#170; e a 13&#170; em 720 Hz. Um pico ali n&#227;o &#233; "
    "atribu&#237;vel a uma ordem espec&#237;fica, e portanto n&#227;o pode ser comparado a "
    "nenhuma linha das tabelas.")
n.p("Por isso a <b>checagem normativa roda apenas no dom&#237;nio abc</b>. O espectro em "
    "eixos <i>dq</i> serve a outro prop&#243;sito: o pico em 120 Hz &#233; a fundamental "
    "refletida em sequ&#234;ncia negativa, e funciona como medida direta do "
    "<b>desequil&#237;brio</b> visto pelo inversor &#8212; que &#233; justamente a grandeza "
    "de interesse nas faltas assim&#233;tricas estudadas no trabalho. O limiar aplicado ali "
    "&#233; emp&#237;rico, extra&#237;do da literatura, e est&#225; identificado como tal na "
    "legenda.")

n.p("<b>6.3 Os segmentos temporais.</b> O espectro &#233; calculado separadamente antes da "
    "falta, durante a falta e depois da elimina&#231;&#227;o. A checagem normativa &#233; "
    "suprimida no segmento <b>durante a falta</b>, e o transit&#243;rio inicial de partida "
    "do PLL &#233; descartado de todo c&#225;lculo. Ambas as decis&#245;es t&#234;m amparo na "
    "nota 118 do guia do 1547, citada na se&#231;&#227;o 4.4: os limites s&#227;o valores de "
    "regime, para condi&#231;&#245;es de mais de uma hora. J&#225; o crit&#233;rio de "
    "desequil&#237;brio em 120 Hz <b>continua valendo durante a falta</b> &#8212; &#233; "
    "exatamente ali que a sequ&#234;ncia negativa &#233; mais severa, e suprimi-lo esvaziaria "
    "o indicador.")

n.p("<b>6.4 Como ler as cores.</b>")
n.table(["Destaque", "Significa"],
        [["vermelho", "excede um limite do IEEE 519 ou do IEEE 1547; a c&#233;lula traz o "
                      "limite violado em seu texto de apoio"],
         ["amarelo", "desequil&#237;brio acima do patamar emp&#237;rico, apenas na linha de "
                     "120 Hz dos eixos <i>dq</i>"],
         ["neutro em destaque", "linha da fundamental &#8212; refer&#234;ncia de escala, "
                                "n&#227;o comparada a limite algum"],
         ["apagado", "valor pr&#243;ximo de zero, sem crit&#233;rio normativo aplic&#225;vel"]],
        [3.6, 11.1])

# ── 7 ────────────────────────────────────────────────────────────────────────
n.h("7. O que esta compara&#231;&#227;o n&#227;o &#233;")
n.p("Este ponto precisa ficar expl&#237;cito para qualquer leitor do relat&#243;rio. A "
    "Cl&#225;usula 4 do 519, resumida na se&#231;&#227;o 3.2, exige agrega&#231;&#227;o em "
    "janelas de 3 segundos e 10 minutos e avalia&#231;&#227;o por percentis acumulados ao "
    "longo de dias e semanas. Nada disso &#233; comput&#225;vel a partir de uma "
    "simula&#231;&#227;o eletromagn&#233;tica cuja dura&#231;&#227;o total &#233; da ordem de "
    "um segundo.")
n.p("Em consequ&#234;ncia, <b>o dashboard faz uma compara&#231;&#227;o indicativa</b> de um "
    "instant&#226;neo determin&#237;stico contra valores normativos, e n&#227;o uma "
    "medi&#231;&#227;o de conformidade. A distin&#231;&#227;o n&#227;o &#233; formalidade: "
    "afirmar conformidade exigiria o procedimento de medi&#231;&#227;o completo. O que a "
    "tabela oferece &#233; uma <b>refer&#234;ncia de ordem de grandeza</b> &#8212; permite "
    "dizer se um harm&#244;nico observado est&#225; pr&#243;ximo, muito abaixo ou muito acima "
    "do que a norma tolera, o que basta para o prop&#243;sito de comparar cen&#225;rios de "
    "conting&#234;ncia entre si.")
n.p("H&#225; ainda tr&#234;s pontos em que o c&#225;lculo se afasta da Cl&#225;usula 4, "
    "registrados por transpar&#234;ncia. A janela usada &#233; de 12 ciclos nos segmentos "
    "de pr&#233; e p&#243;s-falta, coincidindo com a norma, mas de 6 ciclos durante a falta. "
    "A janela de pondera&#231;&#227;o &#233; de Hann, e n&#227;o retangular, escolha feita "
    "para conter vazamento espectral em janelas curtas. E a magnitude de cada harm&#244;nica "
    "&#233; lida como o <b>pico</b> entre os tr&#234;s bins vizinhos, onde a norma pede a "
    "<b>combina&#231;&#227;o RMS</b> dos tr&#234;s &#8212; o que subestima ligeiramente os "
    "valores exibidos.")

# ── 8 ────────────────────────────────────────────────────────────────────────
n.h("8. Pontos em aberto")
n.p("<b>O limite dos &#237;mpares de ordem 11 a 16 &#233; uma infer&#234;ncia.</b> O valor "
    "de 2% aplicado hoje vem da Tabela 2 do 519, e n&#227;o da Tabela 17 do 1547, que "
    "n&#227;o p&#244;de ser extra&#237;da por estar em imagem. A infer&#234;ncia &#233; "
    "razo&#225;vel &#8212; o pr&#243;prio guia afirma que o requisito do 1547 se baseia nos "
    "limites mais restritivos do 519, e os valores de ordem baixa coincidem exatamente "
    "entre as duas normas &#8212; mas <b>n&#227;o foi confirmada por leitura direta</b>. "
    "Est&#225; assinalada como tal no c&#243;digo e no texto de apoio da tabela. Basta abrir "
    "o guia na p&#225;gina impressa 144 e transcrever a linha correspondente para encerrar "
    "a quest&#227;o.")
n.p("<b>Pares de ordem 10 e 12 n&#227;o t&#234;m limite confirmado</b> em nenhuma das duas "
    "fontes dispon&#237;veis em texto. As c&#233;lulas correspondentes ficam sem destaque de "
    "viola&#231;&#227;o, o que &#233; prefer&#237;vel a aplicar um valor inventado.")
n.p("<b>Duas melhorias de ader&#234;ncia est&#227;o mapeadas e n&#227;o implementadas</b>: "
    "trocar a leitura de pico pela combina&#231;&#227;o RMS de tr&#234;s bins, conforme a "
    "Cl&#225;usula 4.1 do 519; e substituir a supress&#227;o da checagem durante a falta por "
    "um limite multiplicado por 1,5, conforme a nota 118 do guia do 1547 &#8212; o que "
    "&#233; mais fiel &#224; norma e mais informativo que suprimir por completo.")

n.refs([
    "IEEE. <i>IEEE Recommended Practice and Requirements for Harmonic Control in "
    "Electric Power Systems</i>. IEEE Std 519-2014. New York: Institute of Electrical "
    "and Electronics Engineers, 2014.",
    "IEEE. <i>IEEE Standard for Interconnection and Interoperability of Distributed "
    "Energy Resources with Associated Electric Power Systems Interfaces</i>. "
    "IEEE Std 1547-2018. New York: Institute of Electrical and Electronics Engineers, 2018.",
    "IEEE. <i>IEEE Application Guide for IEEE Std 1547-2018, IEEE Standard for "
    "Interconnection and Interoperability of Distributed Energy Resources with "
    "Associated Electric Power Systems Interfaces</i>. IEEE Std 1547.2-2023. "
    "New York: Institute of Electrical and Electronics Engineers, 2023.",
    "IEEE. <i>IEEE Standard Conformance Test Procedures for Equipment Interconnecting "
    "Distributed Energy Resources with Electric Power Systems and Associated "
    "Interfaces</i>. IEEE Std 1547.1-2020. New York: Institute of Electrical and "
    "Electronics Engineers, 2020.",
    "IEEE. <i>IEEE Standard General Requirements for Liquid-Immersed Distribution, "
    "Power, and Regulating Transformers</i>. IEEE Std C57.12.00-2000. New York: "
    "Institute of Electrical and Electronics Engineers, 2000.",
    "INTERNATIONAL ELECTROTECHNICAL COMMISSION. <i>Electromagnetic compatibility (EMC) "
    "&#8212; Part 4-7: Testing and measurement techniques &#8212; General guide on "
    "harmonics and interharmonics measurements and instrumentation</i>. IEC 61000-4-7.",
    "INTERNATIONAL ELECTROTECHNICAL COMMISSION. <i>Electromagnetic compatibility (EMC) "
    "&#8212; Part 4-30: Testing and measurement techniques &#8212; Power quality "
    "measurement methods</i>. IEC 61000-4-30.",
    "ALVES, Andr&#233; Gustavo Pereira. <i>Metodologia para Auto-Ajuste de Controladores "
    "de Corrente em Conversores Fonte de Tens&#227;o Conectados a Redes Sujeitas a "
    "Dist&#250;rbios Harm&#244;nicos</i>. Tese (Doutorado em Engenharia El&#233;trica) "
    "&#8212; COPPE/UFRJ, Rio de Janeiro, 2022.",
])

out = n.build()

if "--preview" in sys.argv:
    render_preview(out, sys.argv[sys.argv.index("--preview") + 1])
