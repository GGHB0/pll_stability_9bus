# slx-runner — Execução e Análise do Modelo Simulink

Executa `pll_stability_9bus.slx` via `matlab -batch` (sem GUI), extrai sinais dos
Scopes via signal logging não-destrutivo e calcula métricas do TCC (IAE, ISE,
settling time) com plots matplotlib.

## Quando Ativar

- "rodar a simulação", "executar o modelo", "simular"
- "extrair resultados", "pegar os dados da simulação"
- "calcular IAE", "calcular ISE", "calcular settling time"
- "plotar os sinais", "gerar gráficos da simulação"
- qualquer análise pós-simulação de P, Q, ângulo PLL, correntes

## Arquivos da Skill

| Arquivo | Papel |
|---|---|
| `runner.py` | Gera script .m temporário, chama `matlab -batch`, lê `.mat` |
| `analyze.py` | IAE, ISE, settling time, plots (matplotlib) |
| `signal_map.json` | Mapa nome → Scope SID + porta (derivado do modelo) |

## Uso Típico

```python
import sys
sys.path.insert(0, r'C:\projetos\pll_stability_9bus\.claude\skills\slx-runner')
from runner import run_simulation
from analyze import pll_metrics, plot_pll, plot_power, print_metrics

# 1. Rodar simulação (timeout padrão = 300 s)
data = run_simulation(signals=['ang_pll', 'p_inv', 'q_inv'])

# 2. Métricas do PLL (fault_time em segundos — verificar no params.m)
metrics = pll_metrics(data['t'], data['ang_pll'], fault_time=0.1)
print_metrics(metrics)

# 3. Plots
plot_pll(data['t'], data['ang_pll'], fault_time=0.1, save_path='pll_response.png')
plot_power(data['t'], data['p_inv'], data['q_inv'], fault_time=0.1)
```

## Sinais Disponíveis (signal_map.json)

| Nome | Descrição |
|---|---|
| `ang_pll` | Ângulo estimado pelo PLL (rad) — Scope "Ang", SID 3967 |
| `p_inv` | Potência ativa do inversor (pu) |
| `q_inv` | Potência reativa do inversor (pu) |
| `iabc_inv` | Correntes do inversor Iabc (pu) |
| `iabc_grid` | Correntes da rede Iabc (pu) |
| `vabc_inv` | Tensões do inversor Vabc (pu) |
| `vabc_grid` | Tensões da rede Vabc (pu) |
| `id_ref_meas` | id referência + medido (pu) |
| `iq_ref_meas` | iq referência + medido (pu) |
| `bus1_p/q/v` … `bus3_p/q/v` | P, Q, V das barras 1–3 |

## Pré-requisitos

- MATLAB no PATH (`matlab -batch` funciona no terminal)
- Python: `scipy`, `numpy`, `matplotlib`
- `params.m` na raiz do projeto (carregado automaticamente)

## Notas Técnicas

- Signal logging ativado via `set_param` no `SrcPortHandle` de cada Scope
- `close_system(model, 0)` garante que o `.slx` não é modificado em disco
- Arquivo `sim_results.mat` salvo na raiz do projeto (sobrescrito a cada run)
- Se um SID não for encontrado no modelo, o sinal é pulado com `warning`
