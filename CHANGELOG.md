# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

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

## 2026-07-15 — Espectro FFT multi-modo (a/b/c/d/q) + tabela de harmônicas

Arquivos: `src/pipeline/spectrum.py`, `src/config/settings.py`,
`src/config/__init__.py`, `app.py`, `src/report/renderer.py`

- **SpectrumBuilder multi-modo**: além da fase A, espectros das fases b/c
  (de `sim_data_abc.csv`) e dos eixos d/q (sinais dq a Tsc=200 µs); `build()`
  devolve dicts de figuras/trace_maps por modo + dados de harmônicas.
- **Ciclos inteiros**: janela da FFT truncada a `floor(T·60)/60` s — a
  fundamental (e 120 Hz da seq. negativa) cai exata num bin, sem vazamento
  por janela cortada no meio do ciclo.
- **Seletor de fase** na seção Espectro: botões a/b/c/d/q (sticky entre
  cenários; botões sem dado somem); título/hint acompanham; marcadores
  próprios para dq (`SPEC_MARKERS_DQ`: 2f₁, 6f₁, 12f₁, f_res).
- **Tabela de harmônicas 1ª–7ª** (60–420 Hz) por segmento × fase/eixo, para
  corrente e tensão UFV; célula ≥ 0,4 pu destacada (accent), < 0,02 pu
  apagada — só amplitude na ordem da nominal chama atenção.
- Detalhes em `.claude/kb/dashboard/graficos/espectro-fourier.md`.

## 2026-07-15 — Abas de gráficos + aba Resumo + cards clicáveis

Arquivos: `src/pipeline/chart.py`, `app.py`, `src/report/renderer.py`

- **Abas**: as 3 seções de gráficos empilhadas viram painéis de aba
  (📌 Resumo · ⚡ Inversor UFV · 🔌 Sistema 9-Bus · 📈 Espectro FFT); só a
  aba ativa é renderizada (`Plotly.react` sob demanda via flags `_dirty`) —
  troca de cenário/tema roda 1 react em vez de 3. Abas sem dado somem;
  se a ativa não existe no cenário, cai para a 1ª disponível.
- **Aba Resumo** (padrão): figura nova `build_resume()` no ChartBuilder com
  os painéis essenciais — erro de fase (banda ±tol + tₛ), frequência PLL,
  P/Q UFV e |V| Bus 2 (LVRT). Decimação própria `_RES_MAX_POINTS = 2000`
  limita o custo de duplicar traces no HTML.
- **Cards clicáveis**: métricas ganham `onclick=goToChart(rótulo)` — procura
  o rótulo de painel nas figuras (ordem res → inv → sys), abre a aba e rola
  até o painel usando o domínio do eixo Y (scroll via `setTimeout`, não rAF,
  para funcionar com a aba do browser em segundo plano).
- **Zoom**: `_applyZoom`/ponte manual generalizados para res/inv/sys (spec
  fora — eixo em Hz); só tocam gráficos já plotados e limpos.
- Trade-off registrado: sem visão inv+sys lado a lado rolando a página —
  compensado pela aba Resumo, que junta o essencial das duas seções.

## 2026-07-14 — Regime permanente sem tₛ + revisão dos cards/diagnóstico

Arquivos: `src/pipeline/loader.py`, `src/report/renderer.py`

- **Loader**: em regime (`t_fault` None), `ts`/`ts_delta`/`settled` ficam
  `None` — sem distúrbio não há acomodação a medir. Antes o drift do θ_err
  estourava a tolerância e o card mostrava "> 0.60 s / não acomodou" (bad
  falso), puxando o veredito do regime para "Desempenho crítico".
- **Cards**: card tₛ omitido em regime; grupo "Recuperação do inversor" vira
  "Estabilidade de potência"; tooltips de ΔP/ΔQ ("oscilação sustentada") e do
  pico ("em regime") ajustados ao contexto.
- **Story**: item "Acomodação" some em regime (e sai do veredito); texto do
  "Cenário" corrigido de `T_FAULT` (0.20 s) para `T_SETTLE` (0.10 s), que é a
  janela real das métricas desde 2026-07-12; pico warn diz "em regime".
- **Tabela comparativa**: linha de regime mostra "—" na coluna tₛ.

## 2026-07-14 — Cards de severidade renomeados para "V residual"

Arquivos: `src/report/renderer.py`

- **Cards**: "V min / Barra N" → "V residual B1/B2/B3" — tensão remanescente
  do afundamento (termo PRODIST Módulo 8 / IEC 61000), escolhido para
  comunicar "quanto caiu durante o curto". Subtítulos ganham o papel da
  barra: "POC do inversor (UFV)", "barra do G1 (slack)", "barra do G3".
- **Regime**: sem curto, o nome volta a "V min" (variável `vlab`).
- **Story**: item "Distúrbio" passa de "V_min = X pu" para
  "V residual = X pu".
- **Tabela comparativa** mantém "Vmin B1/B2/B3 (pu)" — cabeçalho genérico
  vale também para a linha de regime.

## 2026-07-14 — Vmin das Barras 1 e 3 (cards + tabela comparativa)

Arquivos: `src/config/settings.py`, `src/config/__init__.py`,
`src/pipeline/loader.py`, `src/report/renderer.py`

- **Loader**: métricas novas `vmin_bus1`/`vmin_bus3` — mínimo de
  `vbus1_pu`/`vbus3_pu` na mesma janela pós-falta do `vmin` (Barra 2);
  `None` quando o CSV não tem as colunas (só o legado `output/sim_data.csv`).
- **Cards**: grupo "Severidade do distúrbio" ganha "V min — Barra 1" e
  "V min — Barra 3" quando há dado (propagação do sag pela rede).
- **Tabela comparativa**: colunas "Vmin B1 (pu)" e "Vmin B3 (pu)" após a
  "Vmin B2 (pu)" (renomeada), ordenáveis como as demais.
- **Settings**: `VBUS2_MIN_THRESH` → `VBUS_MIN_THRESH` (mesma escala
  0.90/0.50 para as 3 barras); veredito LVRT segue só na Barra 2 (POC).
- ⚠️ Achado nos dados: com falta bifásica na própria B1, `vbus1` afunda
  menos (0.788) que B2/B3 (~0.235) — medição da B1 parece estar do lado
  da máquina do G1 (atrás do T1), sustentada pelo gerador. Conferir o
  ponto de medição no modelo com o Bruno.

## Entradas anteriores

- [2026-07-12](docs/changelog/2026-07-12.md) — export de correntes/tensões
  abc, T_SETTLE fora de todos os cálculos, espectro de Fourier segmentado.
- [2026-07-01 a 2026-07-05](docs/changelog/2026-07-early.md) — reestruturação
  do pacote `src/`, decimação (570 MB → 23,7 MB), tabela comparativa, fixes de
  dark mode, overlays de análise (LVRT, tₛ, frequência PLL), zoom sincronizado,
  reavaliação dos cards e veredito.
