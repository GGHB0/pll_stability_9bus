# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
n.p("É a equação do slide 12 com &#916;&#952; girando. Com a corrente comandada no eixo d:")
eq(r"P = \frac{3}{2}V\,i_d\cos\Delta\theta",
   onde="Modelo qualitativo (despreza o i<sub>q</sub> do ONS e a variação de V): se "
        "&#916;&#952; varre todos os ângulos, cos&#916;&#952; troca de sinal e P oscila "
        "entre positivo e negativo, como no gráfico de baixo. O número a citar é o medido: "
        "66,8% do tempo absorvendo, média &#8722;0,40 pu. A malha de corrente não falhou; o "
        "referencial é que está girando, e o inversor vira uma carga oscilante.")
sub("Fundamento: por que só a combinação colapsa")
n.p("Pela fórmula do slide 7, com U &#8776; 0,09 pu na falta (&#8730;U &#8776; 0,3):")
tab(["Na falta (U &#8776; 0,09 pu)", "&#969;<sub>n,ef</sub>", "&#958;<sub>ef</sub>"], [
    ["Nominal", "&#8776; 98 rad/s", "&#8776; 0,21"],
    ["Inadequada", "&#8776; 44 rad/s", "&#8776; 0,09"],
], [6.7, 4.0, 4.0])
n.p("A inadequada atravessa a falta praticamente sem amortecimento. Nenhum fator isolado "
    "explica o colapso: a nominal na Barra 7 recupera (98 ms) e a inadequada na trifásica "
    "da Barra 6 também (106 ms). O colapso aparece na combinação de falta severa com "
    "sintonia inadequada, e ocorre também na Linha 7-8 (retenção de 9,7%).")
nums([["9,2% / 8,2%", "retenção de V<sub>d</sub>, nominal / inadequada"],
      ["98 ms / não retorna", "retorno à faixa de 2° (dentro dos 200 ms)"],
      ["66,8%", "tempo pós-falta absorvendo potência ativa, inadequada (média &#8722;0,40 pu)"]])
box("cuidado", "A tabela de &#969;<sub>n,ef</sub> é conta de bolso (além do TCC). Os cartões "
    "do palco também mostram 44,0° (pico da inadequada) e 5,6% (P absorvida da nominal); o "
    "número de fala é o 66,8%. <b>Reserva</b>: slides ocultos 26 e 28 (Figs. 5.18 a 5.21).")

# --- 7
cap(7, "Código de rede", "§5.5 · Figuras 2.1 e 2.2 · Tabela 5.2 · 5 passos",
    "07_ons_p4.png", "Passo 2 de 5: Barra 7 realçada, caixa &#8220;0,09 pu&#8221; no ponto "
    "saturado da rampa")
box("msg", "O inversor cumpre a letra do Submódulo 2.10 nas trifásicas, mas permanecer "
    "conectado não basta.")
sub("Os dois painéis")
n.p("Esquerda: tensão da fase mais afundada no inversor contra a curva de suportabilidade "
    "(Fig. 2.1). Direita: a rampa da Fig. 2.2 (slide 15), com o ponto de operação de cada "
    "caso (V médio, i<sub>q,ref</sub> médio).")
tab(["Curva de suportabilidade (Fig. 2.1)", "Limite"], [
    ["inferior, de 0 a 0,5 s", "0,2 pu: abaixo disso a desconexão é permitida"],
    ["inferior, de 0,5 a 1 s", "rampa de 0,2 a 0,85 pu"],
    ["superior, até 2,5 s", "1,2 pu"],
], [6.7, 8.0])
box("passo", "<b>1.</b> Só a regra: permanecer conectado e injetar reativo conforme o "
    "afundamento.",
    "<b>2.</b> Barra 7 e Linha 7-8 + o dilema: tensão abaixo de 0,2 pu, desconexão permitida, "
    "e mesmo assim conectado com i<sub>q</sub> saturado em 1 pu; mas com a tensão abaixo de 10%, "
    "a corrente máxima entrega só 0,09 pu de reativo.",
    "<b>3.</b> Mais longe, a injeção acompanha o afundamento: na Barra 6, i<sub>q,ref</sub> médio "
    "de 0,72 pu contra 0,76 pu da rampa, entregando muito mais reativo.",
    "<b>4.</b> Outros curtos acesos: nas assimétricas e na perda de sincronismo o inversor "
    "também fica conectado, mas a potência carrega 120 Hz ou se inverte e drena energia.",
    "<b>5.</b> Cartão de fecho: &#8220;O inversor permaneceu conectado?&#8221; Essa pergunta "
    "é insuficiente: é preciso acompanhar o rastreamento angular durante toda a contingência "
    "e na recuperação.")
