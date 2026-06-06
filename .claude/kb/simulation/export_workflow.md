---
name: export-workflow
description: Como extrair sinais do Simulink e exportar para Python via CSV — workflow validado para o modelo pll_stability_9bus
---

# Export Workflow: Simulink → MATLAB → Python

## Sinais disponíveis no logsout

Após rodar a simulação, o workspace contém `logsout_IEEE9BusLoadflow` (Simulink.SimulationData.Dataset) com 5 sinais logados:

| Nome | Conteúdo |
|---|---|
| `Pinverter` | Potência ativa do inversor (pu) |
| `Qinverter` | Potência reativa do inversor (pu) |
| `iabc_inverter` | Correntes trifásicas do inversor (pu) |
| `iabc_grid` | Correntes trifásicas da rede (pu) |
| `vab_sync` | Tensão de sincronismo Vab |

> `tout` não é salvo automaticamente — usar `P.Values.Time` para obter o vetor de tempo.

## Script MATLAB de exportação

```matlab
P   = logsout_IEEE9BusLoadflow.get('Pinverter');
Q   = logsout_IEEE9BusLoadflow.get('Qinverter');
Ii  = logsout_IEEE9BusLoadflow.get('iabc_inverter');
Ig  = logsout_IEEE9BusLoadflow.get('iabc_grid');
Vab = logsout_IEEE9BusLoadflow.get('vab_sync');

t = P.Values.Time;

T = table(t, P.Values.Data, Q.Values.Data, ...
    'VariableNames', {'t_s', 'P_pu', 'Q_pu'});

writetable(T, 'sim_data.csv');
```

Usar `pwd` no Command Window para confirmar a pasta de destino.

## Leitura no Python

```python
import pandas as pd

df = pd.read_csv('sim_data.csv')
```

## Métricas calculadas no Python

```python
import numpy as np

# IAE e ISE do erro de fase (requer theta_err exportado separadamente)
IAE = np.trapz(np.abs(df['theta_err_rad']), df['t_s'])
ISE = np.trapz(df['theta_err_rad']**2, df['t_s'])

# Ripple de P e Q (janela pós-falta)
pos_falta = df['t_s'] > 0.5
delta_P = df.loc[pos_falta, 'P_pu'].max() - df.loc[pos_falta, 'P_pu'].min()
delta_Q = df.loc[pos_falta, 'Q_pu'].max() - df.loc[pos_falta, 'Q_pu'].min()

# Tempo de acomodação do erro de fase
tol = 0.02
fora = df[np.abs(df['theta_err_rad']) > tol]
ts = fora['t_s'].iloc[-1] if not fora.empty else 0.0
```

## Pendência

O sinal de erro de fase do PLL (`theta_err`) não está no logsout atual.
Para incluí-lo: no Simulink, dentro de system_3963 (Optimal Controller),
clicar com botão direito na linha de saída do somador (θ̂ - θ_grid) → Log signal.
