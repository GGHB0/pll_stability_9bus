# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
bul("Antes da defesa: abrir output/pll_metrics.html no navegador do notebook da defesa "
    "(abre sem internet).",
    "No slide 18: Alt+Tab para o navegador e clicar <b>Modo apresentação</b> no cabeçalho. "
    "O painel entra em tela cheia, com fundo branco.",
    "Seta &#8594; ou PageDown avança; seta &#8592; ou PageUp volta; Esc sai. Nos capítulos "
    "com passos, cada avanço revela um passo; só no último a seta troca de capítulo.",
    "O indicador de segmentos no canto superior direito mostra &#8220;k de n&#8221;.")
sub("O que aparece em todo capítulo")
n.p("Número do capítulo (k/8), a referência no TCC (seção, figura, tabela), o título, a "
    "frase do passo, chips com os casos (clicar liga e desliga), o gráfico e, embaixo, "
    "cartões com os números de cada caso. Clicar num cartão sai do palco e abre o cenário "
    "nas abas.")
box("cuidado", "O slide 18 funciona como porta direta para os oito capítulos do Modo Apresentação (Capítulos 1 a 8) antes resumem os três blocos do Modo Apresentação "
    "(Capítulos 1 a 3, Capítulos 4 e 5, e Capítulos 6 a 8), servindo de roteiro visual antes "
    "de alternar para o navegador.")

# =============================================================================
# PARTE III
# =============================================================================
n.pagebreak()
n.h("PARTE III · Painel HTML, modo apresentação")
n.p("Oito capítulos, na ordem do Cap. 5 do TCC. A sequência conta uma história: onde caem "
    "as faltas, como o PLL parte, o que a distância faz, o que a sequência negativa faz, "
    "como o ganho menor parece ajudar, como ele perde o sincronismo e o que isso diz sobre "
    "o código de rede.")
tab(["Cor", "Significado"], [
    ["azul / laranja", "sintonia nominal / inadequada"],
    ["amarelo &#8594; verde &#8594; ciano &#8594; índigo", "capítulos só com a nominal: do "
     "ponto mais perto ao mais longe da usina"],
    ["cor = barra, traço = curto", "capítulo 4: laranja B7, verde-azulado B6; contínuo "
     "bifásica, tracejado monofásica, grafite trifásica"],
    ["faixa verde", "&#177;2° no erro de fase; &#177;5% em v<sub>d</sub>"],
    ["fundo rosado", "intervalo da falta (0,3 a 0,4 s)"],
], [5.6, 9.1])

# --- 1
cap(1, "Faltas destacadas", "Antes dos resultados · 6 passos", "01_faltas_m2.png",
    "Passo 2 de 6: Barra 7 em destaque, cartão à direita e régua de severidade embaixo")
box("msg", "Quatro pontos de falta, do mais próximo ao mais distante da usina; a pergunta é "
    "como a distância muda a resposta do SRF-PLL.")
tab(["Passo", "Em cena", "O que explicar"], [
    ["1", "Visão geral", "Outros pontos também receberam falta; a análise fica em quatro, "
     "do afundamento mais profundo ao mais raso, com uma linha simples e uma dupla."],
    ["2", "Barra 7", "Logo depois do T2: entre o inversor e a falta só há o transformador. "
     "Caso mais severo; ponto de partida da perda de sincronismo. 3&#966;, 2&#966;, 1&#966;; "
     "duas sintonias."],
    ["3", "Linha 7-8", "Sai da Barra 7; circuito simples, a linha inteira fica sob falta; "
     "ainda perto. Só trifásica; duas sintonias."],
    ["4", "Linha 8-9", "Dois circuitos em paralelo, falta em um; o outro continua conduzindo. "
     "Só trifásica, só nominal."],
    ["5", "Barra 6", "Ramo inferior, entre B4 e B9; três linhas em qualquer caminho até "
     "ela. Caso mais brando, contraponto da B7. 3&#966;, 2&#966;, 1&#966;; duas sintonias."],
    ["6", "Resumo", "Ordem B7, L7-8, L8-9, B6; os quatro com trifásica; B7 e B6 também com "
     "mono e bifásica (capítulo 4)."],
], [1.3, 2.4, 11.0])
sub("Fundamento: distância elétrica")
n.p("Durante uma falta franca, a tensão no ponto do defeito vai a quase zero. A tensão que "
    "sobra no inversor depende de quanta impedância existe entre ele e a falta: é um "
    "divisor de tensão. Com só o T2 no meio (Barra 7), sobra pouco; com três linhas no "
    "caminho (Barra 6), sobra bem mais. &#8220;Distância&#8221; aqui é impedância, não "
    "quilômetro.")
