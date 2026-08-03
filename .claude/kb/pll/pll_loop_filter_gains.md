---
name: pll-loop-filter-gains
description: Ganhos do PI do laço do SRF-PLL (kp_pll=460, ki_pll=105820) — projeto de 2ª ordem por tempo de acomodação, ts=20 ms pelo critério de 1% (Teodorescu eq. 4.38 / Alves 2020 eqs. 9-11), ωn=325,3 e ξ=0,707
source: Alves-Dias-Rolim 2020 §4.1 eqs. (7)-(11); Teodorescu-Liserre-Rodríguez 2011 §4.2.2.3 p.56 eqs. (4.35)-(4.38); Karimi-Ghartemani 2014 eq. (6.4) p.135; params.m
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

## Procedência dos valores

Os ganhos **não foram calculados dentro do repositório** — entram como literais
no netlist PSIM (`P8 = 105820`, `P9 = 460`), migram hardcoded para o bloco
Simulink e chegam ao `params.m` sem justificativa. O laço está normalizado
(`U = 1 pu`), o que é a condição para as fórmulas abaixo valerem sem o `/U`.

Rastreamento completo do netlist, da cadeia de transcrição e da dedução de
`U = 1`: [[pll-gains-provenance]].

## Método de projeto: 2ª ordem por tempo de acomodação

Fonte primária: **Alves, Dias & Rolim (2020), §4.1, eqs. (7)-(11)** — artigo do
próprio coorientador. A malha linearizada do SRF-PLL é de 2ª ordem:

```
G(s) = (Kp·s + Ki) / (s² + Kp·s + Ki)                 (7)
G(s) = (2ξωn·s + ωn²) / (s² + 2ξωn·s + ωn²)           (8)
```

Comparando (7) e (8):

```
Ki = ωn²                                              (9)
Kp = 2·√(Ki)·ξ = 2ξωn                                 (10)
ωn = 4 / (ts·ξ)      ← Alves, critério de 2%          (11)
```

O artigo, citando Teodorescu et al. (2011) e Ogata (2009), estabelece:

- `ξ = 0,707` para resposta transitória ótima (overshoot ≈ 5%);
- `ts` escolhido **entre um e dois períodos da fundamental** da rede.

A mesma sintonia aparece no Teodorescu §4.2.2.3, p.56, eqs. (4.35)-(4.38), ali
na forma `Kp = 2ξωn = 9,2/ts` — que usa o critério de **1%**
(`ts = 4,6/(ξωn)`, apoiado em Franklin et al., ref. [14] do livro).
**É esta a variante usada no projeto** (ver seção "Escolha do `ts`").

Teodorescu observa explicitamente que (4.38) supõe **entrada unitária (V = 1)**,
senão os ganhos devem ser divididos pela amplitude: confirmação independente da
normalização rastreada em [[pll-gains-provenance]].

### De onde vem o 4,6

Não tem nada a ver com a malha do PLL — é o critério de acomodação. A resposta
ao degrau de um sistema de 2ª ordem subamortecido decai dentro de um envelope
exponencial `e^(−ξωn·t)`. O `ts` é o instante em que esse envelope entra na
faixa de tolerância `δ`:

```
e^(−ξωn·ts) = δ      →      ts = ln(1/δ) / (ξωn)
```

O numerador é simplesmente `ln(1/δ)`, arredondado por convenção:

| Tolerância `δ` | `ln(1/δ)` | Numerador usado | Onde aparece |
|---|---|---|---|
| 5% | 2,996 | 3 | Ogata |
| 2% | 3,912 | 4 | Ogata; Alves eq. (11) |
| 1% | 4,605 | **4,6** | Franklin; Teodorescu eq. (4.38) |

Leitura equivalente: `1/(ξωn)` é a **constante de tempo `τ` do envelope**, e
acomodar dentro de 1% custa **4,6 constantes de tempo**. No projeto,
`τ = 1/230 = 4,35 ms` e `4,6·τ = 20 ms`.

O `9,2` de `Kp = 9,2/ts` é `2 × 4,6`, porque `Kp = 2ξωn`.

> **Precisão.** O envelope exato da resposta ao degrau é `e^(−ξωn·t)/√(1−ξ²)`;
> incluir esse fator daria 4,95 em vez de 4,6 para `ξ = 0,707`. A convenção de
> controle despreza o `1/√(1−ξ²)` — os numeradores 3, 4 e 4,6 são aproximações
> padronizadas, não valores exatos.

Por que 1% e não 2%, o que essa escolha custa em rejeição de `2ω₀` e como
defender isso na banca: [[pll-ts-criterion-rationale]].

### Aplicação aos ganhos do projeto

Com `ξ = 0,707` (= `qsi` do `params.m`), invertendo (9) e (10):

```
ωn = √ki_pll = √105 820 = 325,30 rad/s   (51,8 Hz)
ξ  = kp_pll / (2·ωn) = 460 / 650,60 = 0,7070
ξωn = kp_pll/2 = 230
```

