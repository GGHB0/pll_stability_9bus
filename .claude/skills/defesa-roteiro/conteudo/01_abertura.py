# Executado por exec() pelo pdf.py e pelo guia.py, nesta ordem: não importar.
# =============================================================================
# ABERTURA
# =============================================================================
n.h("Como usar este roteiro")
n.p("O roteiro segue a apresentação na ordem real, uma página (ou mais) por slide: os "
    "slides 1 a 18 no PowerPoint, o slide 19 como porta para o painel HTML, os oito "
    "capítulos do <b>modo apresentação</b> e a volta ao PowerPoint nos slides 20 e 21. O "
    "apêndice do deck e os slides ocultos ficam no fim, como <b>conteúdo adicional</b>. Não "
    "há texto de fala para decorar; na modelagem (slides 5 a 16), uma caixa <b>O que falar</b> "
    "dá os tópicos de cada um, na ordem e com quem fala.")
n.p("Cada página tem a miniatura e, embaixo, blocos sempre na mesma ordem:")
bul("<b>Mensagem</b>: a frase que o slide tem de deixar na cabeça da banca.",
    "<b>Fundamentos</b>: a teoria por trás, com as equações, para explicar com as próprias "
    "palavras e aguentar a pergunta seguinte. Quando a equação é do TCC, o número dela "
    "aparece à direita entre parênteses, como (3.18).",
    "<b>Números</b> para saber de cor, todos do TCC entregue (VFinal, 15/10/2026).",
    "<font color='#8A6D3B'><b>O que falar</b></font> (só na modelagem): o roteiro da fala "
    "em tópicos, logo abaixo da mensagem, para dizer com as próprias palavras.",
    "Caixas coloridas: <font color='#2F6FA8'><b>pergunta do rodapé</b></font> do slide, "
    "<font color='#6B4C9A'><b>pergunta provável</b></font> da banca, "
    "<font color='#C27C0E'><b>cuidado</b></font> e <font color='#3D8A57'><b>além do "
    "TCC</b></font> (conta ou leitura física que não está no texto: para entender e "
    "responder, não para dizer por iniciativa própria).",
    "<b>Próximo</b>: a ponte para o slide seguinte.")

n.h("O percurso")
tab(["Trecho", "Onde", "Conteúdo", "Fala"], [
    ["Abertura", "PPTX 1", "Capa, autores, orientadores", "Bruno"],
    ["Motivação", "PPTX 2-4", "Renováveis, blecautes, problema e objetivos", "Bruno"],
    ["Modelagem", "PPTX 5-16", "Inversor, Park, SRF-PLL, rede, sintonia, LCL, corrente, ONS",
     "alternada"],
    ["Método", "PPTX 17-18", "Protocolo de falta e fluxo de análise", "Bruno, Victor"],
    ["Porta", "PPTX 19", "Alt+Tab para o navegador, botão Modo apresentação", "Victor"],
    ["Resultados", "HTML 1-8", "Faltas destacadas ... Todos os casos (passador avança)",
     "a definir"],
    ["Conclusão", "PPTX 20-21", "Síntese e trabalhos futuros", "Bruno, Victor"],
    ["Adicional", "PPTX 22-29", "Apêndice e slides ocultos, para perguntas", "os dois"],
], [2.3, 2.6, 7.6, 2.2])

n.h("A história em cinco frases")
for i, f in enumerate([
        "A geração nova chega por inversores, e a rede perde a sustentação natural das "
        "máquinas síncronas; os blecautes de 2023 e 2025 passaram por esse elo.",
        "O inversor seguidor de rede só sabe onde está a tensão porque o SRF-PLL estima o "
        "ângulo dela, e a falta destrói justamente a tensão que o PLL mede.",
        "Com a sintonia nominal, o PLL atravessa as faltas trifásicas e volta ao sincronismo "
        "em todos os pontos, com severidade ditada pela distância elétrica.",
        "Nas faltas assimétricas, a sequência negativa vira 120 Hz no referencial dq, perto "
        "demais da banda do PI para ser filtrada; reduzir os ganhos filtra melhor, mas na "
        "falta mais severa faz o PLL perder o sincronismo e a usina absorver potência.",
        "Logo, ficar conectado, que é o que a verificação de hoje pergunta, não basta: é "
        "preciso olhar a qualidade do rastreamento angular durante e depois da falta."], 1):
    n.story.append(Paragraph(f, S_BUL, bulletText=f"{i}."))
n.gap(6)

n.h("Convenções que valem para tudo")
tab(["Use", "Evite", "Por quê"], [
    ["sintonia inadequada", "BAD_PLL, PLL ruim", "nome de código não vai para a banca"],
    ["escorregamento de ciclo", "cycle slipping", "é o termo do palco"],
    ["simulação computacional", "a sigla de transitórios eletromagnéticos",
     "o orientador não gostou; fora do deck e do TCC"],
    ["recuperar o sincronismo", "reaquisitar", "a palavra não existe"],
    ["azul = nominal, laranja = inadequada", "trocar as cores", "vale no deck e no painel"],
], [4.6, 4.2, 5.9])
n.note("Sem RoCoF (fora do escopo) e sem citar a contagem exata de cenários: o TCC tem 28 na "
       "Tabela 4.1 e usa 29 no Cap. 5 (defesa_qa.pdf, pergunta 1).")
