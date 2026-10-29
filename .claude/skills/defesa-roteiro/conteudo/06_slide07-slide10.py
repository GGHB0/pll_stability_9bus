# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
bul("<b>Ganho máximo em 90&#176;</b>: acima disso, quanto maior o erro, <b>menor</b> o "
    "sinal que o PI recebe para corrigir.",
    "<b>Ponto instável em 180&#176;</b>: se &#916;&#952; passa de 180&#176;, o sinal de "
    "v<sub>q</sub> inverte e o PLL é empurrado para o próximo ponto de travamento, um ciclo "
    "à frente. É o escorregamento de ciclo, a forma concreta de perder o sincronismo.",
    "<b>U perto de zero</b>: numa falta próxima, v<sub>q</sub> fica quase nulo qualquer que "
    "seja o erro. O PLL fica &#8220;cego&#8221;: a integral segura o último &#916;&#969; e o "
    "ângulo deriva até a tensão voltar.")
box("alem", "Por isso a sintonia lenta e pouco amortecida é a mais exposta: com "
    "&#958;<sub>ef</sub> baixo, a resposta passa do ponto, o erro chega mais longe e fica "
    "mais perto dos 180&#176; no momento em que a tensão volta.")

sub("8. Por que o travamento importa: a conta do erro de ângulo")
n.p("Com o eixo d sobre a tensão, i<sub>d</sub> controla só a potência ativa e "
    "i<sub>q</sub> só a reativa: é o desacoplamento entre P e Q. Se &#952;<sub>PLL</sub> "
    "erra de &#916;&#952;, a corrente que o controle manda no eixo d sai girada de "
    "&#916;&#952; em relação à tensão real. Uma fração cos &#916;&#952; vira ativa e sen "
    "&#916;&#952; vaza para a reativa (e vice-versa para i<sub>q</sub>):")
tab(["Erro de ângulo", "cos &#916;&#952; (fica no eixo certo)", "sen &#916;&#952; (vaza)"], [
    ["5&#176;", "99,6%", "8,7%"],
    ["10&#176;", "98,5%", "17,4%"],
    ["30&#176;", "86,6%", "50,0%"],
    ["90&#176;", "0%", "100%: o reativo pedido pelo ONS sai como ativo"],
], [3.4, 5.0, 6.3])
n.p("Daí a pergunta do rodapé: o suporte de tensão do ONS depende de injetar reativo "
    "<b>na direção certa</b>, e quem dá a direção é o PLL.")
box("banca", "<b>Por que o travamento importa?</b> Um erro em &#952; passa direto às malhas "
    "de corrente e compromete o desacoplamento entre P e Q.")

sub("Glossário de bolso")
tab(["Termo", "Em uma frase"], [
    ["Malha aberta L(s)", "produto de tudo que o sinal atravessa do erro até a saída"],
    ["Malha fechada G(s)", "L/(1+L): como a saída responde à referência"],
    ["Equação característica", "denominador de G(s) igualado a zero; suas raízes são os polos"],
    ["&#969;<sub>n</sub>", "frequência natural: o quão rápido o laço se move"],
    ["&#958;", "amortecimento: o quanto ele oscila antes de assentar (0,707 = clássico)"],
    ["t<sub>s</sub>", "tempo até a resposta ficar dentro de 1% do final (4,6/&#958;&#969;<sub>n</sub>)"],
    ["Tipo", "número de integradores em L(s); tipo 2 segue degrau de frequência sem erro"],
    ["Banda passante", "até onde G(s) segue a entrada; acima, filtra (slide 10)"],
], [4.2, 10.5])
ponte("antes de sintonizar, qual rede o PLL enxerga?")

# --- 8
slide(8, "Sistema IEEE 9 barras", "Modelagem", "Victor, Bruno, Victor", "Fig. 4.1, §4.1, §4.3.1")
box("msg", "O PLL foi modelado no PSIM; a rede, com as máquinas síncronas, vem pronta no Simulink.")
fala(8)
sub("Fundamento: o sistema")
n.p("O caso clássico tem três geradores, três transformadores, seis linhas e três cargas, "
    "em 230 kV. O G2 (192 MVA) sai e a UFV de 100 MW entra na Barra 2; G1 e G3 continuam "
    "síncronos e carregam a inércia que sobra.")
sub("Fundamento: sistema por unidade")
n.p("Tudo é dividido por uma base: potência de 100 MVA e a tensão nominal de cada trecho. "
    "A impedância base sai das duas:")
eq(r"Z_{base} = \frac{V_{base}^2}{S_{base}}",
   onde="20 kV: 4 &#937;; 230 kV: 529 &#937;. Em pu, os 100 MW da usina valem 1 pu e os "
        "transformadores ideais somem das contas.")
sub("Fundamento: Thévenin e os dois softwares")
n.p("A Z<sub>barra</sub> é a inversa da matriz de admitâncias da rede. O elemento "
    "diagonal Z<sub>22</sub> é a impedância de Thévenin vista da Barra 2. No PSIM, modelamos "
    "o inversor chave a chave sob esse equivalente para validar os ganhos; no Simulink, "
    "roda o sistema IEEE 9 barras completo com máquinas síncronas e nível de curto fixo.")
