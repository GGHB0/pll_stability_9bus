---
name: cards-metricas
description: Cards de severidade do distúrbio (V médio por barra, duração, topologia) com semáforo good/warn/bad e bloco de contexto em tópicos — grupo "Desempenho do PLL" e veredito removidos em 2026-08-09
---

# Cards de Métricas e Contexto Narrativo (renderer.py)

Gerados **em Python** por cenário (`_cards_html`, `_story_html`) e embutidos
prontos no JS (`SCENARIOS[key].cardsHtml` / `.storyHtml`) — `switchScenario`
só injeta o HTML em `#cards-area`/`#story-area`, sem recomputar nada no browser.

**Localização (2026-07-24)**: `#cards-area`/`#story-area` moraram para dentro
da aba Resumo (`#sec-res`, [[tabs-navegacao]]) — antes ficavam soltos, visíveis
em qualquer aba; agora só aparecem quando a aba Resumo está ativa. Motivo: o
gráfico próprio da aba Resumo (`build_resume`) foi removido por duplicar
painéis já mostrados em Inversor/Sistema, e cards+contexto passaram a ser
o conteúdo integral dessa aba.

## Grupo único de cards (`_cards_html`)

| Grupo | Cards | Papel |
|---|---|---|
| Severidade do distúrbio | V residual B2 (pu, POC do inversor, vs LVRT), V residual B1/B3 (quando `vbus1_pu`/`vbus3_pu` existem no CSV — propagação do sag; subtítulos "barra do G1 (slack)"/"barra do G3"), Duração da falta (ms, t_fault–t_clear), Topologia (só `line7_8`/`line8_9`, ver abaixo) | Contexto — quão dura foi a falta |

Fonte: `metrics` do [[pipeline-dados]]. Rótulo do grupo vira "Sistema 9-Bus"
em regime permanente (sem falta a caracterizar).

Cada card: nome, valor (ou "—" se `None`), unidade, subtítulo e tooltip via
`title=`.

## Remoções — histórico

**Grupo "Desempenho do PLL" removido por inteiro (2026-08-09)**, a pedido do
usuário: **IAE** (rad·s), **ISE** (rad²·s), **tₛ** (s, ±1.15°),
**\|θ_err\| pico** (°) e **Erro R.P.** (°). Todos os cinco eram funções do
mesmo sinal, o erro de ângulo `θ̂ − θ_rede`, e **não foi encontrada fonte que
sustente acúmulo (IAE/ISE), média (Erro R.P.) ou pico como medida de
desempenho do PLL**. Sem base bibliográfica, os números não podiam ir para o
TCC nem justificar um veredito. Saíram junto:

- Os limiares em `config/settings.py`: `IAE_THRESH`, `ISE_THRESH`,
  `TS_DELTA_THRESH`, `PEAK_ERR_DEG_THRESH`, `ERR_SS_DEG_THRESH`,
  `SYNC_LOSS_DEG` (e os reexports em `config/__init__.py`).
- As colunas `iae`/`ise`/`ts`/`peak` da tabela comparativa — ver
  [[comparison-table]].
- Os itens "Pico de fase", "Acomodação", "Erro de regime" e "Erro acumulado"
  do story, e o **chip de veredito** (que era calculado só com IAE/ISE/tₛ/pico
  e por isso perdeu toda a sua base). CSS `.story-verdict` e `.story.good/
  .warn/.bad` removidos junto.
- As chaves `IAE`, `ISE`, `peak_err`, `ts_delta`, `t_ss`, `err_ss_mean`,
  `err_ss_rms` do `metrics` do loader.

**O que NÃO saiu**: o painel de série temporal "Erro de fase" (chart.py)
continua intacto — o sinal bruto `θ̂ − θ_rede` no tempo não é métrica
derivada. E **`ts`/`settled` continuam sendo calculados no loader**, porque o
instante de acomodação alimenta o marcador tₛ e a faixa ±1,15° do gráfico
([[chart-analysis-overlays]]): saber **como o PLL retorna pós-falta** segue
sendo interesse central do trabalho. O critério em si está em revisão — ver
[[pll-ts-criterion-rationale]].

