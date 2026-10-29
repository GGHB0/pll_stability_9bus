# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
box("prova", "<b>&#8220;Por que o fator 3 no capacitor?&#8221;</b> Sem ele, a ressonância "
    "cairia na metade do chaveamento, onde ainda há conteúdo do PWM. Triplicando C, ela "
    "desce por &#8730;3 para 1.443 Hz, longe dos dois lados.")
box("alem", "O capacitor absorve reativo na fundamental: com X<sub>C</sub> = 1/(377&#183;42,47 "
    "&#956;F) = 62,5 &#937;, são cerca de 6,4 Mvar, 6,4% dos 100 MVA. Se a banca perguntar, "
    "é da ordem do limite usual de 5%.")
box("cuidado", "O TCC associa &#958; = 0,707 ao filtro; não está na tela deste slide (está no "
    "14). Se perguntarem, é o amortecimento adotado no projeto, o mesmo das malhas; não "
    "elabore.")
nums([["30,71 mH", "L<sub>est</sub> = L<sub>1</sub> + L<sub>2</sub> (TCC)"],
      ["9.068,99 rad/s", "&#969;<sub>res</sub> = &#960;f<sub>sw</sub>/&#8730;3 (TCC), 1.443 Hz"],
      ["0,5734 / 0,0054 / 3,1228 &#937;", "R<sub>d1</sub> / R<sub>d2</sub> / R<sub>d3</sub> (TCC)"],
      ["30,42 mH; 0,289 mH; 42,47 &#956;F", "L<sub>1</sub>; L<sub>2</sub>; C (modelo, apêndice)"],
      ["136,36 kV", "V<sub>cc</sub> do modelo, 1,5 &#215; 90,91 kV (apêndice)"]])
box("banca", "<b>Por que a ressonância fica no meio?</b> Longe da rede e do chaveamento; o "
    "amortecimento passivo atenua o pico de ressonância.")
box("banca", "<b>E o barramento CC?</b> Fixado em valor constante, para manter a margem de "
    "modulação necessária.")
ponte("com o filtro definido, a malha que faz a corrente seguir a referência.")

# --- 14
slide(14, "Controle de corrente", "Modelagem", "Bruno, Victor",
      "Fig. 3.1, §3.5 (Eqs. 3.21-3.23), §4.3.2 (Eq. 4.2)")
box("msg", "Um PI com notch em cada eixo faz a corrente do inversor seguir a referência.")
fala(14)
sub("Fundamento: a malha, eixo por eixo")
n.p("Erro (referência menos medida) &#8594; PI &#8594; filtro notch na ressonância do LCL "
    "&#8594; índice de modulação &#8594; PWM a 5 kHz no VSI de dois níveis. Em baixa "
    "frequência, o filtro se comporta como uma indutância só, L<sub>est</sub>:")
eq(r"G_i(s) = \frac{1}{s\,L_{est}}", tag="3.21")
eq(r"s^2 + \frac{K_p}{L_{est}}s + \frac{K_i}{L_{est}} = 0 \ \Rightarrow\ "
   r"K_p = 2\xi\omega_n L_{est},\ \ K_i = \omega_n^2 L_{est}",
   onde="Eqs. (3.22) e (3.23) do TCC: o polinômio característico e os ganhos que saem dele.")
n.p("É a mesma forma canônica do PLL. Com &#958; = 0,707 e &#969;<sub>n</sub> = "
    "4&#8730;2&#183;f<sub>g</sub> = 339,4 rad/s (TeseAGP):")
eq(r"K_p = 2\cdot\frac{1}{\sqrt{2}}\cdot4\sqrt{2}\,f_g\,L_{est} = 8 f_g L_{est}"
   r"\qquad K_i = (4\sqrt{2}\,f_g)^2 L_{est} = 32 f_g^2 L_{est}",
   onde="Pelo critério de 2%, a corrente acomoda em 4/(&#958;&#969;<sub>n</sub>) = 16,7 ms: "
        "um ciclo.")
