# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

## 2026-08-03 — Card e item de diagnóstico "Topologia" (line7_8 vs. line8_9)

Arquivos: `src/report/renderer.py`

- Novo card "Topologia" no grupo Severidade do distúrbio + item "Topologia"
  no diagnóstico narrativo, só para os cenários `line7_8/*` e `line8_9/*`
  (dict `_LINE_TOPOLOGY`, chave = `key.split("/")[0]`). Motivo: as duas
  linhas têm topologia elétrica diferente e isso muda a leitura do
  cenário — a pedido do usuário, que apontou a diferença; confirmado
  também direto no `.slx` antes de escrever o texto.
- **`line7_8`**: 2 blocos `Transmission Line (Three-Phase)` em série
  (5 km + 45 km) com disjuntor em cada ponta — circuito único entre as
  barras 7 e 8. Card "1 circuito", sub "falta no único caminho B7–B8".
- **`line8_9`**: 2 blocos de 100 km cada, ambos ligando Bus8↔Bus9
  diretamente — circuito duplo de verdade, falta atinge só um dos dois.
  Card "2 circuitos", sub "falta em 1 dos 2, em paralelo".
- `_cards_html`/`_story_html` passam a receber `key` (chave do cenário)
  além de `data`. Bug pego na primeira rodada: um loop interno de
  `_cards_html` já usava a variável `key` para outra coisa (chave de
  métrica `vavg_bus1`/`vavg_bus3`), sombreando o parâmetro novo e fazendo
  o card falhar silenciosamente — renomeado para `mkey`.
- SVG do unifilar (`assets/diagrams/ieee9bus_unifilar.svg`) não foi
  tocado, a pedido do usuário.
- Regenerado `output/pll_metrics.html` (26 cenários, incl. `line8_9/2phase`
  e `line8_9/3phase` trazidos do merge do GGHB) e verificado via browser
  pane: card e item aparecem em `line7_8`/`line8_9`, ausentes em `bus*` e
  `regime`; sem overflow de layout, sem erro no console.
- Doc correspondente: `.claude/kb/dashboard/cards/cards-metricas.md`.

## 2026-08-02 — Teto fixo em 1 pu no eixo Y do espectro FFT

Arquivos: `src/pipeline/spectrum.py`

- **Eixo Y deixa de usar autorange** (`rangemode="tozero"`) e passa a ter
  `range=[0, max(1.0, pico_real·1.05)]` fixo por subplot — a pedido do
  usuário: com autorange, um pico de 0,012 pu virava o topo do gráfico e o
  ruído de fundo parecia proeminente, quando na verdade é desprezível frente
  à escala plena (1 pu). Teto padrão é 1 pu; só sobe se o pico real do
  painel ultrapassar isso.
- Escopo confirmado com o usuário: só a aba Espectro FFT (`spectrum.py`),
  não os outros gráficos do dashboard; corrente e tensão (subplots
  separados da mesma figura) têm tetos **independentes**, não
  compartilhados.
- `_mode_fig` agora calcula `row_maxes` (pico real por painel, a partir de
  `amp.max()` de cada segmento) e repassa para `_apply_layout`, que aplica
  o range por eixo (`yaxis`, `yaxis2`, ...) em vez de `update_yaxes` global.
- Regenerado `output/pll_metrics.html` (24 cenários, execução limpa) e
  verificado via JS no browser pane (`bus7/1phase`, eixo d): ambos os
  subplots (corrente e tensão) confirmados com `range: [0, 1]`.

## 2026-08-02 — Legenda explicada da tabela de harmônicas

Arquivos: `src/report/renderer.py`

- **Legenda reformulada em duas camadas** (novo `_harm_legend_html`): linha
  compacta de swatches sempre visível (excede limite normativo /
  desequilíbrio dq / abaixo de 2%) e um `<details>` "Como ler esta tabela"
  com um bloco por critério — conformidade a/b/c (limite, base do percentual
  e norma), desequilíbrio dq, por que dq não é checado por ordem, o `*` de
  "Durante a falta" e o aviso sobre a 1ª linha em d/q. Fecha com as
  referências em forma curta. Substitui o parágrafo único anterior.
- **Regra editorial**: a tela leva só a regra aplicada; a genealogia do
  número (razão Isc/IL, nota "c" da Tab.2 do IEEE 519-2014, descarte de `IL`
  como base) fica no KB — `kb/standards/harmonic_norm_application.md`.
  Limites vêm interpolados de `settings.py`, não hard-coded no texto.
- **`harm-fund` só em a/b/c**: a linha h=1ª das colunas d/q deixa de ser
  marcada como fundamental — no dq a fundamental é DC e sai do espectro com
  a média; o valor é o resíduo em 60 Hz. Passa a cair na escala comum
  (`harm-lo` quando <2%).
- CSS: `.harm-leg-row`/`.harm-leg-sw`/`.harm-help`/`.harm-refs` novos;
  `.harm-leg-viol`/`-unb` viram swatch (fundo) em vez de texto colorido.
- Regenerado `output/pll_metrics.html` (24 cenários) e verificado no browser
  pane (`bus4/1phase`): legenda abre/fecha, swatches nas cores corretas, e a
  classificação segue intacta (h=2ª abc `harm-viol` fora da falta, dq
  `harm-unb` em 0,303/0,309 durante a falta).

## 2026-07-30 — Remoção do painel "Frequência PLL"

Arquivos: `src/pipeline/loader.py`, `src/pipeline/chart.py`,
`src/config/settings.py`, `src/config/__init__.py`

- Removido o painel "Frequência PLL (Hz)" da aba Inversor UFV — a pedido do
  usuário, não fazia sentido para a análise do TCC.