box("cuidado", "A régua é proporcional à tensão residual na Barra 2, mas nenhum número "
    "aparece de propósito (não está no TCC). A Barra 6 é a mais distante, não a 8. "
    "<b>Reserva</b> sem painel: slide 16 (matriz).")

# --- 2
cap(2, "Energização do inversor", "§5.1 · Figura 5.3 · 2 passos", "02_energ_p2.png",
    "Passo 2 de 2: as duas sintonias, marcas de acomodação e o fasor")
box("msg", "Na partida, o SRF-PLL trava na rede: o erro de fase entra na faixa de 2° em "
    "40 ms com a nominal e em 79 ms com a inadequada, quase o dobro.")
box("passo", "<b>1.</b> Só a nominal, com foco na partida: 40 ms.",
    "<b>2.</b> Entra a inadequada: 79 ms. Embaixo, v<sub>d</sub> entra em &#177;5% do valor "
    "final em 34 e 42 ms.")
sub("Como ler o fasor")
n.p("O círculo à direita mostra o ângulo do PLL contra a rede: a marca preta no topo é a "
    "rede, a cunha verde é a faixa de &#177;2°, e cada vetor é uma sintonia. O play percorre "
    "a janela a partir de t = 0: os vetores giram até parar no topo, que é o travamento.")
sub("O que explicar")
n.p("A inadequada oscila mais e demora mais, como esperado de um laço mais lento e menos "
    "amortecido (&#958; = 0,316, &#969;<sub>n</sub> 2,24 vezes menor). Mas, em regime, as "
    "duas chegam ao mesmo ponto de operação, e a falta só começa em 0,3 s, com as duas "
    "travadas: <b>a inadequada é lenta, não quebrada</b>. A diferença só aparece nas "
    "contingências.")
nums([["40 / 79 ms", "erro na faixa de 2°, nominal / inadequada (Fig. 5.3)"],
      ["34 / 42 ms", "v<sub>d</sub> na faixa de 5%, nominal / inadequada"]])
box("cuidado", "Os primeiros milissegundos saem da escala porque a tensão ainda é nula; por "
    "isso a partida fica fora das métricas. <b>Reserva</b>: slide oculto 24.")

# --- 3
cap(3, "Localização: quanto mais perto, mais severa", "§5.2 · Tabela 5.1 · Figura 5.7 · "
    "3 passos", "03_local_p1.png",
    "Passo 1 de 3: foco na falta, mini-mapa com a retenção de v<sub>d</sub> de cada ponto")
box("msg", "A mesma falta trifásica em quatro pontos: quanto mais perto da usina, menos "
    "tensão sobra e maior o erro, mas com a sintonia nominal o erro sempre volta.")
box("passo", "<b>1.</b> v<sub>d</sub> retém 9,2% na Barra 7 e 58,4% na Barra 6 (mini-mapa).",
    "<b>2.</b> Pico do erro de 37,3° na Barra 7 e 7,3° na Barra 6 (fasor).",
    "<b>3.</b> Com a nominal, o erro sempre volta à faixa de 2°: em até 112 ms (sem foco).")