sub("Fundamento: por que notch")
n.p("A ressonância do LCL (slide 13) é uma frequência em que o filtro amplifica em vez de "
    "atenuar. Se a malha de corrente excitar essa frequência, a corrente oscila. Além do "
    "amortecimento passivo, o notch é um filtro que corta uma faixa estreita em torno de "
    "&#969;<sub>res</sub> e deixa o resto passar.")
nums([["5 kHz", "chaveamento do PWM"],
      ["339,4 rad/s", "&#969;<sub>n</sub> = 4&#8730;2&#183;60 do PI de corrente"],
      ["30,71 mH", "L<sub>est</sub> = L<sub>1</sub> + L<sub>2</sub>"],
      ["9.068,99 rad/s", "ressonância do LCL, &#958; = 0,707"],
      ["14,74 / 3.537,8", "K<sub>p</sub> / K<sub>i</sub> de corrente (apêndice, fora do TCC)"]])
box("banca", "<b>Por que dois PIs?</b> O PI do PLL zera v<sub>q</sub> e entrega o ângulo; o "
    "PI de corrente faz i<sub>d</sub> e i<sub>q</sub> seguirem a referência. Cada um tem "
    "projeto próprio.")
box("cuidado", "Nunca confundir os dois: K<sub>p</sub> = 8f<sub>g</sub>L<sub>est</sub> é da "
    "corrente, não do PLL. Os ganhos de corrente aparecem escalados no modelo (de propósito; "
    "valores no apêndice). As bandas dos dois PIs são parecidas (339 e 325 rad/s); a "
    "interação entre eles está fora do escopo (defesa_qa.pdf, pergunta 4).")
ponte("no modelo final, a referência deixa de ser fixa.")

# --- 15
slide(15, "Submódulo 2.10 do ONS", "Modelagem", "Bruno", "Fig. 2.2, Fig. 4.2, §2.5.2, §4.3.2, §5.2")
box("msg", "No modelo final, a tensão medida define o reativo e o ativo fica com o que sobra.")
fala(15)
n.p("No modelo final, as referências fixas da primeira versão (slide 12) dão lugar ao bloco "
    "do Submódulo 2.10, que lê a tensão no PCC e conhece a corrente nominal e a máxima do "
    "conversor. Separação de papéis: o bloco do ONS decide o <b>módulo</b> de cada componente "
    "(i<sub>d,ref</sub> e i<sub>q,ref</sub>); o SRF-PLL decide a <b>direção</b> do eixo "
    "(&#952;<sub>PLL</sub>).")
sub("Fundamento: a rampa (Fig. 2.2)")
eq(r"i_q = \frac{0{,}85 - V}{0{,}35}\quad (0{,}5 \leq V < 0{,}85\ \mathrm{pu}) "
   r"\qquad i_q = 1\ \mathrm{pu}\quad (V < 0{,}5\ \mathrm{pu})",
   onde="Nula em 0,85 pu, igual à nominal em 0,5 pu. Entre 0,85 e 1,1 pu, banda morta "
        "(i<sub>q</sub> = 0, i<sub>d</sub> nominal); acima de 1,1 pu, absorve reativo. "
        "A lógica física é a do slide 3: corrente reativa injetada levanta a tensão "
        "(&#916;V &#8776; X&#183;i<sub>q</sub> em pu). Aqui i<sub>q</sub> é o módulo da "
        "injeção, como no ONS; no código e na Eq. (3.9) o sinal é o oposto "
        "(i<sub>q,ref</sub> = &#8722;2Q/3v<sub>d</sub>).")
sub("Fundamento: o círculo de corrente (exceção de método)")
eq(r"i_d^2 + i_q^2 \leq I_{max}^2 \ \Rightarrow\ i_d \leq \sqrt{I_{max}^2 - i_q^2}",
   onde="A corrente total é limitada pelos semicondutores. O reativo tem prioridade; o eixo "
        "d fica com o que sobra. Abaixo de 0,5 pu quase nada sobra, e a potência ativa cai "
        "durante a falta. Quando a falta é eliminada, a tensão volta à faixa normal, o "
        "reativo adicional zera e o ativo retorna ao patamar pré-falta.")
