# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TCC (Trabalho de Conclusão de Curso) em Engenharia Elétrica — UERJ 2025. Investigates the dynamic behavior of the **SRF-PLL** (Synchronous Reference Frame Phase-Locked Loop) algorithm in grid-tied inverters under severe network contingencies, motivated by the August 15, 2023 Brazilian grid disturbance that disconnected 22,547 MW (~31% of national load).

## Repository Layout

```
pll_stability_9bus/
├── app.py                              ← entry point Python (python app.py)
├── CHANGELOG.md                        ← histórico de alterações do dashboard (por commit)
├── params.m                            ← MATLAB workspace setup (rodar antes de simular)
├── pll_stability_9bus.slx              ← modelo Simulink principal (raiz)
├── pll_stability_9bus_faultInfo.xml    ← metadados do Fault Analyzer
├── requirements.txt                    ← numpy, pandas, plotly
├── src/                                ← pacote Python de análise
│   ├── __init__.py                     ← expõe SimData, ChartBuilder, HTMLRenderer
│   ├── config/settings.py              ← T_FAULT, TOL_RAD, paletas, caminhos
│   ├── pipeline/loader.py              ← SimData: lê CSV, calcula IAE/ISE/ts/ΔP/ΔQ
│   ├── pipeline/chart.py               ← ChartBuilder: monta subplots Plotly
│   └── report/renderer.py              ← HTMLRenderer: gera relatório HTML
├── scripts/
│   ├── export_sim_data.m               ← exporta logsout → output/sim_data.csv
│   └── analyze_sim_data.py             ← script legado (substituído por app.py)
├── notebooks/
│   └── pll_stability_9bus_analysis.ipynb   ← cálculo analítico de parâmetros
├── simulink/                           ← modelos Simulink auxiliares
│   ├── pll_stability_9bus_FaultModel.slx
│   ├── GridTiedInverterOptimalI2.slx   ← referência MathWorks
│   ├── GridTiedInverterOptimalIData.m
│   ├── teste_isolado.slx
│   └── archive/
│       └── pll_stability_9bus.slx.original
├── output/                             ← gerado em runtime (não versionado)
│   ├── sim_data.csv                    ← exportado pelo MATLAB
│   └── pll_metrics.html                ← relatório gerado pelo Python
├── assets/                             ← diagramas, figuras, banner
└── .claude/                            ← base de conhecimento + skills
```

## Workflow de Simulação → Relatório

```
1. MATLAB: abrir pll_stability_9bus.slx → rodar params.m → simular
2. MATLAB: >> export_sim_data          (gera output/sim_data.csv)
3. Python: .venv\Scripts\python app.py (gera output/pll_metrics.html)
```

## Rodando o Pacote Python

```powershell
# Configuração do ambiente (uma vez)
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# Gerar relatório (após exportar CSV do MATLAB)
.venv\Scripts\python.exe app.py

# Caminhos customizados
.venv\Scripts\python.exe app.py --csv output/sim_data.csv --out output/relatorio.html
```

`app.py` instancia `SimData → ChartBuilder → HTMLRenderer` e salva o HTML com
toggle de tema light/dark, 5 cards de métricas e subplots Plotly interativos.

## Rodando o Notebook

```bash
jupyter notebook notebooks/pll_stability_9bus_analysis.ipynb
```

Dependências: `numpy`, `pandas`, `math` (stdlib). Rodar células de cima para baixo
— variáveis de células anteriores são reutilizadas ao longo do notebook.

## Modelos Simulink

Abrir `.slx` no **MATLAB/Simulink R202x**. O modelo simula cenários EMT para
4 tipos de contingência: afundamento simétrico, afundamento assimétrico (introduz
sequência negativa → oscilações de 2ª harmônica no PLL), salto de ângulo e alto RoCoF.

Antes de simular: `>> params.m` no Command Window. Modelos em `simulink/` são
standalone — não referenciados pelo modelo principal.

## Parâmetros do Sistema