**ΔP/ΔQ UFV removidos (2026-07-24)**: card group "Recuperação do
inversor"/"Estabilidade de potência" (excursão máx-mín de P/Q na janela
pós-clear) não fazia sentido como métrica de desempenho do PLL e foi
descartado — junto com `DP_THRESH`/`DQ_THRESH`, as colunas ΔP/ΔQ da tabela
comparativa e o item narrativo "Recuperação"/"Oscilação de potência". O
painel de série temporal "P / Q UFV" (chart.py) não foi afetado — só a
métrica derivada saiu.

## "V residual" e a janela de média

**"V residual"** (2026-07-14): tensão remanescente do afundamento — termo do
PRODIST Módulo 8 / IEC 61000, escolhido pelo usuário no lugar de "V min" para
comunicar "quanto caiu durante o curto". Em **regime** (sem curto) o nome
volta a "V médio B1/B2/B3" (variável `vlab` em `_cards_html`).

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
que o mínimo que ela substitui, pode exigir recalibração (a validar contra a
distribuição real).

## Topologia — circuito único vs. duplo (2026-08-03)

Card no grupo Severidade + item no story, só para `line7_8`/`line8_9`
(dict `_LINE_TOPOLOGY`, chave = `key.split("/")[0]`, thread via parâmetro
`key` em `_cards_html`/`_story_html`). Motivo: as duas linhas têm topologia
elétrica diferente e isso muda a leitura do cenário — confirmado direto no
`.slx` (não só pela descrição do usuário), ver [[ieee9bus-line-params]]:

- **`line7_8`**: 2 blocos `Transmission Line (Three-Phase)` **em série**
  (5 km + 45 km), disjuntor (`SPST Switch`) em cada ponta — **circuito
  único** entre as barras 7 e 8. Card: "1 circuito", sub "falta no único
  caminho B7–B8".
- **`line8_9`**: 2 blocos de **100 km cada, ambos ligando Bus8↔Bus9
  diretamente** (mesmo x, y empilhado — layout de paralelo, confirmado por
  `<Line>`/`<Branch>` no XML) — **circuito duplo** de verdade. A falta
  atinge só um dos dois; o outro segue em serviço. Card: "2 circuitos", sub
  "falta em 1 dos 2, em paralelo".

Card classe `neutral` — mesmo padrão do card Duração. Story: item
"Topologia" logo após "Distúrbio"/"Cenário", também `neutral`. Não aparece
em `bus*`/`regime` (dict não tem essas chaves). SVG do unifilar
(`assets/diagrams/ieee9bus_unifilar.svg`) não foi tocado — a pedido do
usuário, fica reservado para o texto do TCC; qualquer diagrama novo deve ser
um arquivo separado.

## Semáforo (`_classify`)

Restou um único threshold em `config/settings.py`: `VBUS_AVG_THRESH`
(`lower_is_better=False`; mesma escala para V médio das barras 1, 2 e 3).
Alimenta cards, story e a tabela comparativa (`_table_row_data` →
`metricsRow`) — ver [[comparison-table]].

Cálculo de cada card reimplementado célula a célula, com números reais e
verificação cruzada contra o pipeline, em
`notebooks/dashboard_cards_explainer.ipynb` — ver [[cards-explainer-notebook]].

## Story: contexto em tópicos (`_story_html`)

Lista `<ul class="story-list">`. Cada item é uma tupla
`(classe, rótulo, texto)` renderizada como `<li>` com rótulo em negrito e
bolinha `::before` colorida pela classe do semáforo (`neutral` usa
`var(--muted)`).

Ordem fixa: **Distúrbio** (falta de X ms, profundidade do sag vs LVRT — vira
"Cenário" neutro em regime) → **Topologia**. Sem `parts`, fallback
`<p class="story-text">Dados insuficientes…</p>`.

Título: "Contexto do cenário" (ou "Contexto — regime permanente" sem falta) —
era "Diagnóstico pós-falta" enquanto havia veredito. O bloco `.story` é sempre
`neutral` desde 2026-08-09: sem métrica de desempenho, não há o que julgar.
