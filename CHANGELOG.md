# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

## 2026-07-25 — Eixo Y com nome+unidade, título branco fix e remoção do "Comparar PLL"

Arquivos: `src/pipeline/chart.py`, `src/report/renderer.py`

- **Eixo Y dos gráficos** (pedido do usuário): mostrava só a unidade
  (`"°"`, `"pu"`); agora mostra o nome completo da grandeza + unidade entre
  parênteses (ex. `"Ângulo (°)"`, `"P / Q UFV (pu)"`), como já é o texto de
  origem em `_inv_rows`/`_sys_rows`. A barra de título do painel continua
  mostrando só o nome.
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

## 2026-07-24 — Cards e diagnóstico movidos para dentro da aba Resumo

Arquivos: `src/pipeline/chart.py`, `app.py`, `src/report/renderer.py`

- **Motivação (pedido do usuário)**: cards e diagnóstico ficavam soltos
  acima da tab-bar, visíveis em qualquer aba; a aba Resumo tinha um
  gráfico próprio (`build_resume`, de 2026-07-15) que duplicava painéis já
  mostrados em Inversor UFV/Sistema 9-Bus — achado repetitivo.
- **Removido**: `ChartBuilder.build_resume()`/`_res_rows()`/
  `_RES_MAX_POINTS` (`chart.py`); chamada em `app.py` e as chaves
  `fig_res`/`tm_res` do dict de cenário; `resData`/`resLight`/`resDark`/
  `resIdx` do objeto `SCENARIOS` (`renderer.py`); `#plot-res`/`#badge-res`
  do HTML.
- **Movido**: `#cards-area`/`#story-area` para dentro de `#sec-res` — a
  aba Resumo passa a ser só cards + diagnóstico, sem gráfico, e só
  aparece quando essa aba está ativa (antes eram visíveis o tempo todo).
- **JS**: `TIME_TABS` e a ordem de busca do `goToChart` perdem "res" (não
  há mais figura pra buscar); `switchTab` ganhou guard explícito para
  nunca chamar `_renderChart`/`_ensureBridges`/`_applyZoom` na aba Resumo.
  `hasRes` no `SCENARIOS` passa a ser sempre `true` (cards/diagnóstico
  sempre existem, independente de haver gráfico).
- ⚠️ **Achado durante a verificação (não corrigido aqui)**: clique em card
  não navega mais para o painel do gráfico — regressão do commit anterior
  (`b2bbb2a`, redesign dos títulos de painel), não relacionada a esta
  mudança. Detalhes e fix sugerido em
  `dashboard/layout/tabs-navegacao.md`.
- KB atualizado: `dashboard/layout/{estrutura-html,tabs-navegacao}.md`,
  `dashboard/graficos/{construcao-graficos,dashboard-zoom-ghost}.md`,
  `dashboard/cards/cards-metricas.md`, `dashboard/index.md`.

## 2026-07-24 — Remoção dos ícones emoji dos botões/abas

Arquivos: `src/report/renderer.py`

- **Motivação (pedido do usuário)**: os emoji decorativos nos botões da
  filter-bar, nas abas de gráficos e no toggle de tema não ficavam bem
  visualmente.
- Removidos: 🗺 (Mapa IEEE 9-bus), 📊 (Comparativo), 🔍 (Zoom na falta),
  👻 (Comparar PLL), 📌/⚡/🔌/📈 (abas Resumo/Inversor/Sistema/Espectro) e
  🌙/☀️ (ícone do toggle de tema — o rótulo de texto "Dark mode"/"Light
  mode" já bastava, o `<span id="ico">` foi removido).
- Todos os labels viram texto puro; nenhuma função/id JS mudou.
- KB atualizado: `dashboard/layout/{estrutura-html,tabs-navegacao,
  header-branding}.md`, `dashboard/graficos/dashboard-zoom-ghost.md`,
  `dashboard/cards/comparison-table.md`.

## 2026-07-24 — Remoção das métricas ΔP/ΔQ UFV

Arquivos: `src/config/settings.py`, `src/config/__init__.py`,
`src/pipeline/loader.py`, `src/report/renderer.py`

- **Motivação (pedido do usuário)**: ΔP/ΔQ (excursão máx-mín de P/Q na
  janela pós-clear) não fazia sentido como métrica de desempenho do PLL.
- **Loader**: `_compute_metrics` não calcula mais `dP_ufv`/`dQ_ufv`; a
  janela auxiliar pós-clear (`t_rec`/`mask_rec`, usada só por essas duas
  métricas) foi removida — `_compute_metrics` agora tem só a janela
  pós-falta.
- **Cards**: grupo "Recuperação do inversor"/"Estabilidade de potência"
  (só continha os cards ΔP UFV/ΔQ UFV) removido inteiro.
- **Tabela comparativa**: colunas "ΔP (pu)"/"ΔQ (pu)" removidas do cabeçalho,
  de `_table_row_data` e do template JS de linha.
- **Story/veredito**: item narrativo "Recuperação"/"Oscilação de potência"
  removido; `dp_cls`/`dq` saem da lista de classes que definem o veredito
  geral (`statuses`).
- **Settings**: `DP_THRESH`/`DQ_THRESH` removidos de `settings.py` e do
  `config/__init__.py`.
- O painel de série temporal "P / Q UFV" (`chart.py`) não foi afetado — só
  a métrica derivada (excursão) saiu.
- KB atualizado: `dashboard/cards/cards-metricas.md`,
  `dashboard/cards/comparison-table.md`, `dashboard/dados/pipeline-dados.md`,
  `dashboard/layout/tabs-navegacao.md`, `simulation/python_pipeline.md`,
  `pll/pll_contingencies.md`.

## 2026-07-18 — Terminologia "sintonia inadequada" (pedido do professor)

Arquivos: `src/report/renderer.py`

- Rótulos visíveis do modo PLL detuned trocados de "Mal dimensionado"/"PLL
  ruim" para **"Sintonia inadequada"** (poorly tuned PLL): botão do toggle
  PLL e legenda do overlay de comparação.
- Identificadores internos (`BAD_PLL`, sufixo `_bad_pll`) e `params.m`
  inalterados — a mudança é só de texto exibido.
- KB atualizado: `dashboard/index.md`, `layout/bad-pll-dashboard-filter.md`,
  `graficos/dashboard-zoom-ghost.md`, `simulation/export_workflow.md`.

## Entradas anteriores

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
