---
name: simulink-model
aliases: [simulink-model]
description: Arquitetura completa do modelo pll_stability_9bus.slx — hierarquia de subsistemas, parâmetros do InitFcn e implementação do controle
source: pll_stability_9bus.slx (extraído via XML interno)
---

# Modelo Simulink — Arquitetura

## Parâmetros do InitFcn (carregados na inicialização)

```matlab
omega  = 2π × 60          % rad/s
Vcc    = 136363.6 V       % barramento CC (90909.09 × 1.5) — override de simulação, ver [[params-workflow]]
Ts     = 5e-6 s           % passo EMT (200 kHz)
fsw    = 5000 Hz          % frequência de chaveamento
Tsc    = 2e-4 s           % passo do controle (5 kHz)

% Filtro LCL
L1     = 30.42 mH
L2     = 0.289 mH
C1     = 42.47 µF
Rd1    = 0.5734 Ω, Rd2 = 0.00545 Ω, Rd3 = 3.123 Ω
wres   = 9068.99 rad/s    % → fres ≈ 1443 Hz
qsi    = 0.707

% Thevenin na Barra 2
Rth    = 0.01004 Ω
Lth    = 1.16 mH
Lfault = 5.305 mH         % indutância de falta

% Controlador (aplicado com /4)
Kp     = 29.48 / 4 = 7.37
Ki     = 7075.6 / 4 = 1768.9
```

## Hierarquia do Modelo (nível raiz)

```
system_root (IEEE 9 barras)
├── Bus1..Bus9 (Simscape electrical buses)
├── TF 4-1, TF 7-2, TF 9-3 (transformadores)
├── B4-B5, B4-B6, B5-B7, B6-B9, B7-B8, B8-B9 (linhas 50-100 km)
├── Load A: 125 MW/50 MVAr  (Bus5)
│   Load B:  90 MW/30 MVAr  (Bus6)
│   Load C: 100 MW/35 MVAr  (Bus8)
├── Gen1@Bus1  [Swing]  — AVR + Exciter + Governor + Prime Mover
├── Gen2@Bus2  [PV, 163 MW, 1.025 pu] — ainda presente no modelo*
├── Gen3@Bus3  [PV, 85 MW, 1.025 pu]  — AVR + Governor
├── Fault (Three-Phase)  — falta configurable
└── UFV Model  [VSI na Bus2]
```

*Gen2 (máquina síncrona) ainda existe no XML — verificar se está desconectado ou em paralelo com o VSI.

## UFV Model — Subsistema do Inversor (SID=3896)

```
UFV Model
├── VDC1            — fonte CC (Vcc)
├── mH, mH1, mH2   — L1, L2, Lth (filtro LCL, Simscape)
├── Inverter        — ponte VSI 3 fases (Simscape)
├── Gate driver     — 6 sinais de gate → Six-Pulse Gate Multiplexer
├── Measurement inverter   — sensores I/V entre L1 e C1
├── Measurement inverter1  — sensores I/V entre C1 e L2
├── Optimal controller     — controle principal (PLL + corrente)
├── Fourier Analysis (×2)  — análise harmônica
└── Scopes
```

## Optimal Controller — Controle Principal (SID=3963)