box("alem", "<b>Força da rede (SCR).</b> A relação de curto-circuito é a potência de curto "
    "no ponto de conexão dividida pela potência do inversor; com o inversor em 1 pu, é "
    "aproximadamente 1/|Z<sub>th</sub>| em pu. O TCC mantém o nível de curto fixo e varia o "
    "local da falta: varrer o SCR é trabalho futuro.")
nums([["192 MVA", "máquina original da Barra 2"],
      ["100 MW = 1 pu", "UFV, na base de 100 MVA, 60 Hz"],
      ["230 kV / 20 kV", "rede de transmissão / tensão do lado do inversor"]])
box("banca", "<b>Por que dois softwares?</b> O PSIM modela o conversor chave a chave; o "
    "Simulink traz o IEEE 9 barras completo com máquinas síncronas (§4.1 do TCC).")
box("cuidado", "R<sub>th</sub> = 10,04 m&#937; e L<sub>th</sub> = 1,16 mH não estão no TCC; "
    "aparecem só no apêndice (slide 21).")
ponte("com a rede e o método definidos, passa-se à sintonia dos ganhos do PLL.")

# --- 9
slide(9, "Sintonia do PLL", "Modelagem", "Victor, Bruno, Victor", "§3.4, Eqs. (3.10)-(3.20)")
box("msg", "Fixado o amortecimento, resta um único grau de liberdade: o tempo de acomodação.")
fala(9)
n.p("O slide 7 deu a <b>forma</b> do laço: uma malha fechada de 2ª ordem com dois ganhos, "
    "K<sub>p</sub> e K<sub>i</sub>. Este slide responde <b>como se escolhe cada número</b>. "
    "A lógica em uma linha: tornar o laço independente da tensão (passos 1 e 2), trocar os "
    "dois ganhos por duas grandezas com significado físico, &#969;<sub>n</sub> e &#958; "
    "(passo 3), fixar uma delas por um critério clássico (passo 4) e escolher a outra pela "
    "velocidade desejada (passo 5).")

sub("Passo 1: tensão em pu. De onde vem 16.329,93 V")
n.p("A rede do lado do inversor é de 20 kV <b>de linha, eficaz</b>. O detector trabalha com "
    "o <b>pico de fase</b>, então:")
eq(r"V_{pico,fase} = \frac{20\,000}{\sqrt{3}}\cdot\sqrt{2} = 11\,547\cdot 1{,}414 = "
   r"16\,329{,}93\ \mathrm{V}",
   onde="&#8730;3 passa de linha para fase; &#8730;2 passa de eficaz para pico. Com a "
        "transformada invariante em amplitude (slide 6), é esse pico que aparece inteiro em "
        "v<sub>d</sub>.")
n.p("<b>Por que dividir.</b> Sem a divisão, v<sub>q</sub> &#8776; 16.329,93&#183;&#916;&#952; "
    "volts: o ganho do detector seria 16.329,93, e ele entraria multiplicando os dois ganhos "
    "do PI. Dividindo, a tensão nominal vale U = 1 pu, o ganho do detector K<sub>pd</sub> vale "
    "1 e a equação característica do slide 7 fica sem U. É isso que deixa usar as fórmulas "
    "canônicas direto.")
n.p("<b>Por que um valor fixo, e não a amplitude medida.</b> O divisor é constante: em "
    "regime ele dá U = 1, mas na falta a tensão cai e U cai junto. É daí que vem o "
    "amolecimento do laço (&#969;<sub>n</sub>&#8730;U, &#958;&#8730;U, slide 7, passo 6).")
box("alem", "<b>A alternativa que o TCC não usa.</b> Dividir v<sub>q</sub> pela amplitude "
    "medida, &#8730;(v<sub>d</sub>&#178; + v<sub>q</sub>&#178;), torna o laço independente de U "
    "(Karimi-Ghartemani, 2014). O modelo do TCC normaliza por constante, como a maioria das "
    "implementações básicas, e é justamente essa dependência que o trabalho explora.")

sub("Passo 2: linearizar")
n.p("O detector real é v<sub>q</sub> = V<sub>m</sub>&#183;sen(&#952;<sub>ref</sub> &#8722; "
    "&#952;<sub>PLL</sub>). Para projetar, considera-se o PLL já perto do travamento, com "
    "erro pequeno, onde sen x &#8776; x:")
eq(r"v_q \approx V_m(\theta_{ref} - \theta_{PLL}), \qquad V_m = 1\ \mathrm{pu} "
   r"\Rightarrow K_{pd} = 1")
n.p("Projetar no ponto de operação e conferir depois em simulação é o procedimento padrão: "
    "as fórmulas lineares dizem como o laço se comporta em torno do travamento. Longe dele "
    "(erro grande, falta próxima), quem responde é a simulação (slide 7, passo 7).")

