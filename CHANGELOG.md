# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

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

## 2026-07-25 — Eixo Y com nome+unidade, título branco fix e remoção do "Comparar PLL"

Arquivos: `src/pipeline/chart.py`, `src/report/renderer.py`

- **Eixo Y dos gráficos** (pedido do usuário): mostrava só a unidade
  (`"°"`, `"pu"`); agora mostra a **grandeza física genérica** medida +
  unidade (ex. `"Tensão (pu)"`, `"Frequência (Hz)"`, `"Potência (pu)"`),
  via dicionário `_AXIS_LABELS[kind]` em `chart.py` — não o título
  específico do painel (`"P / Q UFV (pu)"`, `"|V| Bus 2 (pu)"`), que o
  usuário rejeitou numa 1ª tentativa por não identificar a grandeza de
  forma consistente entre painéis (mesmo critério do `"Tempo (s)"` no eixo
  X). A barra de título do painel continua mostrando o nome específico.
- **Bug real corrigido — título do painel não ficava branco**: já era
  branco no Python (`_label` em `chart.py`/`spectrum.py`), mas o JS
  `themedLayout` (`renderer.py`) confundia a barra de título com o
  subtítulo de grupo (`_group_title`) — ambos usam `xref="paper"` desde o
  redesign de títulos (`b2bbb2a`, 2026-07-21) — e sobrescrevia a cor para
  cinza/slate em ambos os temas. Fix: distinguir por `yref` (`"paper"` =
  barra de título, intocada; `"y... domain"` = subtítulo de grupo,
  re-temado). Detalhes em `dashboard/layout/dark-mode-legend-title-fixes.md`
  (Fix 5).
- **Removido o overlay "Comparar PLL"** (pedido do usuário — não estava
  sendo usado): botão `ghost-toggle`, `ghostMode`, `_exactEquiv`,
  `_ghostData`, `toggleGhost`, a injeção `.concat(_ghostData(which))` em
  `_renderChart` e o bloco `gbtn` de `_syncCtrlButtons`. **Não afeta** o
  toggle nominal/sintonia inadequada (`pllMode`) — feature separada,
  mantida.
- KB: `dashboard/graficos/construcao-graficos.md` (eixo Y),
  `dashboard/layout/dark-mode-theming.md` +
  `dashboard/layout/dark-mode-legend-title-fixes.md` (novo doc, fragmentado
  do anterior pelo limite de 200 linhas — Fix 5), `dashboard/graficos/
  dashboard-zoom-ghost.md` renomeado para `dashboard-zoom-export.md` (nome
  não fazia mais sentido sem o fantasma), `dashboard/index.md`,
  `dashboard/layout/{estrutura-html,tabs-navegacao}.md`,
  `dashboard/graficos/espectro-fourier.md`; skill `dashboard-html-editor`
  em v1.3.0.

## 2026-07-25 — Cards de tensão: mínimo → média (V médio / V residual médio)

Arquivos: `src/pipeline/loader.py`, `src/config/settings.py`,
`src/config/__init__.py`, `src/report/renderer.py`

- **Motivação (pedido do usuário)**: os cards de severidade (B1/B2/B3)
  mostravam o **mínimo instantâneo** de |V| na janela pós-falta inteira
  (até o fim da simulação). O usuário pediu regras de janela mais precisas
  e a troca do mínimo pela **média**.
- **Regras da nova janela** (`SimData._compute_metrics`): sempre começa em
  `T_SETTLE` (nunca conta o transitório de partida do PLL); em **regime
  permanente** cobre o período inteiro `[T_SETTLE, fim]`; numa **falta**
  fica restrita ao **período do curto** `[t_start, t_clear]` (antes ia até
  o fim da simulação, incluindo a recuperação pós-clear) — mesmo padrão de
  "durante a falta" já usado no espectro FFT (`SpectrumBuilder._segments`).
- **Renomeado** (chave antiga não descrevia mais o cálculo):
  `vmin`/`vmin_bus1`/`vmin_bus3` → `vavg`/`vavg_bus1`/`vavg_bus3`;
  `VBUS_MIN_THRESH` → `VBUS_AVG_THRESH` (mesmos valores 0.90/0.50 pu, a
  revisitar se a distribuição real de médias reclassificar muitos
  cenários). Rótulos: "V min"/"V residual" → **"V médio"**/**"V residual
  médio"**; tabela comparativa: "Vmin B1/B2/B3" → **"V méd. B1/B2/B3"**.
- Tooltip do B1/B3 parou de dizer "durante o curto" fixo em cenários de
  regime (era impreciso — agora reflete a janela real por tipo de cenário).
- KB atualizado: `dashboard/dados/pipeline-dados.md`,
  `dashboard/cards/{cards-metricas,comparison-table}.md`; skill
  `dashboard-html-editor` ganhou linha nova na tabela de mudanças
  ("redefinir cálculo de métrica existente").

## Entradas anteriores

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
