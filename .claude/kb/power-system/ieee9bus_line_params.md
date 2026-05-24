---
name: ieee9bus-line-params
description: Parâmetros de linhas e transformadores — fonte artigo IEEE 2024, comparação A&F, divergência .slx
---

# IEEE 9-bus — Parâmetros de Rede

## Fonte dos Parâmetros (notebook)

Os valores usados no notebook são do sistema **modificado** da Figura 19 de:

> "Comparison of Power Swing Characteristics and Efficacy Analysis of
> Impedance-based Detections in Synchronous Generators and Grid-following Systems"
> IEEE Transactions on Power Systems, DOI 10.1109/TPWRS.2024.3469235

Não usar o Anderson & Fouad como referência de linha — os X diferem em 3 ramos.

## Transformadores (p.u., 100 MVA base)

| De-Para | X (p.u.) | SRated .slx | Nota |
|---------|----------|-------------|------|
| 1-4     | j0.0576  | 100 MVA     | TF 4-1, Yn/Δ, 230/16.5 kV |
| 2-7     | j0.0625  | 100 MVA     | TF 7-2, Yn/Δ, 230/18 kV   |
| 3-9     | j0.0586  | 100 MVA     | TF 9-3, Yn/Δ, 230/13.8 kV |

No .slx os trafos são divididos igualmente: pu_Xl1 = X/2, pu_Xl2 = X/2.
Esses valores coincidem exatamente entre notebook e .slx. ✓

## Linhas de Transmissão — notebook/artigo (p.u.)

| De | Para | R      | X      | B      |
|----|------|--------|--------|--------|
| 4  | 5    | 0.0100 | 0.0680 | 0.1760 |
| 4  | 6    | 0.0170 | 0.0920 | 0.1580 |
| 5  | 7    | 0.0320 | 0.1610 | 0.3060 |
| 6  | 9    | 0.0390 | 0.1738 | 0.3580 |
| 7  | 8    | 0.0085 | 0.0576 | 0.1490 |
| 8  | 9    | 0.0119 | 0.1008 | 0.2090 |

Nota: o notebook usa apenas R+jX (sem B) — susceptância ignorada no cálculo de Ybarra.

## Impedâncias de Geração — shunt nas barras (p.u.)

Representam xd' + X_trafo combinados (conforme Tabela 2.2 do Anderson & Fouad):

| Barra | Zg (p.u.) | xd' + X_trafo |
|-------|-----------|---------------|
| 1     | j0.1184   | 0.0608 + 0.0576 |
| 2     | j0.1823   | 0.1198 + 0.0625 |
| 3     | j0.2399   | 0.1813 + 0.0586 |

## Diferenças: Artigo 2024 vs Anderson & Fouad original

| Linha | X Anderson & Fouad | X Artigo 2024 (usado) | Δ      |
|-------|-------------------|-----------------------|--------|
| 4-5   | 0.0850 pu         | **0.0680 pu**         | −20%   |
| 7-8   | 0.0720 pu         | **0.0576 pu**         | −20%   |
| 6-9   | 0.1700 pu         | **0.1738 pu**         | +2.2%  |

## Divergência .slx vs Notebook

O .slx usa linhas de transmissão distribuídas (parâmetros físicos R Ω/km, L mH/km,
indutância mútua M mH/km, capacitâncias Cl/Cg µF/km). Convertendo para p.u.:

| Linha | X notebook | X .slx (calculado) | Status |
|-------|------------|--------------------|--------|
| 4-5   | 0.0680 pu  | **0.0850 pu**      | ⚠ diverge — único ramo com X diferente |
| 4-6   | 0.0920 pu  | 0.0920 pu          | ✓ |
| 5-7   | 0.1610 pu  | 0.1610 pu          | ✓ |
| 6-9   | 0.1738 pu  | 0.1700 pu          | ~2% |
| 7-8   | 0.0576 pu  | 0.0576 pu          | ✓ |
| 8-9   | 0.1008 pu  | 0.1008 pu          | ✓ |

**Linha 4-5 no .slx:** cabo físico B4-B5 (L=2.9658 mH/km, M=0.5803 mH/km, 50 km)
→ L_pos = L−M = 2.385 mH/km → X = 2π×60 × 2.385e-3 × 50 / 529 ≈ 0.085 pu.

**Resistências:** R_pu do .slx são 1.5–3× maiores que os do notebook em todas as linhas
(parâmetros reais de condutores vs. valores tabelados do benchmark). Impacto secundário
em Z22 pois R contribui pouco para o módulo da impedância Thevenin.

**Linha 7-8 no .slx:** representada por 4 segmentos em série de 5 km com parâmetros
dobrados (R×2, L×2, M×2) → X total ≈ 0.0576 pu. Coincide com o artigo. ✓

**Linha 8-9 no .slx:** 2 segmentos em paralelo de 100 km com parâmetros dobrados
→ X total ≈ 0.1008 pu. ✓
