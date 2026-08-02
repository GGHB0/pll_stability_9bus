---
name: pll-loop-filter-gains
description: Ganhos do PI do laço do SRF-PLL (kp_pll=460, ki_pll=105820) — projeto de 2ª ordem por tempo de acomodação (Alves 2020 eqs. 9-11 / Teodorescu eq. 4.38), ωn=325,3 e ξ=0,707
source: Alves-Dias-Rolim 2020 §4.1 eqs. (7)-(11); Teodorescu-Liserre-Rodríguez 2011 §4.2.2.3 p.56 eqs. (4.35)-(4.38); params.m; PSim/01_Sistema PLL_vfinal_100MVA (backup)1.txt; Karimi-Ghartemani 2014 eq. (6.4) p.135
references:
  - "ALVES, André G. P.; DIAS, Robson F. S.; ROLIM, Luís G. B. A Smooth Synchronization Methodology for the Reconnection of Autonomous Microgrids. Journal of Control, Automation and Electrical Systems, v. 31, p. 665-674, 2020. DOI 10.1007/s40313-020-00576-x."
  - "TEODORESCU, Remus; LISERRE, Marco; RODRÍGUEZ, Pedro. Grid Converters for Photovoltaic and Wind Power Systems. Chichester: John Wiley & Sons, Ltd, 2011. ISBN 978-0-470-05751-3."
  - "OGATA, Katsuhiko. Modern Control Engineering. 5. ed. London: Pearson, 2009."
  - "GOLESTAN, Saeed; GUERRERO, Josep M. Conventional Synchronous Reference Frame Phase-Locked Loop is an Adaptive Complex Filter. IEEE Transactions on Industrial Electronics, v. 62, n. 3, p. 1679-1682, 2015. DOI 10.1109/TIE.2014.2341594."
  - "FRANKLIN, Gene F.; POWELL, J. David; EMAMI-NAEINI, Abbas. Feedback Control of Dynamic Systems. 4. ed. Upper Saddle River: Prentice Hall, 2002. ISBN 0-13-032393-4."
  - "KARIMI-GHARTEMANI, Masoud. Enhanced Phase-Locked Loop Structures for Power and Energy Applications. Hoboken: John Wiley & Sons / IEEE Press, 2014. ISBN 978-1-118-79502-6."
---

# Ganhos do Filtro de Laço do SRF-PLL

## Não confundir com `Kp`/`Ki`

O `params.m` carrega **dois pares de ganhos distintos**:

| Variável | Valor | Malha | Metodologia |
|---|---|---|---|
| `kp_pll` / `ki_pll` | 460 / 105 820 | **PI do laço do SRF-PLL** | este arquivo |
| `Kp` / `Ki` | 29,4815/4 / 7075,56/4 | **controlador de corrente** | [[pll-gains-methodology]] |

A fórmula `Kp = 8·fg·Lest` da TeseAGP dimensiona o **controlador de corrente**,
não o PLL. Só `kp_pll`/`ki_pll` alimentam o bloco de sincronismo.

## Origem: hardcoded no esquemático PSIM

O **cálculo não está registrado em nenhum arquivo do repositório** — o método
está documentado na seção seguinte, mas os valores entram como constantes
literais nos blocos proporcionais do netlist PSIM
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

Evidência de que nunca passaram pelo cálculo: o arquivo de parâmetros do PSIM
(`PSim/parameters100MVA.txt`) carrega `Vcc`, `L1`, `L2`, `C1`, `Rd1-3`, `Kp`,
`Ki`, `qsi`, `wres`, `Rth`, `Lth` — e **não** contém `kp_pll`/`ki_pll`.

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

Isso é coerente com Karimi p.135: os ganhos são fixados "based on the nominal
value of the input signal magnitude".

> **Ressalva.** O parâmetro de amplitude da fonte `VSIN3` no netlist é `20000`.
> A leitura `U = 1` exige interpretá-lo como 20 kV linha-linha RMS (base do
> projeto). Se fosse pico por fase, sairia `U ≈ 1,22 pu` → `ωn ≈ 360 rad/s` e
> `ξ ≈ 0,78`. A leitura `U = 1` é a correta porque só ela reproduz `ξ = 0,707`,
> que é o `qsi` já gravado no `params.m` — ver seção seguinte.

## Método de projeto: 2ª ordem por tempo de acomodação

Fonte primária: **Alves, Dias & Rolim (2020), §4.1, eqs. (7)-(11)** — artigo do
próprio coorientador. A malha linearizada do SRF-PLL é de 2ª ordem:

```
G(s) = (Kp·s + Ki) / (s² + Kp·s + Ki)                 (7)
G(s) = (2ξωn·s + ωn²) / (s² + 2ξωn·s + ωn²)           (8)
```

Comparando (7) e (8):

```
Ki = ωn²             (9)
Kp = 2·√(Ki)·ξ = 2ξωn                                 (10)
ωn = 4 / (ts·ξ)      ← critério de 2%                 (11)
```