sub("Passo 3: forma canônica. Por que &#8220;um único grau de liberdade&#8221;")
n.p("Com K<sub>pd</sub> = 1, a equação característica s&#178; + K<sub>p</sub>s + K<sub>i</sub> "
    "= 0 é comparada termo a termo com a de qualquer sistema de 2ª ordem:")
eq(r"s^2 + K_p\,s + K_i = s^2 + 2\xi\omega_n s + \omega_n^2 \ \Rightarrow\ "
   r"K_p = 2\xi\omega_n, \quad K_i = \omega_n^2")
n.p("São duas incógnitas (K<sub>p</sub>, K<sub>i</sub>) e agora duas grandezas que se sabe "
    "interpretar (&#969;<sub>n</sub>, &#958;). Escolher os ganhos é o mesmo que escolher "
    "&#969;<sub>n</sub> e &#958;. Fixado o &#958; (passo 4), sobra uma escolha só: o "
    "t<sub>s</sub> (passo 5), que define &#969;<sub>n</sub>. É o &#8220;único grau de "
    "liberdade&#8221; do título.")
sub("Relembrando: como ler &#969;<sub>n</sub> e &#958; nos polos")
n.p("As raízes da equação característica, para &#958; &lt; 1, são um par complexo:")
eq(r"s = -\xi\omega_n \pm j\,\omega_n\sqrt{1-\xi^2}",
   onde="Parte real &#8722;&#958;&#969;<sub>n</sub>: velocidade com que a envoltória "
        "e<super>&#8722;&#958;&#969;n t</super> morre; é ela que define o t<sub>s</sub>. "
        "Parte imaginária: frequência da oscilação amortecida. &#969;<sub>n</sub> é a "
        "distância do polo à origem; &#958; é o cosseno do ângulo entre o polo e o semieixo "
        "real negativo.")
n.p("Na sintonia nominal, os polos ficam em <b>&#8722;230 &#177; j230</b>: a 45&#176;, "
    "exatamente na diagonal, porque cos 45&#176; = 0,707. Polo mais à esquerda: decai mais "
    "rápido. Polo mais perto do eixo imaginário: oscila mais. Sobre o eixo imaginário, "
    "oscilação sem amortecimento; à direita dele, instabilidade.")
box("alem", "Conta rápida para conferir: parte real = K<sub>p</sub>/2 = 460/2 = 230; parte "
    "imaginária = &#8730;(K<sub>i</sub> &#8722; 230&#178;) = &#8730;(105.820 &#8722; 52.900) "
    "&#8776; 230.")

sub("Passo 4: fixar &#958; = 0,707. Por que esse valor")
n.p("O &#958; decide o formato da resposta, independente da velocidade. A sobre-elevação "
    "do protótipo de 2ª ordem só depende dele:")
eq(r"M_p = e^{-\pi\xi/\sqrt{1-\xi^2}}")
tab(["&#958;", "M<sub>p</sub>", "Polo com o eixo real", "Leitura"], [
    ["0,316", "35%", "71,6&#176;", "oscila muito (é a sintonia inadequada, slide 10)"],
    ["0,5", "16%", "60&#176;", "ainda oscila bastante"],
    ["<b>0,707</b>", "<b>4,3%</b>", "<b>45&#176;</b>", "<b>compromisso clássico</b>"],
    ["1,0", "0%", "0&#176; (polo duplo real)", "sem oscilação, porém mais lento"],
], [1.8, 1.6, 3.6, 7.7])
n.p("Abaixo de 0,707, a resposta passa do ponto e oscila; acima, fica cada vez mais lenta "
    "para chegar ao valor final, sem ganho real em oscilação. 0,707 é o ponto em que se "
    "aceita um pequeno sobressinal em troca de rapidez. É também o menor &#958; em que a "
    "resposta em frequência do protótipo não tem pico de ressonância. É o valor de Ogata e "
    "o de Alves, Dias e Rolim (2020).")
box("prova", "<b>&#8220;A sobre-elevação do PLL é mesmo 5%?&#8221;</b> Os 4,3% valem para o "
    "protótipo de 2ª ordem sem zero. A G(s) do PLL (TCC 3.18) tem um zero, que vem do PI, "
    "e com ele a resposta ao degrau de fase passa mais: cerca de 21% com a sintonia "
    "nominal (conta de simulação do modelo linear, além do TCC). Resposta segura: o "
    "&#958; = 0,707 foi escolhido pela forma canônica, como em Ogata e em Alves, Dias e "
    "Rolim; o zero do PI aumenta a sobre-elevação ao degrau de fase, e o tempo de "
    "acomodação continua perto dos 20 ms (cerca de 16 ms no modelo linear).")

sub("Passo 5: escolher t<sub>s</sub>. De onde vem o 4,6")
n.p("A resposta de 2ª ordem subamortecida é uma senoide que morre dentro da envoltória "
    "e<super>&#8722;&#958;&#969;n t</super>. O tempo de acomodação é quando essa envoltória "
    "cai a 1% do valor inicial:")
