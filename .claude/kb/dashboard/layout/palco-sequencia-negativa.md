---
name: palco-sequencia-negativa
aliases: [palco-sequencia-negativa]
description: Capítulo "Sequência negativa" do palco da defesa em cinco passos — abc desequilibrado, animação positiva × negativa, 120 Hz em v_d/v_q, v_q no PI do PLL, espectro com matriz; campos sinais, xrange, cartoes do passo, lado "seq" e tccAbc
---

# Palco: Sequência negativa em cinco passos

Refeito em 2026-10-28. Antes, o capítulo abria direto no espectro de v_d,
que mostra **que** aparece 120 Hz, mas não **por quê**. Agora o mecanismo
vem primeiro, no tempo, e o espectro fecha o capítulo. Caso da história:
Barra 6, trifásica × bifásica. A bifásica da Barra 6 é o caso de
[[roteiro-demonstracao-dashboard]] no Compromisso, o que faz a ponte.

| Passo | Gráfico | Painel ao lado | Mensagem |
|---|---|---|---|
| 1 | v_abc do inversor, um painel por caso, 0,28-0,36 s | — | trifásica cai por igual, bifásica desequilibra |
| 2 | o mesmo | animação `seq` | desequilíbrio = positiva + negativa; vista do PLL, a negativa gira a 120 Hz |
| 3 | v_d e v_q do inversor, foco na falta | animação `seq` | em dq, positiva = constante, negativa = 120 Hz |
| 4 | v_q e erro de fase, foco na falta | — | v_q é a entrada do PI: pico de 7,3° × 96,0° |
| 5 | espectro de v_d, 6 casos, matriz | — | 0,29 a 0,72 pu, "> 250×" |

Os números são os da Tabela 5.3 e de `tccInd` (pico 7,3°/96,0°, 120 Hz
0,29-0,72 pu), conforme [[modo-apresentacao-palco]]. A física do 120 Hz
está em [[pll-asymmetric-fault-formal-analysis]].

## Campos novos do passo (`passos_pres`)

- `sinais`: troca os painéis do gráfico naquele passo (o padrão é
  `cap.pres`). `palco.js` passa `ps.sinais || cap.pres` ao `_tccFigure`.
- `xrange`: janela do eixo x do passo (o padrão é `cap.xrange`); o `_foco`
  usa a mesma janela.
- `cartoes=False`: esconde cartões ou matriz naquele passo, e o gráfico
  ganha a altura. A matriz só aparece no passo 5.

## Sinais novos (`SINAIS` em `tcc.js`)

- `vdi`, `vqi`: v_d e v_q **do inversor** (traços "V_d Inv"/"V_q Inv" do
  `invData`), as mesmas grandezas do espectro. O `vd` antigo é o da rede.
- `abc`: expandido em `_tccFigure` num painel por caso visível
  (`"abc|<caso>"`), com as três fases em cores fixas (`FASES_ABC`) e eixo
  em ±1,45 pu. Os dados vêm de `SCENARIOS[k].tccAbc`, que o
  `renderer.py` (`_tcc_abc`) embute **só** para `ABC_CASOS` (`roteiro.py`):
  0,26 a 0,42 s, uma amostra a cada 10 (50 µs).

## Animação `seq` (`seq.js`)

Desenhada pela fórmula, sem dado simulado e sem número (aval do usuário em
2026-10-28, etapa de método). Em cima, a **vista da rede**: positiva no
sentido anti-horário, negativa no horário, presa na ponta da positiva; a
soma (tensão) percorre uma elipse, e o eixo d do PLL acompanha a positiva.
Embaixo, a **vista do PLL**: positiva parada em d, negativa girando a −2θ
em volta da ponta dela, com projeções tracejadas em v_d e v_q. A amplitude
da negativa (0,35) é ilustrativa. O loop é `requestAnimationFrame`, com uma
volta da rede a cada 6 s (`SEQ_MS`); `_seqStop` roda a cada `_renderPres` e
ao sair do palco.

## Casos e chips

Os casos ficam em ordem Barra 7 → Barra 6, para os chips saírem em dois
grupos só. A trifásica da Barra 6 entrou na lista em grafite (como a da
Barra 7). Nos passos 1 a 4, `_SO_B6` esconde a Barra 7 e a monofásica da
Barra 6. No passo 5 tudo aparece: as duas trifásicas ficam no zero, uma
sobre a outra, e a nota da matriz diz isso.

## Relacionados

- [[modo-apresentacao-palco]] — estrutura do palco, foco, destaque, matriz
- [[pll-asymmetric-fault-formal-analysis]] — por que a negativa vira 120 Hz em dq
