---
name: simulink-model
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
├── Sinusoidal Measurement (PLL, Three-Phase) ← bloco de biblioteca Simscape
│     └── estima θ e ω da rede
│
├── Park Transform1 / Park Transform2 (abc → dq)
│
├── MATLAB Function (SID=4439) — função ONS_2_11 (chart_14.xml)
│     Implementa suporte reativo per ONS Subm. 2.10 §5.8
│     Saídas: id_ref, iq_ref, fault_flag
│     Ver [[ons-2-11]] para código completo e lógica das 3 zonas
│
├── PWM Control ─────────────────────────────────────
│     Entradas: Idref, Iqref, Id, Iq
│     ├── Gain Kp/4 (×2, eixos d e q)
│     ├── Gain Ki/4 + Integrador (×2) — ação integral PI
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

## Observações Importantes

- **Kp e Ki são divididos por 4** tanto no notebook quanto no modelo — consistente.
- **Notch implementado em ambos os eixos** (d e q) para amortecimento ativo da ressonância LCL.
- **PLL usa bloco de biblioteca** (`Sinusoidal Measurement (PLL, Three-Phase)`) — não é implementação manual. Os ganhos internos correspondem ao Kp/Ki da metodologia [[pll-gains-methodology]].
- **PWM é SPWM** (comparador com portadora triangular), não SVPWM.
- **Ts = 5 µs** (EMT), **Tsc = 200 µs** (controle) — razão de 40× entre passos.
- `wres = 9068.99 rad/s` → `fres ≈ 1443 Hz` (não confundir rad/s com Hz).
