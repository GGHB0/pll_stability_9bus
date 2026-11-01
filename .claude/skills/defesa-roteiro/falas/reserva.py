"""Fala de reserva completa dos slides 21 a 28 (só o guia de estudos usa)."""

RESERVA_SPEECHES = {
    21: "[Bruno] Slide de apêndice para a arguição: reúne os parâmetros da rede, do equivalente de Thévenin, do filtro LCL e das malhas de controle.",
    22: "[Victor] Slide de apêndice para a arguição: reúne as Tabelas 5.1, 5.2 e 5.3 completas do Capítulo 5.",
    23: (
        "[Victor] (Reserva do Capítulo 2 do painel) Na energização, com a sintonia nominal, vd "
        "acomoda em 34 ms e o erro de fase entra na faixa de 2 graus em 40 ms. Com a sintonia "
        "inadequada, são 42 ms e 79 ms, quase o dobro do tempo.\n\n"
        "[Bruno] Em regime permanente, porém, as duas chegam ao mesmo ponto de operação antes da "
        "falta em 0,3 s: a sintonia inadequada é lenta, não quebrada, e a diferença aparece nas contingências."
    ),
    24: (
        "[Bruno] (Reserva do Capítulo 3 do painel) Nas faltas trifásicas com sintonia nominal, "
        "quanto mais perto da usina, mais severo o afundamento: a retenção de vd vai de 58,4% na "
        "Barra 6 a 9,2% na Barra 7, e o pico do erro sobe de 7,3 para 37,3 graus.\n\n"
        "[Victor] Como a falta é equilibrada, sem sequência negativa, a componente de 120 Hz fica "
        "abaixo de 0,0011 pu, o erro é apenas transitório e o PLL nominal retorna à faixa de 2 graus "
        "em todos os pontos, entre 76 e 112 ms."
    ),
    25: (
        "[Victor] (Reserva do Capítulo 4 do painel) Nas faltas assimétricas, a sequência negativa "
        "aparece em dq como uma oscilação de 120 Hz entre 0,29 e 0,72 pu, mais de 250 vezes maior "
        "que nas trifásicas.\n\n"
        "[Bruno] Como 754 rad/s é apenas 2,32 vezes a frequência natural do laço, o PI não filtra "
        "essa componente. Já no gráfico da direita, na trifásica da Barra 7, a nominal recupera em "
        "98 ms enquanto a inadequada perde o sincronismo por escorregamento de ciclo."
    ),
    26: (
        "[Bruno] (Reserva do Capítulo 5 do painel) Na bifásica da Barra 6, onde a tensão residual "
        "sustenta o laço, a menor banda da sintonia inadequada filtra o 120 Hz: o pico do erro cai "
        "de 96,0 para 34,5 graus e o retorno cai de 48 para 30 ms.\n\n"
        "[Victor] Porém, na Barra 7, onde o afundamento é severo, essa lentidão cobra o preço na "
        "recuperação: o tempo de retorno quase dobra, passando de 46 para 95 ms na monofásica e de "
        "51 para 96 ms na bifásica."
    ),
    27: (
        "[Bruno] (Reserva do Capítulo 6 do painel) No pós-falta da Barra 7 trifásica com sintonia "
        "inadequada, o inversor passa 66,8% do tempo absorvendo potência ativa da rede, com média de "
        "menos 0,40 pu, comportando-se como uma carga oscilante.\n\n"
        "[Victor] A malha de corrente não falhou, mas como o referencial estimado pelo PLL gira "
        "continuamente em escorregamento de ciclo, a corrente comandada no eixo d troca de sinal em "
        "relação à tensão da rede."
    ),
    28: (
        "[Bruno] (Reserva do Capítulo 7 do painel) Pelo Submódulo 2.10 do ONS, nas faltas trifásicas "
        "com sintonia nominal o inversor cumpre a rampa: satura iq em 1,0 pu na Barra 7 e na Linha "
        "7-8 e entrega 0,72 pu frente a 0,76 pu na Barra 6.\n\n"
        "[Victor] Mas na Barra 7, com a tensão em 0,10 pu, a corrente máxima de 1,0 pu entrega "
        "apenas 0,09 pu de potência reativa. E nas assimétricas ou sob perda de sincronismo, o "
        "inversor segue conectado mas entrega potência com 120 Hz ou drena energia: ficar conectado "
        "não basta."
    ),
}
