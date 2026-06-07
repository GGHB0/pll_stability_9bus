---
name: export-workflow
description: Workflow validado Simulink → MATLAB → Python para o modelo pll_stability_9bus
---

# Export Workflow: Simulink → MATLAB → Python

## Sinais disponíveis no logsout

`logsout_IEEE9BusLoadflow` (Simulink.SimulationData.Dataset) — 8 entradas:

| Nome | Conteúdo | Dimensão | Taxa |
|---|---|---|---|
| `Pinverter` | Potência ativa (pu) | escalar | Tsc=200µs |
| `Qinverter` | Potência reativa (pu) | escalar | Tsc |
| `Ang_pll` | Ângulo estimado θ̂ (rad) | escalar | Ts=5µs |
| `Ang_Rede` | Ângulo de referência θ_ref (rad) | escalar | Ts |
| `id` | **Mux [id_ref, id_medido]** (pu) | 2 colunas | Tsc |
| `Iq` | **Mux [iq_ref, iq_medido]** (pu) | 2 colunas | Tsc |
| `iabc_inverter` | Correntes trifásicas inversor (pu) | 3 colunas | Ts |
| `iabc_grid` | Correntes trifásicas rede (pu) | 3 colunas | Ts |

### Estrutura interna de `id` e `Iq`

Cada sinal é gerado por um bloco Selector (system_4021) que extrai colunas
de um Mux de 4 entradas `[idref, id, iqref, iq]`:

- `id.Values.Data(:,1)` → **id_ref** (referência do controlador — sinal limpo)
- `id.Values.Data(:,2)` → **id medido** (sinal real com ruído do filtro)
- `Iq.Values.Data(:,1)` → **iq_ref**
- `Iq.Values.Data(:,2)` → **iq medido**

> `tout` não é salvo automaticamente — usar `P.Values.Time` como eixo de tempo.
> Ang_pll e iabc têm taxa diferente → interpolar sobre t de Pinverter.

## Script MATLAB: `scripts/export_sim_data.m`

Exporta 10 colunas para CSV com interpolação multi-taxa.
Caminho portável — funciona em qualquer máquina sem editar o script:

```matlab
% Raiz do projeto detectada a partir do .slx aberto
proj_root = fileparts(get_param(bdroot, 'FileName'));

ds = logsout_IEEE9BusLoadflow;
t  = ds.get('Pinverter').Values.Time;   % eixo comum (Tsc)

% Interpola sinais de taxa diferente
ang_pll   = interp1(AngPLL.Values.Time, AngPLL.Values.Data, t, 'linear','extrap');
ang_red   = interp1(AngRed.Values.Time, AngRed.Values.Data, t, 'linear','extrap');
id_ref_pu = interp1(Id.Values.Time, Id.Values.Data(:,1), t, 'linear','extrap');
id_pu     = interp1(Id.Values.Time, Id.Values.Data(:,2), t, 'linear','extrap');
iq_ref_pu = interp1(Iq.Values.Time, Iq.Values.Data(:,1), t, 'linear','extrap');
iq_pu     = interp1(Iq.Values.Time, Iq.Values.Data(:,2), t, 'linear','extrap');
theta_err = ang_pll - ang_red;

csv_path = fullfile(proj_root, 'output', 'sim_data.csv');
writetable(T, csv_path);
```

Após exportar o CSV, o script chama automaticamente `app.py` via `system()` e
abre `output/pll_metrics.html` no navegador com `web(html_path)`.

## Execução automática via StopFcn

O pipeline completo pode ser disparado automaticamente ao fim de cada simulação
configurando o **StopFcn** do modelo Simulink:

**Modeling → Model Properties → Callbacks → StopFcn:**

```matlab
proj_root = fileparts(get_param(bdroot, 'FileName'));
run(fullfile(proj_root, 'scripts', 'export_sim_data.m'));
```

Fluxo resultante:
```
▶ Simular  →  StopFcn  →  export_sim_data.m  →  sim_data.csv  →  app.py  →  pll_metrics.html
```

> `fileparts(get_param(bdroot,'FileName'))` retorna o diretório do `.slx` aberto —
> portável entre máquinas independente de onde o repositório foi clonado.

## Colunas do CSV (10 colunas)

`t_s`, `P_pu`, `Q_pu`, `theta_pll_rad`, `theta_ref_rad`, `theta_err_rad`,
`id_ref_pu`, `id_pu`, `iq_ref_pu`, `iq_pu`

> Formato legado (8 col) ainda suportado pelo Python — `has_ref` detecta automaticamente.

## Arquitetura Python: pacote `src/`

```
app.py          ← entry point (python app.py [--csv PATH] [--out PATH])
src/
├── __init__.py   → expõe SimData, ChartBuilder, HTMLRenderer
├── config.py     → T_FAULT=0.5, TOL_RAD=0.02, paletas de cor, caminhos
├── loader.py     → class SimData  — CSV → arrays NumPy + métricas
├── chart.py      → class ChartBuilder — SimData → Plotly figure
└── renderer.py   → class HTMLRenderer — figure → HTML com CSS/JS
```

### Fluxo de execução de `app.py`

```python
data = SimData(csv_path)          # lê CSV, calcula IAE/ISE/ts/ΔP/ΔQ
fig, trace_map = ChartBuilder(data).build()   # subplots Plotly
HTMLRenderer(data, fig, trace_map).render(out) # HTML com tema light/dark
```

### Métricas calculadas por `SimData`

| Métrica | Fórmula | Janela |
|---|---|---|
| IAE | ∫\|θ_err\| dt | t ≥ T_FAULT |
| ISE | ∫θ_err² dt | t ≥ T_FAULT |
| ts | último t com \|θ_err\| > TOL_RAD | t ≥ T_FAULT |
| ΔP | max(P) − min(P) | t ≥ T_FAULT |
| ΔQ | max(Q) − min(Q) | t ≥ T_FAULT |

> `np.trapezoid` (NumPy ≥ 2.0) — `np.trapz` foi removido.

## Rodar

```powershell
# Exportar do MATLAB (após simular):
# >> export_sim_data   (no Command Window)

# Gerar relatório HTML:
.venv\Scripts\python.exe app.py

# Com caminhos customizados:
.venv\Scripts\python.exe app.py --csv output/sim_data.csv --out output/relatorio.html
```

## Ambiente Python

`.venv` local (não versionado). Dependências: `numpy`, `pandas`, `plotly`.

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```
