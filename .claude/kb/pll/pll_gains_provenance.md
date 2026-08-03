---
name: pll-gains-provenance
description: Procedência dos ganhos do SRF-PLL — literais hardcoded no netlist PSIM, cadeia PSIM→Simulink→params.m, e a dedução de que o laço está normalizado (U = 1 pu)
source: PSim/01_Sistema PLL_vfinal_100MVA (backup)1.txt; PSim/parameters100MVA.txt; params.m (commit 219f6ee); Karimi-Ghartemani 2014 p.135; Teodorescu-Liserre-Rodríguez 2011 §4.2.2.3 p.56
references:
  - "KARIMI-GHARTEMANI, Masoud. Enhanced Phase-Locked Loop Structures for Power and Energy Applications. Hoboken: John Wiley & Sons / IEEE Press, 2014. ISBN 978-1-118-79502-6."
  - "TEODORESCU, Remus; LISERRE, Marco; RODRÍGUEZ, Pedro. Grid Converters for Photovoltaic and Wind Power Systems. Chichester: John Wiley & Sons, Ltd, 2011. ISBN 978-0-470-05751-3."
---

# Procedência dos Ganhos do SRF-PLL

Complemento de [[pll-loop-filter-gains]], que documenta **como os ganhos foram
projetados**. Este arquivo cobre **de onde os números vieram fisicamente** e por
que o laço pode ser tratado como normalizado.

## Origem: hardcoded no esquemático PSIM

O **cálculo não está registrado em nenhum arquivo do repositório** — o método
está reconstruído em [[pll-loop-filter-gains]], mas os valores entram como
constantes literais nos blocos proporcionais do netlist PSIM
(`PSim/01_Sistema PLL_vfinal_100MVA (backup)1.txt`):

```text
I     B1     1 2 1 0 -inf inf     ← integrador sobre Vq
P     P8     2 5 105820           ← ramo integral    (ki_pll)
P     P9     1 6 460              ← ramo proporcional (kp_pll)
SUM2P SUMP2  6 5 7 1 1            ← P + I = deltaw
SUM2P SUMP3  7 9 3 1 1            ← deltaw + wRede (376,8 rad/s) = w0
RESETI_I RESETI_I1 3 4 ... 6,2831853   ← VCO (integrador com reset em 2π) → theta
P     P10    3 8 0,1591549430918953    ← 1/(2π) → Freq [Hz]
```

Estrutura canônica Park → PI → VCO, igual à Fig. 6.1 do Karimi.

Evidência de que nunca passaram pelo cálculo dentro do repositório: o arquivo de
parâmetros do PSIM (`PSim/parameters100MVA.txt`) carrega `Vcc`, `L1`, `L2`,
`C1`, `Rd1-3`, `Kp`, `Ki`, `qsi`, `wres`, `Rth`, `Lth` — e **não** contém
`kp_pll`/`ki_pll`.

Cadeia até hoje, toda por transcrição:

1. PSIM — literais em `P8`/`P9`
2. Simulink — hardcoded dentro do bloco `Sinusoidal Measurement (PLL,
   Three-Phase)` como `Kp_LF`/`Ki_LF` (ver [[pll-notch-implementation]])
3. `params.m` — commit `219f6ee` (27/06/2026), 3 linhas, sem justificativa

## Normalização: por que `U = 1 pu`

A eq. (6.4) do Karimi é `s² + h0·U·s + h1·U = 0`, com `U` = magnitude da tensão
de entrada. Para `Kp = 2ξωn` valer sem o `/U`, o laço precisa estar normalizado.
Está — rastreando o netlist:

```text
VSEN3 (Vapcc) → P17 ganho 6,123724356957945e-5 = 1 / 16 329,93
                                     16 329,93 = 20 000 · √(2/3)
```

Propagando pelos ganhos das transformadas:

| Bloco | Ganho | Efeito no pico |
|---|---|---|
| Clarke `P4` / `P7` | 0,816497 (√⅔) / 0,707107 | `A → 1,224745·A` (α, β) |
| Park `P1` / `P2` | −0,816497 | `1,224745·A → A` (d, q) |

O módulo do vetor dq sai igual à entrada normalizada. Com `V_base = 20 kV
linha-linha RMS` → `V_pico_fase = 20 000·√2/√3 = 16 329,93 V`, o ganho de
sensoriamento é exatamente `1/V_pico_fase` → **`U = 1 pu` no nominal**.

Duas confirmações independentes:

- **Karimi p.135** — os ganhos são fixados "based on the nominal value of the
  input signal magnitude".
- **Teodorescu §4.2.2.3, p.56** — a eq. (4.38) supõe explicitamente entrada
  unitária (`V = 1`); caso contrário os ganhos devem ser divididos pela
  amplitude.

> **Ressalva.** O parâmetro de amplitude da fonte `VSIN3` no netlist é `20000`.
> A leitura `U = 1` exige interpretá-lo como 20 kV linha-linha RMS (base do
> projeto). Se fosse pico por fase, sairia `U ≈ 1,22 pu` → `ωn ≈ 360 rad/s` e
> `ξ ≈ 0,78`. A leitura `U = 1` é a correta porque só ela reproduz `ξ = 0,707`,
> que é o `qsi` já gravado no `params.m`.

## Estado da documentação

O método de projeto está fechado e verificado contra os PDFs originais — ver
[[pll-loop-filter-gains]]. O que **não** existe é registro do cálculo dentro do
repositório: os valores sempre entraram como literais. A documentação atual é
reconstrução, conferida contra os ganhos gravados.
