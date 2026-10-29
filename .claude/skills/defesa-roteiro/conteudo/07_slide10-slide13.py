# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
eq(r"e^{-\xi\omega_n t_s} = 0{,}01 \ \Rightarrow\ \xi\omega_n t_s = \ln 100 = 4{,}6 "
   r"\ \Rightarrow\ t_s = \frac{4{,}6}{\xi\omega_n}", tag="3.20",
   onde="Com o critério de 2%, seria ln 50 &#8776; 3,9, arredondado para 4: é o "
        "4/(&#958;&#969;<sub>n</sub>) usado no PI de corrente (slide 14). O 1% é mais "
        "exigente: para o mesmo t<sub>s</sub>, pede um laço um pouco mais rápido.")
n.p("<b>O compromisso.</b> t<sub>s</sub> curto significa &#969;<sub>n</sub> alto e banda "
    "larga: o PLL acompanha rápido, mas deixa passar ruído de medição, harmônicos e o "
    "desequilíbrio (os 120 Hz da sequência negativa, slide 11) para o ângulo. t<sub>s</sub> "
    "longo filtra bem, mas não acompanha variações reais da rede e demora a retomar o "
    "sincronismo depois da falta.")
n.p("<b>Por que 20 ms.</b> Um período de 60 Hz dura 16,7 ms; 20 ms é pouco mais de um "
    "ciclo, ou seja, o PLL acomoda em pouco mais de um ciclo da rede. É o valor de Alves, "
    "Dias e Rolim (2020) e de Teodorescu, Liserre e Rodriguez (2011).")
box("prova", "<b>&#8220;O que acontece se aumentar muito os ganhos?&#8221;</b> &#969;<sub>n</sub> "
    "e a banda sobem: o PLL acompanha mais rápido, mas deixa passar mais ruído, harmônicos e "
    "os 120 Hz da sequência negativa para o ângulo. Com os 20 ms, a banda já fica em 107 Hz, "
    "colada nos 120 Hz (slide 11): ir mais rápido pioraria isso.")

sub("A conta de mão, do t<sub>s</sub> aos ganhos")
n.p("Com &#958; = 0,707 e t<sub>s</sub> = 20 ms, quatro linhas, cada uma usando só a "
    "anterior:")
tab(["", "Conta", "Resultado", "De onde vem"], [
    ["1", "&#958;&#969;<sub>n</sub> = 4,6 / 0,020", "230 rad/s", "critério de 1% (passo 5)"],
    ["2", "K<sub>p</sub> = 2&#183;&#958;&#969;<sub>n</sub> = 2&#183;230", "460",
     "forma canônica (passo 3); o mesmo que 9,2/t<sub>s</sub>"],
    ["3", "&#969;<sub>n</sub> = 230 / 0,707", "325,3 rad/s (51,8 Hz)",
     "divide pelo &#958; fixado (passo 4)"],
    ["4", "K<sub>i</sub> = &#969;<sub>n</sub>&#178; = 325,3&#178;", "105.820",
     "forma canônica (passo 3)"],
], [0.7, 5.0, 3.6, 5.4])
n.p("Repare que K<sub>p</sub> nem precisa do &#958;: 2&#183;&#958;&#969;<sub>n</sub> = "
    "2&#183;4,6/t<sub>s</sub> = 9,2/t<sub>s</sub>, a forma de Teodorescu. O &#958; só entra "
    "para tirar &#969;<sub>n</sub> e, com ele, K<sub>i</sub>. Por isso K<sub>p</sub> fixa a "
    "<b>velocidade</b> e K<sub>i</sub>, junto com K<sub>p</sub>, o <b>amortecimento</b>.")
box("cuidado", "K<sub>i</sub> depende do arredondamento: com &#969;<sub>n</sub> = 325,3 sai "
    "105.820, o valor do TCC e do modelo. Sem arredondar o 0,707 e o 4,6 o número muda na "
    "terceira casa. Na fala, use sempre 105.820.")
nums([["460 / 105.820", "K<sub>pPLL</sub> / K<sub>iPLL</sub> nominais"],
      ["325,3 rad/s", "&#969;<sub>n</sub> nominal, 51,8 Hz"],
      ["0,707", "&#958;; 4,3% no protótipo de 2ª ordem (o TCC diz cerca de 5%); ~21% com o "
                "zero do PI"],
      ["20 ms", "t<sub>s</sub> pelo critério de 1%"]])
box("cuidado", "A régua do slide mostra só &#8220;1 período&#8221; e 20 ms. O porquê do "
    "critério de 1% está em criterio_acomodacao_srf_pll.pdf.")
ponte("esta é a sintonia nominal; para testar a sensibilidade, uma segunda.")

