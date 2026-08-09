---
name: cards-explainer-notebook
description: Notebook didático que reimplementa manualmente o cálculo de cada card do dashboard, com verificação cruzada contra o pipeline real
---

# Notebook explicativo dos cards (`dashboard_cards_explainer.ipynb`)

`notebooks/dashboard_cards_explainer.ipynb` — referência viva de **como**
cada card de `output/pll_metrics.html` chega ao valor mostrado, célula a
célula, com números reais. Complementa [[cards-metricas]] e
[[espectro-fourier]] (que documentam decisões de design/UX), sem repetir o
conteúdo delas.

## Cenários usados

Ambos com PLL **nominal** (bem sintonizado, sem `_bad_pll`), arbitrários
entre os disponíveis:

- `output/results/regime/` — regime permanente (sem falta).
- `output/results/bus7/3phase/` — curto trifásico simétrico na Barra 7
  (`t_fault=0.30 s`, `t_clear=0.40 s`).

## Abordagem: reimplementação manual + verificação cruzada

Cada seção **reimplementa a fórmula manualmente** em NumPy/Pandas (não
chama `SimData`/`SpectrumBuilder` para o cálculo em si), com o arquivo e a
linha do código-fonte (`loader.py`, `spectrum.py`, `renderer.py`) citados
em markdown — mais didático que importar a classe pronta. Constantes de
`src/config/settings.py` (`T_SETTLE`, `TOL_RAD`, `F_FUND_HZ`, ...) **são**
importadas diretamente (não duplicadas), por serem configuração, não lógica
de card.

Para não deixar a cópia divergir do código real com o tempo, toda seção
termina com uma célula de **verificação cruzada**: importa a classe de
produção só para aquele cenário e confere (`assert np.isclose(...)`) que o
valor manual bate com `SimData.metrics`/`SpectrumBuilder().build()`. Se a
fórmula de produção mudar sem o notebook acompanhar, a célula quebra ao
rodar.

## Regra de manutenção

**Card novo ou removido em `src/report/renderer.py::_cards_html` → a seção
correspondente deste notebook entra/sai junto.** A última seção do notebook
("Cards atuais e política de sincronismo") mantém três tabelas que devem
acompanhar qualquer mudança: cards atuais (card → grupo → fonte → seção),
cálculos que não são card mas seguem no pipeline (θ_err, tₛ), e o histórico
de cards removidos com o motivo.

## Seções

1. Setup (carga dos CSVs brutos + constantes de `settings.py`)
2. Erro de fase (θ_err) — wrap `atan2(sin,cos)` + baseline em `t_fault`
3. Janela de métricas (`t_start`) — inclui o recorte `_t_pf`/`_e_pf`
   reutilizado pela seção 4
4. Acomodação do erro de fase (tₛ) — **não é card**, alimenta o marcador do
   painel "Erro de fase"
5. Cards — Severidade: V médio B1/B2/B3, Duração, Topologia (nota: é tabela
   estática, não cálculo — não se aplica ao cenário `bus7/3phase` usado)
6. **Espectro de Fourier (FFT)**, seções dedicadas (pedido explícito do
   usuário — pipeline menos documentado de forma didática antes disso):
   segmentação temporal, pré-processamento (`_amplitude_spectrum`:
   reamostragem, truncamento em ciclos inteiros, remoção de DC, janela de
   Hann), extração de harmônicas (`_harmonics`, pico ±1,5 bin), abc × dq
   (fundamental em 60 Hz vs. DC; nota de que o cenário simétrico escolhido
   deixa a seq. negativa em 120 Hz próxima de zero, ao contrário do que uma
   falta assimétrica mostraria), comparação visual regime × curto
7. Cards atuais e política de sincronismo (tabela de inventário)

## Gotcha replicado do código real

A correção de baseline do erro de fase (`loader.py:100`) usa
`T_FAULT` (fallback, 0,2 s) quando `t_fault is None` — isso inclui o
cenário **regime**, que não tem falta. Ou seja, mesmo em regime o baseline
é tirado em t=0,2 s, não em t=0. O notebook replica esse comportamento por
fidelidade ao valor que efetivamente aparece no relatório (a verificação
cruzada bate exatamente com `SimData.theta_err`).

## Remoção das seções de erro de ângulo (2026-08-09)

Com o grupo "Desempenho do PLL" fora do dashboard ([[cards-metricas]]), as
subseções **4.1 (IAE), 4.2 (ISE), 4.4 (\|θ_err\| pico) e 4.5 (Erro R.P.)**
saíram do notebook — a regra de manutenção acima obriga. A antiga **4.3
(tₛ) virou a seção 4** inteira e ficou: o cálculo continua vivo no
`loader.py` e alimenta o marcador do gráfico ([[chart-analysis-overlays]]).

Dois ajustes que a remoção exigiu:

- O recorte da janela (`_t_pf`/`_e_pf`) morava dentro da célula da IAE, mas
  é recorte, não cálculo de card — **movido para a seção 3**, de onde o tₛ
  passa a consumi-lo.
- A célula de verificação cruzada da seção 4 confere só `ts` agora; os
  `assert` de `IAE`/`ISE`/`peak_err`/`err_ss_mean` saíram porque essas
  chaves não existem mais em `SimData.metrics`.
- O import de `IAE_THRESH`/`ISE_THRESH`/`TS_DELTA_THRESH`/
  `PEAK_ERR_DEG_THRESH`/`ERR_SS_DEG_THRESH` na célula de setup foi
  removido — as constantes não existem mais em `settings.py`.

## Validação

- **2026-08-05**: todas as 40 células executadas fora do Jupyter (via `exec`
  sequencial com o Python do `.venv`, sem `fig.show()`) — verificações
  cruzadas todas OK.
- **2026-08-09**: reexecutado após a remoção — 32 células, todas OK
  (`ts` manual = `0.49723` = `SimData.metrics["ts"]`; `vavg*` e harmônicas
  inalterados).
