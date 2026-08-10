---
name: harmonic-measurement-conditions
description: Condições de medição de harmônico (IEEE 519-2014 Cl.4 + nota 118 do IEEE 1547.2-2023) confrontadas com a FFT implementada em spectrum.py — o que coincide, o que é inaplicável a uma simulação EMT e o que é divergência corrigível
source: IEEE 519-2014 §4.1-4.4 (págs. impressas 4-5 = PDF 16-17); IEEE 1547.2-2023 nota de rodapé 118 (pág. impressa 144)
references:
  - "IEEE. IEEE Recommended Practice and Requirements for Harmonic Control in Electric Power Systems. IEEE Std 519-2014, 2014."
  - "IEEE. IEEE Application Guide for IEEE Std 1547-2018, IEEE Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces. IEEE Std 1547.2-2023, 2023."
  - "INTERNATIONAL ELECTROTECHNICAL COMMISSION. Electromagnetic compatibility (EMC) - Part 4-7: Testing and measurement techniques - General guide on harmonics and interharmonics measurements and instrumentation. IEC 61000-4-7."
  - "INTERNATIONAL ELECTROTECHNICAL COMMISSION. Electromagnetic compatibility (EMC) - Part 4-30: Testing and measurement techniques - Power quality measurement methods. IEC 61000-4-30."
metadata:
  type: reference
---

# Condições de medição × a FFT do projeto

As normas de harmônico têm **duas metades**: a Cláusula 5 do IEEE 519-2014 diz
*qual é o limite*, e a **Cláusula 4** diz *como medir*. O KB cobria só a
primeira. Este arquivo cobre a segunda e a confronta com
`src/pipeline/spectrum.py`. Mapa das cláusulas em
[ieee519_structure.md](ieee519_structure.md); origem dos limites em
[harmonic_significance_criteria.md](harmonic_significance_criteria.md).

## IEEE 519-2014 Cláusula 4 (págs. impressas 4-5)

Abre remetendo a **IEC 61000-4-7** e **IEC 61000-4-30**, e resume o essencial.

### 4.1 Largura da janela de medição

- Janela de DFT = **12 ciclos ≈ 200 ms** em 60 Hz (10 ciclos em 50 Hz).
- Resolução espectral resultante: **5 Hz** (bins em 0, 5, 10 … 55, 60, 65 …).
- **A magnitude da harmônica não é o bin central sozinho**: é o bin central
  (60, 120, 180 Hz…) **combinado em RMS com os dois bins adjacentes de 5 Hz** —
  três valores somados em um único RMS.

O agrupamento de 3 bins existe porque a frequência da rede oscila; a energia da
harmônica vaza para os vizinhos e a norma quer recuperá-la.

### 4.2 / 4.3 — agregação temporal

| Índice | Construção | Duração |
|---|---|---|
| *very short* | RMS de **15 janelas** de 12 ciclos, Eq. (1) | 3 s |
| *short* | RMS de **200 valores** *very short*, Eq. (2) | 10 min |

### 4.4 — avaliação estatística

Não se compara um valor, compara-se **percentil**:

| Índice | Acumulação | Percentil | Comparado a |
|---|---|---|---|
| very short (3 s) | 1 dia | **99º** | limites da Cl.5 |
| short (10 min) | 1 semana | **95º e 99º** | limites da Cl.5 |

Ressalva explícita: o 99º percentil *short time* **não** se recomenda para
harmônico de **tensão** — por isso a Tab.1 tem dois critérios e as tabelas de
corrente têm três.

## IEEE 1547.2-2023 nota 118 — tolerância transitória

> These need to be used as system design values for the worst case for **normal
> operation (conditions that last longer than 1 h)**. For shorter periods, during
> **startups or unusual conditions, the limits may be exceeded by 50%.**

Os limites são valores de **projeto para regime normal com duração > 1 h**. Em
partida ou condição inusual, admite-se excedê-los em **50%** — afrouxamento,
não isenção. Ver [ieee1547_power_quality_clause7.md](ieee1547_power_quality_clause7.md).

## Confronto com `spectrum.py`

| Norma pede | O que o código faz | Veredito |
|---|---|---|
| Janela de 12 ciclos (200 ms) | trunca a ciclos inteiros; pré-falta `0,1→0,3 s` = **exatamente 12 ciclos**; durante a falta `0,3→0,4 s` = **6 ciclos** | pré/pós conformes; falta com metade da janela (segmento já tratado à parte) |
| Resolução de 5 Hz | `df = 1/T` → 5 Hz nos segmentos de 200 ms | coincide |
| Harmônica = **RMS** do bin central + 2 vizinhos | `amp[m].max()` sobre ±1,5 bin → **pico** ([spectrum.py](../../../src/pipeline/spectrum.py) `_harmonics`) | **divergência real** — subestima: com Hann a energia se espalha em 3 bins e só o maior é lido |
| Agregação 3 s (15 janelas) e 10 min (200 valores) | não existe | **inaplicável** — a simulação EMT inteira tem ~1 s |
| Percentil 99º/95º sobre dia/semana | valor único por segmento | **inaplicável** — mesma razão |
| Janela retangular (DFT do IEC) | janela de **Hann** | escolha do projeto, para conter vazamento em janela curta |

## Consequência metodológica — como descrever isso no TCC

Os limites do 519 são de **regime permanente, estatísticos, sobre semanas de
operação real**. O que o dashboard faz é uma **comparação indicativa** de um
instantâneo determinístico contra esses valores. **Não é medição de conformidade
e não deve ser chamada assim** no texto do TCC.

O IEEE 1547 §7.3 sai melhor nessa comparação: o §7.3.1 define o requisito como
condição de **ensaio de tipo em laboratório** (DER servindo carga linear, sem
outras fontes harmônicas), que é exatamente o que uma simulação EMT de um único
inversor reproduz. É argumento a favor de citar o 1547 como critério primário e
o 519 como origem histórica dos valores.

## Pendências abertas (não implementadas)

Levantadas em 2026-08-09 na revisão das duas normas; **nenhuma foi aplicada ao
código** — dependem de decisão do usuário.

1. **Pico → RMS de 3 bins** em `_harmonics`. É a única divergência do §4.1
   corrigível: trocar `amp[m].max()` por `sqrt((amp[m]**2).sum())` na mesma
   janela de ±1,5 bin. Efeito esperado: valores ligeiramente maiores em todas as
   células da tabela abc.
2. **Isenção → limite ×1,5 no segmento "Durante a falta"**. Hoje
   `SPEC_SEG_NO_NORM` remove a checagem por completo; a nota 118 do 1547
   sustentaria aplicar o limite multiplicado por 1,5 (ex.: 6% em vez de 4% para
   ímpar). Mais defensável e mais informativo que isenção total. Ver a seção de
   isenção por segmento em
   [harmonic_norm_application.md](harmonic_norm_application.md).
