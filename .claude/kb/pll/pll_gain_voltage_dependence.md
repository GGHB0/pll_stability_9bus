---
name: pll-gain-voltage-dependence
description: A sintonia do SRF-PLL degrada com a profundidade do afundamento (ωn e ξ ∝ √U) porque o laço é normalizado por constante — equivalência algébrica exata entre o cenário BAD_PLL e o PLL nominal sob U = 0,2 pu
source: Karimi-Ghartemani 2014 eq. (6.4) p.135; Teodorescu-Liserre-Rodríguez 2011 §4.2.2.3 p.56; params.m; PSim/01_Sistema PLL_vfinal_100MVA (backup)1.txt
references:
  - "KARIMI-GHARTEMANI, Masoud. Enhanced Phase-Locked Loop Structures for Power and Energy Applications. Hoboken: John Wiley & Sons / IEEE Press, 2014. ISBN 978-1-118-79502-6."
  - "TEODORESCU, Remus; LISERRE, Marco; RODRÍGUEZ, Pedro. Grid Converters for Photovoltaic and Wind Power Systems. Chichester: John Wiley & Sons, Ltd, 2011. ISBN 978-0-470-05751-3."
metadata:
  type: project
---

# Dependência da Sintonia do SRF-PLL com a Amplitude da Tensão

> Achado de 2026-09-12, na discussão do Cap. 7. O trabalho futuro que ele
> sustentava (Eixo 2) foi **descartado**; o **valor que sobra é a equivalência
> com o cenário BAD_PLL**, que é material de Cap. 5 / defesa em banca. Complementa [[pll-gains-provenance]]
> (que documenta *por que* `U = 1 pu`) e [[pll-loop-filter-gains]] (que
> documenta o projeto dos ganhos).

## O fato de partida

O sensoriamento do PLL tem ganho **constante** `1/16.329,93 V`, o pico de fase
**nominal** (`20 kV · √2/√3`), rastreado no netlist PSIM em
[[pll-gains-provenance]]. Esse divisor não acompanha a tensão real: ele é o
valor de base, não a amplitude medida. É isso que faz `U = 1 pu` valer **no
nominal** e só no nominal.

## A consequência algébrica

Polinômio característico do SRF-PLL linearizado (Karimi eq. 6.4), com `U` =
magnitude da tensão de entrada em pu:

```text
s² + Kp·U·s + Ki·U = 0
```

Logo:

```text
ω_n = √(Ki·U)            ξ = (Kp/2)·√(U/Ki)
```

**Ambos escalam com `√U`.** A sintonia do PLL não é um projeto fixo: ela
degrada sozinha conforme a tensão afunda. O ganho do detector de fase cai
exatamente quando o laço mais precisa dele.

| `U` (pu) | `ω_n` (rad/s) | `ξ` |
|---|---|---|
| 1,00 | 325,3 | 0,707 |
| 0,50 | 230,0 | 0,500 |
| 0,20 | 145,5 | 0,316 |
| 0,10 | 102,9 | 0,224 |

(`Kp,PLL = 460`, `Ki,PLL = 105.820`.)

## A equivalência com o cenário BAD_PLL

O cenário de **sintonia inadequada** multiplica `kp_pll` **e** `ki_pll` por 0,2
(ver [[project_bad_pll]] na memória), resultando em `ω_n = 145,5` e `ξ = 0,316`
— registrados em §4.3.2.3 do TCC.

São **exatamente** os valores da linha `U = 0,20` da tabela acima. Não é
coincidência: no polinômio só entram os **produtos** `Kp·U` e `Ki·U`, então

```text
(0,2·Kp, 0,2·Ki, U = 1)   ≡   (Kp, Ki, U = 0,2)
```

são o mesmo sistema linearizado.

### Leitura

**O PLL com sintonia nominal, durante um afundamento a 0,2 pu no PCC, *é* o
PLL "mal sintonizado" do trabalho.** O cenário `bad_pll` não é apenas uma
hipótese de projeto malfeito: é a condição dinâmica que qualquer SRF-PLL não
normalizado atravessa durante uma falta severa. Isso valida retroativamente a
relevância física do cenário.

## Ressalvas (obrigatórias se isso for para o texto)

1. **A equivalência é do modelo linearizado.** Ela explica a degradação da
   sintonia, **não** descreve a perda de travamento em si, que é fenômeno de
   grande sinal (cycle slipping, ver [[pll-cycle-slip-measurement]]). Nos dois
   casos a resposta de pequenos sinais coincide; o caminho para fora do
   travamento não é o mesmo.
2. **O `U` relevante é a tensão no PCC**, não a da barra faltosa. A
   correspondência com um cenário simulado específico exige ler `Vpcc_pu` no
   patamar da falta, o que ainda **não foi feito**.
3. Sob falta assimétrica há ainda o ripple de `2ω₀` somado ao rebaixamento de
   `U` (ver [[pll-asymmetric-fault-formal-analysis]]) — os dois efeitos
   coexistem e a equivalência acima cobre só o segundo.

## Uso deste achado (o que caiu e o que fica)

**O trabalho futuro derivado daqui foi descartado** pelo usuário em
2026-09-12 (Eixo 2 de [[tcc-trabalhos-futuros]]). Não repropor. O que segue é
o registro técnico da rota que foi considerada.

A correção natural seria **normalizar o erro de fase pela amplitude estimada**
(`v_q/|v|` no lugar de `v_q` cru), fixando o ganho de laço e tornando a
dinâmica do PLL invariante à profundidade do afundamento. Custo: um bloco a
mais no modelo. Limites: com `U → 0` a divisão precisa de limiar/saturação, e
a normalização **não** remove a sequência negativa — por isso o Eixo 2 se
apoia no Eixo 1, em vez de substituí-lo.
