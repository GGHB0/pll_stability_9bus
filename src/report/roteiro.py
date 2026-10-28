"""
roteiro.py — Casos analisados no Cap. 5 do TCC e capítulos da aba Análise TCC.

O painel tem mais cenários do que o TCC discute (Barras 4, 5, 8 e 9, Linha 8-9
bifásica). TCC_CASOS diz em que seção do Cap. 5 cada caso aparece, na ordem
das Tabelas 5.1 a 5.3; o resto vai para o grupo "fora do TCC" do seletor e
fica esmaecido no mapa unifilar. CAPITULOS organiza a aba "Análise TCC"
(demonstração ao vivo da defesa): cada capítulo sobrepõe os
cenários que o TCC compara, com legenda e mini-cartões.

Os números das legendas são os do TCC (VFinal, Tabelas 5.1 a 5.3, §5.1 e
§5.4) e batem com os cards do painel, que saem de pipeline/indicadores.py.
"""

# (id, rótulo do grupo no seletor) — ordem do Cap. 5
TCC_SECOES = (
    ("5.1", "§5.1 Regime permanente"),
    ("5.2", "§5.2 Faltas simétricas"),
    ("5.3", "§5.3 Faltas assimétricas"),
    ("5.4", "§5.4 Perda de sincronismo"),
)
OUTROS_LABEL = "Outros cenários (fora do TCC)"

# caso → seção do Cap. 5. A ordem dentro de cada seção é a das tabelas.
# As trifásicas com sintonia inadequada da Linha 7-8 e da Barra 6 aparecem
# no texto como contraste da Barra 7 (9,7% de retenção, 106 ms) e ficam
# junto dela na §5.4.
TCC_CASOS: dict[str, str] = {
    "regime":                     "5.1",
    "regime_bad_pll":             "5.1",
    "bus7/3phase":                "5.2",
    "line7_8/3phase":             "5.2",
    "line8_9/3phase":             "5.2",
    "bus6/3phase":                "5.2",
    "bus7/2phase":                "5.3",
    "bus7/2phase_bad_pll":        "5.3",
    "bus7/1phase":                "5.3",
    "bus7/1phase_bad_pll":        "5.3",
    "bus6/2phase":                "5.3",
    "bus6/2phase_bad_pll":        "5.3",
    "bus6/1phase":                "5.3",
    "bus6/1phase_ground_bad_pll": "5.3",
    "bus7/3phase_bad_pll":        "5.4",
    "line7_8/3phase_bad_pll":     "5.4",
    "bus6/3phase_bad_pll":        "5.4",
}

# Cores (light, dark). Azul = sintonia nominal, laranja = inadequada, como no
# deck. Nos capítulos só com casos nominais (localização, ONS), escala
# amarelo → verde → ciano → índigo, do mais perto ao mais longe da usina: os
# tons de azul não se distinguiam no fundo escuro da apresentação. As
# assimétricas têm paleta própria (_ASSIM, abaixo).
_NOM = ("#2563eb", "#60a5fa")
_BAD = ("#ea580c", "#fb923c")
_LOC = (("#ca8a04", "#fde047"), ("#16a34a", "#4ade80"),
        ("#0891b2", "#22d3ee"), ("#4f46e5", "#a5b4fc"))
_REF = ("#94a3b8", "#64748b")
# Assimétricas: a cor diz a barra (laranja = Barra 7, verde-azulado = Barra
# 6, longe do azul nominal e do laranja forte da inadequada), o traço diz o
# curto (contínuo = bifásica, tracejado = monofásica) e a trifásica de
# referência vai grafite e grossa por cima, senão some colada no zero.
_B7 = dict(grupo="Barra 7")
_B6 = dict(grupo="Barra 6")
_ASSIM = {
    "bus7/3phase": (("#1f2937", "#e5e7eb"), dict(_B7, larg=4.5, frente=True)),
    "bus7/2phase": (("#b45309", "#fb923c"), _B7),
    "bus7/1phase": (("#f59e0b", "#fcd34d"), dict(_B7, dash="dash")),
    "bus6/3phase": (("#1f2937", "#e5e7eb"), _B6),
    "bus6/2phase": (("#0f766e", "#2dd4bf"), _B6),
    "bus6/1phase": (("#2dd4bf", "#99f6e4"), dict(_B6, dash="dash")),
}
# Sequência negativa: os passos no tempo comparam só as duas da Barra 6
# (trifásica × bifásica); v_abc do inversor vai embutido só para elas.
ABC_CASOS = ("bus6/3phase", "bus6/2phase")
_SO_B6 = ["bus7/3phase", "bus7/2phase", "bus7/1phase", "bus6/1phase"]