tab(["Ponto", "V média (pu)", "i<sub>q</sub> pela rampa", "i<sub>q,ref</sub> média"], [
    ["Barra 7", "0,10", "1,00", "1,00"],
    ["Linha 7-8", "0,11", "1,00", "1,00"],
    ["Linha 8-9", "0,48", "1,00", "0,99"],
    ["Barra 6", "0,58", "0,76", "0,72"],
], [4.2, 3.5, 3.5, 3.5])
sub("Fundamento: o dilema do passo 2")
eq(r"Q \approx V\cdot i_q \approx 0{,}09 \cdot 1{,}0 \approx 0{,}09\ \mathrm{pu}",
   onde="V entre 0,09 e 0,10 pu (0,10 na tabela, arredondado). A corrente é a máxima, mas "
        "a tensão não está lá para virar potência. Cumprir a regra e saturar a corrente "
        "quase não ajuda a rede.")
imagem_palco("07_ons_p5.png", "Passo 5 de 5: cartão de fecho, a tese do trabalho em uma "
             "tela", alt=6.2)
box("cuidado", "&#8220;Fora da região&#8221; da B7 e da L7-8 é leitura aprovada como exceção "
    "(o TCC não diz isso com essas palavras). As simulações acabam 0,3 s depois do início da "
    "falta, então só o patamar de 0,2 pu da curva tem dado. <b>Reserva</b>: slide oculto 29.")

# --- 8
cap(8, "Todos os casos", "Tabelas 5.1 a 5.3", "08_sintese.png",
    "Tabela com os indicadores de todos os casos do TCC")
box("msg", "Não é para apresentar linha por linha: é o ponto de apoio para as perguntas.")
n.p("Cada linha tem a seção do TCC (§5.1 a §5.4), e clicar nela abre o cenário nas abas. As "
    "linhas &#8220;não retorna&#8221; são a Barra 7 e a Linha 7-8 trifásicas inadequadas. "
    "As Barras 4, 5, 8 e 9 não estão aqui, mas estão nas abas por cenário.")
n.p("<b>Volta ao PowerPoint:</b> Esc (sai da tela cheia) e Alt+Tab para o slide 20.")

# =============================================================================
# PARTE IV
# =============================================================================
parte("PARTE IV · De volta ao PowerPoint")
slide(20, "Síntese dos resultados", "Conclusão", "Bruno, Victor, Bruno, Victor", "Cap. 6")
box("msg", "O sincronismo do SRF-PLL é uma decisão de estabilidade do sistema elétrico.")
sub("Os três pontos de apoio à conclusão")
bul("<b>1. Faltas simétricas</b>: com a sintonia nominal, o SRF-PLL reconverge em todos os "
    "pontos; a severidade do afundamento depende diretamente da distância elétrica até a usina.",
    "<b>2. Faltas assimétricas</b>: a fragilidade é estrutural: a componente de sequência "
    "negativa introduz oscilação de 120 Hz que o PI não rejeita, contaminando as potências "
    "injetadas P e Q.",
    "<b>3. Sensibilidade de ganhos</b>: reduzir os ganhos atenua a falta, mas retarda o "
    "restabelecimento e leva ao escorregamento de ciclo na B7, fazendo o inversor drenar "
    "potência da rede.")
sub("Fundamento: por que &#8220;decisão de estabilidade&#8221;")
n.p("A classificação clássica de estabilidade (ângulo, frequência, tensão) foi pensada para "
    "máquinas síncronas. A classificação estendida (Hatziargyriou et al., 2020, relatório IEEE PES TR77) "
    "acrescenta a <b>estabilidade guiada por conversores</b>, causada pela interação entre o "
    "controle do conversor, como o PLL, e a rede. O que o TCC mostra cabe nela: a sintonia "
    "do PLL, que costuma ser tratada como detalhe do equipamento, decide se a usina sustenta "
    "ou drena a rede numa falta.")
box("banca", "<b>Qual é a conclusão central?</b> Permanecer conectado é insuficiente: a "
    "conformidade deve auditar o erro angular dinâmico durante a falta e em toda a "
    "recomposição.")
box("cuidado", "No slide 20, os três cartões destacam diretamente os três pontos conceituais "
    "de apoio à conclusão (sem números isolados no topo), pois todos os indicadores quantitativos "
    "acabaram de ser percorridos no painel interativo.")
ponte("o que fica para depois.")

slide(21, "Trabalhos futuros e encerramento", "Conclusão", "Victor, Bruno, Victor", "Cap. 7")
box("msg", "Dois eixos dão continuidade ao estudo, a partir dos limites deste trabalho.")
sub("Eixo 1: estruturas de sincronismo")
n.p("A fragilidade do capítulo 4 vem de o SRF-PLL misturar as duas sequências no mesmo "
    "v<sub>q</sub>. As alternativas separam antes do laço:")
bul("<b>DDSRF-PLL</b> (referencial síncrono duplo desacoplado): usa dois referenciais, um a "
    "+&#969; e outro a &#8722;&#969;, e uma rede de desacoplamento que tira de cada um a "
    "ondulação causada pelo outro. O PLL roda só sobre a sequência positiva.",
    "<b>DSOGI-PLL</b> (integrador generalizado de segunda ordem duplo): filtros SOGI geram "
    "versões em quadratura das tensões em &#945;&#946;, um cálculo de sequência positiva "
    "extrai só a positiva, e o SRF-PLL comum trabalha sobre ela.")
