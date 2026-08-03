---
name: psim-netlists
description: Topologia dos circuitos PSIM 01 (sistema EMT completo) e 04 (bancada de projeto do controle de corrente), lida das netlists em texto
source: PSim/01_...txt e PSim/04_...txt (netlists PSIM, GGHB, 2026-07-22)
---

# Topologia dos Circuitos PSIM

Lida das netlists em texto exportadas do PSIM e confirmada pelas capturas
dos esquemáticos. Formato de linha: `TIPO nome nó1 nó2 ... parâmetros`. Os
subcircuitos aparecem com prefixo (`Clarke.`, `Park.`, `Correnteref.`). Ver
visão geral em [[psim-modeling]].

> A numeração dos arquivos (`01`, `04`) é **arbitrária** — não indica ordem
> nem sequência de circuitos. São dois esquemáticos independentes.

## Sistema completo — EMT (arquivo `01_...`)

Inversor trifásico de 2 níveis conectado à rede via filtro LCL, com
SRF-PLL e SPWM. `.TIME`: passo 20 µs, total 1 s.

**Rede (Thévenin):**
- `VSIN3 VSIN32` — fonte trifásica senoidal, **20 kV / 60 Hz**.
- `RL3 RL5` — impedância de Thévenin (`Rth = 0,01004`, `Lth = 0,00116`).

**Filtro LCL:**
- `RL3 RL1` — indutor lado inversor (`Rd1 = 0,5734`, `L1 = 0,03042`).
- `RL3 RL2` — indutor lado rede (`Rd2 = 0,005447`, `L2 = 0,000289`).
- `RC3 RdC1` — ramo capacitivo com amortecimento (`Rd3 = 3,1228`,
  `C1 = 4,247e-5`).
- *Obs.:* os valores literais na netlist 01 vêm de `..._VCCnovo.txt`
  (não exportado); a ordem de grandeza bate com [[psim-modeling]].

**Conversor (VSC 2 níveis):**
- `VDC4` — barramento CC = **136,4 kV** (Vcc "novo", ver override em
  [[project_vcc_convention]]).
- `IGBT Q13…Q18` — ponte de 6 chaves (2 níveis).

**Modulação (SPWM):**
- `VTRI2` — portadora triangular, **5 kHz** (fs = 5 kHz).
- `COMP1…3` — comparadores; `NOTGATE`/`ONCTRL` geram os 6 pulsos de gate
  complementares. Índice de modulação `ma` (nó 73).

**Controle de corrente (dq):**
- `SUM10`/`SUM11` — erros de corrente (`idref−id`, `iqref−iq`).
- `TFCN1`/`TFCN2` — compensadores com **notch** na ressonância do LCL:
  numerador `{1, 0, ω_res²}`, denominador `{1, 2ξω_res, ω_res²}`
  (`ω_res² = 8,2247e7`, `2ξω_res = 12 823,6`). Ver
  [[pll-notch-implementation]].
- `DQ_ALPHABETA` → `ALPHABETA_ABC` — referências `md`/`mq` → abc.
- Referências `Idref`/`Iqref` vêm do subcircuito `Correnteref`
  (P/Q → corrente via `DIVD`).

**Medição:**
- `VSEN1…3` (tensões PCC), `ISEN3` (correntes), `ABC2DQO` (corrente do
  inversor → dq), `W3_KWH` (potência ativa), `VAR3` (reativa).

**SRF-PLL** (no esquemático, rotulado em 3 blocos canônicos):
- **Phase Detector (PD):** subcircuitos `Clarke` (abc → αβ) e `Park`
  (αβ → dq, com `SIN_R`/`COS_R` do ângulo estimado θ). Erro = `Vq`.
- **Proportional-Integral (PI):** ganhos `P8`/`P9` sobre `Vq` → `SUM` →
  soma com `w0` (`wRede = 376,8 rad/s`).
- **Voltage-Controlled Oscillator (VCO):** `RESETI_I` = **integrador com
  reset em 2π** que gera θ. Saídas `Freq`, `FasePLL`, `VPLL`.

**Perturbação:**
- `VSTEP2` — **degrau em t = 0,035 s** na referência (via `P28`,
  ganho 1e-8 → degrau de −1 na referência de corrente/Q). É um **degrau
  de referência**, mais simples que os cenários de falta do Simulink.

## Bancada de projeto do controle de corrente (arquivo `04_...`)

Testbench de controle (sem conversor/rede), comparando a resposta do PI
de corrente em duas plantas. `.TIME`: passo 10 µs, total 0,1 s.

**Malha 1 — planta RL simplificada:**
- PI: `P12` = `Kp/4` = 7,370, `P11` = `Ki/4` = 1768,89.
- `PlantaRL` = `TFCTN {0, 130,25}/{1, 18,85}` → `130,25 / (s + 18,85)`
  (1ª ordem). Referência `C1 = 1` (degrau). Saída `IdRL`.

**Malha 2 — planta LCL completa:**
- PI idêntico (`P13`, `P14` = `Ki/4`, `Kp/4`).
- `PlantaLCL` = `1/(5,83e-12·s)` (≈ integrador `1/sC`) em série com
  `PlantaLCL1` = `1/(s² + ω_res²)` (ressonância do LCL). Referência
  `C2 = 1`. Saída `IdLCL`.

**Propósito:** sintonizar o PI de corrente na aproximação RL e **validar
na planta LCL** (que exibe a ressonância) — passo clássico de projeto de
controle. É onde os ganhos `Kp`/`Ki` de [[pll-gains-methodology]] foram
projetados na fase PSIM.
