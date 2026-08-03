---
name: ieee1547-case-studies
description: Estudos de caso reais (CAISO, Entergy) sobre o impacto de ride-through/DVS de DER na recuperação de tensão do sistema — Annex I do IEEE Std 1547.2-2023
source: IEEE Std 1547.2-2023, Annex I, pp.263-268
references:
  - "IEEE. IEEE Application Guide for IEEE Std 1547-2018, IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces. IEEE Std 1547.2-2023, 2023."
---

# Estudos de Caso — Dynamic Voltage Support em Escala Real

Annex I do IEEE Std 1547.2-2023 reúne estudos de caso de operadores de rede
(CAISO, Entergy, NREL, ERCOT) sobre o efeito prático da categoria de
performance e do DVS (ver [ieee1547_ride_through.md](ieee1547_ride_through.md))
na estabilidade de tensão em cenários de alta penetração de DER.

## CAISO — Cenário 2029 Summer Peak (PG&E / Fresno)

- Modelo `DER_A` (positive-sequence, padrão NERC SPIDERWG) representando DER
  atrás do medidor como parte de carga composta, com stall de motores de
  indução monofásicos habilitado
- Cenário hipotético: DER elevado a 80% da capacidade instalada + carga +20%
  (PG&E: 9.270 MW instalados, 7.416 MW despachados)
- 5 casos comparados: sem DER, Categoria II sem/com controle de tensão,
  Categoria III sem/com controle de tensão

**Resultado:** Categoria III com DVS teve a melhor recuperação de tensão;
Categoria II sem controle de tensão teve a pior. A diferença é explicada por
**menos trip de DER** em Categoria III — no barramento de 70 kV próximo à
falta, a tensão do sistema se recupera em todos os casos, mas o DER **não
volta a operar** depois de trip, exceto no caso Categoria III + DVS.

## Entergy — Contingências P7 / bus faults com clearing atrasado

- 177 pontos de DER modelados com `DER_A`, carga composta com stall de
  motores monofásicos habilitado
- Falta trifásica com *stuck breaker* (disjuntor que falha em abrir): 10
  ciclos de clearing na extremidade próxima, **11 ciclos na extremidade
  distante**
- Comparação: DVS agressivo vs. não agressivo vs. tempo de ride-through
  estendido

**Resultado chave:** com o tempo de ride-through padrão (0,16 s — o mesmo
UV2 da Table 8), ~2,5 GW de DER desconectam porque a falta dura mais que o
ride-through permitido (11 ciclos ≈ 0,183 s > 0,16 s). Estendendo o
ride-through para **1,0 s**, todo o DER atravessa a falta sem desconectar, e
com DVS habilitado a resposta de tensão do sistema melhora significativamente.

## Relevância para o TCC

Esses estudos demonstram em escala de sistema real (não simulação de um
único inversor) exatamente o mecanismo que o TCC investiga em 9 barras: a
**margem entre o tempo de acomodação do controle (PLL + malha de corrente) e
o tempo de trip mandatório** determina se o DER contribui para a recuperação
pós-falta ou se agrava o colapso por desconexão em massa — o mesmo padrão
observado no apagão brasileiro de 15/08/2023 (ver
[brasil_2023_root_causes.md](../events/brasil_2023_root_causes.md)) e no
incidente ibérico de 28/04/2025 (ver
[iberia_2025_ibr_lessons.md](../events/iberia_2025_ibr_lessons.md)).

A diferença central: aqui o "trip" é uma decisão de proteção baseada em tempo
de exposição a subtensão (UV2 = 0,16 s), enquanto no TCC a falha de PLL é uma
**perda de sincronismo interna** que corrompe a direção da corrente injetada
mesmo sem trip — um modo de falha adicional não coberto pelos estudos de caso
do IEEE, que assumem controle de corrente/PLL ideal (`DER_A` é um modelo
fenomenológico, não representa dinâmica de PLL).

## Ver também

- [ieee1547_ride_through.md](ieee1547_ride_through.md) — requisitos normativos (Table 8, DVS) que estes estudos avaliam
- [ons_2_11.md](ons_2_11.md) — implementação equivalente no modelo do TCC, com o paradoxo detecção vs. injeção dependente de θ̂
