---
name: lcl-filter
description: Dimensionamento do filtro LCL do inversor VSC (TeseAGP p.102-104 + notebook célula 30)
source: TeseAGP p.78-80 (eqs. 4.1, 3.52); notebooks/pll_stability_9bus_analysis.ipynb célula 30
---

# Filtro LCL — Dimensionamento

## Critério de L1 (ripple de corrente)

```
ΔiL1 = Vcc / (24 · L1 · fs)   →   L1 = Vcc / (ΔiL1 · 24 · fs)
```

- `ΔiL1 < 10%·Ipico` (critério de ripple admissível)
- Reatância de L1 em 60 Hz deve ser ≤ 5% na base Zb

## Critério de L2 e C1 (frequência de ressonância)

```
fres = (1/2π) · sqrt((L1+L2)/(L1·L2·C1))  <  fs/2
```

Escolher `fres` suficientemente abaixo de `fs/2` (Nyquist).

## Frequência de Ressonância com Rede

Com `Lg` presente, L2 efetivo → `L2 + Lg`:

```
ωres = sqrt((L1+L2+Lg) / (L1·(L2+Lg)·C1))
```

Isso é o `ωres_est` usado no projeto do filtro Notch para amortecimento ativo.

## Implementação no Notebook

```python
fs     = 5e3          # Hz (chaveamento)
k      = 0.0095       # razão L2/L1
Iripple = I_pico * 0.0061   # 0,61% do pico

L1  = Vcc / (Iripple * 24 * fs)
L2  = k * L1
Lest = L1 + L2 + Lg   # Lg=0 por padrão

C1x = (L1+L2) / (L1*L2*(np.pi*fs)**2)
C1  = 3 * C1x         # margem adicional de 3x

# Resistores de amortecimento passivo (5% de Xcomponente em 60 Hz)
Rd1 = 0.05 * ωg * L1
Rd2 = 0.05 * ωg * L2
Rd3 = 0.05 / (ωg * C1)

wres = sqrt((L1+L2+Lg) / (L1*(L2+Lg)*C1))
```

## Valores de Referência (TeseAGP, 220V/5kVA/60Hz)

| Componente | Valor | Critério |
|---|---|---|
| L1 | 1 mH | ΔiL1 < 10%, X ≈ 3,9% em Zb |
| L2 | 0,5 mH | garantir comportamento com rede forte |
| C1 | 6,8 µF | fres = 3,34 kHz < fs/2 = 6 kHz |
| fres | 2,07–3,34 kHz | varia com Lg de 6 mH a 0 mH |

## Vcc — Base AGP vs Override de Simulação

Notebook usa `Vcc = ((V_rms·500)/220)·2 = 90 909 V` (base teórica AGP).
`params.m` aplica override `×1,5 → 136 364 V` por necessidade prática da simulação.
**L₁/L₂/C₁/R_d ficam idênticos** porque foram calculados com Vcc = 90 909 V em ambos.
Ver [[params-workflow]] para regras de regeneração.

## Amortecimento Ativo (Notch)

Quando Rd = 0 (sem resistência externa), usa-se filtro Notch em cascata:

```
N_hat(s) = (s² + ωres²) / (s² + 2·ξp·ωres·s + ωres²)
```

com `ξp = 0,7`. Aplicado no laço de corrente para amortecer os polos de ressonância do LCL.
