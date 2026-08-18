# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

## 2026-08-17 — Aba "Sistema 9-Bus" renomeada para "Barras de Geração"

Arquivos: `src/report/renderer.py`, `src/pipeline/chart.py`

A pedido do usuário. Três ocorrências do rótulo trocadas:

- Botão da `tab-bar` (`#tab-sys`).
- Cabeçalho `.section-title` da seção `#sec-sys`.
- Título do grupo de cards de topologia/severidade na aba Resumo, exibido
  quando o cenário é regime permanente (`sev_label` em `_group_severidade`,
  antes idêntico ao nome da aba) — confirmado com o usuário que também
  deveria mudar, já que reutilizava o mesmo texto.

Comentário de docstring em `chart.py` atualizado por consistência. Nenhuma
mudança de comportamento — só rótulo. Verificado no browser pane (servido
via `python -m http.server`): botão, cabeçalho da seção e grupo de cards do
Resumo (cenário `regime`) todos exibindo "Barras de Geração".

## 2026-08-11 — Tabela de critérios na legenda da tabela de harmônicas

Arquivos: `src/report/renderer.py`, `scripts/notas/gen_normas_harmonicos.py`

A pedido do usuário: a formatação condicional da tabela de harmônicas só era
explicada em prosa dentro do `<details>` "Como ler esta tabela". Faltava o
resumo escaneável de *qual limite gera qual cor* — que já existia, em papel,
na seção 6.1 da nota `output/normas_harmonicos.pdf`.

- Novo `HTMLRenderer._harm_criteria_html`: tabela *Grandeza e ordem / Limite /
  Cor / Norma* no topo do `<details>`, com os swatches reais em vez de
  descrever a cor por extenso. A prosa em `<dl>` continua abaixo, como
  detalhamento — não foi substituída.
- **Todos os números vêm de `settings.py`**, nenhum escrito à mão, para a
  tabela não dessincronizar do que `_harm_cell_tier` de fato aplica. Linha
  "Durante a falta" (base ×1,5) só aparece quando `has_relaxed_seg`.
- Helper `_sw(*classes)` reaproveita as classes `.harm-leg-*` da linha
  compacta de legenda; CSS novo `.harm-crit`/`.harm-crit-sw`/`.harm-crit-note`.
- Corrigida uma lacuna achada no caminho: a linha compacta de legenda não
  trazia o swatch **azul da fundamental** (`.harm-leg-fund`, `--accent`),
  embora a tabela destaque a fundamental nessa cor desde 2026-08-05.
- Verificado no browser pane (servido via `python -m http.server`): swatches
  resolvem os tokens certos nos dois temas (claro `#dc2626`/`#ca8a04`/
  `#2563eb`/`#64748b`, escuro `#f87171`/`#fbbf24`/`#60a5fa`/`#9ca3af`); linha
  "Durante a falta" aparece em `bus4/1phase` e some em cenário de regime.
- Nota `normas_harmonicos.pdf` atualizada em paralelo (coluna "Cor" na tabela
  6.1, pontos coloridos na 6.4). Achados do `note-validator` corrigidos junto:
  **IEEE C57.110 citado no corpo mas ausente da bibliografia** (só constava o
  C57.12.00-2000, que é outro standard — a cláusula 7.3.3 invoca os dois para
  coisas diferentes); redação "antes da falta" trocada por "colunas Pré-falta
  e Regime", já que *Regime* é o segmento único dos cenários sem falta; e as
  faixas de ordem ímpar passaram de "3 a 10"/"11 a 16" (bordas do teste no
  código) para "3ª à 9ª"/"11ª à 15ª" (as ordens reais).
- Docs: `.claude/kb/dashboard/graficos/espectro-tabela-harmonicas.md`, que
  também ganhou o registro — até então ausente da KB — da **exceção do âmbar
  na 2ª harmônica de corrente** (`kind=="i", k==2`, segmentos Pré-falta e
  Regime), comportamento em produção desde a correção do vazamento espectral.

## 2026-08-11 — FFT mede a frequência real por segmento (abc) em vez de 60 Hz fixo

Arquivo: `src/pipeline/spectrum.py`

