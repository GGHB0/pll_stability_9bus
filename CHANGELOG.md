# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

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
