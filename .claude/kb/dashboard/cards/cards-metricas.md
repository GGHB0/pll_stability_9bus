---
name: cards-metricas
description: Cards em 2 grupos (severidade / desempenho PLL) com semáforo good/warn/bad, estado "não acomodou", pico de erro de fase e diagnóstico em lista de tópicos com veredito só de desempenho
---

# Cards de Métricas e Diagnóstico Narrativo (renderer.py)

Gerados **em Python** por cenário (`_cards_html`, `_story_html`) e embutidos
prontos no JS (`SCENARIOS[key].cardsHtml` / `.storyHtml`) — `switchScenario`
só injeta o HTML em `#cards-area`/`#story-area`, sem recomputar nada no browser.

**Localização (2026-07-24)**: `#cards-area`/`#story-area` moraram para dentro
da aba Resumo (`#sec-res`, [[tabs-navegacao]]) — antes ficavam soltos, visíveis
em qualquer aba; agora só aparecem quando a aba Resumo está ativa. Motivo: o
gráfico próprio da aba Resumo (`build_resume`) foi removido por duplicar
painéis já mostrados em Inversor/Sistema, e cards+diagnóstico passaram a ser
o conteúdo integral dessa aba.

## 2 grupos de cards (`_cards_html`)

| Grupo | Cards | Papel |
|---|---|---|
| Severidade do distúrbio | V residual B2 (pu, POC do inversor, vs LVRT), V residual B1/B3 (quando `vbus1_pu`/`vbus3_pu` existem no CSV — propagação do sag; subtítulos "barra do G1 (slack)"/"barra do G3"), Duração da falta (ms, t_fault–t_clear), Topologia (só `line7_8`/`line8_9`, ver abaixo) | **Contexto** — quão dura foi a falta; fora do veredito |
| Desempenho do PLL | IAE (rad·s), ISE (rad²·s), tₛ (s, ±1.15°), \|θ_err\| pico (°), **Erro R.P. (°)** | Julga o PLL |

Fonte: `metrics` do [[pipeline-dados]] (janela pós-falta).

**ΔP/ΔQ UFV removidos (2026-07-24)**: card group "Recuperação do
inversor"/"Estabilidade de potência" (excursão máx-mín de P/Q na janela
pós-clear) não fazia sentido como métrica de desempenho do PLL e foi
descartado — junto com `DP_THRESH`/`DQ_THRESH`, as colunas ΔP/ΔQ da tabela
comparativa e o item narrativo "Recuperação"/"Oscilação de potência". O
painel de série temporal "P / Q UFV" (chart.py) não foi afetado — só a
métrica derivada saiu.

**Regime permanente** (2026-07-14): sem distúrbio, tₛ não mede nada — o loader
deixa `ts`/`ts_delta`/`settled` como `None` e o **card tₛ é omitido** (antes
mostrava "não acomodou" bad falso, que ainda contaminava o veredito). Grupo de
severidade renomeado: "Sistema 9-Bus" (cards "V min", sem duração). Tooltip do
pico diz "em regime" no lugar de "pós-falta". Story: sem item "Acomodação",
texto do "Cenário" cita `T_SETTLE` (0.10 s — antes citava `T_FAULT`
desatualizado), pico warn diz "em regime". Linha de regime na tabela
comparativa mostra "—" na coluna tₛ.

**"V residual"** (2026-07-14): tensão remanescente do afundamento — termo do
PRODIST Módulo 8 / IEC 61000, escolhido pelo usuário no lugar de "V min" para
comunicar "quanto caiu durante o curto". Em **regime** (sem curto) o nome
volta a "V min B1/B2/B3" (variável `vlab` em `_cards_html`).

**Mínimo → média (2026-07-25)**: os cards de severidade não mostram mais o
pior instante (`vmin` = `.min()`), e sim a **média** de |V| na barra
(`vavg` = `.mean()`, loader `_compute_metrics`), com janela por regra:
sempre `t ≥ T_SETTLE` (nunca conta o transitório de partida do PLL); em
**regime** a janela é o período inteiro `[T_SETTLE, fim]`; numa **falta** é
só o período do curto `[t_start, t_clear]` (antes ia até o fim da simulação,
incluindo a recuperação pós-clear — isso mudou). Motivo: o mínimo
instantâneo é sensível a um único ponto do transitório; a média durante o
curto é mais fiel ao conceito de "tensão residual" da norma (PRODIST/IEC),
que é definido sobre o período do afundamento, não sobre a pior amostra.
Rótulos: `vlab = "V médio"` (regime) / `"V residual médio"` (falta). O texto
do item "Distúrbio" no story usa "V residual médio = X pu". A tabela
comparativa usa "V méd. B1/B2/B3 (pu)" — genérico, vale para as duas
janelas. Threshold `VBUS_AVG_THRESH` (ex-`VBUS_MIN_THRESH`) manteve os
mesmos valores (0.90/0.50 pu) por ora — como a média tende a ficar mais alta
que o mínimo que ela substitui, pode exigir recalibração se o veredito de
muitos cenários mudar de classe (a validar contra a distribuição real).

Estados especiais:
- **tₛ "não acomodou"** (`settled = False`): valor "> t_end s", classe `bad` —
  substitui o tₛ falso que reportava a última amostra da simulação.
- **\|θ_err\| pico ≥ `SYNC_LOSS_DEG` (90°)**: subtítulo vira
  "perda de sincronismo" (escorregamento do PLL, ex. BAD_PLL com 178°).

## Topologia — circuito único vs. duplo (2026-08-03)