Achado de 2026-08-10 (`kb/standards/harmonic_frequency_leakage.md`): a "2ª
harmônica" de 1,3-2,1% na coluna pré-falta de todo cenário era vazamento
espectral, não distorção real — a rede simulada nunca fecha em 60,000 Hz
exatos (resposta de droop dos geradores síncronos ainda em curso) e a janela
da FFT truncava por `F_FUND_HZ` fixo, desalinhada do ciclo real do sinal.

- Nova função `_measure_f1`: mede a frequência real por cruzamento de zero
  ascendente (interpolado linearmente), com fallback para `F_FUND_HZ` se
  houver menos de 3 cruzamentos ou o resultado fugir de 50-70 Hz.
- `_amplitude_spectrum` e `_harmonics` ganham o parâmetro `f1` (default
  `F_FUND_HZ`), usado no truncamento da janela e na busca do bin — o índice
  de ordem na tabela (rótulo "120 Hz" pra 2ª) continua nominal.
- `_mode_fig` mede `f1` só em modo **abc** (`mode in ("a","b","c")`); em dq a
  fundamental vira DC e cruzamento de zero não se aplica, mantém `F_FUND_HZ`.
- Efeito medido (Regime, corrente, fase a): 3ª harmônica cai de 0,55% para
  0,08%, 4ª de 0,46% para 0,15% — o realinhamento elimina quase todo o
  vazamento nos harmônicos mais distantes da fundamental. A 2ª cai só de
  1,70% para 1,42%: a rede não está só deslocada de 60 Hz, está em **chirp
  contínuo** (frequência ainda caindo ao longo da janela de 0,5 s), e uma
  única `f1` média por janela não cancela o alargamento espectral desse
  chirp — mais pronunciado perto da fundamental. Residual documentado em
  `kb/standards/harmonic_frequency_leakage.md`, não é bug.

## 2026-08-09 — Medição de harmônicas conforme IEEE 519 §4.1 e relaxamento ×1,5 na falta

Arquivos: `src/pipeline/spectrum.py`, `src/report/renderer.py`,
`src/config/settings.py`, `src/config/__init__.py`

Duas divergências normativas levantadas na leitura integral das duas normas
(ver `kb/standards/harmonic_measurement_conditions.md`) foram fechadas.

- `_harmonics`: a amplitude de cada harmônica passa de **pico local** para a
  **combinação RMS do bin central com os dois vizinhos**, que é a definição do
  IEEE 519-2014 §4.1 ("the three values are combined into a single rms value").
- `_amplitude_spectrum` ganha o parâmetro `window`. A tabela passa a ler um
  espectro de janela **retangular** calculado à parte; o gráfico continua com
  **Hann**. Motivo: o agrupamento de 3 bins sobre Hann superestima em **22,5%**
  (a Hann distribui um tom como `[A/2, A, A/2]`, soma quadrática = √1,5·A).
  Confirmado nos dados: a fundamental de `bus4/1phase` saía 1,2254 pu e agora
  sai 1,0006 pu. A retangular é válida porque a janela já é truncada a ciclos
  inteiros.
- Bug de ponto flutuante no truncamento: `floor(0.2*60)` devolvia **11** ciclos
  onde há 12, porque o produto dá 11,999999. Corrigido com `+1e-9`. Com isso
  `df` volta a ser **5,000 Hz** exatos no pré/pós-falta, a grade do §4.1.
- `SPEC_SEG_NO_NORM` (segmentos isentos) → `SPEC_SEG_LIMIT_FACTOR`
  (`{"Durante a falta": 1.5}`). A nota 118 do IEEE 1547.2-2023 **relaxa** os
  limites em 50% em condição inusual, não os suprime. Ímpar vira 6%, 2ª vira
  1,5%; tooltip cita limite base, fator e a nota; legenda e `*` do cabeçalho
  reescritos. **O segmento de falta passou a acusar violações**, onde antes
  nenhuma célula era destacada. O critério de desequilíbrio dq não é relaxado.
- Corrigido o sombreamento de `dc` (componente DC) pela cor escura do segmento
  em `_mode_fig` — era inócuo na ordem atual, mas frágil.
