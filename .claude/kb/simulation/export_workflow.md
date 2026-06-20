---
name: export-workflow
description: Workflow validado Simulink → MATLAB → Python para o modelo pll_stability_9bus
---

# Export Workflow: Simulink → MATLAB → Python

## Sinais disponíveis no logsout

`logsout_IEEE9BusLoadflow` (Simulink.SimulationData.Dataset) — 13 entradas:

| Nome | Conteúdo | Dimensão | Taxa |
|---|---|---|---|
| `Pinverter` | Potência ativa (pu) | escalar | Tsc=200µs |
| `Qinverter` | Potência reativa (pu) | escalar | Tsc |
| `Ang_pll` | Ângulo estimado θ̂ (rad) | escalar | Ts=5e-5 s |
| `Ang_Rede` | Ângulo de referência θ_ref (rad) | escalar | Ts |
| `id` | **Mux [id_ref, id_medido]** (pu) | 2 colunas | Tsc |
| `Iq` | **Mux [iq_ref, iq_medido]** (pu) | 2 colunas | Tsc |
| `iabc_inverter` | Correntes trifásicas inversor (pu) | 3 colunas | Ts |
| `iabc_grid` | Correntes trifásicas rede (pu) | 3 colunas | Ts |
| `V_bus2` | **Magnitude escalar** \|V\| Barra 2 (V ou pu) | escalar | Tsc |
| `Vdq_Inverter` | **Mux [Vd_inv, Vq_inv, ...]** tensão dq no inversor | ≥2 colunas (1=d, 2=q) | Tsc |
| `Vdq_rede` | **Mux [Vd_rede, Vq_rede, ...]** tensão dq da rede | ≥2 colunas (1=d, 2=q) | Tsc |
| `Ang_G1` | Ângulo do rotor de G1 (rad elétrico) | escalar | Tsc |
| `Pe_G1` | Potência elétrica de G1 (pu) | escalar | Tsc |
| `Ang_G3` | Ângulo do rotor de G3 (rad elétrico) | escalar | Tsc |
| `Pe_G3` | Potência elétrica de G3 (pu) | escalar | Tsc |

> `V_bus2` é um sinal escalar de magnitude — **não** é trifásico. Não aplicar transformada de Clarke.
> O script normaliza pela média pré-falta (`t < T_FAULT`) para obter `vbus2_pu`.

### Estrutura interna de `id` e `Iq`

- `id.Values.Data(:,1)` → **id_ref** (referência do controlador — sinal limpo)
- `id.Values.Data(:,2)` → **id medido** (sinal real com ruído do filtro)
- `Iq.Values.Data(:,1)` → **iq_ref**
- `Iq.Values.Data(:,2)` → **iq medido**

> `Ang_pll` e `iabc` rodam a Ts (eixo rápido); demais sinais a Tsc (eixo lento).
> `Ang_Rede` vem do logsout e é interpolada para `t_fast` — mesma fase inicial do modelo.

## Script MATLAB: `scripts/export_sim_data.m`

Exporta **dois CSVs separados** para preservar a taxa nativa de cada grupo de sinais.
Caminho portável — funciona em qualquer máquina sem editar o script:

```matlab
proj_root = fileparts(get_param(bdroot, 'FileName'));
```

### CSV 1 — ângulos (eixo rápido, Ts)

```matlab
t_fast         = AngPLL.Values.Time;
ang_fast       = AngPLL.Values.Data;
ang_red_fast   = interp1(AngRed.Values.Time, AngRed.Values.Data, t_fast, 'linear', 'extrap');
theta_err_fast = wrapToPi(ang_fast - ang_red_fast);

T_angles = table(t_fast, ang_fast, ang_red_fast, theta_err_fast, ...
    'VariableNames', {'t_s','theta_pll_rad','theta_ref_rad','theta_err_rad'});
writetable(T_angles, fullfile(proj_root, 'output', 'sim_data_angles.csv'));
```

### CSV 2 — potência, correntes e tensão (eixo lento, Tsc)

```matlab
t       = P.Values.Time;   % eixo Tsc
T_FAULT = 0.5;             % instante da falta (s)

id_ref_pu = interp1(Id.Values.Time, Id.Values.Data(:,1), t, 'linear', 'extrap');  % → id_ufv_ref_pu no CSV
id_pu     = interp1(Id.Values.Time, Id.Values.Data(:,2), t, 'linear', 'extrap');  % → id_ufv_pu
iq_ref_pu = interp1(Iq.Values.Time, Iq.Values.Data(:,1), t, 'linear', 'extrap'); % → iq_ufv_ref_pu
iq_pu     = interp1(Iq.Values.Time, Iq.Values.Data(:,2), t, 'linear', 'extrap'); % → iq_ufv_pu

% V_bus2 é escalar — extrai e normaliza diretamente (sem Clarke)
V_bus2 = ds.get('V_bus2');
if ~isempty(V_bus2)
    ts_v     = V_bus2.Values;          % timeseries ou timetable
    t_v      = ts_v.Time;
    vmag     = ts_v.Data(:,1);
    Vmag_nom = mean(vmag(t_v < T_FAULT));
    vbus2_pu = interp1(t_v, vmag / Vmag_nom, t, 'linear', 'extrap');
end
```

