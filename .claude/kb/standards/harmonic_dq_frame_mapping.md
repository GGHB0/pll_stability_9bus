---
name: harmonic-dq-frame-mapping
description: Mapeamento formal ordem harmônica → bin do espectro dq (Yazdani & Iravani §4.2.4/4.3, fasor espacial + rotação dq) — por que a fundamental dq é DC, por que só sobra múltiplos de 3f₁, e a colisão 5ª/7ª→6ª (corroborado por Teodorescu §12.3.5.1)
source: Yazdani & Iravani (2010) §4.2.4 p.81-83 (eq.4.13-4.15, Tab.4.1); §4.3/Eq.4.68-4.69 (rotação dq); Teodorescu, Liserre & Rodríguez (2011) §12.3.5.1 p.330-331
references:
  - "YAZDANI, Amirnaser; IRAVANI, Reza. Voltage-Sourced Converters in Power Systems: Modeling, Control, and Applications. Hoboken: John Wiley & Sons / IEEE Press, 2010. ISBN 978-0-470-52156-4."
  - "TEODORESCU, Remus; LISERRE, Marco; RODRÍGUEZ, Pedro. Grid Converters for Photovoltaic and Wind Power Systems. Chichester: John Wiley & Sons, Ltd, 2011. ISBN 978-0-470-05751-3."
metadata:
  type: reference
---

# Mapeamento ordem harmônica → bin do espectro dq

Complementa [harmonic_norm_application.md](harmonic_norm_application.md) (aplicação
no dashboard) e [vsc_topology_and_transforms.md](../inverter/vsc_topology_and_transforms.md)
(fasor espacial e rotação dq, já no KB). Este arquivo é a derivação formal de por que
o espectro dq não serve para checagem por ordem: a fundamental cai em DC, e as
demais ordens colidem em bins compartilhados. **Não é limite novo** — só fundamenta
por que a checagem normativa (IEEE 519/1547) precisa rodar em abc.

## Fasor espacial por sequência (Yazdani §4.2.4, Tabela 4.1, p.83)

Para um sinal trifásico equilibrado com fundamental + um harmônico de ordem `n`
(eq. 4.13), o fasor espacial resultante (eq. 4.14-4.15) separa a fundamental
(gira a `ω`) do harmônico, cuja sequência depende só do resto de `n` por 3:

| Sequência | Ordens (Tabela 4.1) | Fasor espacial |
|---|---|---|
| Positiva | 1, 4, 7, 10, 13, ... | `f̂ₙ·e^(+jnωt)` |
| Negativa | 2, 5, 8, 11, 14, ... | `f̂ₙ·e^(−jnωt)` |
| Zero | 3, 6, 9, 12, ... (múltiplos de 3) | `≡ 0` |

Harmônicos de ordem múltipla de 3 se cancelam no fasor espacial (mesma razão
pela qual sistemas trifásicos a 3 fios não têm 3ª harmônica de sequência zero
circulando) — não aparecem em abc→αβ nem em dq.

## Rotação para dq (Yazdani §4.3, eq. 4.68-4.69)

Já documentado em `vsc_topology_and_transforms.md`: a rotação para o referencial
síncrono é `f_d + j·f_q = f⃗(t)·e^(−jωt)`. Aplicando aos fasores da tabela acima:

```
sequência positiva, ordem n:  e^(+jnωt)·e^(−jωt) = e^(+j(n−1)ωt)  → aparece em (n−1)f₁
sequência negativa, ordem n:  e^(−jnωt)·e^(−jωt) = e^(−j(n+1)ωt) → aparece em (n+1)f₁
```

Essa é a mesma fórmula de deslocamento usada em Teodorescu et al. §12.3.5.1
(p.330-331) para a colisão 5ª/7ª — aqui derivada diretamente da definição de
fasor espacial do Yazdani, com a sequência de cada ordem vindo da Tabela 4.1
em vez de assumida.

## A fundamental (n=1) cai em DC

A fundamental é a primeira linha da Tabela 4.1: ordem `n=1`, sequência
**positiva**. Aplicando a fórmula acima:

```
n = 1 → (n−1)f₁ = 0
```

A fundamental de 60 Hz, depois da rotação dq, vira uma grandeza **DC** — não um
pico em 60 Hz. Isso não é um efeito de implementação do código (remover a média
antes da FFT); é consequência direta da definição de fasor espacial e da
rotação síncrona. Fundamenta o trecho de `harmonic_norm_application.md` sobre a
ausência de pico de 60 Hz no espectro dq exibido.

## Por que só sobram múltiplos de 3f₁ no espectro dq

Combinando as duas seções acima, cada bin do espectro dq recebe a colisão de um
par sequência-positiva/sequência-negativa:

| Bin dq | Ordem positiva (n−1) | Ordem negativa (n+1) |
|---|---|---|
| DC (0 Hz) | 1ª | — |
| 3f₁ (180 Hz) | 4ª | 2ª |
| 6f₁ (360 Hz) | 7ª | 5ª |
| 9f₁ (540 Hz) | 10ª | 8ª |
| 12f₁ (720 Hz) | 13ª | 11ª |

Ordens múltiplas de 3 (3ª, 6ª, 9ª...) já saem zeradas no fasor espacial (seção
1) e não contribuem para nenhum bin. O resultado líquido é que o espectro dq,
em regime equilibrado, só tem energia em múltiplos de 3f₁ — cada bin misturando
duas ordens abc de sequências opostas. Um pico em "h=3ª" nas colunas d/q da
tabela do dashboard não é a 3ª harmônica (que nem existe em dq); é a colisão
2ª/4ª. Mesma ressalva que já vale para o rótulo "h=1ª" (é o resíduo de DC, não
a fundamental).

## O pico em 2f₁ = 120 Hz é a fundamental de sequência negativa, não harmônico

Aplicando a fórmula de deslocamento à própria fundamental (`n=1`) na coluna
"sequência negativa" da Tabela 4.1 (que só existe sob desequilíbrio — em
regime equilibrado essa componente é zero):

```
n = 1, sequência negativa → −(n+1)f₁ = −2f₁
```

O pico em 2f₁ = 120 Hz do espectro dq não é uma harmônica: é a **fundamental
refletida em sequência negativa**, que só ganha amplitude quando o sinal deixa
de ser equilibrado (falta assimétrica — ver
[pll_asymmetric_fault_formal_analysis.md](../pll/pll_asymmetric_fault_formal_analysis.md)).
Isso fundamenta formalmente o uso do pico em 120 Hz como proxy de fração de
sequência negativa, já usado como critério de desequilíbrio em
`harmonic_norm_application.md` — o valor numérico do limiar continua vindo da
TeseAGP, mas a razão de 120 Hz ser o bin certo para observar isso vem daqui.

## Ressalva: só vale para forma de onda equilibrada

A nota de rodapé 3 da p.82 do Yazdani é explícita: a Tabela 4.1 (classificação
de sequência por ordem) só vale para **forma de onda periódica equilibrada**.
Sob falta assimétrica, os harmônicos de um sinal desequilibrado não seguem
necessariamente essa classificação — por isso a análise formal de falta
assimétrica (`pll_asymmetric_fault_formal_analysis.md`) trata a sequência
negativa como uma componente à parte, não como "harmônico de ordem 1 invertido"
igual à tabela acima assume para o caso equilibrado.

## Corroboração cruzada com Teodorescu §12.3.5.1

O Teodorescu et al. (2011) chega à mesma colisão 5ª/7ª→6ª por outro caminho
(MSRF, detecção de harmônico via referencial síncrono múltiplo), sem passar
pela Tabela 4.1 de sequências do Yazdani — ver
[harmonic_physical_origin_teodorescu.md](harmonic_physical_origin_teodorescu.md)
para a citação literal ("they generate six-order harmonics of different
sequences") e o restante da fundamentação daquele livro (origem física de
harmônicos pares, genealogia do limite de 1% na 2ª harmônica), que continua
válida e não se sobrepõe ao que está aqui.