```
Entradas: id_ref, Vabc_grid, Iabc (pu)
│
├── SRF-PLL montado com blocos (é o PLL que atua)
│     Vabc_grid → Park Transform (θ_PLL) → Selector2 (só v_q)
│     → PI (SID=4614: Gain kp_pll + ki_pll·∫, integrador parte de 2π·60) = ω
│     → Angle (SID=4607: integrador com wrap) = θ → Goto AngPLL
│     |v_dq| (Pythagorian Sum) só alimenta o Scope "PLL"
├── Sinusoidal Measurement (PLL, Three-Phase) — bloco de biblioteca SOLTO:
│     nenhuma ligação; o Kp_LF/Ki_LF dele não atua
├── Discrete Transfer Fcn (notch 120 Hz do PLL) — comentado e solto (histórico)
│
├── Park Transform1 (Iabc, θ) → Selector/Demux → I_d, I_q → PWM Control
├── Park Transform2 (Vabc_inverter, θ) → √(v_d²+v_q²) → 1/(0,005s+1)
│     → MATLAB Function (in1: módulo filtrado da tensão do INVERSOR)
│
├── MATLAB Function (SID=4439) — função ONS_2_11 (chart_14.xml)
│     Implementa suporte reativo per ONS Subm. 2.10 §5.8
│     Saídas: id_ref, iq_ref, fault_flag
│     Ver [[ons-2-11]] para código completo e lógica das 3 zonas
│
├── PWM Control ─────────────────────────────────────
│     Entradas: Idref, Iqref, Id, Iq
│     ├── Gain Kp/4 (×2, eixos d e q)
│     ├── Gain Ki/4 + Integrador (×2) — ação integral PI (integrador saturado em ±2)
│     ├── Transfer Fcn (Notch) ×2:
│     │     Num = [1, 0, wres²]
│     │     Den = [1, 2·qsi·wres, wres²]
│     └── Saída: mdq (índices de modulação dq)
│
├── Inverse Park Transform (dq → abc)
│
├── PWM VB — comparador SPWM
│     Repeating Sequence (portadora triangular) vs mdq
│     → 3 Relational Operators → 6 sinais de chaveamento S
│
└── Saída: S → Gate driver
```

## Scopes e Extração de Dados (slx-runner)

30 Scopes no total. Os principais para o TCC (com SID e sinais):

| Scope | SID | Subsistema | Sinais (porta → descrição) |
|---|---|---|---|
| `Ang` | 3967 | 3963 Optimal Controller | p1 → **ângulo PLL** (rad) |
| `MDQ` | 3972 | 3963 | p1 → modulação Mdq |
| `Active & Reactive Power` | 4022 | 4021 | p1 → P_inv (pu), p2 → Q_inv (pu) |
| `Currents` | 4023 | 4021 | p1 → Iabc_inv (pu), p2 → Iabc_grid (pu) |
| `Voltages` | 4078 | 4021 | p1 → Vabc_inv, p2 → Vabc_grid, p3 → Vab_synch |
| `From2`/`From1` (Vabc) | 4032/4025 | 4021 Scopes | logging habilitado 2026-07-12 (`vabc_inverter`/`vabc_grid`) → `sim_data_abc.csv`, ver [[export-workflow]] |
| `id` | 4079 | 4021 | p1 → id ref + medido (pu) |
| `iq` | 4080 | 4021 | p1 → iq ref + medido (pu) |
| `Ang Vdd` | 4495 | 3896 UFV | p1 → mod(Fourier+RepSeq,2π), p2 → AngPLL |
| `Ang Vdd1` | 4501 | 3896 UFV | p1 → fase Fourier bruta de Va_inv (rad) |
| `Bus 1`…`Bus 9` | 4138…4392 | 4396 monitor | p1→P, p2→Q, p3→V por barra |
| `Ang barra` | 4494 | root | p1 → ângulo de barra Simscape |

> **P/Q do monitor de barras saem em unidades físicas (W/VAr), não pu** — taps
> `Goto`/`From` diretos das Busbars (SID 1887 Bus1, SID 3494 Bus3) via
> `PS-Simulink Converter`, sem nenhum Gain de normalização. Diferente do bloco
> "Inverter Active & Reactive Power" (SID 4055, alimenta `Pinverter`/`Qinverter`),
> que recebe `Vabc`/`Iabc` já em pu. O export MATLAB (`add_power_col`, ver
> `kb/simulation/export_workflow.md`) divide `P_bus{N}`/`Q_bus{N}` por
> `S_base = 100 MVA` para corrigir isso.
>
> **Ganhos do SID 4055 corrigidos em 2026-10-03.** Com `Vabc`/`Iabc` em pu de
> pico, o pu é P = (2/3)·Σv·i e Q = (2/(3√3))·Σi·v_ff. O bloco tinha 1/√3
> nos dois (Gain1 SID 4060 → P, Gain SID 4059 → Q): P saía ×√3/2 (pré-falta
> 0,87 pu com id = 1) e Q ×1,5. Hoje 2/3 e 2/(3*sqrt(3)); rodadas antigas são
> reescaladas na leitura, ver [[export-workflow]].

