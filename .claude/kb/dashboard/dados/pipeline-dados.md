---
name: pipeline-dados
description: SimData (loader.py) — leitura dos CSVs do MATLAB, correção do erro de fase, métricas IAE/ISE/tₛ/ΔP/ΔQ/Vmin e frequência estimada do PLL
---

# Pipeline de Dados (src/pipeline/loader.py)

`SimData(csv_path)` carrega um cenário e expõe arrays NumPy + `metrics`.
Descoberta de cenários e roteamento BAD_PLL: ver `kb/simulation/export_workflow.md`.

## Dois CSVs por cenário + fault_info.json

| Arquivo | Taxa | Conteúdo |
|---|---|---|
| `sim_data.csv` | Tsc = 200 µs (eixo lento `t`) | P/Q UFV, correntes dq, tensões de barra, P/Q de barra, geradores |
| `sim_data_angles.csv` | Ts = 5 µs (eixo rápido `t_fast`) | `theta_pll_rad`, `theta_ref_rad`, `theta_err_rad` |
| `fault_info.json` | — | `fault_type`, `t_fault`, `t_clear` reais do cenário |

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

## Métricas pós-falta (`_compute_metrics`)

Janela: `t >= t_fault`. Integrais por `np.trapezoid`.

| Métrica | Definição |
|---|---|
| `IAE` | ∫\|e\|dt (rad·s) |
| `ISE` | ∫e²dt (rad²·s) |
| `ts` | última amostra com \|e\| > `TOL_RAD` (±0.02 rad ≈ ±1.15°); se nunca sai, primeiro instante pós-falta |
| `dP_ufv`, `dQ_ufv` | max − min de P/Q pós-falta (pu) |
| `vmin` | mínimo de `vbus2` pós-falta (pu) — comparado ao LVRT |

Sinal ausente → métrica `None` → "—" nos cards/tabela.

## Frequência estimada do PLL (`_estimate_freq`)

`f̂ = dθ̂/dt / 2π` sobre o ângulo **unwrapped**, por diferença central com
passo largo (k amostras ≈ 0,5 ms para cada lado, ~1 ms de janela):

- O passo largo já atua como filtro passa-baixa — suprime ripple de
  chaveamento sem convolução sobre milhões de pontos de 5 µs (O(n)).
- Usa `theta_pll_fast` (fallback `theta_pll`); expõe `f_pll`, `t_freq`
  (encurtado em k de cada lado) e a flag `has_freq`.
- Alimenta o painel "Frequência PLL (Hz)" — ver [[chart-analysis-overlays]].