tab(["Ponto", "Retenção de V<sub>d</sub>", "Pico do erro", "Retorno a 2°"], [
    ["Barra 7", "9,2%", "37,3°", "98 ms"],
    ["Linha 7-8", "11,3%", "32,5°", "98 ms"],
    ["Linha 8-9", "47,1%", "29,8°", "112 ms"],
    ["Barra 6", "58,4%", "7,3°", "76 ms"],
], [4.2, 3.5, 3.5, 3.5])
sub("O que explicar")
n.p("Sem sequência negativa, a trifásica só reduz a amplitude e dá um salto de fase; o "
    "120 Hz fica entre 0,0002 e 0,0011 pu. O erro é transitório: o laço tipo 2 (slide 7) "
    "leva o erro de volta a zero. As setas no topo vão da eliminação (0,4 s) até o instante "
    "em que o erro entra de vez na faixa; B7 e L7-8 dividem a mesma seta (98 ms). O eixo do "
    "erro está em &#177;60°: corta só o salto do 1º ciclo, que a métrica de pico já "
    "descarta.")
box("prova", "<b>Por que a Linha 8-9 demora mais (112 ms) que a Barra 7, que é mais "
    "severa?</b> O retorno mede a recuperação depois da eliminação, que depende do "
    "transitório pós-falta de cada topologia, não só da profundidade do afundamento. "
    "Confira no §5.2 se o TCC atribui causa antes de afirmar qualquer uma.")
box("cuidado", "<b>Reserva</b>: slide oculto 25 (Tabela 5.1, Fig. 5.7).")

# --- 4
cap(4, "Sequência negativa", "§5.3 · Tabela 5.3 · Figura 5.10 · 5 passos",
    "04_seqneg_p2.png", "Passo 5 de 5: espectro de v<sub>d</sub> na falta, destaque "
    "&#8220;&gt; 250&#215;&#8221; e matriz barra &#215; curto")
box("msg", "Nas faltas assimétricas, a sequência negativa aparece em v<sub>d</sub> como "
    "120 Hz, de 0,29 a 0,72 pu: mais de 250 vezes o maior valor das trifásicas (0,0011 pu).")
box("passo", "<b>1.</b> Em v<sub>abc</sub> (Barra 6): na trifásica as três fases caem por igual; na bifásica ficam desequilibradas.",
    "<b>2.</b> Animação das sequências: o PLL gira com a positiva; a negativa gira ao contrário e, vista do PLL, dá a volta a 120 Hz.",
    "<b>3.</b> Em dq (v<sub>d</sub> e v<sub>q</sub> no tempo): a positiva vira constante e a negativa vira oscilação de 120 Hz só na bifásica.",
    "<b>4.</b> Entrada do PI (v<sub>q</sub> e erro de fase): o PI lê o 120 Hz como erro de fase (pico salta de 7,3° na trifásica para 96,0° na bifásica).",
    "<b>5.</b> No espectro de v<sub>d</sub>, o 120 Hz das assimétricas vai de 0,29 a 0,72 pu: mais de 250 vezes o das trifásicas.")
sub("Fundamento: de onde vem o pico em 120 Hz")
n.p("É a equação do slide 4 aparecendo no gráfico: a sequência negativa vira "
    "V<sup>&#8722;</sup>cos(2&#969;t) em v<sub>d</sub> e o mesmo em v<sub>q</sub>. O PLL não "
    "distingue essa ondulação de um erro de fase real: ela entra em v<sub>q</sub>, passa "
    "pelo PI (a 2,32&#183;&#969;<sub>n</sub>, quase dois terços passam) e contamina o ângulo, "
    "o referencial inteiro e as potências.")
tab(["120 Hz em v<sub>d</sub> (pico do erro)", "Trifásica", "Bifásica", "Monofásica"], [
    ["Barra 7", "0,0002 pu (37,3°)", "0,72 pu (180,0°)", "0,59 pu (89,7°)"],
    ["Barra 6", "0,0011 pu (7,3°)", "0,39 pu (96,0°)", "0,29 pu (12,0°)"],
], [5.0, 3.2, 3.3, 3.2])
n.p("Na bifásica da B7, o erro passa de 90° em 17,8% do intervalo com a nominal e em 14,0% "
    "com a inadequada: nenhuma preserva o alinhamento.")
