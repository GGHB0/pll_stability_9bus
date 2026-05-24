---
name: vsc-reference
description: Modelo e controle do VSC grid-imposed em dq-frame — referência Yazdani-Iravani Cap. 8 e Apêndice B
source: Yazdani & Iravani, Voltage-Sourced Converters in Power Systems, 2010, Cap. 8 e Apêndice B
---

# VSC Grid-Imposed — Modelo e Controle em dq-Frame

## Modelo da Malha de Corrente AC (eqs. 8.45–8.46)

Lado AC do VSC com R+ron e indutância L (termos cruzados Lω aparecem devido à rotação do dq):

```
L·(did/dt) =  Lω·iq − (R+ron)·id + Vtd − Vsd
L·(diq/dt) = −Lω·id − (R+ron)·iq + Vtq − Vsq
```

Desacoplamento cruzado + feed-forward de tensão de rede (eqs. 8.49–8.50):
```
md = (2/VDC)·[ud − Lω·iq + Vsd]
mq = (2/VDC)·[uq + Lω·id + Vsq]
```

Após desacoplamento, cada eixo vira um integrador de 1ª ordem independente:
```
Id(s)/Ud(s) = 1 / (Ls + R+ron)
```

## Controlador PI de Corrente — Pole-Zero Cancellation (eqs. 8.56–8.57)

```
kd(s) = kq(s) = kp·(s + ki/kp) / s
```

Cancelando o polo da planta em s = −(R+ron)/L:
```
kp = L / τi
ki = (R+ron) / τi
```

Malha fechada resultante (1ª ordem):
```
Id(s)/Idref(s) = 1 / (τi·s + 1)
```

**Faixa típica:** τi = 0,5–5 ms (deve ser ao menos 10× menor que 1/fsw em rad/s).

### Exemplo 8.2 (Yazdani-Iravani p.222)

| Parâmetro | Valor |
|-----------|-------|
| L | 100 µH |
| R+ron | 1,63 mΩ (R=0,75 + ron=0,88) |
| VDC | 1250 V |
| fsw | 3420 Hz |
| τi | 2,0 ms |
| kp | 0,05 Ω |
| ki | 0,815 Ω/s |

### Exemplo 8.4 (Yazdani-Iravani p.238) — NPC de 3 níveis

| Parâmetro | Valor |
|-----------|-------|
| L | 200 µH |
| R+ron | 3,26 mΩ |
| VDC | 2500 V |
| fsw | 1680 Hz |
| τi | 1,0 ms |
| kp | 0,2 Ω |
| ki | 3,26 Ω/s |

## Potência em Regime (PLL em lock: Vsq = 0)

```
Ps = (3/2)·Vsd·id    →   idref = (2 / 3Vsd)·Psref
Qs = −(3/2)·Vsd·iq   →   iqref = −(2 / 3Vsd)·Qsref
```

## Critério de Seleção de VDC (Seção 8.4.2, eqs. 8.58–8.59)

```
VDC ≥ 2·V̂t           (SPWM convencional)
VDC ≥ 1,74·V̂t        (PWM com injeção de 3° harmônico)
```

Pior caso logo após degrau em Ps (Qs=0, equação 8.70):
```
Vtd_max = Vsd + (2L / 3τi·Vsd)·ΔPs
V̂t_max  = sqrt(Vtd_max² + Vtq_max²)
```

### Exemplo 8.3 (Yazdani-Iravani p.225)

- Vsd = 0,391 kV, ΔPs = 2,5 MW, τi = 2 ms, L = 100 µH
- V̂t(t₀⁺) = 0,604 kV → VDC_min = 1,208 kV (SPWM) ou 1,050 kV (3°H)
- Escolhido: VDC = 1,250 kV, índice de modulação máx m̂ = 0,965 < 1

## Base em pu para VSC — Apêndice B (Tabelas B.1 e B.2)

### Lado AC

| Grandeza | Expressão | Observação |
|----------|-----------|------------|
| Vb | V̂s (pico L-N) | ≠ base convencional (rms L-N) |
| Pb | (3/2)·Vb·Ib | VA nominal trifásico |
| Ib | 2Pb / (3Vb) | pico da corrente nominal |
| Zb | Vb / Ib | |
| Lb | Zb / ωb | |
| Cb | 1 / (Zb·ωb) | |

### Lado DC

| Grandeza | Expressão |
|----------|-----------|
| Vb_dc | 2·Vb |
| Ib_dc | (3/4)·Ib |
| Rb_dc | (8/3)·Zb |

**Motivação de Vb_dc = 2·Vb:** garante que VDC = 1 pu + índice de modulação = 1 → tensão AC = 1 pu.

**Obs.:** os sinais md/mq **não** são expressos em pu (já adimensionais, |m| ≤ 1).

## Relação com o Modelo Simulink do Projeto

- L efetivo no modelo = L1 = 30,42 mH (fitro LCL), Vsd ≈ Vcc/2 após pu
- VDC = 136 363,6 V (Vcc no InitFcn) — base diferente da referência por se tratar de sistema 20 kV/100 MVA
- τi não explicitado no modelo; Kp/Ki divididos por 4 (ver [[simulink-model]] e [[pll-gains-methodology]])