nums([["0,85 / 0,5 pu", "início da injeção reativa / saturação em 1 pu (Fig. 2.2); entre 0,85 e 1,1 pu, banda morta"]])
box("alem", "<b>O dilema que volta no capítulo 7 do painel.</b> Em pu, Q &#8776; "
    "V&#183;i<sub>q</sub>. Quanto mais a tensão cai, mais corrente reativa a regra pede, e "
    "menos potência reativa essa corrente consegue entregar.")
box("cuidado", "A sobretensão ficou fora do desenho de propósito: sobretensão e incremento "
    "de carga estão fora do escopo do trabalho inteiro.")
box("banca", "<b>Por que priorizar o reativo?</b> Sustenta a tensão sem exceder I<sub>max</sub>; "
    "eliminada a falta, o ativo retorna ao pré-falta.<br/>"
    "<b>Quem orienta as correntes?</b> O SRF-PLL. O bloco do ONS diz quanto de i<sub>d</sub> "
    "e i<sub>q</sub> injetar; o ângulo &#952;<sub>PLL</sub> diz em que direção.")
ponte("juntando todas as partes no sistema completo.")

# --- 16
slide(16, "Sistema completo", "Modelagem", "Bruno", "Fig. 4.2, §4.3.2")
box("msg", "Juntando as partes, este é o inversor usado em todas as simulações.")
fala(16)
sub("Revise em voz alta, de cima para baixo")
bul("<b>Sincronismo</b>: o SRF-PLL entrega &#952;<sub>PLL</sub> às transformações dq.",
    "<b>Referência pelo Submódulo 2.10</b>: antes fixas (P = 1 pu, Q = 0), i<sub>d,ref</sub> "
    "e i<sub>q,ref</sub> seguem a tensão V<sub>PCC</sub>.",
    "<b>Corrente e PWM</b>: os PIs em dq geram a modulação, e o LCL entrega a corrente à "
    "Barra 2.")
n.p("Uma forma de amarrar: são laços com velocidades parecidas, um dentro do outro. O PLL "
    "acomoda em cerca de 20 ms e a corrente em um ciclo (16,7 ms); o PWM chaveia a cada "
    "200 &#956;s. Se der para contar este slide sem olhar, a modelagem está estudada.")
box("banca", "<b>E agora?</b> Com o modelo fechado, as faltas no IEEE 9 barras testam o "
    "SRF-PLL.")
ponte("Passamos agora para o nosso método de teste, para ver como as contingências vão testar esse nosso SRF-PLL.")

# --- 17
slide(17, "Protocolo de contingência", "Método", "Bruno, Victor", "§4.3.4, Tab. 4.1, §5.2")
box("msg", "Todas as simulações seguem a mesma linha do tempo; muda só o local e o tipo da "
    "falta.")
sub("A linha do tempo")
tab(["Trecho", "Intervalo", "O que acontece"], [
    ["Inicialização", "0 a 0,1 s", "o modelo parte e o PLL trava; fora das métricas"],
    ["Pré-falta", "0,1 a 0,3 s", "regime, referência para as métricas em %"],
    ["Falta", "0,3 a 0,4 s", "100 ms = 6 ciclos de 60 Hz"],
    ["Pós-falta", "0,4 a 0,6 s", "200 ms de observação da recuperação"],
], [3.2, 3.0, 8.5])
sub("A matriz")
n.p("Analisadas, da mais próxima à mais distante da usina: Barra 7, Linha 7-8, Linha 8-9 e "
    "Barra 6 (em azul). Trifásica nos quatro; monofásica e bifásica nas Barras 7 e 6. "
    "Sintonia inadequada nas Barras 7 e 6 (os três tipos) e na Linha 7-8 (trifásica). "
    "Barras 4, 5, 8 e 9: simuladas, em cinza, consultáveis no painel. Regime sem falta nas "
    "duas sintonias.")
