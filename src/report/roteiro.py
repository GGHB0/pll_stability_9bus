"""
roteiro.py — Casos analisados no Cap. 5 do TCC e roteiro da demonstração.

O painel tem mais cenários do que o TCC discute (Barras 4, 5, 8 e 9, Linha 8-9
bifásica). TCC_CASOS diz em que seção do Cap. 5 cada caso aparece, na ordem
das Tabelas 5.1 a 5.3; o resto vai para o grupo "fora do TCC" do seletor e
fica esmaecido no mapa unifilar. ROTEIRO é a sequência de passos do modo
roteiro (demonstração da defesa, slide 16 do deck): cada passo escolhe
cenário, aba, zoom e painel, e mostra uma legenda com o que observar.

Os números das legendas são os do TCC (VFinal, Tabelas 5.1 e 5.3, §5.1 e
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

# Passos do modo roteiro. Campos: key, tab (res/inv/sys/spec), zoom (janela
# da falta), panel (fragmento do título do painel para rolar até ele),
# phase (eixo do espectro), table (abre o comparativo só com casos do TCC).
ROTEIRO: list[dict] = [
    dict(key="regime", tab="inv", zoom=False, panel="Erro de fase",
         titulo="Energização do inversor",
         texto="Na partida, o SRF-PLL trava na rede: o erro de fase entra na "
               "faixa de 2° em 40 ms. Com a sintonia inadequada, leva 79 ms."),
    dict(key="bus7/3phase", tab="inv", zoom=True, panel="Erro de fase",
         titulo="Falta trifásica na Barra 7",
         texto="Na barra mais próxima da usina, v_d retém 9,2% do pré-falta. "
               "O erro chega a 37,3° durante a falta e volta à faixa de 2° "
               "em 98 ms após a eliminação."),
    dict(key="bus6/3phase", tab="inv", zoom=True, panel="Erro de fase",
         titulo="A mesma falta na Barra 6",
         texto="Na barra mais distante, v_d retém 58,4%, o pico na falta fica em 7,3° "
               "e o retorno leva 76 ms. A localização define a severidade."),
    dict(key="bus7/3phase_bad_pll", tab="inv", zoom=True, panel="Erro de fase",
         titulo="Barra 7 com sintonia inadequada",
         texto="Mesma falta, com os ganhos do PI reduzidos a 20%. A tensão cai "
               "quase igual (8,2%), mas o erro percorre toda a faixa de ±180° "
               "até o fim da simulação: escorregamento de ciclo, perda de "
               "sincronismo."),
    dict(key="bus7/3phase_bad_pll", tab="inv", zoom=True, panel="P / Q",
         titulo="Consequência na potência",
         texto="Sem sincronismo, a potência ativa troca de sentido: depois da "
               "eliminação, a usina absorve potência ativa em 66,8% do tempo."),
    dict(key="bus6/2phase", tab="spec", phase="d",
         titulo="Falta bifásica na Barra 6: 120 Hz",
         texto="A sequência negativa aparece em v_d como oscilação de 120 Hz "
               "(0,39 pu). Nas faltas trifásicas, essa componente não passa "
               "de 0,0011 pu."),
    dict(key="bus6/2phase", tab="inv", zoom=True, panel="Erro de fase",
         titulo="Bifásica na Barra 6, sintonia nominal",
         texto="Com o 120 Hz, o erro de fase oscila durante a falta e chega a "
               "96,0°. Volta à faixa de 2° em 48 ms."),
    dict(key="bus6/2phase_bad_pll", tab="inv", zoom=True, panel="Erro de fase",
         titulo="A mesma falta com sintonia inadequada",
         texto="Com banda menor, o PLL atenua o 120 Hz: pico de 34,5° na falta e "
               "retorno em 30 ms. Ganho menor é compromisso, não piora "
               "uniforme."),
    dict(key="bus7/3phase", tab="res", table=True,
         titulo="Todos os casos do TCC",
         texto="Comparativo só com os cenários das Tabelas 5.1 a 5.3. Clique no "
               "cabeçalho para ordenar ou numa linha para abrir o cenário."),
]


def tcc_secao(key: str) -> str | None:
    """Seção do Cap. 5 em que o caso aparece, ou None se o TCC não o usa."""
    return TCC_CASOS.get(key)