n.p("Nos dois casos, o 120 Hz deixa de entrar em v<sub>q</sub> sem precisar reduzir a banda: "
    "é a saída para o compromisso dos capítulos 5 e 6.")
sub("Eixo 2: força da rede e múltiplos inversores")
n.p("Varrer a impedância de Thévenin (SCR, slide 8) para mapear a fronteira de perda de "
    "sincronismo e substituir mais máquinas síncronas por conversores, para estudar a "
    "interação entre vários PLLs em rede fraca.")
sub("Limites (diga sem defensividade)")
n.p("IEEE 9 barras com nível de curto fixo, duas sintonias contrastantes, janela de 200 ms "
    "pós-falta: o trabalho identifica e explica um mecanismo, não um envelope universal de "
    "projeto.")
box("cuidado", "Eixos de salto de fase e RoCoF foram descartados: não proponha.")
ponte("agradecimento e abertura para perguntas, com o painel aberto.")

# =============================================================================
# PARTE V
# =============================================================================
parte("PARTE V · Conteúdo adicional",
      "O apêndice do deck (slides 22 e 23) e os slides ocultos (24 a 29) não fazem parte da "
      "apresentação. Servem de apoio quando a banca pergunta algo que pede número de "
      "parâmetro ou a tabela completa. Vale conhecê-los para saber que existem e onde estão.")

slide(22, "Parâmetros: rede, filtro LCL e controle", "Apêndice", "não tem fala",
      "Cap. 3 e 4")
box("msg", "Todos os parâmetros do modelo num slide: base do sistema, conversor, Thévenin, "
    "filtro LCL e ganhos das duas malhas.")
tab(["Quando a banca perguntar", "Onde está no slide"], [
    ["Tensão do barramento CC", "coluna 1: 136,36 kV (1,5 &#215; 90,91 kV do cálculo)"],
    ["Impedância de Thévenin", "coluna 1: R<sub>th</sub> = 10,04 m&#937;, L<sub>th</sub> = "
     "1,16 mH"],
    ["Passo de integração", "coluna 1: 5 &#956;s (elétrico) e 200 &#956;s (controle)"],
    ["L<sub>1</sub>, L<sub>2</sub>, C<sub>f</sub>, R<sub>d</sub>",
     "coluna 2: 30,42 mH, 0,289 mH, 42,47 &#956;F e as resistências de amortecimento"],
    ["Ganhos de corrente e do PLL", "coluna 3: 14,74 e 3.537,8 (corrente); 460 e 105.820; "
     "92 e 21.164"],
], [5.0, 9.7])
box("cuidado", "Vários desses valores não estão no TCC (são do modelo). Por que o "
    "V<sub>cc</sub> é 1,5 vezes o do cálculo: com o valor do cálculo, o PWM senoidal "
    "sobremodulava na escala de 100 MW.")

slide(23, "Tabelas 5.1, 5.2 e 5.3 completas", "Apêndice", "não tem fala", "Cap. 5")
box("msg", "As três tabelas do Cap. 5 num slide: trifásicas com o suporte do ONS e "
    "assimétricas nas duas sintonias.")
n.p("É a mesma informação do capítulo 8 do painel, em formato de slide. Use quando o painel "
    "não estiver à mão. O cartão de baixo resume por que o efeito da sintonia se inverte "
    "entre a Barra 6 (a inadequada filtra melhor) e a Barra 7 (a inadequada recupera "
    "devagar): é a história dos capítulos 5 e 6.")
box("cuidado", "O cartão da esquerda menciona um ganho efetivo &#8220;12 vezes&#8221; menor; "
    "prefira a explicação do capítulo 6 deste roteiro (&#969;<sub>n</sub> e &#958; caem com "
    "&#8730;U).")

n.h("Slides ocultos: a reserva do painel")
tab(["Slide", "Substitui o capítulo", "Conteúdo"], [
    ["24", "2 · Energização", "Fig. 5.3, 34/40 ms e 42/79 ms"],
    ["25", "3 · Localização", "Fig. 5.7 e Tabela 5.1"],
    ["26", "4 · Sequência negativa", "Figs. 5.10 e 5.18, 250&#215;, 98 ms"],
    ["27", "5 · Compromisso", "Fig. 5.14 e a parte assimétrica da Tabela 5.3"],
    ["28", "6 · Perda de sincronismo", "Figs. 5.20 e 5.21, 66,8%, média &#8722;0,40 pu"],
    ["29", "7 · Código de rede", "Fig. 2.2 e Tabela 5.2, 0,09 pu"],
], [1.6, 5.0, 8.1])
n.p("Se o navegador falhar, mostre esses slides na ordem da tabela (indo direto pelo número) "
    "e siga o mesmo roteiro da Parte III.")

n.h("Outros materiais")