O artigo, citando Teodorescu et al. (2011) e Ogata (2009), estabelece:

- `ξ = 0,707` para resposta transitória ótima (overshoot ≈ 5%);
- `ts` escolhido **entre um e dois períodos da fundamental** da rede.

A mesma fórmula aparece no Teodorescu §4.2.2.3, p.56, eqs. (4.35)-(4.38), ali
na forma `Kp = 2ξωn = 9,2/ts` — que usa o critério de **1%** (`ts = 4,6/(ξωn)`,
apoiado em Franklin et al., ref. [14] do livro). Teodorescu observa
explicitamente que (4.38) supõe **entrada unitária (V = 1)**, senão os ganhos
devem ser divididos pela amplitude: confirmação independente da normalização
rastreada na seção anterior.

### Aplicação aos ganhos do projeto

Com `ξ = 0,707` (= `qsi` do `params.m`), invertendo (9) e (10):

```
ωn = √ki_pll = √105 820 = 325,30 rad/s   (51,8 Hz)
ξ  = kp_pll / (2·ωn) = 460 / 650,60 = 0,7070
ξωn = kp_pll/2 = 230
```

Na direção direta, partindo de `ωn = 325,3`:

```
Kp = 2 · 0,707 · 325,3 = 459,99      → 460       ✓
Ki = 325,3²            = 105 820,09  → 105 820   ✓
```

### ⚠️ Qual `ts`? Depende do critério

| Critério | Fórmula | `ts` resultante | em ciclos de 60 Hz |
|---|---|---|---|
| **2%** — Alves eq. (11) / Ogata | `ts = 4/(ξωn)` | **17,4 ms** | 1,04 T |
| **1%** — Teodorescu eq. (4.38) | `ts = 9,2/Kp` | **20,0 ms** | 1,20 T |

Os dois caem dentro da faixa "1 a 2 períodos" recomendada por Alves, e **os
números não permitem decidir qual foi usado**. A favor dos 20 ms: `9,2/0,020`
dá 460 exato, e um projetista escolhe `ts` redondo. A favor dos 17,4 ms: é o
critério que o artigo do coorientador de fato documenta.

Aferição do método no próprio artigo (Tabela 2, protótipo 15 V / 60 Hz):
`PI2 = PI4 = 400 + 40 000/s` → `ωn = 200`, `ξ = 1,0`, `ts = 20 ms` por (11).
Confirma a mecânica das equações, com outro par `ξ`/`ts`.

## Procedência e cadeia de citação

| Elemento | Citar |
|---|---|
| `Ki = ωn²`, `Kp = 2ξωn`, `ωn = 4/(ts·ξ)` | **Alves, Dias & Rolim (2020), §4.1, eqs. (9)-(11)** |
| Mesma sintonia na forma `Kp = 9,2/ts`; normalização por `V` | Teodorescu, Liserre & Rodríguez (2011), §4.2.2.3, p.56 |
| `ξ = 0,707` e critério de acomodação de 2ª ordem | Ogata (2009), 5. ed. — citado por Alves |
| Metodologia de sintonia por FT de malha fechada | Golestan & Guerrero (2015) — citado por Alves |
| Equação característica `s² + h0·U·s + h1·U = 0` | Karimi-Ghartemani (2014), eq. (6.4), p.135 |

> **Onde NÃO está:** Blaabjerg, Teodorescu, Liserre & Timbus, "Overview of
> Control and Grid Synchronization for Distributed Power Generation Systems"
> (IEEE TIE, 2006) cita PLL 23 vezes mas **não traz a fórmula de sintonia** —
> nenhuma ocorrência de settling time, damping ou frequência natural. Verificado
> em 2026-08-02; não reabrir.

## O que continua em aberto

`ts` é a única grandeza livre do projeto — todo o resto decorre dela e de
`ξ = 0,707`. Não há registro no repositório de qual valor foi escolhido nem por
quê (ver tabela dos dois critérios acima). Se o TCC precisar defender o valor, o
argumento natural é o compromisso entre banda de rastreamento e rejeição do
ripple de 2ω₀ sob falta assimétrica — ver [[pll-asymmetric-fault-formal-analysis]].

## Relação com o cenário BAD_PLL

`BAD_PLL` escala **os dois** ganhos por 0,2 (`params.m`), o que preserva a razão
`ki/kp` e portanto move o par no plano ξ–ωn assim:

```
kp' = 0,2·kp,  ki' = 0,2·ki
ωn' = √(0,2)·ωn = 0,447·325,3 = 145,5 rad/s
ξ'  = 0,2·kp / (2·ωn') = 92 / 291,0 = 0,3162 = 0,707·√0,2
```

Ou seja, o cenário degrada **banda e amortecimento simultaneamente**
(`ωn` e `ξ` ambos por `√0,2`), não só a velocidade de rastreamento — leitura
útil ao descrever a "sintonia inadequada" no TCC. Ver [[bad-pll-scenario]] e
[[pll-reactive-inertia]].