# Capítulos da aba "Análise TCC" (demonstração ao vivo da defesa).
# Campos: id, curto (botão), titulo, ref (seção/figura do TCC), texto,
# kind (time/spec/ons/tabela), casos [(key, cor) ou (key, cor, estilo), com
# estilo opcional: dash, larg, grupo (rótulo antes dos chips, respiro entre
# os cartões) e frente (curva por cima)], sinais (o 1º é o
# padrão), pres (sinais empilhados no modo apresentação), xrange,
# metricas (chaves de tccInd nos mini-cartões). O kind "mapa" não tem
# gráfico: desenha o unifilar e percorre passos (seta → antes de trocar de
# capítulo), cada um com id do ponto, rotulo e pos na régua (∝ tensão residual
# na Barra 2, ver kb ieee9bus-thevenin), cenario aberto pelo botão, faltas e
# inadequada (cobertura conforme kb cenarios-simulados).
# Só no modo apresentação (palco): passos_pres troca a legenda por uma frase
# por passo (texto, ocultar = casos escondidos naquele passo, lado opcional
# que troca o painel ao lado naquele passo, foco = [t0, t1] que esmaece o
# gráfico fora da janela, destaque=True mostra o número de destaque do
# capítulo, que nos capítulos com passos só aparece nesses), lado põe um
# painel ao lado do gráfico ("fasor" ou "minimapa") e destaque escreve um
# número grande sobre o gráfico (sinal, num, txt, x/y do alvo, ax/ay da
# caixa; sem x, a caixa fica solta em ax/ay; lado=True põe o número no
# painel ao lado); notas põe caixas menores com seta (sinal, txt, x/y do
# alvo, ax/ay da caixa, cor opcional). Números só os da legenda e dos
# cartões. matriz troca os cartões por uma tabela linhas × colunas (chave =
# prefixo da linha + "/" + sufixo da coluna, realce = coluna sombreada,
# rotulos = nome curto das métricas, nota = rodapé). faixa_err fixa o eixo
# do erro de fase (palco e aba) para a faixa de 2° aparecer.
# No kind "ons", o passo aceita realce = casos em cena (os outros esmaecem)
# e outros=True (acende os demais curtos), e o destaque aponta o ponto do
# caso (key) no painel da rampa. cartoes_pres=False tira os cartões do palco.
# fecho = {pergunta, resposta} vela o gráfico e põe a conclusão num cartão
# grande (último passo do capítulo, a tese do trabalho em uma tela).
CAPITULOS: list[dict] = [
    dict(id="faltas", pres=[], curto="Faltas destacadas", kind="mapa",
         titulo="Faltas destacadas", ref="Antes dos resultados",
         texto="Quatro pontos de falta, do mais próximo ao mais distante da "
               "usina fotovoltaica.",
         casos=[], sinais=[], xrange=None, metricas=[],
         passos=[
             dict(titulo="Quatro pontos, uma pergunta", tag="Visão geral",
                  texto=["Outros pontos da rede também receberam falta, mas a "
                         "análise se concentra em quatro deles: duas barras "
                         "(7 e 6) e duas linhas (7-8 e 8-9).",
                         "Cada um tem uma particularidade. Juntos, vão do "
                         "afundamento mais profundo ao mais raso e incluem uma "
                         "linha de circuito simples e outra de circuito duplo."],
                  papel="<b>Pergunta:</b> como a distância da falta muda a "
                        "resposta do SRF-PLL?"),
             dict(id="b7", rotulo="B7", pos=0.03, cenario="bus7/3phase",
                  titulo="Barra 7", tag="Mais próxima da usina", tom="near",
                  texto=["Fica logo depois do transformador T2, que liga a "
                         "usina à rede. Entre o inversor e a falta, só há "
                         "esse transformador.",
                         "É o caso mais severo: o afundamento de tensão no "
                         "ponto de conexão é o mais profundo."],
                  papel="<b>No estudo:</b> o extremo severo, ponto de partida "
                        "da análise de perda de sincronismo.",
                  faltas=["trifásica", "bifásica", "monofásica"], inadequada=True),
             dict(id="l78", rotulo="L7-8", pos=0.19, cenario="line7_8/3phase",
                  titulo="Linha 7-8", tag="Circuito simples", tom="mid",
                  texto=["Sai da Barra 7 em direção ao centro da rede. A falta "
                         "é aplicada na própria linha.",
                         "Como não há circuito paralelo, a linha inteira fica "
                         "sob falta, e o ponto continua eletricamente perto "
                         "da usina."],
                  papel="<b>No estudo:</b> falta em linha próxima à usina, "
                        "comparada à Barra 7.",
                  faltas=["trifásica"], inadequada=True),
             dict(id="l89", rotulo="L8-9", pos=0.66, cenario="line8_9/3phase",
                  titulo="Linha 8-9", tag="Circuito duplo", tom="mid",
                  texto=["Dois circuitos em paralelo ligam as Barras 8 e 9. A "
                         "falta é aplicada em apenas um deles.",
                         "O outro circuito continua conduzindo, e as duas "
                         "barras seguem ligadas durante a falta."],
                  papel="<b>No estudo:</b> falta em linha com um caminho "
                        "alternativo preservado.",
                  faltas=["trifásica"], inadequada=False),
             dict(id="b6", rotulo="B6", pos=0.97, cenario="bus6/3phase",
                  titulo="Barra 6", tag="Mais distante da usina", tom="far",
                  texto=["Fica no ramo inferior da rede, entre as Barras 4 e "
                         "9. Qualquer caminho da usina até ela passa por "
                         "três linhas.",
                         "É o caso mais brando: parte da tensão se mantém no "
                         "ponto de conexão do inversor."],
                  papel="<b>No estudo:</b> o extremo brando, o contraponto da "
                        "Barra 7.",
                  faltas=["trifásica", "bifásica", "monofásica"], inadequada=True),
             dict(titulo="Faltas destacadas", tag="Resumo", resumo=True,
                  texto=["Da mais próxima à mais distante da usina: Barra 7, "
                         "Linha 7-8, Linha 8-9 e Barra 6.",
                         "Os quatro pontos recebem falta trifásica. Nas Barras "
                         "7 e 6 também há faltas monofásica e bifásica, que "
                         "entram no capítulo de sequência negativa."],
                  papel="<b>Daqui em diante:</b> os capítulos comparam estes "
                        "casos, nas duas sintonias do PLL."),
         ]),
    dict(id="energ", pres=["err", "vd"], curto="Energização", kind="time",
         titulo="Energização do inversor", ref="§5.1 · Figura 5.3",
         texto="Na partida, o SRF-PLL trava na rede: o erro de fase entra na "
               "faixa de 2° em 40 ms com a sintonia nominal e em 79 ms com a "
               "inadequada.",
         casos=[("regime", _NOM), ("regime_bad_pll", _BAD)],
         sinais=["err", "vd"], xrange=[0.0, 0.2], metricas=["terr2", "tvd5"],
         lado="fasor",
         passos_pres=[
             dict(texto="Com a sintonia nominal, o erro de fase entra na faixa "
                        f"de 2° em <b style='color:{_NOM[0]}'>40 ms</b>.",
                  ocultar=["regime_bad_pll"], foco=[0.0, 0.06]),
             dict(texto="Com a sintonia inadequada, leva "
                        f"<b style='color:{_BAD[0]}'>79 ms</b>: quase o dobro.",
                  ocultar=[]),
         ]),
    dict(id="local", pres=["err", "vd"], curto="Localização", kind="time",
         titulo="Falta trifásica: quanto mais perto, mais severa",
         ref="§5.2 · Tabela 5.1 · Figura 5.7",
         texto="A mesma falta em quatro pontos, do mais próximo ao mais "
               "distante da usina. A retenção de v<sub>d</sub> vai de 9,2% (Barra 7) a "
               "58,4% (Barra 6), e com a sintonia nominal o erro sempre volta "
               "à faixa de 2°, em até 112 ms.",
         casos=[("bus7/3phase", _LOC[0]), ("line7_8/3phase", _LOC[1]),
                ("line8_9/3phase", _LOC[2]), ("bus6/3phase", _LOC[3])],
         sinais=["err", "vd", "P"], xrange=[0.25, 0.6],
         metricas=["ret", "pico", "ts"], lado="minimapa", faixa_err=[-60, 60],
         passos_pres=[
             dict(texto="Quanto mais perto da usina, menos tensão sobra: "
                        "v<sub>d</sub> retém <b>9,2%</b> na Barra 7 e "
                        "<b>58,4%</b> na Barra 6.",
                  ocultar=[], lado="minimapa", foco=[0.3, 0.4]),
             dict(texto="O erro de fase também cresce: pico de "
                        "<b>37,3°</b> na Barra 7 e <b>7,3°</b> na Barra 6.",
                  ocultar=[], lado="fasor", foco=[0.3, 0.4]),
             dict(texto="Com a sintonia nominal, o erro sempre volta à faixa "
                        "de 2°: em até <b>112 ms</b>.",
                  ocultar=[], lado="fasor"),
         ]),
    dict(id="seqneg", pres=["spec"], curto="Sequência negativa", kind="spec",
         titulo="Faltas assimétricas: de onde vem o 120 Hz",
         ref="§5.3 · Tabela 5.3 · Figura 5.10",
         texto="Nas faltas assimétricas, a sequência negativa aparece em v<sub>d</sub> "
               "como uma oscilação de 120 Hz, de 0,29 a 0,72 pu: mais de 250 "
               "vezes o maior valor das trifásicas (0,0011 pu). O gráfico é o "
               "espectro de v<sub>d</sub> do inversor durante a falta; a matriz "
               "traz os valores da Tabela 5.3.",
         casos=[(k, *_ASSIM[k]) for k in ("bus7/3phase", "bus7/2phase", "bus7/1phase",
                                          "bus6/3phase", "bus6/2phase", "bus6/1phase")],
         sinais=["spec"], xrange=[0.0, 400.0], metricas=["a120", "pico"],
         destaque=dict(sinal="spec", num="&gt; 250×", x=122, y=0.29, ax=200, ay=0.55,
                       txt="a menor assimétrica contra<br>as trifásicas"),
         notas=[dict(sinal="spec", x=121, y=0.004, ax=180, ay=0.24,
                     txt="<b>Barra 7 trifásica</b><br>0,0002 pu")],
         matriz=dict(linhas=[["Barra 7", "bus7"], ["Barra 6", "bus6"]],
                     colunas=[["Trifásica", "3phase"], ["Bifásica", "2phase"],
                              ["Monofásica", "1phase"]],
                     realce=0, rotulos={"pico": "pico do erro"},
                     nota="Amplitude de 120 Hz em v<sub>d</sub> durante a falta e "
                          "pico do erro de fase. As duas trifásicas ficam no zero, "
                          "uma sobre a outra."),
         # passos no tempo na Barra 6 (a bifásica é o caso do Compromisso) e,
         # por último, o espectro com todas as assimétricas e a matriz
         passos_pres=[
             dict(texto="Na trifásica, as três fases caem por igual. Na "
                        "bifásica, ficam <b>desequilibradas</b>.",
                  sinais=["abc"], xrange=[0.28, 0.36], ocultar=_SO_B6,
                  cartoes=False),
             dict(texto="O desequilíbrio é a soma de duas sequências. O PLL gira "
                        "junto com a <b>positiva</b>. A <b>negativa</b> gira ao "
                        "contrário e, vista do PLL, dá a volta a <b>120 Hz</b>.",
                  sinais=["abc"], xrange=[0.28, 0.36], ocultar=_SO_B6,
                  cartoes=False, lado="seq"),
             dict(texto="Em dq, a positiva vira um valor constante e a negativa, "
                        "uma oscilação de 120 Hz: v<sub>d</sub> e v<sub>q</sub> "
                        "oscilam só na bifásica.",
                  sinais=["vdi", "vqi"], xrange=[0.25, 0.6], foco=[0.3, 0.4],
                  ocultar=_SO_B6, cartoes=False, lado="seq"),
             dict(texto="v<sub>q</sub> é a entrada do PI do PLL, que lê a oscilação "
                        "como erro de fase: pico de <b>7,3°</b> na trifásica e "
                        "<b>96,0°</b> na bifásica.",
                  sinais=["vqi", "err"], xrange=[0.25, 0.6], foco=[0.3, 0.4],
                  ocultar=_SO_B6, cartoes=False),
             dict(texto="No espectro de v<sub>d</sub>, o 120 Hz das assimétricas "
                        "vai de <b>0,29</b> a <b>0,72 pu</b>: mais de 250 vezes "
                        "o das trifásicas.",
                  ocultar=[], destaque=True),
         ]),
    dict(id="comp", pres=["err", "vd"], curto="Compromisso da sintonia", kind="time",
         titulo="Ganho menor filtra melhor o 120 Hz",
         ref="§5.3 · Tabela 5.3 · Figura 5.14",
         texto="Na falta bifásica da Barra 6, a sintonia inadequada filtra "
               "mais o 120 Hz: o pico na falta cai de 96,0° para 34,5° e o "
               "retorno de 48 para 30 ms. Mas, na trifásica da Barra 7, a "
               "mesma sintonia perde o sincronismo.",
         casos=[("bus6/2phase", _NOM), ("bus6/2phase_bad_pll", _BAD)],
         sinais=["err", "vd"], xrange=[0.25, 0.6],
         metricas=["pico", "ts", "a120"],
         passos_pres=[
             dict(texto="Com a sintonia nominal, o 120 Hz da falta passa para o erro de "
                        f"fase: pico de <b style='color:{_NOM[0]}'>96,0°</b>.",
                  ocultar=["bus6/2phase_bad_pll"], foco=[0.3, 0.4]),
             dict(texto="Com a inadequada, o 120 Hz em v<sub>d</sub> é quase o "
                        "mesmo (0,39 e 0,37 pu), mas o erro fica em "
                        f"<b style='color:{_BAD[0]}'>34,5°</b> e volta em "
                        f"<b style='color:{_BAD[0]}'>30 ms</b>.",
                  ocultar=[], foco=[0.3, 0.46]),
             dict(texto="Aqui, o ganho menor parece vantagem. <b>E numa falta "
                        "mais severa?</b>",
                  ocultar=[]),
         ]),
    dict(id="sinc", pres=["err", "P"], curto="Perda de sincronismo", kind="time",
         titulo="Barra 7 trifásica: a sintonia decide o sincronismo",
         ref="§5.4 · Figuras 5.18 e 5.19",
         texto="A tensão v<sub>d</sub> retém quase o mesmo nas duas sintonias (9,2% e 8,2%). "
               "Com a nominal, o erro volta à faixa de 2° em 98 ms; com a "
               "inadequada, percorre toda a faixa de ±180° até o fim da "
               "simulação.",
         casos=[("bus7/3phase", _NOM), ("bus7/3phase_bad_pll", _BAD)],
         sinais=["err", "P", "Q", "vd"], xrange=[0.25, 0.6],
         metricas=["ret", "pico", "ts"], lado="fasor",
         passos_pres=[
             dict(texto="O caso mais severo: com a sintonia nominal, o erro volta à "
                        f"faixa de 2° em <b style='color:{_NOM[0]}'>98 ms</b>.",
                  ocultar=["bus7/3phase_bad_pll"], foco=[0.4, 0.5]),
             dict(texto="A tensão v<sub>d</sub> retém quase o mesmo (9,2% e 8,2%), mas, com "
                        "a inadequada, o erro percorre toda a faixa de ±180° "
                        "(escorregamento de ciclo): "
                        f"<b style='color:{_BAD[0]}'>perde o sincronismo</b>.",
                  ocultar=[], foco=[0.4, 0.6]),
             dict(texto="O ganho que filtrava o 120 Hz na Barra 6 é o que perde "
                        "o sincronismo aqui.",
                  ocultar=[]),
         ]),
    dict(id="ons", pres=[], curto="Código de rede", kind="ons",
         titulo="Código de rede: permanência e corrente reativa",
         ref="§5.5 · Figuras 2.1 e 2.2 · Tabela 5.2",
         texto="O Submódulo 2.10 pede duas coisas durante a falta: permanecer "
               "conectado enquanto a tensão estiver dentro da região de "
               "suportabilidade e injetar corrente reativa proporcional ao "
               "afundamento. A Barra 7 e a Linha 7-8 levam a tensão abaixo de "
               "0,2 pu, onde a desconexão é permitida, e mesmo assim o inversor "
               "fica conectado com i<sub>q</sub> saturado em 1 pu. A Barra 6 fica "
               "dentro da região, com i<sub>q,ref</sub> médio de 0,72 pu contra "
               "0,76 pu da rampa.",
         casos=[("bus7/3phase", _LOC[0]), ("line7_8/3phase", _LOC[1]),
                ("line8_9/3phase", _LOC[2]), ("bus6/3phase", _LOC[3])],
         sinais=[], xrange=None, metricas=["Vmed", "rampa", "iqref"],
         cartoes_pres=False,
         destaque=dict(key="bus7/3phase", num="0,09 pu",
                       txt="de potência reativa na Barra 7,<br>"
                           "com i<sub>q</sub> saturado em 1 pu"),
         passos_pres=[
             dict(texto="O Submódulo 2.10 pede duas coisas durante a falta: "
                        "<b>permanecer conectado</b> e <b>injetar corrente "
                        "reativa</b> conforme o afundamento.",
                  ocultar=["bus7/3phase", "line7_8/3phase", "line8_9/3phase",
                           "bus6/3phase"]),
             dict(texto="A Barra 7 e a Linha 7-8 levam a tensão abaixo de "
                        "0,2 pu, onde a desconexão é permitida. O inversor "
                        "fica conectado com i<sub>q</sub> saturado em "
                        "<b>1 pu</b>, mas, com a tensão retida abaixo de 10% "
                        "do valor pré-falta, entrega só <b>0,09 pu</b> de "
                        "reativo.",
                  ocultar=["line8_9/3phase", "bus6/3phase"], destaque=True),
             dict(texto="Mais longe, a injeção acompanha o afundamento: na "
                        "Barra 6, i<sub>q,ref</sub> médio de <b>0,72 pu</b> "
                        "contra 0,76 pu da rampa. Com mais tensão, a área "
                        "V · i<sub>q</sub>, o reativo entregue, fica bem maior.",
                  ocultar=[]),
             dict(texto="Nas assimétricas e na perda de sincronismo, o "
                        "inversor também permanece conectado, mas a potência "
                        "carrega o 120 Hz ou se inverte e drena energia do "
                        "sistema.",
                  ocultar=[], outros=True),
             dict(texto="A permanência conectada não é suficiente para "
                        "caracterizar conformidade.",
                  ocultar=[], outros=True,
                  fecho=dict(
                      pergunta="O inversor permaneceu conectado?",
                      resposta="Essa pergunta é insuficiente: é preciso "
                               "acompanhar a qualidade do rastreamento angular "
                               "ao longo de toda a contingência e na "
                               "recuperação.")),
         ]),
    dict(id="sintese", pres=[], curto="Todos os casos", kind="tabela",
         titulo="Todos os casos do TCC",
         ref="Tabelas 5.1 a 5.3",
         texto="Indicadores de todos os cenários analisados, nas duas "
               "sintonias. Clique numa linha para abrir o cenário nas abas.",
         casos=[], sinais=[], xrange=None, metricas=[]),
]


def tcc_secao(key: str) -> str | None:
    """Seção do Cap. 5 em que o caso aparece, ou None se o TCC não o usa."""
    return TCC_CASOS.get(key)
