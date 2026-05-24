---
name: pll-gains-methodology
description: Metodologia de cálculo dos ganhos Kp/Ki do SRF-PLL usada no projeto (TeseAGP eqs 3.21-3.22 + notebook)
source: TeseAGP p.107-109 (Figs. 4.4, 4.5); notebooks/pll_stability_9bus_analysis.ipynb células 30/39
---

# Cálculo dos Ganhos do SRF-PLL — Metodologia do Projeto

## Equações Base (TeseAGP, eqs. 3.21 e 3.22)

```
Kp = 8 · fg · Lest
Ki = 32 · fg² · Lest
```

onde:
- `fg = 60 Hz` — frequência fundamental da rede
- `Lest ≈ L1 + L2 + Lg` — indutância total estimada (filtro + rede)
- `Lg` é estimado por injeção de harmônicos inter-harmônicos via CCBH

Origem das constantes 8 e 32: cancelamento polo-zero do controlador de corrente no referencial síncrono, projetado para frequência de cruzamento `ωgc ≈ 527,4 rad/s` com margem de fase `≈ 61,7°` (antes do Notch).

## Implementação no Notebook (`notebooks/pll_stability_9bus_analysis.ipynb`)

```python
# Célula 30 / 39
Lg   = 0                    # Lg=0: sem indutância de rede adicional explícita
Lest = L1 + L2 + Lg         # Lest = indutância equivalente total

Kp = 8 * 60 * (L1 + L2 + Lest)   # ≠ 8*fg*Lest da tese!
Ki = 32 * 60**2 * (L1 + L2 + Lest)
```

**Diferença em relação à tese:** o notebook usa `(L1+L2+Lest)` como argumento, não apenas `Lest`.
Com `Lg=0`: `Lest = L1+L2`, então o notebook calcula `Kp = 8·fg·2·(L1+L2)` — fator 2 a mais.
Isso é equivalente a considerar `Lest_efetivo = 2·(L1+L2)` na equação da tese.

## Estimação de Lest em Campo (TeseAGP, Fig. 4.4)

```
Lest = Vh / (ωh · Ih) · sin(θVh - θIh)
```

onde `Vh`, `Ih`, `θVh`, `θIh` são amplitude e fase da tensão/corrente na frequência inter-harmônica injetada `fh = 90 Hz` (3° harmônico de `f1 = 30 Hz`).

Relação com os parâmetros físicos:
```
Lg = Lest - (L1 + L2)
ωres_est = sqrt(Lest / (L1 · (L2 + Lg) · C1))
```

## Estabilidade com Variação de Lg (TeseAGP, Tabela 4.2)

| Lg (mH) | fres (kHz) | MF (°) | MG (dB) |
|---------|------------|--------|---------|
| 0       | 3,34       | 59,7   | 24,4    |
| 1,5     | 2,36       | 58,9   | 23,2    |
| 3,0     | 2,19       | 58,7   | 22,9    |
| 6,0     | 2,07       | 58,5   | 22,7    |

Sistema mantém margens satisfatórias (MF > 58°, MG > 22 dB) mesmo para rede fraca (Lg = 6 mH, SCR ≈ 5).

## Parâmetros do Sistema IEEE 9 Barras (Notebook)

```python
V_base = 20 kV,  S_base = 100 MVA,  Z_base = 4 Ω
fg = 60 Hz,  fs = 5 kHz  (chaveamento)
k = 0.0095  (razão L2/L1)

Vcc = (V_base * 500/220) * 2   # tensão CC proporcional à base
L1  = Vcc / (Iripple * 24 * fs)
L2  = k * L1
C1  = 3 * C1x   # C1x = (L1+L2)/(L1·L2·(π·fs)²)
```

Thevenin na Barra 2: `Z22 = Zbarra_ohm["Barra 2","Barra 2"]`
(diagonal da inversa da Ybarra × Z_base)
