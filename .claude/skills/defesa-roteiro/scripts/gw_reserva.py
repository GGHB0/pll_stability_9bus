"""Guia de estudos: slides ocultos de reserva e perguntas do defesa_qa."""
from falas import SLIDE_SPEECHES
from gw_builder import PALCO_SPEECHES, WordRoteiroBuilder
from gw_util import *  # noqa: F401,F403


def inject_defesa_qa_and_hidden_slides(wb: WordRoteiroBuilder, slides_jpg_fn):
    """Adiciona no final da Parte V os slides ocultos 23-28 com fala de reserva e as 9 perguntas do defesa_qa.pdf."""
    wb.h("Detalhamento dos Slides Ocultos de Reserva (Slides 23 a 28)")
    wb.p(
        "Caso o navegador falhe no dia da apresentação, estes 6 slides no final do PowerPoint "
        "substituem diretamente os Capítulos 2 a 7 do Modo Apresentação:"
    )
    hidden_meta = [
        (23, "Energização (Reserva do Painel 2)", "§5.1 · Figura 5.3 · 34/40 ms vs. 42/79 ms"),
        (24, "Faltas trifásicas (Reserva do Painel 3)", "§5.2 · Figura 5.7 e Tabela 5.1 · 9,2% a 58,4%"),
        (25, "Sequência negativa e perda de sincronismo (Reserva dos Painéis 4 e 6)", "§5.3 e §5.4 · Figuras 5.10 e 5.18 · > 250× e 98 ms"),
        (26, "Compromisso da sintonia nas assimétricas (Reserva do Painel 5)", "§5.3 · Figura 5.14 e Tabela 5.3 · 96,0° &#8594; 34,5° na B6; retorno dobra na B7"),
        (27, "Dinâmica pós-falta e absorção de potência (Reserva do Painel 6)", "§5.4 · Figuras 5.20 e 5.21 · 66,8% do tempo absorvendo P (média −0,40 pu)"),
        (28, "Conformidade com o Submódulo 2.10 do ONS (Reserva do Painel 7)", "§5.5 · Figura 2.2 e Tabela 5.2 · Q = 0,09 pu na Barra 7"),
    ]
    for s_num, tit, ref in hidden_meta:
        wb.faixa("RESERVA", s_num, tit, ref, imagem=slides_jpg_fn(s_num))
        wb.add_slide_speech_box(s_num)

    wb.h("Respostas Rápidas para Cruzamentos entre Deck e TCC (defesa_qa.pdf)")
    wb.p(
        "Estes 9 pontos cobrem divergências ou detalhes internos do TCC entregue (VFinal, 15/10/2026) "
        "que a banca pode perguntar na arguição:"
    )
    qa_list = [
        ("1. Quantos cenários foram simulados (28 na Tabela 4.1 vs. 29 no Cap. 5)?",
         "Foram simulados <b>29 cenários: 21 com a sintonia nominal e 8 com a sintonia inadequada</b> "
         "(28 com falta e 1 em regime permanente). Na Tabela 4.1 faltam a marca da Linha 7-8 inadequada "
         "e a linha de regime permanente, mas ambas estão descritas e analisadas no Capítulo 5 (§5.1 e §5.4)."),
        ("2. Por que os objetivos da Introdução citam sobrecorrentes e impedância da rede?",
         "O Capítulo 6 registra as duas ressalvas: as sobrecorrentes não se manifestam porque o controle "
         "limita a referência de corrente antes disso; e a impedância da rede foi observada variando a "
         "distância elétrica da falta (da Barra 7 à Barra 6) com nível de curto fixo."),
        ("3. Quais são os valores de Vcc, L1, L2, Cf e Rd que não estão no texto do Cap. 4?",
         "Estão no modelo Simulink e no Slide 21 (Apêndice): V<sub>cc</sub> = 136,36 kV (1,5 &#215; 90,91 kV "
         "do cálculo para evitar sobremodulação do PWM na escala de 100 MW), L<sub>1</sub> = 30,42 mH, "
         "L<sub>2</sub> = 0,289 mH (L<sub>est</sub> = 30,71 mH), C<sub>f</sub> = 42,47 &#956;F e resistores "
         "de amortecimento passivo R<sub>d</sub> em série."),
        ("4. A malha de corrente (339,4 rad/s) e o PLL nominal (325,3 rad/s) têm quase a mesma banda?",
         "Sim: cada malha seguiu a sua referência clássica (Alves, 2022 para acomodar a corrente em 1 ciclo; "
         "Alves, Dias e Rolim, 2020 e Teodorescu et al., 2011 para acomodar o PLL em 20 ms). Os ganhos de "
         "corrente ficaram fixos em todas as simulações para isolar o efeito do PLL; a interação entre bandas "
         "próximas fica fora do escopo."),
        ("5. O cartão nas abas por cenário mostra 8,3% na Barra 7, mas o TCC e o palco dizem 9,2%.",
         "São métricas diferentes: <b>9,2%</b> é a retenção de v<sub>d</sub> em percentual do valor pré-falta "
         "(Tabela 5.1 e cartões do Modo Apresentação). Já 8,3% no cartão superior da aba por cenário é o "
         "módulo da tensão |V| na Barra 2."),
        ("6. O blecaute de 15/08/2023 desligou 22.547 MW (Introdução) ou 23.368 MW (§2.4.3 e Slide 3)?",
         "O valor consolidado oficial é <b>23.368 MW (34,5% da demanda do momento)</b>, do Relatório de "
         "Análise de Perturbação do ONS (RAP-ONS 00012/2023) detalhado na §2.4.3."),
        ("7. Onde ocorre o escorregamento de ciclo (cycle slipping)?",
         "Ocorre com a <b>sintonia inadequada nas faltas trifásicas severas: Barra 7 e Linha 7-8</b> (§5.4, "
         "Fig. 5.18), onde o erro gira continuamente após a eliminação e não retorna até 0,6 s. Nas faltas "
         "assimétricas (§5.3), a fragilidade é a oscilação estacionária de 120 Hz."),
        ("8. Por que a potência reativa na Barra 7 é de apenas 0,09 pu com corrente reativa saturada em 1,0 pu?",
         "Porque Q &#8776; V&#183;i<sub>q</sub>: como a tensão média durante a falta na Barra 7 cai para "
         "0,10 pu (menos de 10%), mesmo injetando 1,0 pu de corrente reativa a potência entregue fica em 0,09 pu."),
        ("9. E o modo formador de rede (grid-forming / GFM)?",
         "Está fora do escopo de simulação. O Capítulo 7 propõe dar continuidade mantendo inversores seguidores "
         "de rede: evoluir a estrutura de sincronismo (DDSRF-PLL e DSOGI-PLL) e varrer as condições de rede (SCR)."),
    ]
    for q_t, q_a in qa_list:
        wb.box("prova", q_a, titulo=q_t)