# --- 11
slide(11, "Duas sintonias do PLL", "Modelagem", "Bruno, Victor", "§3.4 (eq. 3.20), §4.3")
box("msg", "A sintonia inadequada reduz os dois ganhos em 80%: laço mais lento e menos "
    "amortecido.")
fala(11)
sub("Fundamento: a conta da inadequada")
eq(r"K_p = 0{,}2\cdot460 = 92 \qquad K_i = 0{,}2\cdot105\,820 = 21\,164")
eq(r"\omega_n = \sqrt{21\,164} = 145{,}5\ \mathrm{rad/s} \qquad "
   r"\xi = \frac{92}{2\cdot145{,}5} = 0{,}316",
   onde="Como K<sub>i</sub> cai 5 vezes, &#969;<sub>n</sub> cai &#8730;5 &#8776; 2,24 vezes; "
        "&#958; cai na mesma proporção. Pelo mesmo critério, t<sub>s</sub> sobe para cerca "
        "de 100 ms.")
sub("Fundamento: o cartão t<sub>s</sub>: 20 &#8594; 100 ms")
n.p("É a régua do slide anterior aplicada às duas colunas. Como &#958;&#969;<sub>n</sub> = "
    "K<sub>p</sub>/2, o t<sub>s</sub> só depende de K<sub>p</sub>: 4,6/230 = 20 ms na nominal e "
    "4,6/46 = 100 ms na inadequada. K<sub>p</sub> &#215; 0,2 deixa o laço 5 vezes mais lento, "
    "e 100 ms é a duração inteira da falta (0,1 s).")
box("banca", "<b>O 100 ms está no TCC?</b> Não escrito: o TCC dá só os 20 ms. Sai da "
    "Eq. (3.20), t<sub>s</sub> = 4,6/(&#958;&#969;<sub>n</sub>), com &#958; e &#969;<sub>n</sub> "
    "da tabela. Se perguntarem, refazer a conta.")
sub("Para o slide 25: 754 rad/s = 2,32&#183;&#969;<sub>n</sub>")
n.p("A oscilação da sequência negativa é de 120 Hz, ou 754 rad/s: só 2,32 vezes a "
    "&#969;<sub>n</sub> nominal. Um laço de segunda ordem só atenua bem o que está muito "
    "acima da sua &#969;<sub>n</sub>. Quanto passa sai do módulo de G(j&#969;):")
eq(r"|G(j\omega)| = \frac{\sqrt{K_i^2 + (K_p\,\omega)^2}}"
   r"{\sqrt{(K_i - \omega^2)^2 + (K_p\,\omega)^2}}")
box("alem", "Contas com o modelo linear e U = 1 (tabela abaixo).")
tab(["", "Nominal", "Inadequada"], [
    ["&#969;<sub>n</sub> ; &#958;", "325,3 rad/s ; 0,707", "145,5 rad/s ; 0,316"],
    ["Polos ; ângulo com o eixo real", "&#8722;230 &#177; j230 ; 45&#176;",
     "&#8722;46 &#177; j138 ; 71,6&#176;"],
    ["Banda de &#8722;3 dB de G(s)", "669 rad/s (107 Hz)", "242 rad/s (38 Hz)"],
    ["|G(j754)|: quanto do 120 Hz passa", "0,63", "0,13"],
    ["t<sub>s</sub> (critério de 1%)", "20 ms", "~100 ms"],
], [6.0, 4.35, 4.35])
n.p("A leitura: a banda da sintonia nominal (107 Hz) fica colada nos 120 Hz, então quase "
    "dois terços da oscilação chegam ao ângulo. A inadequada deixa passar um oitavo, por "
    "isso filtra melhor (capítulo 5 do painel), mas responde cinco vezes mais devagar "
    "(capítulo 6).")
box("alem", "<b>A inadequada não é artificial.</b> Pela fórmula do slide 7, a sintonia "
    "nominal com U = 0,2 pu tem &#969;<sub>n</sub> = 325,3&#183;&#8730;0,2 = 145,5 rad/s e "
    "&#958; = 0,707&#183;&#8730;0,2 = 0,316: exatamente a inadequada. Um afundamento para "
    "0,2 pu deixa o laço nominal com a dinâmica da sintonia inadequada. Bom argumento se a "
    "banca questionar o fator 0,2.")
nums([["92 / 21.164", "K<sub>p</sub> / K<sub>i</sub> inadequados (nominais &#215; 0,2)"],
      ["145,5 rad/s; 0,316", "&#969;<sub>n</sub> (23,2 Hz); &#958;"],
      ["t<sub>s</sub>: 20 &#8594; 100 ms", "4,6/(&#958;&#969;<sub>n</sub>), laço 5 vezes mais lento"]])