- `loader.py`: deletados `_estimate_freq()`, a chamada em `__init__` e os
  atributos `t_freq`/`f_pll`/`has_freq`.
- `chart.py`: removida a linha do painel em `_inv_rows` (`has_freq` →
  `rows.append`), o bloco `elif kind == "freq"` em `_add_panel` (curva
  `f̂ PLL` + faixa ONS §5.2.1) e a entrada `"freq"` de `_AXIS_LABELS`.
- `settings.py`/`config/__init__.py`: removidas as constantes
  `FREQ_CONTINUOUS`, `FREQ_TRIP_MIN`, `FREQ_TRIP_MAX` (só usadas nesse
  painel). Painel não tinha consumidores em cards/tabela/story — remoção
  isolada, sem impacto em outras seções.
- Regenerado `output/pll_metrics.html` (24 cenários) e verificado no browser
  pane (regime + `bus7/3phase`): aba Inversor fica com Ângulo, Erro de fase,
  Corrente dq, Tensão dq e P/Q — sem o painel de frequência.

## 2026-07-29 — Destaque normativo (IEEE 519/1547) na tabela de harmônicas do FFT

Arquivos: `src/config/settings.py`, `src/report/renderer.py`

- **Tabela de harmônicas (aba Espectro) passa a comparar contra limites
  normativos reais**, em vez do destaque estético anterior (`harm-top`
  ≥0,4 pu / `harm-lo` <0,02 pu uniforme). Novo helper
  `HTMLRenderer._harm_cell_tier`: linha h=1ª sempre isenta (fundamental,
  classe `harm-fund`); colunas abc (a/b/c) comparadas ao IEEE 519-2014
  Tab.1/Tab.2 e IEEE 1547-2018 §7.3 (ímpares h<11: 4,0%; pares h=2/4/6:
  1%/2%/3%; tensão: 3,0% flat) — classe `harm-viol`; coluna dq (d/q), só a
  2ª harmônica (120 Hz, sequência negativa) usa o patamar empírico da
  TeseAGP (2%/3%) — classes `harm-warn`/`harm-unb`.
- **Segmento "Durante a falta" isento só da checagem abc/IEEE** (limites de
  regime permanente não valem durante o curto-circuito em si); o critério
  de desequilíbrio dq continua valendo em todos os segmentos, inclusive
  durante a falta — é onde a sequência negativa é mais relevante. Erro
  descoberto e corrigido durante a verificação: a 1ª versão isentava os
  dois critérios no mesmo segmento, o que fazia o alerta de desequilíbrio
  nunca disparar na prática.
- Novas constantes em `settings.py`: `CURR_ODD_LIMIT_PU`,
  `CURR_EVEN_LIMITS_PU`, `VOLT_INDIVIDUAL_LIMIT_PU`,
  `DQ_UNBALANCE_WARN_PU`/`_HIGH_PU`, `SPEC_SEG_NO_NORM`. Tooltip HTML
  (`title=`) em cada célula violada citando o limite/norma. Legenda de
  cores abaixo das tabelas. Tokens de tema `--danger`/`--warn` novos no CSS
  (light/dark).
- KB: `standards/harmonic_significance_criteria.md`,
  `dashboard/graficos/espectro-fourier.md`.

## 2026-07-28 — Faixa de frequência ONS §5.2.1 no painel "Frequência PLL"

Arquivos: `src/config/settings.py`, `src/pipeline/chart.py`

- **Faixa de frequência no painel "Frequência PLL"** (pedido do usuário):
  `add_hrect` verde (58,5–62,5 Hz, operação contínua) + duas `add_hline`
  vermelhas tracejadas (56 Hz / 63 Hz, trip instantâneo), conforme ONS
  Submódulo 2.10 §5.2.1 (eólica/UFV). Novas constantes `FREQ_CONTINUOUS`,
  `FREQ_TRIP_MIN`, `FREQ_TRIP_MAX` em `config/settings.py`.
- Tentativa de painel adicional "Deslizamento de Fase PLL" (Δθ vs. relógio
  nominal de 60 Hz) foi implementada e **revertida a pedido do usuário** —
  não era o que tinha sido pedido; `loader.py` não foi alterado nesta entrada.
- KB: `dashboard/graficos/chart-analysis-overlays.md`,
  `standards/ons_frequency_ride_through.md` (já existia, criado em sessão
  anterior).

## Entradas anteriores

- [2026-07-25](docs/changelog/2026-07-25.md) — eixo Y com nome+unidade,
  título branco fix, remoção do overlay "Comparar PLL", cards de tensão
  mínimo → média (V médio / V residual médio).
- [2026-07-18 a 2026-07-24](docs/changelog/2026-07-18_24.md) — terminologia
  "sintonia inadequada", remoção dos ícones emoji dos botões/abas, remoção
  das métricas ΔP/ΔQ UFV, cards/diagnóstico movidos para a aba Resumo.
- [2026-07-15](docs/changelog/2026-07-15.md) — espectro FFT multi-modo
  (a/b/c/d/q) + tabela de harmônicas, abas de gráficos + aba Resumo + cards
  clicáveis.
- [2026-07-14](docs/changelog/2026-07-14.md) — regime sem tₛ, cards de
  severidade renomeados para "V residual", Vmin das Barras 1 e 3.
- [2026-07-12](docs/changelog/2026-07-12.md) — export de correntes/tensões
  abc, T_SETTLE fora de todos os cálculos, espectro de Fourier segmentado.
- [2026-07-01 a 2026-07-05](docs/changelog/2026-07-early.md) — reestruturação
  do pacote `src/`, decimação (570 MB → 23,7 MB), tabela comparativa, fixes de
  dark mode, overlays de análise (LVRT, tₛ, frequência PLL), zoom sincronizado,
  reavaliação dos cards e veredito.