box("prova", "<b>Por que não pôr um notch em 120 Hz?</b> Reduz a ondulação, mas um filtro "
    "dentro do laço também atrasa e reduz a banda, que é o recurso de que a recuperação "
    "precisa. A saída estrutural é separar as sequências antes do laço (DDSRF, DSOGI: "
    "trabalho futuro, slide 20).")
box("alem", "<b>Bifásica pior que monofásica:</b> é a ligação das redes de sequência do slide "
    "16 (paralelo na bifásica, série na monofásica). <b>Pico em 60 Hz em algumas curvas:</b> "
    "componente contínua transitória nas fases, vista em dq a 60 Hz (slide 6).")
box("cuidado", "<b>Reserva</b>: slide oculto 25 (Fig. 5.10).")

# --- 5
cap(5, "Compromisso da sintonia", "§5.3 · Tabela 5.3 · Figura 5.14 · 3 passos",
    "05_comp_p2.png", "Passo 2 de 3: Barra 6 bifásica, nominal e inadequada")
box("msg", "Na bifásica da Barra 6, o ganho menor filtra melhor o 120 Hz: o pico do erro cai "
    "de 96,0° para 34,5° e o retorno de 48 para 30 ms.")
box("passo", "<b>1.</b> Com a nominal, o 120 Hz da falta passa para o erro de fase: pico de "
    "96,0°.",
    "<b>2.</b> Com a inadequada, o 120 Hz em v<sub>d</sub> é quase o mesmo (0,39 e 0,37 pu), "
    "mas o erro fica em 34,5° e volta em 30 ms.",
    "<b>3.</b> Aqui, o ganho menor parece vantagem. E numa falta mais severa? (sem foco)")
sub("O que explicar")
n.p("A perturbação na tensão é a mesma nas duas; o que muda é quanto dela chega ao ângulo. "
    "Pela tabela do slide 10, a nominal deixa passar 0,63 do 120 Hz e a inadequada 0,13. Na "
    "Barra 6 a tensão positiva que sobra (v<sub>d</sub> médio de 0,72 pu) sustenta o "
    "sincronismo, e a filtragem vence.")
n.p("Mas o mesmo ganho menor deixa a recuperação lenta onde a tensão cai mais: na Barra 7 o "
    "retorno quase dobra (46 &#8594; 95 ms na monofásica, 51 &#8594; 96 ms na bifásica) e na "
    "trifásica da Barra 6 vai de 76 para 106 ms. <b>A frase-ponte do passo 3 é a virada da "
    "defesa</b>: o capítulo seguinte responde.")
box("cuidado", "<b>Reserva</b>: slide oculto 26 (Fig. 5.14, Tab. 5.3) e apêndice 22.")

# --- 6
cap(6, "Perda de sincronismo", "§5.4 · Figuras 5.18 e 5.19 · 3 passos", "06_sinc_p3.png",
    "Passo 3 de 3: erro de fase e P na Barra 7 trifásica; o &#8220;66,8%&#8221; fica sob "
    "o fasor")
box("msg", "Na Barra 7 trifásica, a sintonia decide o sincronismo: com a nominal o erro volta "
    "em 98 ms; com a inadequada percorre toda a faixa de &#177;180° até o fim, e a usina "
    "absorve potência ativa em 66,8% do tempo após a eliminação.")
box("passo", "<b>1.</b> O caso mais severo: com a nominal, o erro volta à faixa de 2° em 98 ms.",
    "<b>2.</b> A tensão retém quase o mesmo (9,2% e 8,2%), mas com a inadequada o erro "
    "percorre toda a faixa de &#177;180° (escorregamento de ciclo): perde o sincronismo.",
    "<b>3.</b> O ganho que filtrava o 120 Hz na Barra 6 é o que perde o sincronismo aqui.")
sub("Fundamento: escorregamento de ciclo")
n.p("O ângulo estimado deixa de acompanhar a rede e passa a girar em relação a ela: o erro "
    "varre &#177;180° sem parar, e cada &#8220;dente de serra&#8221; do gráfico é uma volta "
    "perdida. No fasor, o vetor laranja dá voltas enquanto o azul fica no topo.")
sub("Fundamento: por que P fica negativa")
