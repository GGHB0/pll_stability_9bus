---
name: ieee1547-power-quality-clause7
description: Mapa da Cláusula 7 (Power quality) do guia IEEE 1547.2-2023 — Tabelas 15-18, notas 118/119, a condição de ensaio de laboratório do §7.3.1, a condicionante do trafo no §7.3.3 e o roteiro EMTP do §7.5
source: IEEE 1547.2-2023 Cl.7 (págs. impressas 137-148 = PDF 138-149); citações literais do IEEE 1547-2018 §7.1-7.4
references:
  - "IEEE. IEEE Application Guide for IEEE Std 1547-2018, IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces. IEEE Std 1547.2-2023, 2023."
  - "IEEE. IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces. IEEE Std 1547-2018, 2018."
  - "IEEE. IEEE Standard Conformance Test Procedures for Equipment Interconnecting Distributed Energy Resources with Electric Power Systems and Associated Interfaces. IEEE Std 1547.1-2020, 2020."
  - "IEEE. IEEE Standard General Requirements for Liquid-Immersed Distribution, Power, and Regulating Transformers. IEEE Std C57.12.00-2000, 2000."
metadata:
  type: reference
---

# IEEE 1547.2-2023 Cláusula 7 — Power quality

Complementa [harmonic_significance_criteria.md](harmonic_significance_criteria.md)
(de onde vem cada limite) e [ieee519_structure.md](ieee519_structure.md) (a norma
de origem). Cobre a Cláusula 7 inteira, não só o §7.3 de harmônicos —
as demais subcláusulas explicam *por que* os limites de harmônico são o que são.

**O documento é o guia de aplicação, não o standard.** O que está entre aspas
é citação literal do IEEE 1547-2018; o resto é comentário. Arquivo
`805035543-Ieee-Standard-1547-2018.pdf` (nome enganoso — ver
`.claude/skills/pdf-kb-updater/section-maps.md`). **Página do PDF = impressa + 1.**
Extração em `~/pdfext/ieee1547_73_power_quality.txt`.

Cada subcláusula segue o mesmo padrão: citação do requisito → `.1 Background`
(de onde veio o número) → `.2 Potential impacts` → `.3 Tips, techniques`.

## Tabela 15 — mudanças de QEE 2003 → 2018 (pág. impressa 137)

| Item | 1547-2003 | 1547-2018 |
|---|---|---|
| Injeção CC | 0,5% da corrente | sem mudança |
| RVC | não existia | novo: ΔV MT 3%, BT 5% |
| Flicker | "não deve causar" | novo: Pst < 0,35, Plt < 0,25 |
| **Harmônico de corrente** | **< 5% TDD** | **< 5% TRD, Relaxed Evens** |
| **Harmônico de tensão** | **nenhum** | **nenhum** |
| Sobretensão temporária | "no disturbing GFO" | novo: até 138% Vₗ₋ₒ ou ₗ₋ₗ |
| Sobretensão instantânea cumulativa | não existia | novo: 2 pu@1,5 ms e 1,4 pu@16 ms |

Duas leituras diretas:

1. A linha **"Harmonic Voltage: None → None"** é a diferença estrutural com o
   519: o 1547 **não impõe limite de distorção de tensão** (é responsabilidade
   do operador da rede). Logo `VOLT_INDIVIDUAL_LIMIT_PU = 0,03` **só** pode vir
   da Tabela 1 do 519 — não há alternativa no 1547.
2. `TDD → TRD` e "Relaxed Evens" são as **únicas** duas mudanças de harmônico
   entre 2003 e 2018.

## §7.1 — Injeção CC (págs. impressas 137-140)

Requisito: a DER não deve injetar CC maior que **0,5% da corrente nominal de
saída** no RPA.

O `7.1.2` contém, de passagem, **a única frase de todo o guia com os números de
harmônico em texto extraível** (pág. impressa 138):

> …IEEE Std 1547-2018 limits DER harmonic currents to 4% at individual odd
> harmonics, 1% at 2nd order harmonic, 2% at 4th order harmonic, 3% at 6th
> order harmonic, 4% at 8th order harmonic, and 5% Total Rated Distortion (TRD).

Cadeia causal do `7.1.2`, relevante ao TCC: CC injetado → offset de fluxo →
**saturação do trafo de distribuição** → pico de corrente de excitação **rico em
harmônicos pares e ímpares** → soma vetorial com os harmônicos do inversor. Com
indutância de magnetização de 100-200 pu e "headroom" de fluxo de 10-20%, bastam
**0,05% a 0,2%** da corrente nominal do trafo para iniciar a saturação.

**É a origem física do limite de 1% na 2ª harmônica**: harmônico par não é
natural do PWM, é sintoma de assimetria/offset CC. Corrobora, por outro caminho,
a genealogia já registrada em
[harmonic_physical_origin_teodorescu.md](harmonic_physical_origin_teodorescu.md).

`7.1.3`: injeção CC só preocupa em DER **sem transformador** entre inversor e PCC.

## §7.2, §7.4 e §7.5 — demais requisitos de QEE

RVC (Tabela 16), flicker, sobretensão e o roteiro de estudo de QEE ficam em
[ieee1547_pq_other_clauses.md](ieee1547_pq_other_clauses.md) — nenhum é aplicado
ao dashboard, mas o §7.5 endossa explicitamente a metodologia EMT do TCC.

