# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
n.p("Os reatores de barra, que poderiam segurar a tensão, eram manobrados à mão, e a subida "
    "levou cerca de um minuto, rápida demais para uma decisão humana. Em Portugal, ao "
    "contrário, as renováveis recebem em tempo real uma referência de tensão do operador.")
n.p("<b>O que é a oscilação forçada de 0,63 Hz.</b> Uma rede tem frequências próprias de "
    "oscilação (modos naturais), como uma corda tem suas notas. A de 0,63 Hz não era uma "
    "delas: não aparecia no modelo da rede nem nos meses anteriores. Ela era <b>imposta</b> "
    "por um equipamento que injetava potência oscilando. A ENTSO-E rastreou a fonte até uma "
    "usina inversorizada de grande porte na região de Badajoz, anterior ao código de rede "
    "europeu atual e operando com potência limitada. Quando a usina subiu a potência, a "
    "oscilação diminuiu. Ela ainda excitou o modo de 0,2 Hz entre áreas, que tinha "
    "amortecimento muito baixo. Por isso o relatório fala em <b>instabilidade guiada por "
    "conversor</b>: a malha de controle de um conversor foi a fonte.")
box("alem", "<b>Inércia teria salvado?</b> Não. A ENTSO-E testou: mesmo com inércia bem "
    "maior, a perda de sincronismo não teria sido evitada, porque a cascata derrubou o "
    "torque sincronizante rápido demais. Em simulação, mais margem de reativo teria evitado "
    "o colapso. A conclusão do painel é que o fenômeno central foi a falta de controle de "
    "tensão. Isso reforça o argumento do TCC: a sustentação da rede passou para o controle.")

sub("Chile em detalhe: uma proteção, duas ilhas, dois colapsos")
n.p("O sistema chileno é longo e estreito: cerca de 3.100 km de Arica a Chiloé, com o norte "
    "exportando para o centro-sul. No instante do evento, 1.800 MW (cerca de 90% da "
    "capacidade) passavam por uma única linha dupla de 500 kV, Nueva Maitencillo–Nueva Pan "
    "de Azúcar, e 73% da geração era solar e eólica.")
n.table(["Hora (local)", "O que aconteceu"], [
    ["13h35", "A transmissora desabilita a comunicação da proteção diferencial de um dos "
              "circuitos; a linha segue protegida pelas proteções de retaguarda"],
    ["15h13", "Reinicia o controlador de comunicações sem avisar nem pedir autorização ao "
              "operador (CEN)"],
    ["15h15–15h16", "Na ressincronização, a proteção dispara indevidamente os dois "
                    "circuitos de 500&#160;kV, risco previsto no manual do fabricante"],
    ["+1,5 s", "O 220 kV em paralelo fica sobrecarregado e abre: o país se divide em duas "
               "ilhas"],
    ["+4 s / +4 min", "A ilha centro-sul colapsa por frequência em segundos; a ilha norte "
                      "resiste cerca de 4 min e colapsa por tensão"],
], [3.3, 11.4])
n.gap(8)
n.p("<b>Por que a proteção disparou sozinha.</b> A proteção diferencial de linha compara a "
    "corrente que entra por uma ponta com a que sai pela outra. Em operação normal, a soma "
    "das correntes que entram pelas duas pontas é nula; numa falta dentro da linha, não é:")
eq(r"I_{dif} = |\,\bar I_A + \bar I_B\,| \approx 0 \quad \mathrm{(sem\ falta)}",
   onde="As duas pontas estão a centenas de quilômetros, e as amostras de corrente precisam "
        "estar alinhadas no tempo pela comunicação. Um desalinhamento de &#916;t gira uma "
        "corrente em relação à outra de &#969;&#916;t, e a diferença aparente cresce com a "
        "corrente: com 1.800 MW passando, um erro pequeno de sincronismo parece falta "
        "interna e a proteção abre.")
