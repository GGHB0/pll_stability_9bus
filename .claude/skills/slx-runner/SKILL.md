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
| `signal_map.json` | Mapa nome → bloco SID + porta (derivado do modelo) |

## Uso Típico

```python
import sys
sys.path.insert(0, r'C:\projetos\pll_stability_9bus\.claude\skills\slx-runner')
from runner import run_simulation
from analyze import pll_metrics, plot_pll, plot_power, plot_angle_comparison, print_metrics

# 1. Rodar simulação (timeout padrão = 300 s)
data = run_simulation(signals=['ang_pll', 'ang_vdd', 'ang_vdd_pll', 'rep_seq',
                               'p_inv', 'q_inv', 'id_ref_meas', 'iq_ref_meas',
                               'bus2_v', 'ang_barra'])

# 2. Comparação de ângulos: Fourier × PLL × Referência
plot_angle_comparison(data['t'], data['ang_vdd'], data['ang_pll'],
                      rep_seq=data['rep_seq'], fault_time=0.1,
                      save_path='angle_comparison.png')

# 3. Métricas do PLL
metrics = pll_metrics(data['t'], data['ang_pll'], fault_time=0.1)
print_metrics(metrics)

# 4. Potência e correntes
plot_power(data['t'], data['p_inv'], data['q_inv'], fault_time=0.1)
plot_pll(data['t'], data['ang_pll'], fault_time=0.1)
```

## Sinais Disponíveis (signal_map.json)

### Ângulos (comparação Fourier × PLL)

| Nome | Descrição |
|---|---|
| `ang_pll` | Ângulo SRF-PLL (rad) — Scope "Ang", SID 3967 |
| `ang_vdd` | mod(Fourier_angle + RepSeq, 2π) — ângulo absoluto do inversor |
| `ang_vdd_pll` | AngPLL no scope de comparação "Ang Vdd" (≡ ang_pll) |
| `ang_fourier_raw` | Fase Fourier bruta do fundamental de Va_inv (antes do mod) |
| `rep_seq` | Repeating Sequence ωt (rampa 0→2π por ciclo = referência da rede) |
| `ang_barra` | Ângulo de barra via PS-Simulink Converter (root) |

### Potência e Corrente

| Nome | Descrição |
|---|---|
| `p_inv` | Potência ativa do inversor (pu) |
| `q_inv` | Potência reativa do inversor (pu) |
| `id_ref_meas` | id referência + medido (pu) |
| `iq_ref_meas` | iq referência + medido (pu) |
| `iabc_inv` | Correntes do inversor Iabc (pu) |
| `iabc_grid` | Correntes da rede Iabc (pu) |

### Tensões

| Nome | Descrição |
|---|---|
| `vabc_inv` / `vabc_grid` | Tensões trifásicas inversor/rede (pu) |
| `bus1_v` … `bus9_v` | Tensão em cada barra (barras 1–9 todas mapeadas) |
| `bus1_p/q` … `bus9_p/q` | Potência ativa/reativa em cada barra |

## Pré-requisitos

- MATLAB no PATH (`matlab -batch` funciona no terminal)
- Python: `scipy`, `numpy`, `matplotlib`
- `params.m` na raiz do projeto (carregado automaticamente)

## Notas Técnicas

- Signal logging ativado via `set_param` no `SrcPortHandle` do bloco destino
- `scope_sid` pode ser qualquer bloco (não só Scope) — o runner usa a **porta de entrada** para rastrear o sinal fonte
- `close_system(model, 0)` garante que o `.slx` não é modificado em disco
- `rep_seq` é capturado via porta 2 do Sum block SID=4497 (não tem Scope próprio)
- Arquivo `sim_results.mat` salvo na raiz do projeto (sobrescrito a cada run)
