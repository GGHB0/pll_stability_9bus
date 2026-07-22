---
name: pipeline-dados
description: SimData (loader.py) — leitura dos CSVs do MATLAB, correção do erro de fase, métricas em duas janelas (IAE/ISE/tₛ/pico pós-falta; ΔP/ΔQ pós-clear) e frequência estimada do PLL
---

# Pipeline de Dados (src/pipeline/loader.py)

`SimData(csv_path)` carrega um cenário e expõe arrays NumPy + `metrics`.
Descoberta de cenários e roteamento BAD_PLL: ver `kb/simulation/export_workflow.md`.

## Três CSVs por cenário + fault_info.json

| Arquivo | Taxa nominal | Conteúdo |
|---|---|---|
| `sim_data.csv` | Tsc = 200 µs (eixo `t`) | P/Q UFV, correntes dq, tensões de barra, P/Q de barra, geradores |
| `sim_data_angles.csv` | Ts = 5 µs (eixo `t_fast`) | `theta_pll_rad`, `theta_ref_rad`, `theta_err_rad` |
| `sim_data_abc.csv` | nativa de `iabc_inverter` (eixo `t_abc`) | `ia/ib/ic_ufv_pu` + `va/vb/vc_ufv_pu` (+ `_grid_pu` de ambos se logado) — flags `has_iabc_ufv`/`has_vabc_ufv`/`_grid`; opcional, paineis abc do espectro |
| `fault_info.json` | — | `fault_type`, `t_fault`, `t_clear` reais do cenário |

> ⚠️ **Taxas invertidas nos CSVs atuais** (medido 2026-07-12): `sim_data.csv`
> está com dt = 5 µs (120.001 amostras/0,6 s) e `sim_data_angles.csv` com
> dt = 200 µs (3.001 amostras) — o oposto do nominal acima. Loader e
> SpectrumBuilder são imunes (interpolação/`dt` mediano), mas o "eixo rápido"
> dos ângulos hoje tem MENOS resolução que o lento. Verificar no modelo se a
> troca de decimação no logging foi intencional antes de confiar em análises
> que dependam da resolução de θ (ripple de chaveamento, por ex.).

- `fault_type == "regime"` → `t_fault = t_clear = None` (sem linhas de falta,
  botão de zoom desabilitado no HTML).
- Sem `fault_info.json` → fallback `T_FAULT` de `config/settings.py`.
- Colunas opcionais viram flags `has_*` (`has_dq_ufv`, `has_vbus2`, `has_gen1`,
  `has_pq_bus1`, `has_vdq_ufv`, …) — o ChartBuilder só monta painel se a flag
  estiver ligada. Geradores usam sufixo `_g1`/`_g3`.

## Correção do erro de fase (theta_err)

1. **Wrapping**: `Ang_pll`/`Ang_Rede` são dente-de-serra (0→2π→0); a diferença
   bruta tem spikes de ±2π em resets desalinhados. `arctan2(sin, cos)` leva
   para [−π, π].
2. **Baseline**: subtrai o valor do erro na última amostra antes de `t_fault`,
   re-wrapping em seguida — IAE/ISE/tₛ medem só o desvio induzido pela falta,
   não o drift pré-existente do Repeating Sequence de referência.
3. A mesma correção (wrapping + baseline do eixo lento) é aplicada ao eixo
   rápido `theta_err_fast`.

O erro do eixo rápido é interpolado para o eixo lento (`np.interp`) antes da
correção — as métricas são calculadas no eixo lento.

## Métricas (`_compute_metrics`) — duas janelas

- **Pós-falta** (`t ≥ max(t_fault, T_SETTLE)`): erro de fase (IAE/ISE/tₛ/pico)
  e `vmin`.
- **Pós-clear** (`t ≥ max(t_clear, T_SETTLE)`): `dP_ufv`/`dQ_ufv` — mede a
  *recuperação*, não o colapso durante o afundamento (senão toda falta daria
  ΔP ≈ 1 pu).