## §7.3 — Limitação de distorção de corrente (págs. impressas 144-146)

Texto normativo citado literalmente:

> When the DER is serving **balanced linear loads**, harmonic current injection
> into the Area EPS at the PCC shall not exceed the limits stated below in Table
> 17 and Table 18. The harmonic current injections shall be **exclusive of any
> harmonic currents due to harmonic voltage distortion present in the Area EPS
> without the DER connected.**

Duas condicionantes numa frase: vale sob carga **equilibrada e linear**, e é
limite de **contribuição da DER**, não de distorção total do sistema.

### Tabelas 17 e 18 — a lacuna

A extração de texto devolve **só título e rodapé de fonte, sem nenhum número**
(o conteúdo é imagem no PDF, pág. impressa 144):

```
Table 17 — Maximum odd harmonic current distortion in percent of rated current (Irated)
   Source: Table 26 of IEEE Std 1547-2018
Table 18 — Maximum even harmonic current distortion in percent of rated current (Irated)
   Source: Table 27 of IEEE Std 1547-2018
```

O **título** já confirma por texto o que importa: base é **`Irated`**, não `IL`.
É o que torna o 1547 aplicável a uma simulação e o 519 não. Status da lacuna e
o valor interino de `11≤h<17` em
[harmonic_significance_criteria.md](harmonic_significance_criteria.md).

### Nota de rodapé 118 — tolerância transitória (pág. impressa 144)

> These need to be used as system design values for the worst case for **normal
> operation (conditions that last longer than 1 h)**. For shorter periods, during
> **startups or unusual conditions, the limits may be exceeded by 50%.**

**Base normativa para duas decisões que o projeto tinha tomado por raciocínio
próprio:** descartar a partida do PLL (`T_SETTLE`) e não cobrar conformidade
durante a falta (`SPEC_SEG_NO_NORM`). Com uma correção de precisão: a norma
**afrouxa em 50%**, não isenta — durante a falta o limite rigoroso seria 6%
(ímpar) e não "sem limite". Consequência para o dashboard em
[harmonic_norm_application.md](harmonic_norm_application.md).

### Nota de rodapé 119 — inconsistência interna do guia

Fala em *"the index of TDD… in percent of maximum demand load current (15-min or
30-min demand)"*, o que **contradiz** a Tabela 15 (`< 5% TRD`) e os títulos das
Tab. 17/18 (`percent of rated current`). É resíduo editorial herdado do 519.
Prevalece o texto normativo e o título das tabelas: **TRD sobre `Irated`**.

### §7.3.1 Background — o requisito é condição de ensaio de laboratório

Confirma a genealogia — *"adapted from IEEE Std 519-2014"*, *"based on the **most
restrictive** harmonic current limits from IEEE Std 519-2014"* — que é a base
textual da inferência do valor de `11≤h<17`.

E então, pág. impressa 145:

> When the RPA is at the PCC, the IEEE 1547 requirement applies only to the
> harmonic current at the PCC with the DER serving linear loads; i.e., **in a
> system with no other harmonic sources. In practice, this is not achievable in
> the field, but is the basis for DER unit testing in a laboratory setting.**

**Achado mais forte do capítulo para este TCC.** O requisito é definido numa
condição idealizada que a própria norma admite ser irrealizável em campo, e que
existe para **ensaio de tipo**. Uma simulação EMT com um único inversor e sem
outras fontes harmônicas **é exatamente essa condição**. Ou seja: o 519 é
critério **estatístico de campo** (percentis sobre semanas, inaplicável aqui),
enquanto o 1547 §7.3 é critério de **condição controlada** — metodologicamente
compatível com o que o projeto simula. Isso inverte o peso entre as duas normas
para efeito de justificar o dashboard.

Complemento: no **IEEE 1547.1-2020**, o ensaio de tipo para harmônicos é feito
**no ponto de conexão da DER**, não no PCC, justamente para isolar a
contribuição do inversor.

### §7.3.2 Impacto das DERs

Divisão de responsabilidade idêntica à do 519: **corrente injetada é do operador
da DER; distorção de tensão da rede é do operador da rede.**

Dois pontos citáveis: o receio histórico com harmônicos de inversor vem de
**inversores a tiristor comutados pela rede** (PWM moderno *"can generate a clean
output"*); e inversores PWM *"present an effective impedance to the grid and can
become a **'sink'** of harmonic currents generated by other sources"* — o
inversor pode **absorver** harmônico da rede, não só injetar. Conecta com a tese
do AGP sobre susceptibilidade a distúrbio harmônico
([agp_current_control_theory](../inverter/agp_current_control_theory.md)).

### §7.3.3 Tips — condicionante do transformador (pág. impressa 146)

> The harmonic current distortion limits shown in Table 17 and Table 18 are
> **only permissible provided that** the transformer that connects the user to
> the area EPS are not be subjected to harmonic currents in excess of **5% of the
> transformer's rated current** (see IEEE Std C57.12.00-2000).

Os limites das Tab. 17/18 são **condicionais**. Acima de 5% no trafo de conexão,
a metodologia do IEEE C57.110 tem de ser aplicada (nota 120) e o trafo pode
precisar ser maior ou "de-ratado". Não altera o cálculo do dashboard, mas é
condicionante da validade dos limites que aplicamos.