n.p("<b>Por que cada ilha caiu de um jeito.</b>")
bul("<b>Centro-sul</b> (70% da carga): ficou com déficit de cerca de 1.800 MW, uns 25% da "
    "demanda. Faltando potência, a energia sai da rotação das máquinas e a frequência cai. "
    "O corte automático de carga atuou, mas cerca de 230 MW não foram cortados como "
    "previsto; a frequência firmou em 48,5 Hz, voltou a cair e, ao passar de 47,5 Hz, mais "
    "geração saiu e veio o colapso.",
    "<b>Norte</b> (30% da carga): ficou com sobra de geração. O desligamento automático de "
    "geração segurou a ilha por cerca de 4 min, mas a tensão subiu: as renováveis não "
    "faziam controle dinâmico de reativo e um equipamento de compensação foi perdido. "
    "Linha longa com pouca carga ainda gera reativo pela própria capacitância (efeito "
    "Ferranti), o que empurra a tensão para cima.")
n.p("<b>Por que está no trabalho, se o gatilho foi humano.</b> O disparo foi erro de "
    "proteção, mas a ilha norte caiu pela mesma deficiência do Brasil (falta de suporte "
    "dinâmico de reativo das renováveis), e a resposta do operador foi uma das 14 medidas "
    "corretivas: publicar guia e proposta de norma para inversores <b>GFM e GFL</b>, para "
    "que as usinas renováveis prestem suporte à rede. O relatório do CEN também só registra "
    "se cada proteção atuou ou não; o comportamento interno do sincronismo dos inversores "
    "não aparece, e é esse comportamento que o TCC simula.")

sub("Os três eventos lado a lado")
tab(["", "Brasil 2023", "Ibéria 2025", "Chile 2025"], [
    ["Gatilho", "Proteção abre linha de 500 kV", "Subida de tensão",
     "Disparo indevido de proteção diferencial"],
    ["Problema de tensão", "Afundamento, colapso de tensão", "Sobretensão em cascata",
     "Sobretensão na ilha norte"],
    ["Papel dos inversores", "Suporte de reativo aquém dos modelos",
     "Fator de potência fixo; fonte da 0,63 Hz", "Sem controle dinâmico de reativo"],
    ["Resultado", "23.368 MW; quatro ilhas", "Espanha e Portugal inteiros",
     "11.066 MW; país inteiro"],
], [3.2, 3.8, 3.8, 3.9])
box("cuidado", "O TCC (§2.4.1 e §2.4.2) traz só o essencial: escala máxima, subida de "
    "tensão, cascata por sobretensão, 0,63 Hz guiada por conversor, fator de potência fixo, "
    "mais de 2,5 GW; e no Chile 11.066 MW, 73%, intervenção não autorizada na proteção "
    "diferencial, duas ilhas em 1,5 s, ilha norte por tensão, centro-sul por frequência, "
    "revisão de requisitos GFM/GFL. Horários, Badajoz, Granada, Portugal e o mecanismo "
    "detalhado vêm dos relatórios (ENTSO-E 2026, CEN 2025): use para responder, não na fala.",
    "Duas simplificações do slide que a banca pode notar: no Chile, o slide diz que o "
    "desligamento \"isolou o norte\", mas foram duas ilhas e a centro-sul caiu por "
    "frequência; e na Ibéria o problema foi sobretensão, não afundamento, embora o rodapé "
    "fale em falha \"no afundamento\". Se perguntarem: o elo comum é a resposta de tensão "
    "e de sincronismo do controle dos inversores durante o transitório.")
box("prova", "<b>O apagão ibérico foi falta de inércia?</b> Não: a ENTSO-E mostrou que mais "
    "inércia não evitaria a perda de sincronismo; faltou controle de tensão.",
    "<b>O que é instabilidade guiada por conversor?</b> Categoria da classificação "
    "estendida de estabilidade (Cap. 2): instabilidade causada pela interação das malhas "
    "de controle dos conversores, como o PLL e o controle de corrente, com a rede.",
    "<b>Se o Chile foi erro humano, por que citar?</b> Pelo modo como a perturbação se "
    "propagou (ilha norte por tensão) e pela resposta regulatória, que mirou o controle dos "
    "inversores (GFM e GFL).")