Após exportar, o script chama `app.py` via `system()` e abre o HTML no navegador.

## Estrutura de pastas de resultados

```
output/results/
├── regime/                   ← regime permanente (cenário global, sem barra)
├── bus{1..9}/
│   ├── 3phase/
│   ├── 2phase_ground/
│   ├── 2phase/
│   └── 1phase_ground/
└── line{A}_{B}/              ← falta em linha (A < B por convenção)
    ├── 3phase/               ← linhas: 1-4, 4-5, 5-6, 3-6, 6-7, 7-8, 8-2, 8-9, 9-4
    ├── 2phase_ground/
    ├── 2phase/
    └── 1phase_ground/
```

`regime` fica na raiz de `results/` — representa o sistema inteiro em operação normal.
Faltas em barra: `bus{N}/{fault_type}/`. Faltas em linha: `line{A}_{B}/{fault_type}/` (A < B).

Cada pasta recebe: `sim_data.csv`, `sim_data_angles.csv`, `fault_info.json`.
`fault_info.json` inclui campo `fault_line: [A, B]` quando for falta em linha (senão `[]`).

## Arquivos de saída (por cenário)

| Arquivo | Colunas | Taxa | Uso |
|---|---|---|---|
| `sim_data.csv` | `t_s, P_ufv_pu, Q_ufv_pu, id_ufv_ref_pu, id_ufv_pu, iq_ufv_ref_pu, iq_ufv_pu [, vd_ufv_pu, vq_ufv_pu, vd_rede_pu, vq_rede_pu, vbus2_pu, ang_g1_rad, pe_g1_pu, ang_g3_rad, pe_g3_pu]` | Tsc | eixo de tempo principal do Python |
| `sim_data_angles.csv` | `t_s, theta_pll_rad, theta_ref_rad, theta_err_rad` | Ts | alta resolução para θ_err e IAE/ISE/ts |
| `fault_info.json` | `fault_bus, fault_type, t_fault, t_clear, duration_s, timestamp, model` | — | metadados do cenário para rastreabilidade |

> Sufixo `_ufv` identifica sinais do inversor UFV; `_rede` identifica sinais da rede. Geradores síncronos: padrão `ang_g{n}_rad` / `pe_g{n}_pu` (ex: `ang_g1_rad`, `pe_g3_pu`).
> `Vdq_*` são normalizados pelo valor pré-falta de `Vd` (componente d). Pré-falta: `Vd ≈ 1 pu`, `Vq ≈ 0`.

> `vbus2_pu` é opcional: incluído quando `V_bus2` existe no logsout. Python detecta via `"vbus2_pu" in df.columns`.

> Formato legado (colunas de ângulo dentro de `sim_data.csv`) ainda é suportado pelo Python.

## Configuração do cenário em `params.m`

Antes de cada simulação, editar apenas estas linhas na seção `%% Cenário de simulação`:

```matlab
% Falta em BARRA:  FAULT_BUS = N;      FAULT_LINE = [];
% Falta em LINHA:  FAULT_BUS = 0;      FAULT_LINE = [A, B];
% Regime perm.:    FAULT_TYPE='regime'; FAULT_BUS = 0; FAULT_LINE = [];

FAULT_BUS  = 7;           % Barra do curto (0 se falta em linha ou regime)
FAULT_LINE = [];          % Par [A, B] para falta em linha; [] para falta em barra
FAULT_TYPE = '3phase';    % Ver tabela abaixo

T_FAULT    = 0.5;         % Instante de aplicação da falta [s]
T_CLEAR    = 0.6;         % Instante de remoção da falta   [s]
T_DUR      = T_CLEAR - T_FAULT;  % Duração [s] — calculado automaticamente
```

| `FAULT_TYPE`      | Descrição                        | Pasta de saída                         |
|-------------------|----------------------------------|----------------------------------------|
| `'regime'`        | Regime permanente, sem falta     | `output/results/regime/`               |
| `'3phase'`        | Curto trifásico simétrico        | `output/results/bus{N}/3phase/`        |
| `'2phase_ground'` | Bifásico com terra (seq. neg.)   | `output/results/bus{N}/2phase_ground/` |
| `'2phase'`        | Bifásico sem terra               | `output/results/bus{N}/2phase/`        |
| `'1phase_ground'` | Monofásico (mais frequente)      | `output/results/bus{N}/1phase_ground/` |

Faltas em linha usam `FAULT_LINE = [A, B]` (A < B por convenção) → pasta `output/results/line{A}_{B}/{fault_type}/`.

Linhas do IEEE 9 barras: **1-4, 4-5, 5-6, 3-6, 6-7, 7-8, 8-2, 8-9, 9-4**.

`export_sim_data.m` lê essas variáveis via `ws_var()` e roteia automaticamente para a pasta correta.

## Execução automática via StopFcn

**Modeling → Model Properties → Callbacks → StopFcn:**

