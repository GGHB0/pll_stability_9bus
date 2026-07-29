---
name: china-lvrt-windfarm-test
description: Norma chinesa Q/GDW392-2009 de LVRT e teste de campo em turbina eólica PMSG (Mongólia Interior) — dados empíricos de falta simétrica vs. assimétrica
source: Hu, Meng, Bu, Ren, "Test and Analysis of Low Voltage Ride-through Characteristic of Wind Farm", IJAPE Vol.2 Issue 4, 2013, pp.186-191
references:
  - "HU; MENG; BU; REN. Test and Analysis of Low Voltage Ride-through Characteristic of Wind Farm. International Journal of Advancements in Power and Energy (IJAPE), v. 2, n. 4, p. 186-191, 2013. (prenomes completos não confirmados na extração)"
---

# LVRT — Norma Chinesa e Teste de Campo em Turbina Eólica

## Contexto

Artigo de teste de campo (não simulação) numa turbina PMSG de 850 kW (conversor
de potência plena, 690 V, 70 m de altura de cubo) em parque eólico na Mongólia
Interior, conforme a norma chinesa **Q/GDW392-2009** ("technical regulations for
wind farms connected to power grid") e IEC 61400-21:2008.

## Curva LVRT e Suporte Reativo Dinâmico

Estrutura igual à do `ONS_2_11` e à do IEEE 1547: afundamento a 20% da tensão
nominal por até 625 ms, recuperação a 90% dentro de 2 s pós-eliminação da falta.

**Fórmula de corrente reativa dinâmica** (equivalente ao droop do `ONS_2_11`):

```
ΔI_Q = 1,5 · (0,9 − U_T) · I_N        para 0,2 ≤ U_T ≤ 0,9 pu
```

onde `U_T` é a tensão do PCC em pu e `I_N` a corrente nominal do parque.

**Tempo de resposta normativo:** ≤ 75 ms desde o instante do afundamento;
duração mínima do suporte: ≥ 550 ms.

### Comparação de Ganho de Droop entre Normas

| Norma | Ganho de corrente reativa | Referência de tensão |
|---|---|---|
| China Q/GDW392-2009 | `1,5·(0,9−U_T)` | Magnitude absoluta de U_T |
| ONS Submódulo 2.10 (`ONS_2_11`) | droop linear direto | Magnitude absoluta de V_pcc |
| IEEE 1547-2018 DVS (§6.4.2.6) | proporcional a %ΔV | Desvio de média móvel pré-evento |

Três normas, três referências diferentes de tensão — ver
[ieee1547_ride_through.md](ieee1547_ride_through.md) para a tabela completa
IEEE × ONS. O coeficiente chinês (1,5) e a estrutura de droop absoluto são
estruturalmente mais próximos do `ONS_2_11` do que do DVS do IEEE (que usa
`Vaverage` móvel).

## Resultados de Campo — Simétrico vs. Assimétrico (P ≥ 0,9 Pn)

### Afundamento a 20% Un, falta trifásica simétrica

- Tensão: 1,0 → 0,20 pu, duração 625 ms
- Potência ativa P: 1,0 pu → **0,24 pu** (colapso quase total)
- Potência reativa Q: praticamente nula (0,01 pu) — quase sem suporte de tensão
- Recuperação: P volta a 0,98 pu, Q retorna a zero (fator de potência unitário)

### Afundamento a 20% Un, falta bifásica assimétrica

- Tensão de linha U_bc: 1,0 → 0,20 pu, mesma duração (625 ms)
- Potência ativa P: mantida em **0,82 pu** (bem menos afetada que o caso simétrico)
- Potência reativa Q: **0,27 pu** (suporte de tensão real, ao contrário do caso simétrico)
- **Desequilíbrio de corrente entre fases:** A = 1,0 pu, B = 0,87 pu, C = 1,45 pu
  (todas dentro do limite do conversor, mas claramente assimétricas)

### Leitura para o TCC

O caso assimétrico produz **desequilíbrio de corrente entre fases** — manifestação
física, em dado de campo, do mesmo fenômeno que a análise formal de
[pll_contingencies.md](../pll/pll_contingencies.md) (Yazdani-Iravani §12.5.2) descreve
para o SRF-PLL: a componente de sequência negativa introduzida por faltas
desbalanceadas. Lá o efeito é derivado como oscilação de 2ª harmônica (120 Hz) em
`Vsq` e ripple em P/Q; aqui aparece como corrente de fase desigual num conversor de
potência plena real. É um dado comparativo útil (turbina PMSG, não inversor
fotovoltaico, mas mesma interface de eletrônica de potência) — não implica que
esta turbina usa SRF-PLL sem filtro de sequência negativa, já que o artigo não
detalha a malha de controle interna.

Contraste notável: no caso simétrico a reativa quase não responde (Q≈0,01 pu)
apesar da norma prever suporte dinâmico — sugere que, em afundamento profundo e
balanceado, a prioridade do controle vai para conter o colapso de ativa (limite de
corrente do conversor), similar ao trade-off de Q-priority discutido em
[ieee1547_ride_through.md](ieee1547_ride_through.md).

## Ver também

- [lvrt.md](lvrt.md) — definição geral de LVRT
- [ieee1547_ride_through.md](ieee1547_ride_through.md) — categorias, Table 8, DVS, comparação com `ONS_2_11`
- [ons_2_11.md](ons_2_11.md) — implementação real no modelo Simulink do TCC
- [pll_contingencies.md](../pll/pll_contingencies.md) — análise formal de falta assimétrica no SRF-PLL (Yazdani-Iravani §12.5.2)
