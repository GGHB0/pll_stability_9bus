---
name: pll-gains-methodology
description: Metodologia TeseAGP (Kp=8·fg·Lest) dos ganhos do CONTROLADOR DE CORRENTE — não é o ganho do PLL, ver pll_loop_filter_gains.md
source: TeseAGP p.107-109 (Figs. 4.4, 4.5); notebooks/pll_stability_9bus_analysis.ipynb células 30/39
references:
  - "ALVES, André Gustavo Pereira. Metodologia para Auto-Ajuste de Controladores de Corrente em Conversores Fonte de Tensão Conectados a Redes Sujeitas a Distúrbios Harmônicos. Tese (Doutorado em Engenharia Elétrica) — COPPE/UFRJ, Rio de Janeiro, 2022."
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

> ⚠️ **Nota (2026-08-05).** A explicação acima (crossover/margem de fase) e a
> derivação de cancelamento polo-zero por `Ki/Kp=R/L` (fator 4) documentada
> em [[agp-current-control-theory]] são **ambas distintas** da explicação
> que o TCC efetivamente adotou (nova §3.5, Equações 3.21–3.23, entregue
> 2026-08-05): reaplicação da **forma canônica de 2ª ordem** já usada para o
> PLL (mesma Equação 3.18), com `ξ=1/√2=0,707` — idêntico ao do PLL — e
> `ωn=4√2·fg≈339,4 rad/s`. Essa leitura foi verificada algebricamente contra
> os números reais (`Kp=29,48`, `Ki=7075,6`, `Lest=61,42 mH`) e confirmada
> contra `pll_stability_9bus_analysis.ipynb` célula 41
> (`ωn≈339,4 rad/s, ξ=0,707`) — é a explicação mais bem verificada das três,
> mas nenhuma citação de página específica da TeseAGP foi feita no TCC para
> esta fórmula (decisão explícita do usuário, ver
> `kb/tcc-word/historico_entregas.md`).

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

## Armadilhas de leitura (verificadas 2026-08-04)

Três confusões recorrentes ao reescrever essas fórmulas em texto:

1. **É `fg`, não `ω0`.** A fórmula usa a frequência em **hertz** (60), não em
   rad/s. Confere: `8·60·(0,030421+0,000289+0,030710) = 29,481`, que é o valor
   gravado no modelo. Com `ω0 = 2π·60` sairia 96,1.
2. **`Lest` não é `Lth`.** Aqui `Lest = L1+L2 = 30,71 mH` (indutância do filtro
   vista pelo controlador, com `Lg=0`). O `Lth = 1,16 mH` que aparece nos
   parâmetros é a **indutância de Thévenin da rede** usada como fonte
   equivalente na fase PSIM (ver [[psim-modeling]] e [[ieee9bus-thevenin]]) —
   grandeza diferente, que só convive no mesmo arquivo. Trocar uma pela outra
   dá 15,30 no lugar de 29,48.
3. **Estes não são os ganhos do PLL.** `Kp`/`Ki` daqui alimentam o
   **controlador de corrente**, cuja saída vai para a modulante do SPWM. Os
   ganhos do laço de sincronismo são `kp_pll = 460` e `ki_pll = 105 820`,
   projetados por tempo de acomodação — ver [[pll-loop-filter-gains]]. A
   divisão por 4 também é exclusiva desta família: os ganhos do PLL entram no
   bloco de sincronismo sem escalamento algum.

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

Vcc = (V_base * 500/220) * 2   # tensão CC base AGP — params.m aplica ×1.5; Kp/Ki invariantes (ver [[params-workflow]])
L1  = Vcc / (Iripple * 24 * fs)
L2  = k * L1
C1  = 3 * C1x   # C1x = (L1+L2)/(L1·L2·(π·fs)²)
```

Thevenin na Barra 2: `Z22 = Zbarra_ohm["Barra 2","Barra 2"]`
(diagonal da inversa da Ybarra × Z_base)
