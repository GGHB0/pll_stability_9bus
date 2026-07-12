---
name: export-workflow
description: Workflow validado Simulink → MATLAB → Python para o modelo pll_stability_9bus (logsout, sinais de barra, sim_data.csv)
---

# Export Workflow: Simulink → MATLAB → Python

## Sinais disponíveis no logsout

`logsout_IEEE9BusLoadflow` (Simulink.SimulationData.Dataset):

| Nome | Conteúdo | Dimensão | Taxa |
|---|---|---|---|
| `Pinverter` | Potência ativa UFV (pu) | escalar | Tsc=200µs |
| `Qinverter` | Potência reativa UFV (pu) | escalar | Tsc |
| `Ang_pll` | Ângulo estimado θ̂ (rad) | escalar | Ts=5e-5 s |
| `Ang_Rede` | Ângulo de referência θ_ref (rad) | escalar | Ts |
| `id` | **Mux [id_ref, id_medido]** (pu) | 2 colunas | Tsc |
| `Iq` | **Mux [iq_ref, iq_medido]** (pu) | 2 colunas | Tsc |
| `iabc_inverter` | Correntes trifásicas inversor (pu) | 3 colunas | Ts |
| `iabc_grid` | Correntes trifásicas rede (pu) | 3 colunas | Ts |
| `vabc_inverter` | Tensões trifásicas inversor (pu) | 3 colunas | Ts |
| `vabc_grid` | Tensões trifásicas rede (pu) | 3 colunas | Ts |
| `V_bus1`, `V_bus2`, `V_bus3` | Magnitude escalar \|V\| da barra (V, bruto) | escalar | Tsc |
| `Vdq_Inverter` | **Mux [Vd_inv, Vq_inv, ...]** tensão dq no inversor | ≥2 colunas (1=d, 2=q) | Tsc |
| `Vdq_rede` | **Mux [Vd_rede, Vq_rede, ...]** tensão dq da rede | ≥2 colunas (1=d, 2=q) | Tsc |
| `Ang_G1`, `Ang_G3` | Ângulo do rotor (rad elétrico) | escalar | Tsc |
| `Pe_G1`, `Pe_G3` | Potência elétrica do gerador (pu — já normalizada pela máquina) | escalar | Tsc |
| `P_bus1`, `Q_bus1`, `P_bus3`, `Q_bus3` | P/Q medidos na barra (**MW/MVAr brutos**, não pu) | escalar (Mux coluna 1 relevante) | Tsc |

> `Ang_pll` e `iabc` rodam a Ts (eixo rápido); demais sinais a Tsc (eixo lento).
> `V_bus{N}` é escalar de magnitude — **não** aplicar transformada de Clarke.

> ⚠️ **Discrepância observada (2026-07-12)**: nos CSVs exportados em
> `output/results/` as taxas estão **invertidas** — `sim_data.csv` a 5 µs e
> `sim_data_angles.csv` a 200 µs. Ou o logging do modelo mudou (decimação dos
> sinais trocada) ou a tabela acima está desatualizada. Pipeline Python não
> quebra (interpola pelo tempo real), mas conferir no Simulink qual taxa cada
> sinal logado usa hoje. Ver nota em [[pipeline-dados]].

### Origem estrutural: por que P_bus/Q_bus não são pu mas Pinverter/Qinverter são

Ver `.claude/kb/inverter/simulink_model.md` (seção Scopes/Bus monitor, SID 4396).
`Pinverter`/`Qinverter` vêm do subsistema "Inverter Active & Reactive Power" (SID 4055),
que computa `P/Q` a partir de `Vabc_inverter`/`Iabc_inverter` — sinais **já em pu**
desde a etapa de medição upstream. `P_bus1/Q_bus1/P_bus3/Q_bus3` são taps `Goto`/`From`
diretos das Busbars Simscape (SID 1887 "Bus1 16.5kV", SID 3494 "Bus3 13.8kV") via
blocos `PS-Simulink Converter` **sem nenhum Gain/Product de normalização** — saem em
unidades físicas (W, VAr). Por isso o script de export precisa dividir por `S_base`
explicitamente (ver abaixo), diferente de `Pinverter`/`Qinverter`.

### Estrutura interna de `id` e `Iq`

- `id.Values.Data(:,1)` → **id_ref** (referência do controlador — sinal limpo)
- `id.Values.Data(:,2)` → **id medido** (sinal real com ruído do filtro)
- `Iq.Values.Data(:,1)` → **iq_ref**; `Iq.Values.Data(:,2)` → **iq medido**

## Script MATLAB: `scripts/export_sim_data.m`

Exporta **três CSVs separados** (preserva a taxa nativa de cada grupo). Caminho portável:
`proj_root = fileparts(get_param(bdroot, 'FileName'))`.

- **CSV 1** (`sim_data_angles.csv`, eixo Ts): `t_s, theta_pll_rad, theta_ref_rad, theta_err_rad`.
- **CSV 2** (`sim_data.csv`, eixo Tsc): potência, correntes dq, tensões — construído por
  `build_base_table` + funções auxiliares aplicadas em cadeia:

| Função | Uso | Normalização |
|---|---|---|
| `add_vdq_cols` | `Vdq_Inverter`, `Vdq_rede` | ÷ média pré-falta de Vd |
| `add_vmag_col` | `V_bus1/2/3` | ÷ média pré-falta (pu relativo, não pu absoluto) |
| `add_scalar_col` | `Ang_G1/G3`, `Pe_G1/G3` | nenhuma — sinal já pu (ângulo em rad) |
| `add_power_col` | `P_bus1`, `Q_bus1`, `P_bus3`, `Q_bus3` | ÷ `S_BASE_MVA = 100` (100 MVA, base do sistema) |

