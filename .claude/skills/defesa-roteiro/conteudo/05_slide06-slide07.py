# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
n.p("<b>2. Produto de cossenos.</b> Na linha de v<sub>d</sub>, cada fase entra como "
    "cos(&#952;<sub>ref</sub> &#8722; k&#183;2&#960;/3)&#183;cos(&#952; &#8722; k&#183;2&#960;/3). "
    "A identidade cos A cos B = &#189;[cos(A &#8722; B) + cos(A + B)] separa cada produto em "
    "duas parcelas:")
bul("<b>cos(A &#8722; B)</b>: os deslocamentos de 2&#960;/3 se cancelam e sobra "
    "cos(&#952;<sub>ref</sub> &#8722; &#952;) <b>igual nas três fases</b>. Somadas, dão "
    "3&#183;&#189; = 3/2.",
    "<b>cos(A + B)</b>: os deslocamentos se somam (0, &#8722;4&#960;/3, +4&#960;/3), são três "
    "cossenos defasados de 120&#176; e <b>a soma é zero</b>. É essa parcela que gira a 2&#969; "
    "e some quando a tensão é equilibrada.")
n.p("Na linha de v<sub>q</sub> é o mesmo, com cos A sen B no lugar, e sobra o seno da diferença.")
n.p("<b>3. O 2/3 cancela o 3/2.</b> Por isso a transformação é chamada de invariante em "
    "amplitude:")
eq(r"v_d = \frac{2}{3}\cdot\frac{3}{2}\,V_m\cos(\theta_{ref} - \theta_{PLL}) "
   r"= V_m\cos(\theta_{ref} - \theta_{PLL})")
eq(r"v_q = \frac{2}{3}\cdot\frac{3}{2}\,V_m\,\mathrm{sen}(\theta_{ref} - \theta_{PLL}) "
   r"= V_m\,\mathrm{sen}(\theta_{ref} - \theta_{PLL})",
   onde="A linha de v<sub>q</sub> é a do TCC (§3.4, antes da 3.10). A de v<sub>d</sub> sai da "
        "mesma conta, mas o TCC não a escreve: se a banca pedir a fonte, é a Equação (3.5) "
        "com essa substituição.")
tab(["Situação", "v<sub>d</sub>", "v<sub>q</sub>", "Leitura"], [
    ["&#952;<sub>PLL</sub> = &#952;<sub>ref</sub> (travado)", "V<sub>m</sub>", "0",
     "amplitude inteira em d: as senoides viraram constantes"],
    ["erro pequeno &#916;&#952;", "&#8776; V<sub>m</sub>", "&#8776; V<sub>m</sub>&#183;&#916;&#952;",
     "v<sub>q</sub> mede o erro de ângulo (slides 7 e 9)"],
    ["erro de 90&#176;", "0", "V<sub>m</sub>", "o vetor caiu inteiro no eixo q"],
], [4.2, 2.0, 2.6, 6.2])
box("base", "O v<sub>d</sub> diz <b>quanto</b> de tensão há e o v<sub>q</sub> diz <b>quanto o "
    "ângulo está errado</b>. O PLL usa só o v<sub>q</sub>: leva ele a zero e, com isso, alinha o "
    "eixo d com a tensão da rede.")
box("alem", "<b>Por que só v<sub>q</sub>, e não v<sub>d</sub>, vai para o PI?</b> Perto do "
    "travamento, o cosseno é quase 1 e varia pouco com o erro, enquanto o seno varia "
    "linearmente. Por isso o v<sub>q</sub> é o sinal que carrega o erro de fase.")
sub("Fundamento: por que o controle quer dq")
n.p("Um PI zera o erro em regime de um sinal <b>constante</b>: a parte integral acumula até "
    "o erro sumir. Para uma senoide, o integrador nunca para de oscilar e sempre sobra erro "
    "de amplitude e de fase. Em dq, o controle de corrente e o PLL viram problemas de sinal "
    "contínuo, e o PI resolve.")