box("banca", "<b>Por que reduzir os ganhos?</b> Simula uma malha de sincronismo mais lenta "
    "e menos amortecida; no caso-limite, o SRF-PLL deixa de recuperar o sincronismo após a "
    "eliminação da falta.")
ponte("com o sincronismo resolvido, o inversor.")

# --- 12
slide(12, "Referência de corrente", "Modelagem", "Victor, Bruno",
      "§3.1.3-3.1.4, Eqs. (3.8)-(3.9); diagrama: exceção de método (PSIM)")
box("msg", "Na primeira versão do inversor, a referência de corrente saía direto da "
    "potência desejada.")
fala(12)
sub("Fundamento: potência em dq")
eq(r"P = \frac{3}{2}\left(v_d i_d + v_q i_q\right) \qquad "
   r"Q = \frac{3}{2}\left(v_q i_d - v_d i_q\right)", tag="3.8",
   onde="O 3/2 compensa o 2/3 da Park invariante em amplitude.")
n.p("Com o PLL travado, v<sub>q</sub> = 0 e cada potência depende de uma só corrente "
    "(TCC 3.9). Invertendo:")
eq(r"i_{d,ref} = \frac{2P}{3v_d} \qquad i_{q,ref} = -\frac{2Q}{3v_d}",
   onde="Em pu, o 3/2 some. Na versão do PSIM: P<sub>ref</sub> = 1 pu (100 MW) em degrau "
        "aplicado em 35 ms e Q<sub>ref</sub> = 0, divididos por v<sub>d</sub> vindo do "
        "próprio SRF-PLL.")
box("alem", "<b>E se o ângulo estiver errado?</b> Escrevendo a tensão no referencial do PLL "
    "(v<sub>d</sub> = V cos&#916;&#952;, v<sub>q</sub> = V sen&#916;&#952;) e substituindo "
    "acima, sai a equação a seguir.")
eq(r"P = \frac{3}{2}V\left(i_d\cos\Delta\theta + i_q\sin\Delta\theta\right) \qquad "
   r"Q = \frac{3}{2}V\left(i_d\sin\Delta\theta - i_q\cos\Delta\theta\right)",
   onde="Com &#916;&#952; = 0 volta ao caso desacoplado. Com &#916;&#952; grande, a corrente "
        "que o controle chama de ativa vira reativa, e com |&#916;&#952;| &gt; 90° a ativa "
        "muda de sinal. É o mecanismo da potência absorvida no capítulo 6 do painel.")
box("banca", "<b>Por que o PLL importa aqui?</b> A divisão só vale com v<sub>q</sub> = 0; "
    "quem alinha o eixo d e entrega v<sub>d</sub> é o SRF-PLL.")
box("cuidado", "&#8220;35 ms&#8221; é o único número fora do TCC neste slide (aprovado). O "
    "TCC se contradiz sobre o desacoplamento (§3.1.4 diz que não há, §3.5 diz que há); o "
    "slide não afirma nenhum dos dois.")
ponte("antes da malha de corrente, o filtro que liga o inversor à rede.")

# --- 13
slide(13, "Filtro LCL", "Modelagem", "Bruno, Victor",
      "§4.3.2 e §4.3.2.1 (só os resultados; equações fora do TCC)")
box("msg", "Quatro passos fixam o filtro, com a ressonância entre a rede e o chaveamento.")
fala(13)
box("cuidado", "Slide de exceção de método (aprovada em 27/10/2026): o TCC entregue só traz "
    "os resultados (L<sub>est</sub> = 30,71 mH, &#969;<sub>res</sub> = 9.068,99 rad/s, "
    "R<sub>d1</sub>, R<sub>d2</sub>, R<sub>d3</sub>), não as equações. Na tela e na fala, só os "
    "números do TCC. Os intermediários abaixo (L<sub>1</sub>, L<sub>2</sub>, C, V<sub>cc</sub>) "
    "são do modelo e servem para responder, não para dizer.")
sub("Fundamento: por que LCL")
n.p("O inversor chaveia a 5 kHz: a tensão de saída é uma sequência de pulsos, e a corrente "
    "carrega ondulação nessa frequência. O filtro deixa passar os 60 Hz e barra o "
    "chaveamento. Um L simples precisaria de indutância enorme; o LCL atenua muito mais "
    "com menos material (60 dB por década acima da ressonância, contra 20 dB do L). O preço "
    "é a ressonância, que o passo 3 posiciona e o passo 4 amortece.")
sub("Os quatro passos, com os números do modelo")
n.p("Base: 100 MW em 20 kV dão 2.887 A eficazes por fase, ou 4.082 A de pico. "
    "V<sub>cc</sub> do cálculo = 90,91 kV (o modelo usa 1,5 vez esse valor, ver abaixo).")