Na direção direta — que é a ordem real do projeto — partindo de `ts = 20 ms` e
`ξ = 0,707` pelo critério de 1%:

```
ξωn = 4,6 / ts = 4,6 / 0,020 = 230
Kp  = 2ξωn = 9,2 / ts = 460                      → kp_pll   ✓
ωn  = 230 / 0,707 ≈ 325,3 rad/s   (51,8 Hz)
Ki  = ωn² ≈ 105 820                              → ki_pll   ✓
```

> **Arredondamento.** `ξ = 0,707` tem três casas decimais. Sem arredondar,
> `230/0,707` dá `ωn = 325,32 rad/s` e `Ki = 105 832`, ~0,01% acima do valor
> gravado — o `ξ` exato que fecha em `Kp = 460`/`Ki = 105 820` é `0,70704`.
> Os dois ganhos fecham nos valores gravados dentro dessa precisão.

## Escolha do `ts`

`ts` é a **única grandeza escolhida por julgamento** no projeto — `ξ = 0,707` é
convenção de 2ª ordem e todo o resto decorre das eqs. (9)-(11).

**Valor adotado: `ts = 20 ms` pelo critério de 1%** (`ts = 4,6/(ξωn)`,
Teodorescu eq. 4.38). Confirmado pelo autor em 2026-08-02; substitui a dúvida
registrada anteriormente entre 1% e 2%.

A faixa "um a dois períodos da fundamental" (16,7 a 33,3 ms em 60 Hz) tem
limite físico dos dois lados:

| Limite | Razão |
|---|---|
| **Piso ≈ 1 T** | Não há informação de fase de um sinal de 60 Hz em menos de um ciclo. Abaixo disso o modelo linearizado deixa de valer (supõe malha lenta em relação à portadora) e o PLL vira amplificador de ruído em vez de ficar mais rápido. |
| **Teto ≈ 2 T** | O controlador de corrente opera no referencial `dq` entregue pelo PLL. Enquanto o PLL não reconverge, `id`/`iq` são projetados em eixo errado → injeção de reativo indevida e, no limite, perda de sincronismo. |

`20 ms = 1,20 T` fica logo no início da faixa: reconverge dentro do primeiro
ciclo pós-falta sem descer ao regime onde a linearização se quebra. E é número
redondo — `9,2/0,020` dá 460 exato, o que é consistente com escolher o `ts` e
deixar o ganho cair como consequência.

Por que este critério e não o de 2% (`ts = 17,4 ms` pela mesma eq. 11 do
Alves): [[pll-ts-criterion-rationale]].

Aferição do método no próprio artigo do Alves (Tabela 2, protótipo 15 V/60 Hz):
`PI2 = PI4 = 400 + 40 000/s` → `ωn = 200`, `ξ = 1,0`, `ts = 20 ms` por (11).
Confirma a mecânica das equações com outro par `ξ`/`ts`.

## Consequência: banda vs. rejeição de 2ω₀

`ωn = 325,3 rad/s = 51,8 Hz` está logo abaixo da própria fundamental. O ripple
de sequência negativa sob falta assimétrica está em `2ω₀ = 754 rad/s`, ou seja a
apenas **2,32·ωn** — separação pequena demais para um PI simples atenuar (sem
zeros em ±j2ω₀, ver [[srf-pll-theory]]).

O mesmo `ts` curto que garante reconvergência rápida é o que deixa o PLL exposto
no cenário assimétrico. Esse é o compromisso central do trabalho — ver
[[pll-asymmetric-fault-formal-analysis]] e [[pll-contingencies]].

## Procedência e cadeia de citação

| Elemento | Citar |
|---|---|
| `Ki = ωn²`, `Kp = 2ξωn`; faixa de `ts` de 1 a 2 períodos | **Alves, Dias & Rolim (2020), §4.1, eqs. (9)-(11)** |
| **`Kp = 9,2/ts` (critério de 1%) — forma usada no projeto**; normalização por `V` | **Teodorescu, Liserre & Rodríguez (2011), §4.2.2.3, p.56, eqs. (4.35)-(4.38)** |
| `ξ = 0,707` e critério de acomodação de 2ª ordem | Ogata (2009), 5. ed. — citado por Alves |
| Metodologia de sintonia por FT de malha fechada | Golestan & Guerrero (2015) — citado por Alves |
| Equação característica `s² + h0·U·s + h1·U = 0` | Karimi-Ghartemani (2014), eq. (6.4), p.135 |

> **Onde NÃO está:** Blaabjerg, Teodorescu, Liserre & Timbus, "Overview of
> Control and Grid Synchronization for Distributed Power Generation Systems"
> (IEEE TIE, 2006) cita PLL 23 vezes mas **não traz a fórmula de sintonia** —
> nenhuma ocorrência de settling time, damping ou frequência natural. Verificado
> em 2026-08-02; não reabrir.

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