box("alem", "O que <b>não</b> gira a +&#969; aparece oscilando em dq. Sequência negativa "
    "(gira a &#8722;&#969;): aparece a 2&#969; = 120 Hz. Componente contínua nas fases (o "
    "deslocamento transitório da corrente de curto): aparece a &#969; = 60 Hz. Harmônicos: "
    "o 5º (sequência negativa) e o 7º (positiva) aparecem os dois a 6&#969; = 360 Hz. "
    "Isso explica o pico em 60 Hz de algumas curvas no espectro do capítulo 4 do painel.")
box("banca", "<b>E o ângulo &#952;?</b> A transformação só vale se &#952; for o ângulo real "
    "da tensão. Quem estima &#952; é o PLL.")
ponte("como o PLL encontra &#952;.")

# --- 7
slide(7, "Estrutura do SRF-PLL", "Modelagem", "Victor", "Fig. 4.3, §3.4, Eqs. (3.10)-(3.19)")
box("msg", "O SRF-PLL gira o referencial dq até alinhar o eixo d com a tensão da rede.")
fala(7)
n.p("Este é o slide em que a banca mais pode puxar teoria de controle. A seção abaixo "
    "remonta o raciocínio do zero, na ordem em que ele se encadeia: o que é uma malha, "
    "onde cada bloco do PLL entra nela, como sai a função de transferência, como ler polos "
    "e amortecimento, por que o erro vai a zero e por que o afundamento amolece o laço.")

sub("1. Relembrando: a malha fechada")
n.p("Toda malha de controle tem as mesmas peças: uma <b>referência</b> (o que se quer), "
    "uma <b>saída</b> (o que se tem), um <b>comparador</b> que forma o erro, um "
    "<b>controlador</b> que transforma o erro em ação e uma <b>planta</b> que responde à "
    "ação. A realimentação faz a saída perseguir a referência: enquanto houver erro, o "
    "controlador age. O SRF-PLL é exatamente isso, só que a grandeza controlada é um "
    "<b>ângulo</b>:")
tab(["Peça da malha", "No SRF-PLL", "Sinal"], [
    ["Referência", "ângulo real da tensão da rede (não é medido direto)", "&#952;<sub>g</sub>"],
    ["Saída", "ângulo estimado pelo PLL", "&#952;<sub>PLL</sub>"],
    ["Comparador / sensor", "Park da tensão medida: compara os dois ângulos sem medir "
     "&#952;<sub>g</sub>", "v<sub>q</sub> &#8776; U&#183;(&#952;<sub>g</sub> &#8722; "
     "&#952;<sub>PLL</sub>)"],
    ["Controlador", "PI (o &#8220;filtro de laço&#8221;)", "&#916;&#969;"],
    ["Planta (atuador)", "VCO: integrador que transforma frequência em ângulo",
     "&#952;<sub>PLL</sub> = &#8747;&#969;<sub>PLL</sub>dt"],
], [3.4, 7.3, 4.0])
box("base", "O PLL é um controlador de posição angular: a Park mede o erro, o PI decide a "
    "correção de velocidade e o integrador transforma velocidade em posição.")

sub("2. Os três blocos, um a um")
bul("<b>Detector de fase (PD)</b>: a própria Park sobre a tensão medida. Como mostrado no "
    "slide 6, v<sub>q</sub> = U&#183;sen(&#952;<sub>g</sub> &#8722; &#952;<sub>PLL</sub>). "
    "Para erro pequeno, sen x &#8776; x, e v<sub>q</sub> &#8776; U&#183;&#916;&#952;: o erro "
    "de ângulo multiplicado pela amplitude. O v<sub>d</sub> &#8776; U do diagrama é a "
    "amplitude estimada, usada depois nas referências de corrente (slide 11).",
    "<b>Filtro de laço (PI)</b>: recebe v<sub>q</sub> e entrega a correção de frequência "
    "&#916;&#969;. A parte proporcional reage ao erro presente; a integral acumula o erro "
    "passado e é ela que &#8220;memoriza&#8221; um desvio de frequência da rede.",
    "<b>VCO</b> (oscilador controlado por tensão, nome herdado do PLL analógico): no "
    "digital, é um integrador. Soma &#916;&#969; à nominal &#969;<sub>0</sub> = 2&#960;&#183;60 "
    "e integra para dar &#952;<sub>PLL</sub>, que volta à Park da tensão (a realimentação "
    "tracejada em laranja) e segue para as malhas de corrente.")
