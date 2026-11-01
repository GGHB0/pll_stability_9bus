"""Tópicos "O que falar" da modelagem (slides 5 a 15), do roteiro de estudo."""

FALAS = {
5: [("Victor", "Iniciando a parte de modelagem no slide 5, nós nos deparamos com o modelo do nosso sistema. Começando pela fonte primária, que vai ser uma fonte renovável: nós escolhemos utilizar um barramento CC ideal, ignorando a dinâmica do elo CC e o rastreamento de máxima potência, os MPPTs."),
    ("Victor", "Seguindo para a direita, temos o inversor, que faz a conversão trifásica e é quem vai receber os comandos do controle. Logo após, temos o filtro de acoplamento LCL, conectando a usina ao ponto de acoplamento comum na rede elétrica, o sistema IEEE de 9 barras. O sinal medido ali vai para o controle digital do SRF-PLL para fazer a realimentação e o rastreamento do ângulo da rede.")],
6: [("Victor", "Para poder fazer o rastreamento dessa rede, é utilizada a transformada de Park. O conceito básico dela é transformar as tensões trifásicas em duas grandezas lineares e constantes, dividindo em v<sub>d</sub> e v<sub>q</sub>."),
    ("Victor", "Como vocês podem ver, aqui segue a matriz de transformação e, logo abaixo, observamos as equações resultantes dessa multiplicação. O objetivo do PLL é fazer com que o seu ângulo esteja exatamente em referência ao ângulo da rede. Assim, para v<sub>d</sub> teremos o cosseno de zero, e para v<sub>q</sub> o seno de zero."),
    ("Victor", "E por que a gente utiliza essa transformada de Park? Porque quando aplicamos sinais senoidais num controlador PI, o erro se propaga e a gente nunca consegue trazer esse erro a zero. Porém, quando convertemos para sinais constantes, a ação integral consegue zerar esse sinal facilmente. Então, esse é o grande porquê de utilizar a transformada de Park na nossa detecção de fase.")],
7: [("Victor", "Passando para o slide 7, a gente consegue verificar a modelagem da nossa malha de controle fechada. Como já explicamos, a transformada de Park vai ser o nosso detector de fase. O objetivo dela é enviar a componente v<sub>q</sub> para o controlador PI, e nós queremos utilizar o PI para fazer esse v<sub>q</sub> convergir para zero, zerando o erro. Consequentemente, o v<sub>d</sub> vai convergir para a amplitude total da tensão."),
    ("Victor", "Tendo em vista que referenciamos um set point com a frequência natural da rede, no VCO nós integramos esse sinal de velocidade angular e obtemos o ângulo do PLL. Esse ângulo faz a realimentação de volta para a transformada de Park, fechando o laço. Como a gente pode ver do lado direito, utilizamos as fórmulas da equação característica de segunda ordem para poder dimensionar os ganhos K<sub>p</sub> e K<sub>i</sub> do nosso PLL.")],
8: [("Victor", "O sistema de teste é o IEEE de 9 barras modificado. A máquina síncrona da Barra 2 (192 MVA) foi substituída pela usina fotovoltaica de 100 MW (1 pu na base de 100 MVA). G1 e G3 permanecem como fontes síncronas mantendo a inércia remanescente da rede."),
    ("Bruno", "Modelamos em duas etapas complementares: no PSIM montamos o PLL e o inversor chave a chave sob o equivalente de Thévenin da Barra 2 para validar os ganhos; no Simulink roda a rede completa com 9 barras, máquinas síncronas e nível de curto fixo para simular todas as contingências.")],
9: [("Victor", "Etapa 1: a tensão entra em pu, dividida pelo pico nominal de fase, 16.329,93 V. "
      "Assim o ganho do detector vale 1 e v<sub>q</sub> é o próprio erro de ângulo."),
     ("Bruno", "Etapas 2 a 4: linearizado, o laço tem a forma canônica, K<sub>i</sub> = "
      "&#969;<sub>n</sub>&#178; e K<sub>p</sub> = 2&#958;&#969;<sub>n</sub>. Fixa-se &#958; = 0,707, "
      "o clássico de Ogata, com cerca de 5% de sobre-elevação. Sobra um só grau de liberdade: "
      "t<sub>s</sub>."),
     ("Victor", "Use a régua: t<sub>s</sub> = 4,6/(&#958;&#969;<sub>n</sub>) pelo critério de 1%. "
      "Curto demais deixa passar ruído e desequilíbrio; longo demais não acompanha a rede. 20 ms, "
      "pouco mais de um ciclo, como em Alves, Dias e Rolim (2020) e Teodorescu, Liserre e "
      "Rodriguez (2011). Leia a caixa final: K<sub>p</sub> = 460, &#969;<sub>n</sub> = 325,3 rad/s "
      "(51,8 Hz), K<sub>i</sub> = 105.820.")],
10: [("Bruno", "Aponte a coluna laranja: a sintonia inadequada multiplica os dois ganhos por 0,2, "
      "92 e 21.164. A &#969;<sub>n</sub> cai para 145,5 rad/s e o &#958; para 0,316: laço mais lento "
      "e menos amortecido. No caso-limite, o PLL não recupera o sincronismo depois da falta."),
     ("Victor", "Cartão da direita: o t<sub>s</sub> vai de 20 para 100 ms pela mesma fórmula, "
      "4,6/(&#958;&#969;<sub>n</sub>). Laço 5 vezes mais lento, tanto quanto a própria falta "
      "(0,1 s). &#8220;São essas duas sintonias que comparamos nos resultados.&#8221;")],
11: [("Victor", "Agora o inversor. Na primeira versão, no PSIM, pede-se 1 pu de ativo (os 100 MW) "
      "num degrau aos 35 ms e reativo zero. Cada um é dividido pelo v<sub>d</sub> que vem do PLL, e "
      "saem as referências de corrente."),
     ("Bruno", "Cartão de baixo, à esquerda: é a equação de potência em dq invertida. Só vale com "
      "v<sub>q</sub> = 0, eixo d alinhado, e quem garante isso é o PLL.")],
12: [("Bruno", "&#8220;Antes da malha de corrente, o filtro que liga o inversor à rede.&#8221; "
      "Percorra a figura da esquerda para a direita: barramento CC constante, inversor a 5 kHz, "
      "o LCL e o PCC. Passos 1 e 2: L<sub>1</sub> sai do limite de ondulação da corrente "
      "(depende de V<sub>cc</sub> e f<sub>sw</sub>); L<sub>2</sub> é proporcional a L<sub>1</sub>; "
      "somados, L<sub>est</sub> = 30,71 mH, que volta no PI de corrente."),
     ("Victor", "Passo 3: o capacitor fecha a ressonância em 9.068,99 rad/s; aponte a régua, entre "
      "a rede e o chaveamento. Passo 4: resistências em série com os indutores e o capacitor "
      "atenuam o pico. Feche com a caixa da direita: barramento CC em valor constante, para "
      "manter a margem de modulação.")],
13: [("Bruno", "Figura 3.1, eixo por eixo: erro &#8594; PI &#8594; notch na ressonância do LCL "
      "&#8594; índice de modulação &#8594; PWM a 5 kHz no inversor de dois níveis."),
     ("Victor", "O filtro é o do slide anterior; o notch corta a ressonância dele. O PI segue a mesma forma canônica do PLL: &#958; = 0,707 e "
      "&#969;<sub>n</sub> = 4&#8730;2&#183;f<sub>g</sub>, a corrente acomoda em um ciclo; "
      "K<sub>p</sub> = 8f<sub>g</sub>L<sub>est</sub> e K<sub>i</sub> = "
      "32f<sub>g</sub>&#178;L<sub>est</sub>, com L<sub>est</sub> = 30,71 mH. Feche com o rodapé: "
      "são dois PIs, um sincroniza, o outro faz a corrente seguir a referência.")],
14: [("Bruno", "No modelo final do nosso inversor, nós substituímos aquelas referências fixas por "
      "essa lógica de suporte de subtensão do Submódulo 2.10 do ONS. Como vocês podem ver no "
      "gráfico à esquerda, é a tensão que define o reativo. Quando a tensão medida permanece numa "
      "faixa normal, entre 0,85 e 1,1 por unidade, a corrente reativa de referência é zero e o "
      "inversor injeta potência ativa nominal."),
     ("Bruno", "Quando essa tensão afunda abaixo de 0,85 durante uma falta, o código de rede exige a "
      "injeção de corrente reativa proporcional a esse afundamento, seguindo essa rampa da equação. "
      "Isso vai até o limite de saturação: quando a tensão chega a 0,5 p.u. ou menos, o inversor "
      "injeta 100% da corrente máxima, ou seja, 1 p.u. de corrente reativa."),
     ("Bruno", "No gráfico à direita, vemos a nossa regra de prioridade sobre o limite de corrente. "
      "A corrente máxima forma esse raio, e a corrente reativa tem prioridade total para sustentar a "
      "tensão. A corrente ativa fica apenas com o que sobra dentro desse círculo.")],
15: [("Bruno", "Juntando então todas essas partes, chegamos ao nosso modelo completo, que foi "
      "utilizado em todas as simulações, como mostra a Figura 4.2 do TCC."),
     ("Bruno", "Na parte superior, temos a etapa de potência, com o inversor, o filtro LCL e o "
      "ponto de acoplamento da Barra 2. Na parte inferior, o controle digital, onde tudo se conecta: "
      "o SRF-PLL entrega o ângulo, o Submódulo 2.10 define as referências de corrente a partir da "
      "tensão, e as malhas de controle geram a modulação."),
     ("Bruno", "Com o modelo fechado, passamos agora para o nosso método de teste, para ver como as "
      "contingências vão testar esse nosso SRF-PLL.")],
}
