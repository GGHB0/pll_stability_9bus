---
name: ieee1547-pq-other-clauses
description: Requisitos de QEE do IEEE 1547-2018 que NÃO são de harmônico — RVC (Tabela 16), flicker, sobretensão (§7.4) e o roteiro de estudo de QEE do §7.5, que endossa a metodologia EMT do TCC
source: IEEE 1547.2-2023 §7.2, §7.4, §7.5 (págs. impressas 140-148 = PDF 141-149)
references:
  - "IEEE. IEEE Application Guide for IEEE Std 1547-2018, IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces. IEEE Std 1547.2-2023, 2023."
  - "IEEE. IEEE Recommended Practice for the Analysis of Fluctuating Installations on Power Systems. IEEE Std 1453-2015, 2015."
  - "IEEE. IEEE Recommended Practice and Requirements for Harmonic Control in Electric Power Systems. IEEE Std 519-2014, 2014."
  - "INTERNATIONAL ELECTROTECHNICAL COMMISSION. Electromagnetic compatibility (EMC) - Part 3-7: Limits - Assessment of emission limits for the connection of fluctuating installations to MV, HV and EHV power systems. IEC TR 61000-3-7."
metadata:
  type: reference
---

# IEEE 1547.2-2023 — requisitos de QEE não harmônicos

Continuação de
[ieee1547_power_quality_clause7.md](ieee1547_power_quality_clause7.md) (§7.1 e
§7.3, os que sustentam os limites do dashboard). **Nenhuma das cláusulas abaixo
é aplicada ao dashboard** — estão aqui para não serem confundidas com os
critérios que aplicamos, e pelo §7.5, que endossa a metodologia do TCC.

## §7.2.1 — RVC (Rapid Voltage Changes), pág. impressa 140

Requisito: com PCC em **média tensão**, a DER não pode causar degrau/rampa de
tensão RMS excedendo **3% do nominal** e **3% por segundo** média em 1 s. Em
**baixa tensão**, **5%** e **5%/s**.

**Tabela 16 — níveis de planejamento para RVC** (pág. impressa 141):

| Nº de mudanças (n) | ΔVmax/V (%), ≤ 35 kV |
|---|---|
| n ≤ 4 por dia | 5-6 |
| n ≤ 2 por hora e > 4 por dia | 4 |
| 2 < n ≤ 10 por hora | 3 |

*Source: Modified from Table 3 of IEEE Std 1453-2015.*

O comentário logo abaixo explica a escolha do requisito: como o 1547-2018 se
aplica a **instalações individuais**, adotou-se **o limite mais estrito (3%)**,
reservando capacidade do sistema para outros eventos. É a mesma lógica da nota
"c" da Tab.2 do IEEE 519-2014 — alvo isolado recebe sempre a linha mais
restritiva.

**Não confundir com os cenários do TCC:** RVC é definido (IEC 61000-4-30:2015)
como transição entre **dois estados de regime permanente** durante a qual a
tensão RMS **não excede limiares de sag/swell (±10%)**. Um afundamento de falta
**não é** um RVC.

## §7.2.2 — Flicker, pág. impressa 142

Requisito: a contribuição da DER medida no PCC não deve exceder o maior entre os
limites da Tabela 25 e os limites individuais da IEC TR 61000-3-7. Pela Tabela
15: **Pst < 0,35, Plt < 0,25**.

Fora do escopo do TCC — é fenômeno de flutuação lenta (sombreamento por nuvem,
variação de vento), não de contingência de rede.

## §7.4 — Limitação de contribuição a sobretensão, págs. impressas 146-148

Requisito: a DER não deve contribuir para sobretensões instantâneas ou de
frequência fundamental.

| Tipo | Limite |
|---|---|
| Frequência fundamental | **138% de Vₗ₋ₒ**, equivalente a coeficiente de aterramento 0,8 (`Vₗ₋ₒ ≤ 0,8·Vₗ₋ₗ`) |
| Instantânea | **2,0 / 1,7 / 1,4 / 1,2 pu**, conforme "duração cumulativa" definida no 1547-2018 |

Alvos declarados: **GFOV** (ground fault overvoltage) e **LROV** (load rejection
overvoltage). Referencia IEEE C62.92 (aterramento) e o §4.12 do 1547-2018
("Integration with Area EPS Grounding").

O guia diz que sobretensão relacionada a DER *"is generally not considered, in
the case of inverter DER"* — é preocupação de gerador rotativo grande sem
aterramento adequado.

**Não confundir com a `ONS_2_11`:** o valor 1,2 pu daqui é vizinho do
`V > 1,1 pu` que dispara a zona de absorção de reativo em
[ons_2_11.md](ons_2_11.md), mas os contextos são distintos — coordenação de
isolamento × suporte de tensão sob defeito.

## §7.5 — Roteiro de um estudo de QEE, pág. impressa 148

Passos recomendados pelo guia:

- **"Build the area EPS and DER models in an electromagnetic transients program
  (EMTP)."** Para estudo de harmônico, um programa de análise harmônica
  especializado pode ser usado no lugar.
- **"Simulate fault-and-clear operations at various area EPS and DER operating
  conditions."** Avaliar transitórios e sobretensões temporárias contra
  isolamento e capacidade de para-raios.
- Simular chaveamento de capacitor, chaveamento da DER e partida de motores
  próximos.
- Simular condição de fase aberta, se possível (ferrorressonância).
- Estimar o flicker contribuído pela DER, per IEEE 1453-2015.
- **"Estimate the harmonics contributed by the DER, per IEEE Std 519-2014."**

**Relevância para o TCC:** a metodologia do trabalho — modelo EMT do IEEE 9
barras com o inversor, cenários de falta com abertura — é **literalmente o
roteiro recomendado pelo guia da própria norma**. E o último item fecha o
circuito normativo: o IEEE 1547 remete a estimativa de harmônicos ao IEEE 519.
As duas normas encaixam, não competem. Usar isto ao justificar a metodologia,
em vez de apresentá-la só como escolha de conveniência.
