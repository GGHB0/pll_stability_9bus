---
name: python-pipeline
description: Arquitetura Python (src/) que consome sim_data.csv — SimData, ChartBuilder, painéis, métricas
---

# Pipeline Python: `src/`

```
app.py                  ← entry point (python app.py [--out PATH]); varre output/results/**/sim_data.csv
src/
├── __init__.py         → reexporta SimData, ChartBuilder, HTMLRenderer (API pública)
├── config/
│   └── settings.py     → T_FAULT, TOL_RAD, thresholds, paletas, caminhos
├── pipeline/            → CSV → dados → figuras Plotly
│   ├── loader.py         → SimData: lê sim_data.csv + sim_data_angles.csv, calcula métricas
│   └── chart.py           → ChartBuilder: subplots Plotly (usa t_fast p/ painéis de ângulo)
└── report/               → figuras → HTML
    └── renderer.py         → HTMLRenderer: HTML multi-cenário com tema light/dark
```

Reorganizado em subpacotes (2026-07) — antes eram 4 arquivos soltos em `src/`.
`src/__init__.py` continua a única superfície pública; `app.py` não referencia
os subpacotes diretamente. Imports internos usam `..config`/`..pipeline` (relativos
ao nível do subpacote, não ao topo de `src/`).

Ver `kb/simulation/export_workflow.md` para o formato de `sim_data.csv` consumido aqui.

## Painéis gerados por `ChartBuilder`

### Seção Inversor (`_inv_rows`)

| Painel | Kind | Condição | Conteúdo |
|--------|------|----------|----------|
| Ângulo (°) | `ang` | `has_ang` | θ Rede + θ̂ PLL |
| Erro de fase (°) | `err` | `theta_err is not None` | erro com banda ±TOL_RAD |
| Corrente dq UFV (pu) | `dq_combined` | `has_dq_ufv` | id/iq medido (+ ref se `has_ref_ufv`) |
| Tensão dq (pu) | `vdq_combined` | `has_vdq_ufv or has_vdq_rede` | Vd/Vq rede + inversor |
| P / Q UFV (pu) | `pq_combined` | sempre | P e Q do UFV |

### Seção Sistema (`_sys_rows`)

Painéis agrupados por barra (não combinados), na ordem Bus 2 → Bus 1 → Bus 3
— facilita comparar cada barra isoladamente:

| Painel | Kind | Condição | Conteúdo |
|--------|------|----------|----------|
| \|V\| Bus 2 (pu) | `vbus2` | `has_vbus2` | \|V\| Bus 2 + linha LVRT |
| \|V\| Bus 1 (pu) | `vbus1` | `has_vbus1` | \|V\| Bus 1 + linha LVRT |
| P Bus 1 (pu) \| Q Bus 1 (pu) | `p_bus1` / `q_bus1` | `has_pq_bus1` | P/Q da Barra 1, lado a lado |
| \|V\| Bus 3 (pu) | `vbus3` | `has_vbus3` | \|V\| Bus 3 + linha LVRT |
| P Bus 3 (pu) \| Q Bus 3 (pu) | `p_bus3` / `q_bus3` | `has_pq_bus3` | P/Q da Barra 3, lado a lado |

> Painéis "Ângulo rotor (δ G1/G3)" e "Pe geradores" foram **removidos** (2026-07) —
> ângulo de rotor não normalizado crescia linearmente e perdeu relevância na análise
> atual. Os dados brutos (`ang_g1`, `pe_g1`, `ang_g3`, `pe_g3`) continuam sendo
> exportados/carregados por `SimData`, só não são mais plotados.

## Lógica de leitura em `SimData`

1. Lê `sim_data.csv` → `self.t`, `self.P_ufv`, `self.Q_ufv`, correntes dq UFV.
2. Procura `sim_data_angles.csv` na mesma pasta:
   - **Se existe**: carrega `t_fast`, `theta_pll_fast`, `theta_ref_fast`; aplica
     baseline correction (remove drift pré-falta); interpola `theta_err` para `self.t`.
   - **Fallback legado**: lê colunas de ângulo de `sim_data.csv` se presentes.
3. Cada grupo de colunas opcionais expõe um par `has_X` (bool) + atributo(s) `None`
   quando ausente — permite CSVs antigos carregarem sem erro.

## Atributos expostos por `SimData` (além de ângulo/dq/vdq)

| Atributo | Flag | Descrição |
|---|---|---|
| `vbus1`, `vbus2`, `vbus3` | `has_vbus1/2/3` | \|V\| de barra, pu relativo à média pré-falta |
| `p_bus1`, `q_bus1` | `has_pq_bus1` | P/Q Barra 1, pu (base 100 MVA) |
| `p_bus3`, `q_bus3` | `has_pq_bus3` | P/Q Barra 3, pu (base 100 MVA) |
| `ang_g1`, `pe_g1` | `has_gen1` | ângulo (rad) / Pe (pu) do rotor G1 — **não plotado**, só carregado |
| `ang_g3`, `pe_g3` | `has_gen3` | idem para G3 — **não plotado**, só carregado |

## Métricas calculadas (`_compute_metrics`)

| Métrica (chave dict) | Fórmula | Janela |
|---|---|---|
| `IAE` | ∫\|θ_err\| dt | t ≥ T_FAULT |
| `ISE` | ∫θ_err² dt | t ≥ T_FAULT |
| `ts` | último t com \|θ_err\| > TOL_RAD | t ≥ T_FAULT |
| `dP_ufv` | max(P_ufv) − min(P_ufv) | t ≥ T_FAULT |
| `dQ_ufv` | max(Q_ufv) − min(Q_ufv) | t ≥ T_FAULT |
| `vmin` | min(vbus2_pu) | t ≥ T_FAULT |

`np.trapezoid` (NumPy ≥ 2.0). Baseline correction: subtrai `theta_err[idx_fault-1]`
antes de `T_FAULT` para zerar drift da Repeating Sequence de referência.

## Rodar

```powershell
# Exportar do MATLAB (após simular): >> export_sim_data   (Command Window)

.venv\Scripts\python.exe app.py
.venv\Scripts\python.exe app.py --out output/relatorio.html
```