`add_power_col(T, ds, t, sig_name, col_name, S_base_mva)` extrai a coluna (1) do
Mux e divide por `S_base_mva` antes de interpolar — mesma base de 100 MVA usada
em todo o pipeline Python (ver `V_base = 20 kV, S_base = 100 MVA` em
`kb/power-system/ieee9bus_topology.md`).

> ⚠️ **Gotcha unidade**: `P_bus1/3`, `Q_bus1/3` saem do Busbar (Simscape) já em
> **MW/MVAr**, não em W/VAr — confirmado pelo usuário (2026-07). Dividir por
> `100e6` (achando que era W) gera pu ~1e6× menor que o correto; a base certa
> para esses 4 sinais é `100` (MVA), não `100e6` (VA).

> Sinais Mux de 2 elementos onde só a coluna (1) é pertinente (P_bus1, Q_bus1, P_bus3,
> Q_bus3): confirmado pelo usuário — sempre usar `Data(:,1)`.

- **CSV 3** (`sim_data_abc.csv`, taxa nativa de `iabc_inverter`, 2026-07-12):
  `t_s, ia/ib/ic_ufv_pu` + `ia/ib/ic_grid_pu` (se `iabc_grid` estiver logado,
  interpoladas no mesmo eixo). Função `export_abc`; pulada silenciosamente se
  `iabc_inverter` não existir no logsout. Uso: espectro em abc **verdadeiro**
  — a Park inversa dos sinais dq perde a sequência zero das faltas à terra.
  Consumo Python: `SimData.t_abc`/`ia_ufv`/… (flags `has_iabc_ufv`/`_grid`);
  alimenta o painel "Corrente i_a UFV (abc)" do espectro
  ([[espectro-fourier]]) — só aparece após **re-exportar** os cenários.
- **Tensões abc** (mesmo CSV 3, 2026-07-12): `va/vb/vc_ufv_pu` +
  `va/vb/vc_grid_pu`, já em pu na medição (sem normalização adicional).
  Exigiu habilitar o signal logging de `Vabc_inverter`/`Vabc_grid` no
  `.slx` (blocos `From` em `UFV Model/Scopes`, mesmo padrão de
  `iabc_inverter`/`_grid`) — feito via `matlab -batch`
  (`set_param(outPort, 'DataLogging', 'on')`). Flags `has_vabc_ufv`/`_grid`;
  alimenta o painel "Tensão v_a UFV (abc)" ([[espectro-fourier]]).

Após exportar, o `StopFcn` chama `export_sim_data.m`, que por sua vez pode disparar
`app.py` (ver `kb/simulation/python_pipeline.md`).

## Estrutura de pastas de resultados

```
output/results/
├── regime/                   ← regime permanente (sem barra)
├── bus{1..9}/{fault_type}/   ← falta em barra
└── line{A}_{B}/{fault_type}/ ← falta em linha (A < B por convenção)
```

Linhas do IEEE 9 barras: **1-4, 4-5, 5-6, 3-6, 6-7, 7-8, 8-2, 8-9, 9-4**.
`fault_type` ∈ `{3phase, 2phase_ground, 2phase, 1phase_ground}`; sufixo `_bad_pll`
quando `BAD_PLL=true` (ver [[bad-pll-scenario]]).

Cada pasta recebe: `sim_data.csv`, `sim_data_angles.csv`, `sim_data_abc.csv`
(se `iabc_inverter` logado) e `fault_info.json`.

## Colunas de `sim_data.csv`

```
t_s, P_ufv_pu, Q_ufv_pu, id_ufv_ref_pu, id_ufv_pu, iq_ufv_ref_pu, iq_ufv_pu
[, vd_ufv_pu, vq_ufv_pu, vd_rede_pu, vq_rede_pu]
[, vbus1_pu, vbus2_pu, vbus3_pu]
[, ang_g1_rad, pe_g1_pu, ang_g3_rad, pe_g3_pu]
[, p_bus1_pu, q_bus1_pu, p_bus3_pu, q_bus3_pu]
```

Todas as colunas entre `[...]` são opcionais — Python detecta via `"col" in df.columns`
e o formato legado (sem essas colunas) continua carregando sem erro.

## Flag BAD_PLL

Simula PLL mal dimensionado: `kp_pll` reduzido a 20% do nominal.

```matlab
% params.m
BAD_PLL = false;          % true → kp_pll mal dimensionado (×0.2)
if BAD_PLL
    kp_pll = kp_pll * 0.2;
end
```

```matlab
% export_sim_data.m
BAD_PLL = ws_var('BAD_PLL', false);
folder_type = FAULT_TYPE;
if BAD_PLL
    folder_type = [FAULT_TYPE, '_bad_pll'];   % → output/results/bus{N}/{fault_type}_bad_pll/
end
```

| `BAD_PLL` | `kp_pll` efetivo | Pasta (ex.: bus5 / 3phase) |
|-----------|-----------------|-------------------------------------|
| `false`   | 460 (nominal)   | `output/results/bus5/3phase/`        |
| `true`    | 92 (×0,2)       | `output/results/bus5/3phase_bad_pll/`|

O campo `bad_pll` também é salvo em `fault_info.json`.

## Execução automática via StopFcn

**Model Properties → Callbacks → StopFcn:**

```matlab
proj_root = fileparts(get_param(bdroot, 'FileName'));
run(fullfile(proj_root, 'scripts', 'export_sim_data.m'));
```

Fluxo: `▶ Simular → StopFcn → export_sim_data.m → output/results/{regime|bus{N}|line{A}_{B}}/{fault_type}/`