eq(r"L_1 = \frac{V_{cc}}{24\,f_{sw}\,\Delta i_{L1}} = "
   r"\frac{90\,909}{24\cdot5000\cdot24{,}9} = 30{,}42\ \mathrm{mH}",
   onde="<b>Passo 1.</b> A ondulação da corrente cresce com V<sub>cc</sub> e cai com "
        "L<sub>1</sub> e f<sub>sw</sub>; o 24 é o fator de pior caso do VSI de dois níveis "
        "usado na tese de Alves. A ondulação admitida foi 0,61% do pico (24,9 A).")
eq(r"L_2 = k\,L_1 = 0{,}0095\cdot30{,}42 = 0{,}289\ \mathrm{mH} \qquad "
   r"L_{est} = L_1 + L_2 = 30{,}71\ \mathrm{mH}",
   onde="<b>Passo 2.</b> L<sub>est</sub> é o número do TCC: é a indutância que a malha de "
        "corrente enxerga em baixa frequência (planta 1/(sL<sub>est</sub>), slide 14).")
eq(r"C_x = \frac{L_1 + L_2}{L_1 L_2\,(\pi f_{sw})^2} = 14{,}16\ \mu\mathrm{F} \qquad "
   r"C = 3\,C_x = 42{,}47\ \mu\mathrm{F}",
   onde="<b>Passo 3.</b> C<sub>x</sub> poria a ressonância exatamente na metade do "
        "chaveamento (&#960;f<sub>sw</sub> = 15.708 rad/s, 2,5 kHz). O fator 3 a puxa para "
        "baixo por &#8730;3, com margem.")
eq(r"\omega_{res} = \sqrt{\frac{L_1 + L_2}{L_1 L_2 C}} = \frac{\pi f_{sw}}{\sqrt{3}} = "
   r"9\,068{,}99\ \mathrm{rad/s}\ (1\,443\ \mathrm{Hz})",
   onde="Cerca de 24 vezes a fundamental e 0,29 vez o chaveamento: a &#8220;faixa "
        "intermediária segura&#8221; do TCC.")
eq(r"R_{d1} = 0{,}05\,\omega_g L_1 = 0{,}5734\ \Omega \quad "
   r"R_{d2} = 0{,}05\,\omega_g L_2 = 0{,}0054\ \Omega \quad "
   r"R_{d3} = \frac{0{,}05}{\omega_g C} = 3{,}1228\ \Omega",
   onde="<b>Passo 4.</b> Cada resistência vale 5% da reatância do seu elemento em 60 Hz "
        "(&#969;<sub>g</sub> = 377 rad/s): amortece o pico de ressonância e quase não mexe "
        "na fundamental.")
sub("Por que o V<sub>cc</sub> é alto")
n.p("No TCC: o barramento CC foi &#8220;fixado em valor constante para manter a margem de "
    "modulação necessária&#8221;. No modelo, V<sub>cc</sub> = 136,36 kV, 1,5 vez os 90,91 kV "
    "do cálculo. A conta que mostra o porquê (além do TCC):")
bul("A reatância de L<sub>1</sub> em 60 Hz é 377&#183;30,42 mH = 11,47 &#937;. Com "
    "2.887 A, a queda nela é cerca de 33,1 kV eficazes por fase.",
    "A tensão de fase da rede é 11,55 kV eficazes. Somando em quadratura, o inversor precisa "
    "sintetizar cerca de 35 kV eficazes, ou 49,6 kV de pico por fase.",
    "No PWM senoidal, o pico de fase máximo sem sobremodular é V<sub>cc</sub>/2. Com 90,91 kV, "
    "dá 45,5 kV: falta tensão e o PWM sobremodula. Com 136,36 kV, dá 68,2 kV: índice de "
    "modulação perto de 0,73, com folga.")
box("prova", "<b>&#8220;L<sub>1</sub> de 30 mH num sistema de 20 kV não é grande demais?&#8221;</b> "
    "É. Na base de 20 kV e 100 MVA (Z<sub>base</sub> = 4 &#937;), 11,47 &#937; são cerca de "
    "2,9 pu, quando o usual fica abaixo de 0,1 pu. Vem do critério de ondulação com uma "
    "ondulação admitida pequena (0,61%). Resposta segura: o filtro foi dimensionado pelo "
    "critério de ondulação de corrente e mantido igual em todos os cenários, então não "
    "interfere na comparação entre sintonias, que é o objeto do trabalho; a consequência foi "
    "exigir um barramento CC maior, para manter a margem de modulação. Otimizar o filtro "
    "fica fora do escopo.")