nums([["23.368 MW", "carga perdida no Brasil, 34,5% da nacional (§2.4.3)"],
      ["265 GW&#183;s", "inércia do SIN no evento: não faltou inércia"],
      ["> 2,5 GW; 0,63 Hz", "Ibéria: desconexão por sobretensão; oscilação antes do colapso"],
      ["11.066 MW; 73%", "Chile: carga perdida; participação solar e eólica"]])
box("banca", "<b>O que une os três eventos?</b> Perturbações ordinárias viraram blecautes "
    "porque o controle e o sincronismo dos inversores falharam no afundamento.")
box("cuidado", "A introdução do TCC traz 22.547 MW (31%) e a §2.4.3 traz 23.368 MW (34,5%). "
    "O deck usa 23.368 MW, do RAP do ONS (defesa_qa.pdf, pergunta 6).")
ponte("por que o sincronismo falha justamente no afundamento?")

# --- 4
slide(4, "Problema e objetivos", "Motivação", "Bruno", "Cap. 1")
box("msg", "O SRF-PLL depende de uma tensão limpa, justamente o que a falta na rede destrói.")
sub("Fundamento: os três estragos da falta na tensão medida")
bul("<b>Afundamento</b>: a amplitude cai. Como a amplitude multiplica o ganho do laço do "
    "PLL (slide 7), o laço fica mais lento e menos amortecido.",
    "<b>Salto de fase</b>: o ângulo da tensão muda de repente, e o PLL precisa correr atrás.",
    "<b>Assimetria</b>: a falta desequilibrada cria sequência negativa, que no referencial "
    "dq vira uma oscilação de 120 Hz em v<sub>q</sub>, e v<sub>q</sub> é exatamente o sinal "
    "de erro do PLL.")
sub("Fundamento: componentes simétricas (Fortescue)")
n.p("Qualquer conjunto trifásico desequilibrado se decompõe em três conjuntos "
    "equilibrados: sequência positiva (gira no sentido da rede), negativa (gira ao "
    "contrário) e zero (as três fases iguais). Uma falta trifásica só reduz a positiva; "
    "faltas mono e bifásicas criam negativa.")
eq(r"v_{abc} = v^{+} + v^{-} + v^{0}")
n.p("Vista por eixos que giram a +&#969;, a positiva fica parada e a negativa gira a "
    "&#8722;2&#969;. Por isso, com uma componente negativa de amplitude V<sup>&#8722;</sup>, "
    "aparece em dq uma parcela oscilando a 2&#969; = 120 Hz:")
eq(r"v_d = V^{+} + V^{-}\cos(2\omega t + \phi) \qquad v_q = -V^{-}\sin(2\omega t + \phi)",
   onde="Forma de Yazdani e Iravani (2010), §8.3.5; o sinal e a fase &#966; dependem da "
        "convenção. O PLL lê esse v<sub>q</sub> como se fosse erro de ângulo.")
sub("Cadeia causal da figura e objetivos")
n.p("Tensão degradada &#8594; erro de ângulo &#8594; correntes d e q orientadas no lugar "
    "errado &#8594; o desacoplamento entre P e Q se perde &#8594; o inversor não entrega o "
    "suporte de reativo que o Submódulo 2.10 pede. <b>Objetivo geral:</b> analisar a "
    "dinâmica, a sensibilidade à sintonia e a robustez do SRF-PLL de um inversor de 100 MW "
    "sob contingências no IEEE 9 barras. <b>Específicos:</b> modelar no Simulink, comparar "
    "sintonia nominal e inadequada sob faltas simétricas e assimétricas, verificar o suporte "
    "de subtensão (ONS).")
box("banca", "<b>Qual é a pergunta central?</b> Como a sintonia do PI do SRF-PLL define a "
    "fronteira entre manter o suporte de tensão e perder o sincronismo durante a falta?")
