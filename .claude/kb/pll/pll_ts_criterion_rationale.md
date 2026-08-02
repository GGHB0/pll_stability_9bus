---
name: pll-ts-criterion-rationale
description: Defesa da escolha do critério de 1% (numerador 4,6) na sintonia do SRF-PLL — argumento a favor, argumento contra (15% mais ripple de 2ω₀) e como redigir isso no TCC
source: Franklin-Powell-Emami-Naeini 2002 (critério de 1%); Ogata 2009 (critérios de 2% e 5%); Teodorescu-Liserre-Rodríguez 2011 §4.2.2.3 p.56; Alves-Dias-Rolim 2020 §4.1; cálculo próprio de |G(j2ω₀)|
references:
  - "FRANKLIN, Gene F.; POWELL, J. David; EMAMI-NAEINI, Abbas. Feedback Control of Dynamic Systems. 4. ed. Upper Saddle River: Prentice Hall, 2002. ISBN 0-13-032393-4."
  - "OGATA, Katsuhiko. Modern Control Engineering. 5. ed. London: Pearson, 2009."
  - "TEODORESCU, Remus; LISERRE, Marco; RODRÍGUEZ, Pedro. Grid Converters for Photovoltaic and Wind Power Systems. Chichester: John Wiley & Sons, Ltd, 2011. ISBN 978-0-470-05751-3."
  - "ALVES, André G. P.; DIAS, Robson F. S.; ROLIM, Luís G. B. A Smooth Synchronization Methodology for the Reconnection of Autonomous Microgrids. Journal of Control, Automation and Electrical Systems, v. 31, p. 665-674, 2020. DOI 10.1007/s40313-020-00576-x."
---

# Critério de Acomodação do SRF-PLL — Defesa da Escolha

Complemento de [[pll-loop-filter-gains]], que documenta o método. Este arquivo
responde à pergunta que a banca pode fazer: **por que 1% e não 2%?**

Contexto: o `ts = 20 ms` com numerador 4,6 foi adotado seguindo o vídeo do
André (coorientador), que remete a Alves 2020 e Teodorescu 2011. A escolha
veio antes da leitura do artigo — o que não é problema, mas exige que o
argumento técnico esteja montado.

## O ponto de partida honesto

**Não existe argumento que torne 4,6 mais correto que 4.** Os dois descrevem o
mesmo envelope exponencial `e^(−ξωn·t)`, mudando só onde se desenha a faixa de
tolerância (`4,6 = ln 100`, `4 ≈ ln 50`). Qualquer defesa tem que ser sobre o
**resultado** — `ξωn = 230 rad/s` — e não sobre a constante.

Mas a escolha não é gratuita. Com `ts = 20 ms` fixo:

| Critério | `Kp = 2·ln(1/δ)/ts` | `ωn` | `Ki = ωn²` |
|---|---|---|---|
| 1% — numerador 4,6 | **460** | 325,3 rad/s | **105 820** |
| 2% — numerador 4 | 400 | 282,8 rad/s | 80 000 |

15% de diferença no ganho proporcional. Muda o sistema que vai para a simulação.

## Argumento a favor do critério mais apertado

O PLL não é uma malha qualquer: é o **gerador da referência angular** que define
o eixo `dq` do controlador de corrente. Erro residual de ângulo não fica contido
no PLL — propaga-se multiplicativamente para `id`/`iq` como acoplamento cruzado
entre ativa e reativa. Para um dispositivo cuja saída é referência de outro
laço, exigir a faixa mais apertada é a escolha conservadora.

Isso é coerente com a divisão da literatura: **Franklin** adota 1% ao tratar de
acomodação; **Ogata** apresenta 2% e 5% como caracterização genérica da resposta
ao degrau.

Este é o argumento a usar. É suficiente e é honesto.

## Argumento contra — levantar antes que perguntem

Ganho maior alarga a banda, e banda mais larga deixa passar mais ripple de
`2ω₀`. No laço linearizado, a transferência do ripple de `vq` para `θ` é a
mesma `G(s)` do rastreamento de fase:

```
θ(s)/vq(s) = (Kp·s + Ki) / (s² + Kp·s + Ki)
```

Avaliada em `2ω₀ = 754,0 rad/s` (120 Hz):

| Ganhos | Critério | `|G(j2ω₀)|` |
|---|---|---|
| Kp = 460, Ki = 105 820 | 1% | **0,627** |
| Kp = 400, Ki = 80 000 | 2% | 0,543 |

**Cerca de 15% mais ripple atravessa com o critério de 1%.** Como o eixo do
trabalho é justamente a vulnerabilidade do SRF-PLL sob falta assimétrica, o
critério mais apertado piorou marginalmente o fenômeno investigado.

Não invalida nada — mas é melhor apresentar do que ser perguntado. Ver
[[pll-asymmetric-fault-formal-analysis]].

## Como redigir no TCC

Não defender o 4,6. Defender o `ξωn = 230 rad/s`, isto é, reconvergência dentro
de aproximadamente um ciclo da fundamental. O critério entra como **convenção
adotada**, com citação, e `ts` como a escolha de projeto. É como a literatura
apresenta, e evita pedir justificativa para uma constante que é `ln(100)`.

## Critério de projeto ≠ critério de avaliação

Os dois convivem no trabalho e são coisas diferentes:

| | Critério de projeto | Critério de avaliação |
|---|---|---|
| Natureza | relativo ao degrau | absoluto |
| Valor | 1% (numerador 4,6) | ±0,02 rad = ±1,15° |
| Onde entra | sintonia de `kp_pll`/`ki_pll` | métrica `ts` do dashboard e das simulações |

Não se convertem um no outro sem fixar a amplitude do degrau de fase. Deixar
implícito que são o mesmo critério é o tipo de detalhe que vira pergunta na
defesa. Ver [[pll-contingencies]] para as métricas.

## Nota em PDF

Este conteúdo está também em `output/criterio_acomodacao_srf_pll.pdf`, gerado
por `scripts/notas/gen_criterio_acomodacao.py` (skill `tcc-pdf-notes`).