eq(r"\Delta\omega = K_{pPLL}\,v_q + K_{iPLL}\int v_q\,dt \qquad "
   r"\theta_{PLL} = \int(\omega_0 + \Delta\omega)\,dt")
n.p("<b>Sinal da correção.</b> Se a rede está adiantada (&#952;<sub>g</sub> &gt; "
    "&#952;<sub>PLL</sub>), v<sub>q</sub> &gt; 0, o PI aumenta &#916;&#969;, o PLL gira mais "
    "depressa e alcança a rede. Se está atrasada, o contrário. Quando v<sub>q</sub> = 0, o "
    "eixo d está sobre a tensão: o PLL travou.")
n.p("<b>Por que o feed-forward &#969;<sub>0</sub>?</b> O ângulo da rede é uma rampa, "
    "&#952;<sub>g</sub> = &#969;<sub>0</sub>t + &#966;. Somando &#969;<sub>0</sub> por fora, o "
    "PI só precisa cuidar do <b>desvio</b> em torno de 60 Hz. Sem ele, a integral teria de "
    "construir 377 rad/s a partir de zero na partida, com um transitório longo e grande.")

sub("3. Relembrando: Laplace, integrador e PI")
n.p("Em Laplace, derivar vira multiplicar por s e integrar vira dividir por s. Assim o VCO "
    "é 1/s e o PI é:")
eq(r"C(s) = K_p + \frac{K_i}{s} = \frac{K_p\,s + K_i}{s}",
   onde="Um <b>polo na origem</b> (o integrador do PI) e um <b>zero</b> em s = "
        "&#8722;K<sub>i</sub>/K<sub>p</sub>. Na sintonia nominal, 105.820/460 = 230 rad/s.")
box("base", "Polo: valor de s que faz a função ir ao infinito, define o modo natural de "
    "resposta. Zero: valor de s que zera a função, muda a forma da resposta (no PLL, aumenta "
    "a sobre-elevação, ver slide 9). Integrador = polo em s = 0.")

sub("4. Montando a malha fechada passo a passo")
n.p("Com o PD linearizado (ganho U), a malha aberta é o produto dos três blocos:")
eq(r"L(s) = U\cdot\frac{K_p s + K_i}{s}\cdot\frac{1}{s} = \frac{U(K_p s + K_i)}{s^2}",
   onde="Da esquerda para a direita: U é o detector (Park linearizada), a fração do meio é "
        "o PI e 1/s é o VCO. O s&#178; do denominador são os dois integradores.")
n.p("Fechando a realimentação unitária, G = L/(1 + L):")
eq(r"G(s) = \frac{\theta_{PLL}(s)}{\theta_g(s)} = "
   r"\frac{U K_p\,s + U K_i}{s^2 + U K_p\,s + U K_i}",
   onde="Com U = 1 pu, é a Eq. (3.18) do TCC. A forma com U é a de Karimi-Ghartemani "
        "(2014), eq. 6.4: s<super>2</super> + h<sub>0</sub>Us + h<sub>1</sub>U = 0.")
n.p("O denominador é a <b>equação característica</b> (o cartão da direita do slide). "
    "Igualando à forma canônica de 2ª ordem, termo a termo:")
eq(r"s^2 + U K_p\,s + U K_i = 0 \quad\Leftrightarrow\quad s^2 + 2\xi\omega_n s + \omega_n^2 = 0",
   onde="Com U = 1 pu: K<sub>p</sub> = 2&#958;&#969;<sub>n</sub> (coeficiente de s) e "
        "K<sub>i</sub> = &#969;<sub>n</sub><super>2</super> (termo independente), TCC 3.19.")
box("base", "Dois integradores na malha aberta (PI e VCO) dão uma malha fechada de 2ª ordem. "
    "Toda a sintonia se resume a escolher onde ficam os dois polos.")

n.p("Como ler &#969;<sub>n</sub> e &#958; nos polos, e como se escolhem os seus valores, "
    "fica para o slide 9.")

sub("5. Relembrando: tipo do sistema e erro em regime")
n.p("O <b>tipo</b> de uma malha é o número de integradores na malha aberta L(s). Ele diz "
    "que entradas a malha segue com erro nulo em regime, pelo teorema do valor final, "
    "e<sub>&#8734;</sub> = lim<sub>s&#8594;0</sub> s&#183;E(s), com:")