- Verificado: `app.py` roda os 26 cenários; HTML traz 96 marcações `*` no
  cabeçalho e 307 tooltips citando a nota 118.

## 2026-08-09 — Remoção dos cards de erro de ângulo (grupo "Desempenho do PLL")

Arquivos: `src/report/renderer.py`, `src/pipeline/loader.py`,
`src/config/settings.py`, `src/config/__init__.py`,
`notebooks/dashboard_cards_explainer.ipynb`

- A pedido do usuário: **não foi encontrada fonte que comprove** que acúmulo
  (IAE/ISE), média (Erro R.P.) e pico do erro de ângulo `θ̂ − θ_rede` medem
  desempenho do PLL. Sem base bibliográfica os números não podem ir para o
  TCC nem sustentar um veredito, então o grupo inteiro saiu do relatório.
- `renderer.py`: `_cards_html` perde os 5 cards e o `_group("Desempenho do
  PLL", ...)` — resta só o grupo de severidade. `_table_row_data` e o
  cabeçalho/JS da tabela comparativa perdem as colunas `iae`/`ise`/`ts`/
  `peak` (sobram as 3 de tensão). `_story_html` perde os itens "Pico de
  fase", "Acomodação", "Erro de regime" e "Erro acumulado" **e o chip de
  veredito** (era calculado só com essas métricas); o bloco passa a ser
  sempre `neutral` e o título vira "Contexto do cenário" / "Contexto —
  regime permanente" (era "Diagnóstico pós-falta"). CSS `.story-verdict` e
  `.story.good/.warn/.bad` removidos.
- `settings.py`/`config/__init__.py`: `IAE_THRESH`, `ISE_THRESH`,
  `TS_DELTA_THRESH`, `PEAK_ERR_DEG_THRESH`, `ERR_SS_DEG_THRESH` e
  `SYNC_LOSS_DEG` deletados. `VBUS_AVG_THRESH` é o único threshold restante.
- `loader.py`: `_compute_metrics` deixa de calcular `IAE`, `ISE`,
  `peak_err`, `ts_delta`, `t_ss`, `err_ss_mean`, `err_ss_rms`.
- **`ts`/`settled` ficaram** (decisão explícita do usuário): o instante de
  acomodação importa porque interessa saber *como o PLL retorna pós-falta*.
  O painel "Erro de fase", a faixa ±1,15° e o marcador tₛ seguem intactos —
  só a exibição como card com semáforo saiu. O critério de ±0,02 rad em si
  fica para revisão numa sessão futura.
- Notebook explainer: seções 4.1/4.2/4.4/4.5 removidas, 4.3 (tₛ) virou a
  seção 4, recorte `_t_pf`/`_e_pf` movido para a seção 3, verificação
  cruzada reduzida ao `ts`. Reexecutado: 32 células, todas OK (`ts` manual =
  `0.49723` = valor de produção).
- Verificado: `app.py` roda os 26 cenários; no HTML gerado restam só os
  cards de severidade (V médio/residual B1-B3, Duração, Topologia), 4
  colunas na tabela comparativa e o story com "Distúrbio"/"Cenário" +
  "Topologia"; 13 marcadores tₛ preservados nos gráficos.

## Entradas anteriores

- [2026-08-05](docs/changelog/2026-08-05.md) — linha de 0 Hz (fundamental em
  DC) na tabela dq, tabela de harmônicas separada em abc e dq.
- [2026-08-03](docs/changelog/2026-08-03.md) — card e item de diagnóstico
  "Topologia" (line7_8 vs. line8_9, circuito único vs. duplo).
- [2026-08-02](docs/changelog/2026-08-02.md) — teto fixo em 1 pu no eixo Y
  do espectro FFT, legenda explicada da tabela de harmônicas.
- [2026-07-28 a 2026-07-30](docs/changelog/2026-07-28_30.md) — faixa de
  frequência ONS §5.2.1 no painel "Frequência PLL" (depois removido),
  destaque normativo (IEEE 519/1547) na tabela de harmônicas, remoção do
  painel "Frequência PLL".
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