- **Regime** (`t_fault` None): ambas viram `t ≥ T_SETTLE`.

**`T_SETTLE = 0.1 s`** (settings.py, 2026-07-12): nenhuma janela de cálculo
começa antes disso — a partida do PLL (trava em ~0.08 s; pior sinal é |V|
Bus 2 em 0.078 s) é inicialização, não desempenho, e fica fora das integrais
e da FFT ([[espectro-fourier]]). Com `t_fault = 0.3 s` nos cenários atuais o
clamp é inócuo nas faltas; muda o regime (antes usava `T_FAULT = 0.2` de
fallback). ⚠️ A normalização pu do MATLAB (`Vnom = mean(vmag(t < T_FAULT))`
em `export_sim_data.m`) ainda inclui a partida → viés de ~1.1% em
`vbus*_pu`/`vd/vq` (regime lê 0.9887 pu); correção ficou fora do escopo
(decisão do usuário: só Python) e exigiria re-exportar.

| Métrica | Definição |
|---|---|
| `IAE` | ∫\|e\|dt (rad·s), pós-falta |
| `ISE` | ∫e²dt (rad²·s) |
| `peak_err` | max \|e\| pós-falta (rad) — cards mostram em °, ≥90° = perda de sincronismo |
| `ts` / `settled` | última amostra com \|e\| > `TOL_RAD` (±0.02 rad ≈ ±1.15°). Se \|e\| ainda está fora nos últimos 2 ms da janela → `ts = None`, `settled = False` ("não acomodou" — evita tₛ falso no fim da simulação). **Regime → sempre `None`/`None`**: sem distúrbio não há o que acomodar (card omitido, "—" na tabela) |
| `ts_delta` | `ts − t_fault` (base da classificação good/warn/bad) |
| `t_ss` | início do regime: `ts` se `settled`, `T_SETTLE` em regime, senão `None` |
| `err_ss_mean`, `err_ss_rms` | erro de fase **sustentado** em R.P. — média/RMS de \|e\| para `t ≥ t_ss` (rad; cards em °). `None` se a falta não reacomodou. Separa o erro de regime do `peak_err` transitório (Ponto 1 do professor, 2026-07-21) |
| `dP_ufv`, `dQ_ufv` | max − min de P/Q **pós-clear** (pu) |
| `vmin` | mínimo de `vbus2` pós-falta (pu) — severidade do sag vs LVRT |
| `vmin_bus1`, `vmin_bus3` | idem para `vbus1`/`vbus3` — propagação do sag pela rede (cards de severidade + colunas Vmin B1/B3 na tabela; veredito LVRT continua só na B2) |

Sinal ausente → métrica `None` → "—" nos cards/tabela.

## Frequência estimada do PLL (`_estimate_freq`)

`f̂ = dθ̂/dt / 2π` sobre o ângulo **unwrapped**, por diferença central com
passo largo (k amostras ≈ 0,5 ms para cada lado, ~1 ms de janela):

- O passo largo já atua como filtro passa-baixa — suprime ripple de
  chaveamento sem convolução sobre milhões de pontos de 5 µs (O(n)).
- Usa `theta_pll_fast` (fallback `theta_pll`); expõe `f_pll`, `t_freq`
  (encurtado em k de cada lado) e a flag `has_freq`.
- Alimenta o painel "Frequência PLL (Hz)" — ver [[chart-analysis-overlays]].

## Consumidores do SimData

- `ChartBuilder` (séries temporais) — [[construcao-graficos]].
- `SpectrumBuilder` (FFT segmentada pré-falta/falta/pós-falta em dB) —
  consome `t`/`t_fast`, `theta_err(_fast)`, `iq_ufv_meas`, `Q_ufv` e
  `t_fault`/`t_clear`; ver [[espectro-fourier]].
- `HTMLRenderer` (cards/story/tabela) — usa `metrics` direto.