eq(r"E(s) = \theta_g - \theta_{PLL} = \frac{1}{1+L(s)}\,\theta_g(s) = "
   r"\frac{s^2}{s^2 + U K_p s + U K_i}\,\theta_g(s)")
tab(["O que a rede faz", "&#952;<sub>g</sub>(s)", "Só P (tipo 1)", "PI (tipo 2, o do TCC)"], [
    ["Salto de fase &#916;&#966;", "&#916;&#966;/s", "0", "0"],
    ["Degrau de frequência &#916;&#969;", "&#916;&#969;/s&#178;",
     "&#916;&#969;/(U&#183;K<sub>p</sub>), constante", "0"],
], [4.4, 2.6, 3.9, 3.8])
n.p("O s&#178; no numerador de E(s) é a assinatura do tipo 2: cancela o s&#178; do degrau "
    "de frequência e o erro vai a zero. Fisicamente, a integral do PI guarda o "
    "&#916;&#969; necessário com v<sub>q</sub> = 0. É por isso que, depois da falta, o PLL "
    "volta a zero sozinho, desde que não perca o sincronismo no caminho.")
box("prova", "<b>&#8220;Por que PI e não só um ganho proporcional?&#8221;</b> Só com P, o "
    "laço é tipo 1 (só o integrador do VCO). Se a frequência da rede se desvia, sobra um "
    "erro de ângulo permanente &#916;&#969;/(U&#183;K<sub>p</sub>): v<sub>q</sub> fica "
    "diferente de zero e o eixo d nunca alinha de fato. O integrador do PI zera esse erro.")

sub("6. O que o afundamento faz com o laço")
n.p("Como a tensão é dividida por um valor fixo (o porquê está no slide 9), U fica dentro "
    "do ganho do detector: em regime U = 1, mas na falta U cai. Casando a equação "
    "característica com a forma canônica, agora com U livre:")
eq(r"\omega_{n,\mathrm{ef}}^2 = U K_i \Rightarrow \omega_{n,\mathrm{ef}} = \omega_n\sqrt{U}"
   r"\qquad 2\xi_{\mathrm{ef}}\omega_{n,\mathrm{ef}} = U K_p \Rightarrow "
   r"\xi_{\mathrm{ef}} = \xi\sqrt{U}")
eq(r"t_{s,\mathrm{ef}} = \frac{4{,}6}{\xi_{\mathrm{ef}}\,\omega_{n,\mathrm{ef}}} = "
   r"\frac{9{,}2}{U K_p} = \frac{20\ \mathrm{ms}}{U}",
   onde="O laço amolece justamente quando mais precisa reagir: a frequência natural e o "
        "amortecimento caem com &#8730;U, e o tempo de acomodação (critério de 1% do slide "
        "10) cresce com 1/U.")
tab(["U (pu)", "&#969;<sub>n,ef</sub> (rad/s)", "&#958;<sub>ef</sub>", "t<sub>s,ef</sub>",
     "Leitura"], [
    ["1,0", "325,3", "0,707", "20 ms", "sintonia nominal"],
    ["0,5", "230,0", "0,500", "40 ms", "afundamento moderado"],
    ["0,25", "162,7", "0,354", "80 ms", "&#969;<sub>n</sub> e &#958; à metade"],
    ["0,2", "145,5", "0,316", "100 ms", "igual à sintonia inadequada"],
    ["0,09", "97,6", "0,212", "~220 ms", "ordem da tensão na falta (capítulo 6 do painel)"],
], [1.6, 2.8, 1.6, 1.9, 6.8])
n.note("Valores do modelo linear, válidos enquanto o erro de ângulo for pequeno. O "
       "t<sub>s,ef</sub> é um indicador de tendência: a tensão não fica parada num U só "
       "durante a falta.")

sub("7. Onde o modelo linear deixa de valer")
n.p("O detector real é v<sub>q</sub> = U&#183;sen(&#916;&#952;), não U&#183;&#916;&#952;. "
    "A aproximação erra cerca de 5% em 30&#176; e piora depois. Três consequências:")
