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
# deck; na comparação por localização, azul do mais escuro (perto da usina)
# ao mais claro (longe).
_NOM = ("#2563eb", "#60a5fa")
_BAD = ("#ea580c", "#fb923c")
_LOC = (("#1e3a8a", "#dbeafe"), ("#1d4ed8", "#93c5fd"),
        ("#3b82f6", "#60a5fa"), ("#7cb1f8", "#2563eb"))
_REF = ("#94a3b8", "#64748b")

# Capítulos da aba "Análise TCC" (demonstração da defesa, slide 16 do deck).
# Campos: id, curto (botão), titulo, ref (seção/figura do TCC), texto,
# kind (time/spec/ons/tabela), casos [(key, cor)], sinais (o 1º é o
# padrão), xrange, metricas (chaves de tccInd nos mini-cartões).
CAPITULOS: list[dict] = [
    dict(id="energ", curto="Energização", kind="time",
         titulo="Energização do inversor", ref="§5.1 · Figura 5.3",
         texto="Na partida, o SRF-PLL trava na rede: o erro de fase entra na "
               "faixa de 2° em 40 ms com a sintonia nominal e em 79 ms com a "
               "inadequada.",
         casos=[("regime", _NOM), ("regime_bad_pll", _BAD)],
         sinais=["err", "vd"], xrange=[0.0, 0.2], metricas=["terr2", "tvd5"]),
    dict(id="local", curto="Localização", kind="time",
         titulo="Falta trifásica: quanto mais perto, mais severa",
         ref="§5.2 · Tabela 5.1 · Figura 5.7",
         texto="A mesma falta em quatro pontos, do mais próximo ao mais "
               "distante da usina. A retenção de v<sub>d</sub> vai de 9,2% (Barra 7) a "
               "58,4% (Barra 6), e com a sintonia nominal o erro sempre volta "
               "à faixa de 2°, em até 112 ms.",
         casos=[("bus7/3phase", _LOC[0]), ("line7_8/3phase", _LOC[1]),
                ("line8_9/3phase", _LOC[2]), ("bus6/3phase", _LOC[3])],
         sinais=["err", "vd", "P"], xrange=[0.25, 0.6],
         metricas=["ret", "pico", "ts"]),
    dict(id="sinc", curto="Perda de sincronismo", kind="time",
         titulo="Barra 7 trifásica: a sintonia decide o sincronismo",
         ref="§5.4 · Figuras 5.18 e 5.19",
         texto="A tensão cai quase igual nas duas sintonias (9,2% e 8,2%). "
               "Com a nominal, o erro volta à faixa de 2° em 98 ms; com a "
               "inadequada, percorre toda a faixa de ±180° até o fim da "
               "simulação, e a usina absorve potência ativa em 66,8% do "
               "tempo após a eliminação.",
         casos=[("bus7/3phase", _NOM), ("bus7/3phase_bad_pll", _BAD)],
         sinais=["err", "P", "Q", "vd"], xrange=[0.25, 0.6],
         metricas=["ret", "pico", "ts", "fracP"]),
    dict(id="seqneg", curto="Sequência negativa", kind="spec",
         titulo="Faltas assimétricas: a sequência negativa vira 120 Hz",
         ref="§5.3 · Tabela 5.3 · Figura 5.10",
         texto="Nas faltas assimétricas, a sequência negativa aparece em v<sub>d</sub> "
               "como uma oscilação de 120 Hz, de 0,29 a 0,72 pu: mais de 250 "
               "vezes o maior valor das trifásicas (0,0011 pu). O gráfico é o "
               "espectro de v<sub>d</sub> do inversor durante a falta; os cartões "
               "seguem a receita do TCC.",
         casos=[("bus7/2phase", _LOC[0]), ("bus7/1phase", _LOC[1]),
                ("bus6/2phase", _LOC[2]), ("bus6/1phase", _LOC[3]),
                ("bus7/3phase", _REF)],
         sinais=["spec"], xrange=[0.0, 400.0], metricas=["a120", "pico"]),
    dict(id="comp", curto="Compromisso da sintonia", kind="time",
         titulo="Ganho menor é compromisso, não piora uniforme",
         ref="§5.3 · Tabela 5.3 · Figura 5.14",
         texto="Na falta bifásica da Barra 6, a sintonia inadequada filtra "
               "mais o 120 Hz: o pico na falta cai de 96,0° para 34,5° e o "
               "retorno de 48 para 30 ms. Na trifásica da Barra 7, a mesma "
               "sintonia perdeu o sincronismo.",
         casos=[("bus6/2phase", _NOM), ("bus6/2phase_bad_pll", _BAD)],
         sinais=["err", "vd"], xrange=[0.25, 0.6],
         metricas=["pico", "ts", "a120"]),
    dict(id="ons", curto="Código de rede", kind="ons",
         titulo="Corrente reativa contra a rampa do ONS",
         ref="§5.5 · Tabela 5.2",
         texto="O Submódulo 2.10 pede corrente reativa proporcional ao "
               "afundamento. Nas trifásicas, a referência de i<sub>q</sub> acompanha a "
               "rampa: satura em 1 pu da Barra 7 à Linha 8-9 e fica em "
               "0,72 pu na Barra 6, contra 0,76 pu previstos.",
         casos=[("bus7/3phase", _LOC[0]), ("line7_8/3phase", _LOC[1]),
                ("line8_9/3phase", _LOC[2]), ("bus6/3phase", _LOC[3])],
         sinais=[], xrange=None, metricas=["Vmed", "rampa", "iqref"]),
    dict(id="sintese", curto="Todos os casos", kind="tabela",
         titulo="Todos os casos do TCC",
         ref="Tabelas 5.1 a 5.3",
         texto="Indicadores de todos os cenários analisados, nas duas "
               "sintonias. Clique numa linha para abrir o cenário nas abas.",
         casos=[], sinais=[], xrange=None, metricas=[]),
]


def tcc_secao(key: str) -> str | None:
    """Seção do Cap. 5 em que o caso aparece, ou None se o TCC não o usa."""
    return TCC_CASOS.get(key)