- Base: 20 kV / 100 MVA / 60 Hz
- Rede IEEE 9 barras; inversor conectado na Barra 2
- Impedância de Thevenin: diagonal `Z_ii` de `inv(Ybarra)` na barra de conexão
- Ressonância do filtro LCL: `ω_res = 9068.99 rad/s`, `ξ = 0.707`, `fs = 5 kHz`
- Ganhos do PLL: `Kp = 8·60·(L1+L2+Lest)`, `Ki = 32·60²·(L1+L2+Lest)`
- Vcc no modelo: 136.364 kV (×1.5 override proposital vs 90.9 kV do notebook)

## Sinais Logados (logsout_IEEE9BusLoadflow)

| Sinal | Conteúdo | Colunas |
|---|---|---|
| `Pinverter`, `Qinverter` | Potência ativa/reativa (pu) | 1 |
| `Ang_pll`, `Ang_Rede` | Ângulos PLL e rede (rad) | 1 |
| `id` | **Mux [id_ref, id_medido]** (pu) | 2 |
| `Iq` | **Mux [iq_ref, iq_medido]** (pu) | 2 |
| `iabc_inverter`, `iabc_grid` | Correntes trifásicas (pu) | 3 |

`Ang_pll` e `iabc` correm a Ts=5 µs; demais a Tsc=200 µs → interpolar sobre t de `Pinverter`.

## Métricas de Desempenho

IAE, ISE, tempo de acomodação ts (critério ±1.15° = 0.02 rad), ΔP_ufv, ΔQ_ufv pós-falta.
Calculados por `SimData` em `src/pipeline/loader.py`. Conformidade LVRT per IEEE 1547-2018.

Atributos `SimData`: `P_ufv`, `Q_ufv`, `id_ufv_meas`, `iq_ufv_meas`, `id_ufv_ref`, `iq_ufv_ref`,
`f_pll`/`t_freq` (frequência estimada do PLL em Hz, derivada de θ̂).
Flags: `has_dq_ufv`, `has_ref_ufv`, `has_freq`. Colunas CSV: `P_ufv_pu`, `Q_ufv_pu`, `id_ufv_pu`, `iq_ufv_pu`, `id_ufv_ref_pu`, `iq_ufv_ref_pu`.
Quando variáveis dos geradores forem adicionadas, usar sufixo `_gen1`, `_gen2` etc.

## Knowledge Base (.claude/)

```
.claude/
├── kb/
│   ├── project-scope.md       ← escopo TCC, status dos capítulos, tabela de contingências
│   ├── dashboard/             ← relatório HTML: dados/, graficos/, cards/, layout/ (ver index.md)
│   ├── pll/                   ← teoria SRF-PLL, metodologia Kp/Ki, cenários de contingência
│   ├── inverter/              ← filtro LCL, arquitetura Simulink, referência VSC
│   ├── power-system/          ← IEEE 9 barras, Thevenin, inércia, VSG
│   ├── simulation/            ← workflow export, override Vcc, runtime (Ts/fsw/Tsc)
│   ├── standards/             ← LVRT, IEEE 1547-2018, ONS
│   └── python/                ← padrões Python clean code + pipeline NumPy/Pandas/Plotly
├── commands/
│   └── git.yaml               ← convenções de git do projeto
├── rules/
│   └── limits.md              ← limite 200 linhas/arquivo, mapa de pastas do kb
└── skills/
    └── slx-explorer/          ← inspeção de .slx via Python/XML (sem MATLAB)
```

## Inspecionando o Modelo Simulink Sem MATLAB

Arquivos `.slx` são ZIPs com XML internamente:

```python
import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile('pll_stability_9bus.slx', 'r') as z:
    xml = z.read('simulink/blockdiagram.xml').decode('utf-8', errors='replace')
```

SIDs principais: rede raiz (`system_root`), UFV Model/VSI (`3896`), Optimal Controller
(`3963`), PWM Control/PI+Notch (`3974`), PWM comparator (`3997`), Measurement (`4021`).
Ver `kb/inverter/simulink_model.md` para o mapa completo.

## Nota sobre os Ganhos Kp/Ki

Os ganhos são divididos por 4 **duas vezes**: uma no notebook (conversão pu,
Z_base = 4 Ω) e outra dentro dos blocos Gain do Simulink. A dupla divisão compensa
um mismatch de ~6× entre V_base_LN e Vcc/2 na normalização do SPWM, combinado
com fator ×2 por usar `(L1+L2+Lest)` ao invés de `Lest` na fórmula.
