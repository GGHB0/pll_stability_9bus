# -*- coding: utf-8 -*-
"""Nota tecnica: propostas de correcao das citacoes de alto risco do TCC V10."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from pdfnote import Note, render_preview  # noqa: E402
from reportlab.platypus import KeepTogether  # noqa: E402

n = Note(
    title="Revis&#227;o das cita&#231;&#245;es do TCC",
    subtitle="Cinco trechos em que a fonte citada n&#227;o sustenta a frase, e o que propomos no lugar",
    out=ROOT / "output" / "revisao_citacoes_alto_risco.pdf",
    meta_left="Trabalho de Conclus&#227;o de Curso &#183; Engenharia El&#233;trica &#183; UERJ<br/>"
              "Para an&#225;lise de Victor e Bruno &#183; base: TCC_Victor_Bruno_V10.docx",
    meta_right="Nota t&#233;cnica<br/>27 de setembro de 2026",
    running_head="Revis&#227;o das cita&#231;&#245;es do TCC: alto risco",
)
# titulo de secao nao fica sozinho no pe da pagina; subscrito em celula
# de tabela pede entrelinha maior que a padrao (13 pt) para nao encavalar
n.s_h.keepWithNext = 1
n.s_cell.leading = 15


def caso(atual, proposta):
    n.table(["", "Texto"],
            [["<b>Atual</b>", f"<i>{atual}</i>"],
             ["<b>Proposta</b>", proposta]],
            [2.3, 12.4])
    # atual e proposta lado a lado na mesma pagina, para comparar
    n.story.append(KeepTogether([n.story.pop()]))
    n.gap(6)


# ------------------------------------------------------------------ 1
n.h("1. O que foi feito")
n.p("Levantamos todas as cita&#231;&#245;es do corpo do V10: s&#227;o 65, apoiadas em 20 entradas da "
    "lista de refer&#234;ncias. Para cada uma, a pergunta &#233; uma s&#243;: <b>a p&#225;gina da "
    "fonte diz o que a frase afirma?</b> Esta nota traz os cinco trechos de maior risco, que "
    "foram conferidos contra os PDFs da pasta Bibliografia. Nos cinco, a fonte citada n&#227;o "
    "sustenta a frase como est&#225; escrita.")
n.p("A regra das propostas &#233; mexer o m&#237;nimo. Quando j&#225; existe na lista uma fonte que "
    "diz exatamente o que a frase diz, trocamos s&#243; a cita&#231;&#227;o. Quando nenhuma fonte "
    "sustenta a frase inteira, ajustamos o texto ao que a fonte diz. Nenhuma proposta traz "
    "refer&#234;ncia nova: todas as fontes usadas j&#225; s&#227;o citadas no trabalho. A &#250;nica "
    "ressalva &#233; o IEA (2026): ele &#233; citado no Cap. 2, mas ainda n&#227;o tem entrada na "
    "lista de refer&#234;ncias, e essa entrada falta de qualquer forma (se&#231;&#227;o 7).")
n.note("Nada foi alterado no Word. O documento s&#243; muda depois da aprova&#231;&#227;o de voc&#234;s.")

# ------------------------------------------------------------------ 2
n.h("2. Contextualiza&#231;&#227;o: intermit&#234;ncia das renov&#225;veis (MOHAN, 2003)")
n.p("<b>O que a fonte diz.</b> O Mohan trata do assunto s&#243; no &#167;17-4 (p. 475-477), e ali "
    "descreve a interface de eletr&#244;nica de pot&#234;ncia necess&#225;ria para ligar PV, e&#243;lica e "
    "armazenamento &#224; rede. N&#227;o fala de flutua&#231;&#227;o da gera&#231;&#227;o, de falta de "
    "armazenamento nem de confiabilidade. O IEA (2026, p. 12), j&#225; citado no Cap. 2, liga o "
    "aumento das renov&#225;veis vari&#225;veis &#224; necessidade de flexibilidade e de capacidade "
    "despach&#225;vel.")
caso("A incorpora&#231;&#227;o dessas fontes enfrenta obst&#225;culos cr&#237;ticos, como a flutua&#231;&#227;o "
     "da gera&#231;&#227;o e a aus&#234;ncia de sistemas de armazenamento em grande escala, que "
     "comprometem a confiabilidade e a estabilidade din&#226;mica do sistema el&#233;trico "
     "(MOHAN, 2003).",
     "A incorpora&#231;&#227;o dessas fontes enfrenta obst&#225;culos cr&#237;ticos, como a variabilidade "
     "da gera&#231;&#227;o, que aumenta a necessidade de flexibilidade e de capacidade despach&#225;vel "
     "no sistema el&#233;trico (IEA, 2026).")
n.p("<b>E o Mohan?</b> O Mohan n&#227;o sai do trabalho por causa disso. Ele &#233; uma boa fonte, "
    "s&#243; que para outra afirma&#231;&#227;o. Hoje este &#233; o &#250;nico lugar onde ele &#233; citado, "
    "ent&#227;o, se a troca for feita sem mais nada, ele fica na lista sem cita&#231;&#227;o no texto. "
    "Duas formas de mant&#234;-lo, cada uma em trecho que ele de fato sustenta:")
n.table(["Op&#231;&#227;o", "Onde e como"],
        [["<b>A</b>",
          "Na mesma frase, acrescentar o que o &#167;17-4 (p. 475) diz: \"&#8230;e a conex&#227;o dessas "
          "fontes &#224; rede, que exige uma interface de eletr&#244;nica de pot&#234;ncia (MOHAN, 2003)\"."],
         ["<b>B</b>",
          "No &#167;3.3.1 (PWM), que hoje cita s&#243; o Teodorescu: o Cap. 8 do Mohan (a partir da "
          "p. 200) trata justamente do inversor chaveado que sintetiza tens&#227;o alternada a partir "
          "de uma fonte CC. A cita&#231;&#227;o vira (MOHAN, 2003; TEODORESCU; LISERRE; RODRIGUEZ, "
          "2011)."]],
        [2.3, 12.4])
n.gap(6)

# ------------------------------------------------------------------ 3
n.h("3. Contextualiza&#231;&#227;o: controle versus in&#233;rcia f&#237;sica (XIONG et al., 2025)")
n.p("<b>O que a fonte diz.</b> O Xiong (p. 1) op&#245;e o gerador s&#237;ncrono, cuja oscila&#231;&#227;o "
    "&#233; regida pelo &#226;ngulo f&#237;sico entre as fontes, ao inversor GFL, cuja oscila&#231;&#227;o "
    "depende da din&#226;mica de controle. N&#227;o fala de in&#233;rcia. O Wu e Wang (2020, p. 1) diz "
    "quase literalmente a primeira parte da frase: diferente do gerador s&#237;ncrono, o conversor "
    "n&#227;o tem uma lei f&#237;sica que governe seu sincronismo, e seu comportamento din&#226;mico "
    "depende dos algoritmos de controle.")
caso("&#8230;dependem de algoritmos digitais de controle, ao contr&#225;rio das m&#225;quinas "
     "s&#237;ncronas que conferem estabilidade pela in&#233;rcia f&#237;sica das m&#225;quinas "
     "rotativas (XIONG et al., 2025).",
     "&#8230;dependem de algoritmos digitais de controle, ao contr&#225;rio das m&#225;quinas "
     "s&#237;ncronas, cuja din&#226;mica de sincronismo &#233; regida por leis f&#237;sicas "
     "(WU; WANG, 2020; XIONG et al., 2025).")

# ------------------------------------------------------------------ 4
n.h("4. Motiva&#231;&#227;o: in&#233;rcia dos IBRs (WU; WANG, 2020)")
n.p("<b>O que a fonte diz.</b> A palavra <i>inertia</i> n&#227;o aparece nenhuma vez no Wu e Wang, "
    "que trata da estabilidade transit&#243;ria do PLL. O Strauss-Mincu et al. (2026, p. 95 e 97), "
    "j&#225; citado no trabalho, diz o que a frase diz: a in&#233;rcia vem tradicionalmente das "
    "m&#225;quinas s&#237;ncronas e diminui &#224; medida que os inversores entram. O texto fica igual; "
    "troca s&#243; a cita&#231;&#227;o.")
caso("&#8230;visto que tais fontes carecem de in&#233;rcia rotacional intr&#237;nseca, resultando em "
     "uma menor resposta inercial global do sistema (WU; WANG, 2020).",
     "&#8230;visto que tais fontes carecem de in&#233;rcia rotacional intr&#237;nseca, resultando em "
     "uma menor resposta inercial global do sistema (STRAUSS-MINCU et al., 2026).")

# ------------------------------------------------------------------ 5
n.h("5. Motiva&#231;&#227;o: sequ&#234;ncia negativa no SRF-PLL (WU; WANG, 2020)")
n.p("<b>O que a fonte diz.</b> O Wu e Wang s&#243; menciona a falta assim&#233;trica para dizer que, "
    "nela, se usa um pr&#233;-filtro na entrada do PLL; a an&#225;lise do artigo &#233; toda de falta "
    "sim&#233;trica. A oscila&#231;&#227;o em frequ&#234;ncia dupla causada pela sequ&#234;ncia negativa "
    "est&#225; no Teodorescu, Liserre e Rodriguez (2011, &#167;8.3, p. 182-186), que mostra o "
    "&#226;ngulo e a amplitude detectados oscilando em 2&#969;. J&#225; a perda de sincronismo sob "
    "afundamento severo &#233; o assunto central do Wu e Wang. A proposta separa as duas "
    "afirma&#231;&#245;es, cada uma com a sua fonte.")
caso("Nessas condi&#231;&#245;es, a componente de sequ&#234;ncia negativa gera um sinal oscilat&#243;rio de "
     "frequ&#234;ncia dupla em v<sub>q</sub> que pode impedir a converg&#234;ncia do controlador do "
     "PLL, levando &#224; perda de sincronismo (WU; WANG, 2020).",
     "Nessas condi&#231;&#245;es, a componente de sequ&#234;ncia negativa gera um sinal oscilat&#243;rio de "
     "frequ&#234;ncia dupla em v<sub>q</sub>, que se propaga para a fase e a amplitude estimadas "
     "pelo PLL (TEODORESCU; LISERRE; RODRIGUEZ, 2011). Em afundamentos severos, o la&#231;o pode "
     "ainda perder o sincronismo (WU; WANG, 2020).")

# ------------------------------------------------------------------ 6
n.h("6. Cap. 3, &#167;3.2: in&#233;rcia e desvio angular (WU; WANG, 2020; XIONG et al., 2025)")
n.p("<b>O que a fonte diz.</b> Nenhum dos dois artigos diz que os geradores s&#237;ncronos "
    "remanescentes sofrem desvios angulares mais r&#225;pidos. A afirma&#231;&#227;o tamb&#233;m &#233; "
    "imprecisa fisicamente: a in&#233;rcia de cada m&#225;quina n&#227;o muda quando entram inversores; "
    "o que cai &#233; a in&#233;rcia total da rede. O Strauss-Mincu et al. (2026) diz duas coisas que "
    "servem aqui: com menos in&#233;rcia, a taxa de varia&#231;&#227;o da frequ&#234;ncia (RoCoF) aumenta "
    "(p. 106), e os requisitos de estabilidade transit&#243;ria precisam ser reavaliados com a "
    "predomin&#226;ncia dos inversores (p. 101).")
caso("Com o aumento da gera&#231;&#227;o baseada em inversores, a in&#233;rcia total da rede diminui, o "
     "que prejudica diretamente a estabilidade transit&#243;ria do sistema el&#233;trico. Sob "
     "condi&#231;&#245;es de falta, a redu&#231;&#227;o desse amortecimento inercial faz com que os "
     "geradores s&#237;ncronos remanescentes sofram desvios angulares muito mais r&#225;pidos e "
     "acentuados. Esse cen&#225;rio dificulta a absor&#231;&#227;o do impacto de grandes "
     "perturba&#231;&#245;es, colocando em risco a manuten&#231;&#227;o do sincronismo das usinas "
     "(WU; WANG, 2020; XIONG et al., 2025).",
     "Com o aumento da gera&#231;&#227;o baseada em inversores, a in&#233;rcia total da rede diminui, o "
     "que eleva a taxa de varia&#231;&#227;o da frequ&#234;ncia durante perturba&#231;&#245;es. Com a "
     "predomin&#226;ncia da gera&#231;&#227;o conectada por inversores, os requisitos de estabilidade "
     "transit&#243;ria, isto &#233;, da capacidade de manter o sincronismo diante de faltas severas, "
     "precisam ser reavaliados (STRAUSS-MINCU et al., 2026).")

# ------------------------------------------------------------------ 7
n.h("7. Para decidir")
n.table(["#", "Decis&#227;o"],
        [["1", "Aprovar, ajustar ou recusar cada um dos cinco textos propostos (se&#231;&#245;es 2 a 6)."],
         ["2", "Mohan: op&#231;&#227;o A, op&#231;&#227;o B, as duas, ou tir&#225;-lo da lista (se&#231;&#227;o 2)."],
         ["3", "Seis fontes citadas n&#227;o t&#234;m PDF na pasta e n&#227;o puderam ser conferidas: "
               "BOLLEN (2000), KUNDUR (1994), OGATA (2009), RODRIGUEZ et al. (2007), SHADOUL et "
               "al. (2022) e ESCOBAR et al. (2021). Voc&#234;s conseguem os PDFs?"],
         ["4", "ANDERSON; FOUAD (2003) e IEEE 1547-2018 est&#227;o na lista, mas n&#227;o s&#227;o citados "
               "no texto: citar em algum ponto ou tirar da lista?"]],
        [1.0, 13.7])
n.gap(6)
n.note("Ainda a conferir, em rodadas seguintes: as cita&#231;&#245;es de m&#233;dio risco (Yazdani e "
       "Iravani, Teodorescu et al., Alves) e as de baixo risco (Cap. 2). Tamb&#233;m faltam na "
       "lista quatro entradas citadas no texto: IEA (2026), KUNDUR et al. (2004), GU; GREEN "
       "(2023) e COORDINADOR EL&#201;CTRICO NACIONAL (2025).")

n.refs([
    "INTERNATIONAL ENERGY AGENCY (IEA). <i>Global Energy Review 2026</i>. Paris: IEA, 2026.",
    "MOHAN, N. <i>Power Electronics: Converters, Applications, and Design</i>. 3. ed. Hoboken: "
    "John Wiley &amp; Sons, 2003.",
    "STRAUSS-MINCU, D. et al. Inverter-Dominated Future Power Systems: A Roadmap for System "
    "Stability. <i>IEEE Power and Energy Magazine</i>, v. 24, p. 93-107, 2026. "
    "DOI 10.1109/MPE.2025.3617895.",
    "TEODORESCU, R.; LISERRE, M.; RODRIGUEZ, P. <i>Grid Converters for Photovoltaic and Wind "
    "Power Systems</i>. Chichester: John Wiley &amp; Sons, 2011.",
    "WU, H.; WANG, X. Design-Oriented Transient Stability Analysis of PLL-Synchronized "
    "Voltage-Source Converters. <i>IEEE Transactions on Power Electronics</i>, v. 35, n. 4, "
    "p. 3573-3589, abr. 2020. DOI 10.1109/TPEL.2019.2937942.",
    "XIONG, Y. et al. Comparison of Power Swing Characteristics and Efficacy Analysis of "
    "Impedance-based Detections in Synchronous Generators and Grid-following Systems. <i>IEEE "
    "Transactions on Power Systems</i>, v. 40, n. 3, p. 2545-2556, maio 2025. "
    "DOI 10.1109/TPWRS.2024.3469235.",
])

out = n.build()
if "--preview" in sys.argv:
    render_preview(out, sys.argv[sys.argv.index("--preview") + 1])
