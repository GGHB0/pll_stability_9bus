---
name: export-workflow
description: Como extrair sinais do Simulink e exportar para Python via CSV — workflow validado para o modelo pll_stability_9bus
---

# Export Workflow: Simulink → MATLAB → Python

## Sinais disponíveis no logsout

Após rodar a simulação, o workspace contém `logsout_IEEE9BusLoadflow` (Simulink.SimulationData.Dataset) com 8 sinais logados:

| Nome no logsout | Conteúdo | Dimensão |
|---|---|---|
| `Pinverter` | Potência ativa do inversor (pu) | escalar |
| `Qinverter` | Potência reativa do inversor (pu) | escalar |
| `Ang_pll` | Ângulo estimado pelo PLL θ̂ (rad) | escalar |
| `Ang_Rede` | Ângulo de referência da rede θ_ref (rad) | escalar |
| `id` | Corrente de eixo d (pu) | vetor 2 col |
| `Iq` | Corrente de eixo q (pu) | vetor 2 col |
| `iabc_inverter` | Correntes trifásicas do inversor (pu) | vetor 3 col |
| `iabc_grid` | Correntes trifásicas da rede (pu) | escalar |

> `tout` não é salvo automaticamente — usar `P.Values.Time` para obter o vetor de tempo.
> `id` e `Iq` têm 2 colunas (medida e referência) — usar `(:,1)` para a corrente medida.

## Script MATLAB de exportação

Script em `scripts/export_sim_data.m`. Resumo:

```matlab
ds = logsout_IEEE9BusLoadflow;
P      = ds.get('Pinverter');
Q      = ds.get('Qinverter');
AngPLL = ds.get('Ang_pll');
AngRed = ds.get('Ang_Rede');
Id     = ds.get('id');
Iq     = ds.get('Iq');

t = P.Values.Time;
theta_err = AngPLL.Values.Data - AngRed.Values.Data;

T = table(t, P.Values.Data, Q.Values.Data, ...
    AngPLL.Values.Data, AngRed.Values.Data, theta_err, ...
    Id.Values.Data(:,1), Iq.Values.Data(:,1), ...
    'VariableNames', {'t_s','P_pu','Q_pu', ...
    'theta_pll_rad','theta_ref_rad','theta_err_rad','id_pu','iq_pu'});

writetable(T, 'sim_data.csv');
```

## Script Python de análise

Script em `scripts/analyze_sim_data.py`. Calcula IAE, ISE, ts, ΔP, ΔQ e plota 6 painéis.

```python
import numpy as np, pandas as pd
df = pd.read_csv('sim_data.csv')
theta_err = df['theta_err_rad'].to_numpy()
t = df['t_s'].to_numpy()
mask = t >= 0.5          # ajustar T_FAULT conforme cenário
IAE = np.trapz(np.abs(theta_err[mask]), t[mask])
ISE = np.trapz(theta_err[mask]**2, t[mask])
```

## Colunas do CSV

`t_s`, `P_pu`, `Q_pu`, `theta_pll_rad`, `theta_ref_rad`, `theta_err_rad`, `id_pu`, `iq_pu`

## Ambiente Python

O projeto tem `.venv` e `requirements.txt` com `numpy`, `pandas`, `matplotlib`.
`.venv` está no `.gitignore` — não é versionado.

Para recriar:
```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Para ativar e rodar a análise:
```powershell
.venv\Scripts\Activate.ps1
python scripts\analyze_sim_data.py
```