```matlab
proj_root = fileparts(get_param(bdroot, 'FileName'));
run(fullfile(proj_root, 'scripts', 'export_sim_data.m'));
```

Fluxo resultante:
```
▶ Simular → StopFcn → export_sim_data.m ─┬─[regime]──────→ output/results/regime/
                                          ├─[linha A-B]───→ output/results/line{A}_{B}/{fault_type}/
                                          └─[barra N]─────→ output/results/bus{N}/{fault_type}/
                                            (cada pasta recebe sim_data.csv, sim_data_angles.csv, fault_info.json)
```

## Arquitetura Python: pacote `src/`

```
app.py          ← entry point (python app.py [--csv PATH] [--out PATH])
src/
├── loader.py   → SimData: lê sim_data.csv + sim_data_angles.csv, calcula métricas
├── chart.py    → ChartBuilder: subplots Plotly (usa t_fast para painéis de ângulo)
└── renderer.py → HTMLRenderer: HTML com tema light/dark
```

### Painéis gerados por `ChartBuilder` (ordem de exibição)

| Painel | Kind | Condição | Conteúdo |
|--------|------|----------|----------|
| Ângulo (°) | `ang` | `has_ang` | θ Rede + θ̂ PLL |
| Erro de fase (°) | `err` | `theta_err is not None` | erro com banda ±TOL_RAD |
| \|V\| Barra 2 (pu) | `vbus` | `has_vbus2` | tensão normalizada + linha LVRT |
| P (pu) | `P` | sempre | P UFV |
| Q (pu) | `Q` | sempre | Q UFV |
| iₓ UFV (pu) | `id` | `has_ref_ufv` | id medido + id ref |
| iᵱ UFV (pu) | `iq` | `has_ref_ufv` | iq medido + iq ref |
| Vd (pu) | `vd_track` | `has_vdq_*` | Vd rede + Vd inversor |
| Vq (pu) | `vq_track` | `has_vdq_*` | Vq rede + Vq inversor |
| Ângulo rotor (°) | `ang_gen` | `has_gen1 or has_gen3` | δ G1 e/ou δ G3 em graus |
| Pe geradores (pu) | `pe_gen` | `has_gen1 or has_gen3` | Pe G1 e/ou Pe G3 |

### Lógica de leitura em `SimData`

1. Lê `sim_data.csv` → `self.t`, `self.P_ufv`, `self.Q_ufv`, correntes dq UFV
2. Procura `sim_data_angles.csv` na mesma pasta:
   - **Se existe**: carrega `t_fast`, `theta_pll_fast`, `theta_ref_fast`; aplica
     baseline correction (remove drift pré-falta); interpola `theta_err` para `self.t`
     para uso nas métricas IAE/ISE/ts
   - **Fallback legado**: lê colunas de ângulo de `sim_data.csv` se presentes

### Atributos de ângulo expostos por `SimData`

| Atributo | Eixo | Descrição |
|---|---|---|
| `t_fast` | Ts | eixo de tempo rápido |
| `theta_pll_fast` | Ts | θ̂ PLL bruto |
| `theta_ref_fast` | Ts | θ_ref analítico |
| `theta_err_fast` | Ts | erro de fase corrigido (baseline removida) |
| `theta_err` | Tsc | theta_err_fast interpolado para eixo lento (métricas) |

### Atributos de geradores expostos por `SimData`

| Atributo | Flag | Descrição |
|---|---|---|
| `ang_g1` | `has_gen1` | ângulo do rotor G1 (rad), eixo Tsc |
| `pe_g1` | `has_gen1` | potência elétrica G1 (pu), eixo Tsc |
| `ang_g3` | `has_gen3` | ângulo do rotor G3 (rad), eixo Tsc |
| `pe_g3` | `has_gen3` | potência elétrica G3 (pu), eixo Tsc |

Flags `has_gen1` / `has_gen3` → `True` apenas se ambas as colunas existirem no CSV.

### Métricas calculadas

| Métrica (chave dict) | Fórmula | Janela |
|---|---|---|
| `IAE` | ∫\|θ_err\| dt | t ≥ T_FAULT |
| `ISE` | ∫θ_err² dt | t ≥ T_FAULT |
| `ts` | último t com \|θ_err\| > TOL_RAD | t ≥ T_FAULT |
| `dP_ufv` | max(P_ufv) − min(P_ufv) | t ≥ T_FAULT |
| `dQ_ufv` | max(Q_ufv) − min(Q_ufv) | t ≥ T_FAULT |
| `vmin` | min(vbus2_pu) | t ≥ T_FAULT |

> `np.trapezoid` (NumPy ≥ 2.0). Baseline correction: subtrai `theta_err[idx_fault-1]`
> antes de T_FAULT para zerar drift da Repeating Sequence de referência.

## Rodar

```powershell
# Exportar do MATLAB (após simular):
# >> export_sim_data   (no Command Window)

# Gerar relatório HTML:
.venv\Scripts\python.exe app.py

# Com caminhos customizados:
.venv\Scripts\python.exe app.py --csv output/sim_data.csv --out output/relatorio.html
```