box("cuidado", "As notas falam em sobrecorrentes; o TCC conclui que elas não se manifestam "
    "(defesa_qa.pdf, pergunta 2). Não puxe o assunto.")
ponte("Passo agora a palavra ao Victor, que vai iniciar o bloco de modelagem.")

# --- 5
slide(5, "Fonte renovável", "Modelagem", "Victor", "Fig. 3.2, §3.2, §4.1, §4.3.1")
box("msg", "A usina fotovoltaica ou eólica se conecta à rede por um inversor seguidor de rede.")
fala(5)
sub("Fundamento: a cadeia da figura")
bul("<b>Fonte primária</b>: um barramento CC ideal (tensão constante).",
    "<b>Conversor</b>: VSI (inversor fonte de tensão) trifásico de dois níveis; as chaves "
    "ligam cada fase ao + ou ao &#8722; do barramento, e o PWM faz a média dessa tensão "
    "seguir a referência senoidal.",
    "<b>Filtro e PCC</b>: o filtro LCL tira o chaveamento da corrente; o PCC (ponto de "
    "acoplamento comum) é a Barra 2.",
    "<b>Controle</b>: mede a tensão no PCC, o SRF-PLL (em laranja) estima o ângulo e as "
    "malhas de corrente decidem o chaveamento.")
n.p("<b>Por que CC ideal, sem elo CC e sem MPPT?</b> Para isolar o fenômeno estudado. O "
    "elo CC e o rastreamento de máxima potência têm dinâmicas próprias que se misturariam "
    "ao sincronismo. Com a fonte ideal, tudo o que se vê na falta vem da rede CA, do PLL e "
    "da malha de corrente.")
box("banca", "<b>Como o inversor segue a rede?</b> O controle trabalha em dq, e o SRF-PLL "
    "rastreia o ângulo da tensão no PCC.")
ponte("&#8220;trabalha em dq&#8221; pede a transformada de Park.")

# --- 6
slide(6, "Transformada de Park", "Modelagem", "Victor", "Eqs. (3.4)-(3.7), §3.1.2")
box("msg", "Girando com a rede, a transformada de Park torna constantes as grandezas "
    "trifásicas.")
fala(6)
sub("Fundamento: a transformação")
n.p("As três fases são projetadas em dois eixos, d e q, que giram no ângulo &#952;. No TCC "
    "a transformação é invariante em amplitude (fator 2/3): a amplitude de fase reaparece "
    "inteira em dq.")
eq(r"v_d = \frac{2}{3}\left[v_a\cos\theta + v_b\cos\left(\theta-\frac{2\pi}{3}\right)"
   r" + v_c\cos\left(\theta+\frac{2\pi}{3}\right)\right]")
eq(r"v_q = -\frac{2}{3}\left[v_a\sin\theta + v_b\sin\left(\theta-\frac{2\pi}{3}\right)"
   r" + v_c\sin\left(\theta+\frac{2\pi}{3}\right)\right]",
   onde="Forma em cosseno; o TCC (Eqs. 3.5 a 3.7) pode usar outra convenção de seno, "
        "cosseno ou sinal. O resultado abaixo é o mesmo em qualquer uma.")
sub("Fundamento: as duas linhas embaixo da matriz")
n.p("A matriz é a transformação geral, com um &#952; qualquer. No inversor, quem fornece "
    "&#952; é o PLL, então &#952; = &#952;<sub>PLL</sub>. A rede tem o seu próprio ângulo, "
    "&#952;<sub>ref</sub>, que ninguém mede direto. A linha embaixo da matriz mostra o que "
    "sai da Park nessa situação. A conta tem três passos.")
n.p("<b>1. Tensões da rede.</b> Equilibradas, de amplitude de fase V<sub>m</sub>, como no "
    "TCC (§3.4, logo antes da Equação 3.10):")
eq(r"v_a = V_m\cos\theta_{ref},\quad v_b = V_m\cos(\theta_{ref} - 2\pi/3),\quad "
   r"v_c = V_m\cos(\theta_{ref} + 2\pi/3)")
