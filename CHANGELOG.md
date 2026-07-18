# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

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

## 2026-07-12 — Export de tensões abc + painel v_a no espectro

Arquivos: `pll_stability_9bus.slx`, `scripts/export_sim_data.m`,
`src/pipeline/loader.py`, `src/pipeline/spectrum.py`

- **Modelo**: signal logging habilitado (via `matlab -batch`) nas saídas
  `Vabc_inverter`/`Vabc_grid` do subsistema `UFV Model/Scopes` (mesma
  configuração já usada em `iabc_inverter`/`iabc_grid`) — nomes de log
  `vabc_inverter`/`vabc_grid`. Confirmado no XML do `.slx`: 21 → 23 sinais
  logados.
- **`export_abc`** ganha `va/vb/vc_ufv_pu` e `va/vb/vc_grid_pu` no mesmo
  `sim_data_abc.csv` (já em pu na medição, sem normalização adicional) —
  pula em silêncio se o sinal não estiver logado, como as correntes.
- **Loader**: flags `has_vabc_ufv`/`has_vabc_grid`, arrays `va/vb/vc_ufv`
  e `va/vb/vc_grid`.
- **Espectro**: 5º painel "Tensão v_a UFV (abc)".
- ⚠️ Exige **re-exportar** os cenários (`.slx` atualizado + `git pull`
  antes de simular) — ver `.claude/kb/simulation/resimulacao-abc.md`.

## 2026-07-12 — Export de correntes abc + painel fase A no espectro

Arquivos: `scripts/export_sim_data.m`, `src/pipeline/loader.py`,
`src/pipeline/spectrum.py`

- **CSV 3 `sim_data_abc.csv`** (novo, taxa nativa): `export_abc` exporta
  `iabc_inverter` (colunas `ia/ib/ic_ufv_pu`) e, se logado, `iabc_grid`
  (`ia/ib/ic_grid_pu` interpoladas no mesmo eixo). Motivação: espectro em
  abc verdadeiro — a Park inversa perde a sequência zero das faltas à terra.
- **Loader**: carrega o CSV abc quando existe (`t_abc`, `ia/ib/ic_ufv`,
  `ia/ib/ic_grid`, flags `has_iabc_ufv`/`has_iabc_grid`); CSVs antigos
  seguem funcionando sem ele.
- **Espectro**: 4º painel "Corrente i_a UFV (abc)" quando há dados abc.
  Contexto (validado com fase A reconstruída): em abc a fundamental fica em
  60 Hz (~0 dB) e a **sequência negativa cai também em 60 Hz** — invisível
  (+0.1 dB na falta 1φ); o ripple dq de 120 Hz vira banda lateral em 180 Hz
  (−14.7 dB). Por isso o painel abc **complementa** os painéis dq (onde a
  seq. negativa aparece isolada em 120 Hz), não os substitui.
- ⚠️ O painel só aparece após **re-exportar** os cenários no MATLAB
  (os CSVs atuais não têm abc).

## 2026-07-12 — T_SETTLE: partida do PLL fora de todos os cálculos

Arquivos: `src/config/settings.py`, `src/config/__init__.py`,
`src/pipeline/loader.py`, `src/pipeline/spectrum.py`

Motivação (pedido do usuário): o PLL leva ~0.08 s para travar na rede no
início da simulação — esse transitório é partida, não falta de desempenho,
e não deve contaminar métrica nenhuma, principalmente o Fourier.

- **Nova constante `T_SETTLE = 0.1 s`**: medida nos dados (bus6/1phase) —
  o sinal mais lento é |V| Bus 2, que acomoda em 0.078 s (θ_err em 0.039 s,
  P em 0.034 s, Q em 0.062 s). 0.1 s dá margem e ainda deixa 0.2 s de
  pré-falta limpo antes de t_fault = 0.3 s.
- **Espectro de Fourier**: janela pré-falta passa de `[T_FAULT=0.2, t_fault]`
  para `[T_SETTLE=0.1, t_fault]` — exclui a partida por critério documentado
  (antes era acidente da constante de fallback) e **dobra a janela**:
  resolução de 10 Hz → 5 Hz. Regime usa `[T_SETTLE, t_end]`.
- **Integrais IAE/ISE e demais métricas** (`_compute_metrics`): janelas
  clampadas em `max(t_fault, T_SETTLE)`; regime usa `T_SETTLE` no lugar de
  `T_FAULT`. Com t_fault = 0.3 s nos cenários atuais, os valores de falta
  não mudam — o clamp protege cenários futuros com falta precoce.
- **Fora do escopo (decisão do usuário: só Python)**: a normalização pu no
  MATLAB (`export_sim_data.m`, `Vnom = mean(vmag(t < T_FAULT))`) ainda
  inclui a partida → viés de ~1.1% nas colunas `vbus*_pu`/`vd/vq`
  (regime fica em 0.9887 pu em vez de 1.0). Corrigir exige editar o .m e
  re-exportar os cenários.

## 2026-07-12 — Espectro de Fourier segmentado (pedido do orientador)

Arquivos: `src/pipeline/spectrum.py` (novo), `src/config/settings.py`,
`src/__init__.py`, `src/pipeline/__init__.py`, `app.py`,
`src/report/renderer.py`, `.claude/kb/dashboard/graficos/espectro-fourier.md`

- **Nova seção "Espectro de Fourier — referencial dq"**: FFT de amplitude
  (Hann, média removida, grade uniforme por reamostragem) de θ_err, i_q e
  Q UFV, com um traço por segmento temporal — **pré-falta** (cinza),
  **falta** (vermelho), **pós-falta** (azul); cenário de regime vira traço
  único. Eixo y em **dB re 1 pu/rad** (20·log10, piso −100 dB), formato
  Amplitude (dB) × Hz da literatura, pedido do orientador; x default
  0–1500 Hz (duplo-clique expande até 2 kHz).
- **Marcadores físicos**: vlines em 120 Hz (2ª harmônica no dq = sequência
  negativa da falta assimétrica) e 1443 Hz (ressonância do filtro LCL).
- **Validação**: falta 1φ bus6 → pico de 120 Hz no θ_err durante a falta
  12× maior que na 3φ equivalente (2,73e-2 vs 2,20e-3 rad).
- Integrado ao tema dark/light, ao seletor de cenário e ao fantasma
  nominal×BAD_PLL; zoom na falta (domínio do tempo) não afeta o espectro.
- Custo no HTML: ~95 KB/cenário (~1,7 MB total).

## Entradas anteriores

- [2026-07-01 a 2026-07-05](docs/changelog/2026-07-early.md) — reestruturação
  do pacote `src/`, decimação (570 MB → 23,7 MB), tabela comparativa, fixes de
  dark mode, overlays de análise (LVRT, tₛ, frequência PLL), zoom sincronizado,
  reavaliação dos cards e veredito.
