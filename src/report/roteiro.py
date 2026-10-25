"""
roteiro.py — Casos analisados no Cap. 5 do TCC e capítulos da aba Análise TCC.

O painel tem mais cenários do que o TCC discute (Barras 4, 5, 8 e 9, Linha 8-9
bifásica). TCC_CASOS diz em que seção do Cap. 5 cada caso aparece, na ordem
das Tabelas 5.1 a 5.3; o resto vai para o grupo "fora do TCC" do seletor e
fica esmaecido no mapa unifilar. CAPITULOS organiza a aba "Análise TCC"
(demonstração da defesa, slide 16 do deck): cada capítulo sobrepõe os
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
    "bus6/2phase": (("#0f766e", "#2dd4bf"), _B6),
    "bus6/1phase": (("#2dd4bf", "#99f6e4"), dict(_B6, dash="dash")),
}

# Capítulos da aba "Análise TCC" (demonstração da defesa, slide 16 do deck).
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
# que troca o painel ao lado naquele passo), lado põe um
# painel ao lado do gráfico ("fasor" ou "minimapa") e destaque escreve um
# número grande sobre o gráfico (sinal, num, txt, x/y do alvo, ax/ay da
# caixa; sem x, a caixa fica solta em ax/ay; lado=True põe o número no
# painel ao lado); notas põe caixas menores com seta (sinal, txt, x/y do
# alvo, ax/ay da caixa, cor opcional). Números só os da legenda e dos
# cartões. faixa_err fixa o eixo do erro de fase (palco e aba) para a faixa
# de 2° aparecer.
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
                  ocultar=["regime_bad_pll"]),
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
                  ocultar=[], lado="minimapa"),
             dict(texto="O PLL também se desvia mais: pico do erro de "
                        "<b>37,3°</b> na Barra 7 e <b>7,3°</b> na Barra 6.",
                  ocultar=[], lado="fasor"),
         ]),
    dict(id="sinc", pres=["err", "P"], curto="Perda de sincronismo", kind="time",
         titulo="Barra 7 trifásica: a sintonia decide o sincronismo",
         ref="§5.4 · Figuras 5.18 e 5.19",
         texto="A tensão cai quase igual nas duas sintonias (9,2% e 8,2%). "
               "Com a nominal, o erro volta à faixa de 2° em 98 ms; com a "
               "inadequada, percorre toda a faixa de ±180° até o fim da "
               "simulação, e a usina absorve potência ativa em 66,8% do "
               "tempo após a eliminação.",
         casos=[("bus7/3phase", _NOM), ("bus7/3phase_bad_pll", _BAD)],
         sinais=["err", "P", "Q", "vd"], xrange=[0.25, 0.6],
         metricas=["ret", "pico", "ts", "fracP"], lado="fasor",
         destaque=dict(lado=True, num="66,8%",
                       txt="do tempo absorvendo potência ativa após a "
                           "eliminação, com a sintonia inadequada")),
    dict(id="seqneg", pres=["spec"], curto="Sequência negativa", kind="spec",
         titulo="Faltas assimétricas: a sequência negativa vira 120 Hz",
         ref="§5.3 · Tabela 5.3 · Figura 5.10",
         texto="Nas faltas assimétricas, a sequência negativa aparece em v<sub>d</sub> "
               "como uma oscilação de 120 Hz, de 0,29 a 0,72 pu: mais de 250 "
               "vezes o maior valor das trifásicas (0,0011 pu). O gráfico é o "
               "espectro de v<sub>d</sub> do inversor durante a falta; os cartões "
               "seguem a receita do TCC.",
         casos=[(k, *_ASSIM[k]) for k in ("bus7/3phase", "bus7/2phase", "bus7/1phase",
                                          "bus6/2phase", "bus6/1phase")],
         sinais=["spec"], xrange=[0.0, 400.0], metricas=["a120", "pico"],
         destaque=dict(sinal="spec", num="&gt; 250×", x=122, y=0.29, ax=200, ay=0.55,
                       txt="a menor assimétrica contra<br>as trifásicas"),
         notas=[dict(sinal="spec", x=121, y=0.004, ax=180, ay=0.24,
                     txt="<b>Barra 7 trifásica</b><br>0,0002 pu")]),
    dict(id="comp", pres=["err", "vd"], curto="Compromisso da sintonia", kind="time",
         titulo="Ganho menor é compromisso, não piora uniforme",
         ref="§5.3 · Tabela 5.3 · Figura 5.14",
         texto="Na falta bifásica da Barra 6, a sintonia inadequada filtra "
               "mais o 120 Hz: o pico na falta cai de 96,0° para 34,5° e o "
               "retorno de 48 para 30 ms. Na trifásica da Barra 7, a mesma "
               "sintonia perdeu o sincronismo.",
         casos=[("bus6/2phase", _NOM), ("bus6/2phase_bad_pll", _BAD)],
         sinais=["err", "vd"], xrange=[0.25, 0.6],
         metricas=["pico", "ts", "a120"]),
    dict(id="ons", pres=[], curto="Código de rede", kind="ons",
         titulo="Código de rede: permanência e corrente reativa",
         ref="§5.5 · Figuras 2.1 e 2.2 · Tabela 5.2",
         texto="O Submódulo 2.10 pede duas coisas durante a falta: permanecer "
               "conectado enquanto a tensão estiver dentro da região de "
               "suportabilidade e injetar corrente reativa proporcional ao "
               "afundamento. A Barra 7 e a Linha 7-8 levam a tensão abaixo de "
               "0,2 pu, onde a desconexão é permitida, e mesmo assim o inversor "
               "fica conectado com i<sub>q</sub> saturado em 1 pu. A Barra 6 fica "
               "dentro da região, com 0,72 pu contra 0,76 pu previstos.",
         casos=[("bus7/3phase", _LOC[0]), ("line7_8/3phase", _LOC[1]),
                ("line8_9/3phase", _LOC[2]), ("bus6/3phase", _LOC[3])],
         sinais=[], xrange=None, metricas=["Vmed", "rampa", "iqref"]),
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
