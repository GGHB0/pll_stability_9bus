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

Estado após a implementação de 2026-08-09 (antes disso a tabela usava pico do
espectro de Hann, e o segmento de falta era isento):

| Norma pede | O que o código faz | Veredito |
|---|---|---|
| Janela de 12 ciclos (200 ms) | trunca a ciclos inteiros; pré/pós-falta = **12 ciclos**, durante a falta = **6 ciclos** | pré/pós conformes; falta com metade da janela |
| Resolução de 5 Hz | `df = 1/T` → **5,000 Hz** exatos no pré/pós; 10 Hz durante a falta | conforme onde a janela é de 12 ciclos |
| Harmônica = **RMS** do bin central + 2 vizinhos | `sqrt((amp[m]**2).sum())` sobre ±1,5 bin em `_harmonics` | **conforme** desde 2026-08-09 |
| Janela retangular (DFT do IEC) | **retangular na tabela**, Hann só no gráfico exibido | **conforme** na medição; ver a armadilha abaixo |
| Agregação 3 s (15 janelas) e 10 min (200 valores) | não existe | **inaplicável** — a simulação EMT inteira tem ~1 s |
| Percentil 99º/95º sobre dia/semana | valor único por segmento | **inaplicável** — mesma razão |

## Armadilha: RMS de 3 bins exige janela retangular

Aplicar o agrupamento de 3 bins do §4.1 sobre um espectro de **Hann**
**superestima em 22,5%**. A Hann distribui um tom bin-centrado de amplitude
`A` como `[A/2, A, A/2]`, então a soma quadrática dá `√1,5·A ≈ 1,2247·A`.
Verificado numericamente e depois nos dados reais: antes da correção a
fundamental do pré-falta de `bus4/1phase` saía **1,2254 pu**; com janela
retangular sai **1,0006 pu**.

A retangular é legítima aqui **porque a janela já é truncada a um número
inteiro de ciclos** — não há vazamento nas harmônicas. É exatamente a premissa
do método do IEC 61000-4-7 que o §4.1 resume. Por isso
`_amplitude_spectrum` ganhou o parâmetro `window`: `"hann"` para o gráfico
(legibilidade), `"rect"` para a tabela (medição).

## Bug de ponto flutuante no truncamento a ciclos inteiros

Encontrado ao validar a mudança acima. `int(np.floor(dur * 60))` devolvia
**11** ciclos para um segmento de 0,2 s, porque `0.2*60 = 11.999999...` em
ponto flutuante. Consequência: `df = 5,4545 Hz` em vez de 5,000 Hz, e o grupo
de 3 bins caía em ±5,45 Hz em vez dos ±5 Hz da norma. Corrigido com
`np.floor(dur * F_FUND_HZ + 1e-9)`. As harmônicas continuavam caindo em bins
exatos (60/11 divide todo k·60), então não havia vazamento — o custo era só
sair da grade de 5 Hz exigida pelo §4.1.

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

## Efeito da mudança nos valores exibidos

Medido em `bus4/1phase` (fase a, corrente). O RMS de 3 bins captura as bandas
laterais de ±5 Hz, que é justamente o que a norma quer incluir — por isso as
harmônicas de ordem baixa, próximas do piso de ruído, sobem bastante em termos
relativos, embora continuem muito abaixo do limite:

| Segmento | h | Pico/Hann (antes) | RMS3/retangular (agora) |
|---|---|---|---|
| Pré-falta | 1ª | 0,99926 | 1,00059 |
| Pré-falta | 5ª | 0,00168 | 0,00337 |
| Pós-falta | 5ª | 0,00212 | 0,03032 |
| Durante a falta | 2ª | 0,60554 | 0,58730 |

O salto no pós-falta vem do transitório de recuperação, que é **banda larga**:
o pico de um único bin ignorava essa energia, o agrupamento de 3 bins a
contabiliza. É o comportamento pretendido pelo §4.1, não um artefato.

## Ainda em aberto

O **segmento "Durante a falta" continua com janela de 6 ciclos** (`df` = 10 Hz),
metade da janela de 12 ciclos do §4.1, porque a falta em si dura 0,1 s nos
cenários. O grupo de 3 bins ali cobre ±10 Hz em vez de ±5 Hz. Não há correção
possível sem alongar a falta na simulação — fica como limitação declarada.