### Cadeia Fourier → Ângulo Absoluto (subsistema UFV, SID 3896)

```
Va_inverter (Vabc_inverter via From2)
  → Demux (SID 4490)
  → Fourier Analysis (SID 4486, f=60 Hz, n=[1]) — extrai fase φ do fundamental
        out:2 (fase φ) ──┐
                         ├─ Sum (SID 4497, ++) ─→ Mod(⋅, 2π) ─→ Ang Vdd p1
Repeating Sequence ──────┘        (SID 4502)      (ângulo absoluto wrapped)
(SID 4500, 0→2π em T=1/60 s = ωt)
        out:2 (fase φ) ──→ Ang Vdd1 p1   (fase bruta, antes do mod)

AngPLL (via Goto SID 4504 no Optimal Controller, tag=AngPLL)
  → From3 (SID 4505) → Ang Vdd p2   (PLL para comparação direta)
```

Extração via `slx-runner` skill (não modifica o .slx):
```python
from runner import run_simulation
from analyze import plot_angle_comparison
data = run_simulation(signals=['ang_pll', 'ang_vdd', 'rep_seq', 'p_inv', 'q_inv'])
plot_angle_comparison(data['t'], data['ang_vdd'], data['ang_pll'], data['rep_seq'])
```
Ver `.claude/skills/slx-runner/SKILL.md` para uso completo.

## Observações Importantes

- **Kp e Ki são divididos por 4** tanto no notebook quanto no modelo — consistente.
- **Notch implementado em ambos os eixos** (d e q) para amortecimento ativo da ressonância LCL.
- **PLL montado com blocos, não o de biblioteca:** Park → v_q → PI (`kp_pll`/`ki_pll` do `params.m`, Gains do SID 4614) → integrador com wrap. O `Sinusoidal Measurement (PLL, Three-Phase)` continua no diagrama, com `Kp_LF`/`Ki_LF` gravados, mas **sem nenhuma ligação** (conferido no grafo em 2026-10-02; a KB dizia o contrário até então). Ganhos: [[pll-loop-filter-gains]], **não** o `Kp`/`Ki` de [[pll-gains-methodology]], que é o controlador de corrente.
- **PWM é SPWM** (comparador com portadora triangular), não SVPWM.
- **Controle de corrente sem desacoplamento ωL nem feedforward de v_g:** PI → notch → `m_dq` direto, sem `/V_cc` (Mux com eixo 0 = 0). A teoria da TeseAGP prevê o desacoplamento; a implementação não ([[agp-current-control-theory]]).
- **Onde entram v_gd e v_gq (tensão da rede em dq):** só no PLL, e só o v_q (o módulo vai para scope). O controle de corrente não recebe tensão nenhuma: as 4 entradas do PWM Control são I_d,ref, I_q,ref, I_d e I_q. A única tensão que chega às referências é o **módulo da tensão do inversor**, filtrado (τ = 5 ms), na MATLAB Function do ONS. Base da Figura 3.1 do TCC (`assets/diagrams/current_control_dq_blocos.svg`).
- **Ts = 5 µs** (EMT), **Tsc = 200 µs** (controle) — razão de 40× entre passos.
- `wres = 9068.99 rad/s` → `fres ≈ 1443 Hz` (não confundir rad/s com Hz).