sub("Fundamento: os tipos de falta e as redes de sequência")
bul("<b>Trifásica</b>: simétrica; só a rede de sequência positiva participa. Afunda a "
    "tensão, sem sequência negativa.",
    "<b>Bifásica (fase-fase)</b>: as redes positiva e negativa ficam em paralelo no ponto "
    "da falta; ali, a tensão de sequência negativa iguala a positiva. É a que mais gera "
    "sequência negativa.",
    "<b>Monofásica (fase-terra)</b>: as três redes (positiva, negativa e zero) ficam em "
    "série; a de sequência zero divide a tensão, e a negativa sai menor que na bifásica.")
box("banca", "<b>Por que observar até 0,6 s?</b> São 200 ms após a eliminação; essa janela "
    "delimita o alcance das conclusões sobre a recuperação.")
box("cuidado", "Não diga quantos cenários: o slide também não diz (28 &#215; 29, "
    "defesa_qa.pdf). &#8220;Não retorna&#8221; significa &#8220;não retorna dentro da "
    "janela de 200 ms&#8221;. Os 0,1 s de inicialização são exceção de método.")
ponte("como os resultados foram extraídos.")

# --- 18
slide(18, "Fluxo de análise", "Método", "Bruno, Victor, Bruno", "§4.3.3; métricas em §5.1-5.3")
box("msg", "Cada simulação do Simulink vira arquivos CSV, tratados em Python até um painel "
    "interativo.")
n.p("Ao fim de cada simulação o Simulink exporta os sinais em duas taxas de amostragem; o "
    "Python alinha as duas num eixo de tempo comum e calcula os mesmos indicadores para "
    "todos os cenários. Nenhuma métrica é lida à mão no gráfico.")
sub("Ferramentas (cartões 3 e 4)")
n.p("No Python, o pandas trata os dados e o Plotly desenha os gráficos. O painel usa HTML, "
    "CSS e JavaScript, que não dominávamos: foi construído com um agente de inteligência "
    "artificial num modelo de harness. Nós definimos as regras, as ferramentas e as "
    "verificações; o agente programa dentro desses limites, e cada número do painel foi "
    "conferido contra a simulação.")
box("banca", "<b>Quem garante os números do painel?</b> O agente só escreveu o código. Os "
    "indicadores saem dos CSV do Simulink pelo mesmo cálculo para todos os cenários, e "
    "os valores do Cap. 5 do TCC foram conferidos contra a simulação.")
sub("As cinco métricas (saiba definir cada uma)")
tab(["Métrica", "Definição"], [
    ["Retenção de V<sub>d</sub>", "v<sub>d</sub> durante a falta em % do valor pré-falta"],
    ["Pico do erro de fase", "maior |&#916;&#952;| na falta, depois do 1º ciclo (o salto "
     "do 1º ciclo é descartado)"],
    ["Retorno à faixa de 2°", "tempo contado da eliminação até o erro entrar de vez em "
     "&#177;2°"],
    ["Componente de 120 Hz", "amplitude no espectro de v<sub>d</sub> durante a falta"],
    ["P e Q", "médias no intervalo da falta"],
], [4.4, 10.3])
sub("Fundamento: o espectro")
n.p("O espectro é a transformada de Fourier de v<sub>d</sub> na janela da falta. A "
    "resolução em frequência é o inverso da duração da janela:")
eq(r"\Delta f = \frac{1}{T} = \frac{1}{0{,}1\ \mathrm{s}} = 10\ \mathrm{Hz}",
   onde="Com 6 ciclos inteiros, 60 e 120 Hz caem exatamente em pontos do espectro, sem "
        "vazamento. Por isso o gráfico do capítulo 4 tem pontos a cada 10 Hz.")
nums([["9,2%", "retenção de V<sub>d</sub> na Barra 7, trifásica, nominal (exemplo da fala)"]])
box("banca", "<b>Dos dados aos resultados.</b> É assim que lemos os resultados: abrimos agora "
    "o painel interativo ao vivo, no modo apresentação.")
ponte("slide 19, abrir o painel.")

# =============================================================================
# PARTE II
# =============================================================================
parte("PARTE II · A passagem para o painel")
slide(19, "Demonstração ao vivo", "Porta para o painel", "Victor", "Figs. 5.10, 5.18")
box("msg", "A partir daqui os resultados são mostrados no painel interativo, no modo "
    "apresentação.")
sub("O que fazer")