Card novo no grupo Severidade + item novo no story, só para `line7_8`/
`line8_9` (dict `_LINE_TOPOLOGY`, chave = `key.split("/")[0]`, thread via
parâmetro `key` em `_cards_html`/`_story_html`). Motivo: as duas linhas têm
topologia elétrica diferente e isso muda a leitura do cenário —
confirmado direto no `.slx` (não só pela descrição do usuário), ver
[[ieee9bus-line-params]]:

- **`line7_8`**: 2 blocos `Transmission Line (Three-Phase)` **em série**
  (5 km + 45 km), disjuntor (`SPST Switch`) em cada ponta — **circuito
  único** entre as barras 7 e 8. Card: "1 circuito", sub "falta no único
  caminho B7–B8".
- **`line8_9`**: 2 blocos de **100 km cada, ambos ligando Bus8↔Bus9
  diretamente** (mesmo x, y empilhado — layout de paralelo, confirmado por
  `<Line>`/`<Branch>` no XML) — **circuito duplo** de verdade. A falta
  atinge só um dos dois; o outro segue em serviço. Card: "2 circuitos", sub
  "falta em 1 dos 2, em paralelo".

Card classe `neutral` (contexto, não entra no veredito) — mesmo padrão do
card Duração. Story: item "Topologia" logo após "Distúrbio"/"Cenário",
também `neutral`. Não aparece em `bus*`/`regime` (dict não tem essas
chaves). SVG do unifilar (`assets/diagrams/ieee9bus_unifilar.svg`) não foi
tocado — a pedido do usuário, fica reservado para o texto do TCC; qualquer
diagrama novo deve ser um arquivo separado.

## Erro R.P. — erro de fase em regime permanente (2026-07-21)

Resposta ao **Ponto 1 do professor**: o card `|θ_err| pico` (ex.: regime = 1,4°)
foi lido como "erro em regime permanente", mas é o **pico transitório** (máx
instantâneo) sobre toda a janela `t ≥ T_SETTLE`. Card novo separa os conceitos:

- **`Erro R.P.` (°)** = erro de fase **sustentado**, `err_ss_mean` = média de
  `|θ̂ − θ_rede|` na janela **após a acomodação** (`t ≥ t_ss`). Loader também
  expõe `err_ss_rms`. Subtítulo mostra a janela ("média |e|, t ≥ 0.100 s").
- **`t_ss`** (início do regime): `tₛ` quando a falta reacomodou
  (`settled=True`); `T_SETTLE` em regime permanente (PLL já travado). Falta que
  **não** reacomodou (`settled=False`) não tem regime → `t_ss/err_ss_* = None` e
  o **card é omitido** (ver `_compute_metrics` no [[pipeline-dados]]).
- Threshold `ERR_SS_DEG_THRESH = (0.5, 1.0)` em graus (PLL bem sintonizado
  tende a ~0°). Valores reais: regime 0,48° (good), regime_bad_pll 0,74° (warn),
  bus7/3phase 0,73° (t_ss=0,55 s).
- O card `|θ_err| pico` teve o subtítulo trocado de "máx |θ̂ − θ_rede|" para
  **"pico transitório"** e o tooltip reforça que é distinto do erro de R.P.
- **Não** entra no veredito do story (evita reclassificar cenários em massa);
  aparece só como card + item narrativo informativo.

Cada card: nome, valor (ou "—" se `None`), unidade, subtítulo e tooltip via `title=`.

## Semáforo (`_classify`)

Thresholds em `config/settings.py`: `IAE_THRESH`, `ISE_THRESH`,
`TS_DELTA_THRESH`, `PEAK_ERR_DEG_THRESH`, `VBUS_AVG_THRESH`
(`lower_is_better=False`; mesma escala para V médio das barras 1, 2 e 3 — mas
o veredito LVRT usa só a B2). Para tₛ o classificado é
`ts_delta = tₛ − t_fault` (vem pronto do loader). Calibrados sobre a
distribuição real dos 12 cenários (2026-07): pico saudável 1°, faltas
trifásicas remotas ~26–35° (warn), BAD_PLL 178° (bad).

Os mesmos thresholds/classes alimentam a tabela comparativa
(`_table_row_data` → `metricsRow`) — ver [[comparison-table]].

## Story: diagnóstico em tópicos (`_story_html`)

Lista `<ul class="story-list">` (antes era parágrafo corrido). Cada item é
uma tupla `(classe, rótulo, texto)` renderizada como `<li>` com rótulo em
negrito e bolinha `::before` colorida pela classe do semáforo daquela
métrica (mesmas cores dos cards; `neutral` usa `var(--muted)`).

Ordem fixa dos itens: **Distúrbio** (falta de X ms, profundidade do sag vs
LVRT — vira "Cenário" neutro em regime) → **Pico de fase** →
**Acomodação** (ou "não reacomodou") → **Erro de regime** (erro sustentado
`err_ss_mean` em °, só quando há `t_ss`) → **Erro acumulado** (IAE).
Redação específica por classe, encurtada porque o rótulo já
carrega o assunto. Item só aparece nas mesmas condições das frases antigas
(ex.: pico `good` continua omitido). Sem `parts`, fallback
`<p class="story-text">Dados insuficientes…</p>`.

**Veredito** (chip à direita): pior classe entre as métricas de
**desempenho** (IAE, ISE, tₛ/settled, pico) — `V min NÃO
entra`: falta severa com PLL exemplar não vira "crítico" (ex. Barra 8
trifásica: V_min 0.107 mas veredito "em atenção"). Labels: `bad` →
"Desempenho crítico", `warn` → "Desempenho em atenção", `good` →
"Desempenho bom", nada disponível → "Dados insuficientes". A classe também
colore a borda esquerda do bloco `.story`; título vira "Diagnóstico —
regime permanente" quando não há falta.
