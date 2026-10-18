---
name: defesa-pendencias
description: Pendências do deck da defesa — divergências com o TCC, tempo de fala, decisões de conteúdo em aberto
aliases: [defesa-pendencias]
---

# Deck da defesa — pendências

> Levantadas na primeira leitura do esboço (2026-10-16). Mapa dos slides em
> [[defesa-deck-map]]; divergência de número se resolve pelo TCC canônico
> ([[tcc-pendencias]] guarda as do próprio TCC). Entregas em
> [[defesa-historico-entregas]].

## Em aberto

- **Reestruturação da MODELAGEM (decidida em 2026-10-18, Alternativa 1)**:
  5 slides na ordem do trabalho real (dq → 9 barras/Thévenin → bancada do
  PLL entre duas fontes ideais → ganhos → inversor em etapas PWM/LCL/100 MW),
  deck 25 → 26. Exceção à regra abaixo **só para o método** (bancada e
  sequência de montagem, de [[psim-modeling]]); nenhum número fora do TCC
  na tela (R_th, L_th, Vdc e m ficam para a arguição). **Tela entregue em
  2026-10-18.** Depois, no mesmo dia, o slide 5 foi dividido em dois (deck
  26 → 27): 5 = transformada de Park (equação 3.5, gancho "E o ângulo θ?"),
  6 = Fig. 4.3 com os blocos PD, PI e VCO. Pendente: **falas dos slides
  5-10** (5, 6 e 8 têm só o marcador "[Victor] Fala a escrever"; 7, 9 e 10
  ainda têm as antigas). Itens que saíram da tela e devem ir para a fala:
  compromisso de banda do PI (slide 6), Rd1/Rd2/Rd3
  (slide 10), PI de corrente com ξ 0,707 e ωn = 4√2·fg (antiga fala do 6).

- **Regra (2026-10-17)**: o deck traz só o que está no TCC entregue
  (VFinal), com o mesmo valor; nada de ressalva na fala. A partida "até
  0,1 s" saiu do slide 9 por isso.
- **Inconsistências do próprio TCC entregue** (o deck evita os dois lados):
  Tabela 4.1 diz 28 cenários (21 + 7), mas a Tabela 5.3 já usa a
  monofásica na Barra 7 inadequada (29 = 21 + 8); a introdução traz
  22.547 MW (31%) e a §2.4.3, 23.368 MW (34,5%), que é o número do deck.
- **Demo (slide 14)**: o cartão do painel mostra "V residual médio B2"
  (0,099 / 0,094 pu), não a retenção de Vd do TCC (9,2% / 8,2%). As notas
  citam só o TCC; não ler o cartão em voz alta.
- **Ensaiar a demo (slide 14) no notebook da defesa, sem internet**: abrir
  `output/pll_metrics.html` antes, no cenário Barra 7 trifásica nominal;
  conferir os nomes dos botões citados nas notas (Zoom na falta, aba
  Espectro FFT em dq). O cabeçalho do HTML ainda diz "UERJ 2025".
- **Crédito do template (CC BY 4.0)**: o visual vem do "Project
  Portfolio" do SlidesCarnival; falta a linha de crédito (sugestão: discreta
  no último slide do apêndice). Decisão do Victor.
- **Cosmético (slide-validator)**: ~1 in vazio no pé da capa; vão de ~0,5 in
  entre a tabela e a pergunta no slide 9 (ganhos).
- A capa troca de figuras do TCC para fotos de usinas (2026-10-16); o
  crédito CC BY acima vale só para o template, não para as fotos (Pexels).
- **6. Fontes**: Arial (título) + Calibri (corpo) do tema, sem mudança no
  deck. Conferir no notebook da defesa e levar o PDF de reserva.
- **Figuras dedicadas do apêndice** (caso `figura_dedicada.md` da skill):
  5.14 (slide 21), 5.5/5.6 (slide 22), 5.20/5.21 (slide 25). Corpo (13, 15,
  16) entregue em 2026-10-18.
- **Opcionais do slide-validator (figuras dedicadas, 2026-10-18)**: slide 16
  com moldura direita até x 12,30 (não 12,95) e ticks ~10,5 pt nas 5.10/5.18;
  faixa cinza do 1º ciclo sem legenda nas 5.7/5.18 (explicar na fala, está
  no texto da Fig. 5.7); rótulo "falta" encosta na curva no painel Barra 7;
  cartão "250×" do slide 16, onde o TCC diz "mais de 250 vezes"; título do
  cartão "Sintonia nominal" do slide 13 em roxo (design: azul = nominal).
- **Opcional**: rótulos internos da Fig. 4.3 (slide 6) seguem pequenos
  (6-8 pt) mesmo com a figura a 6,2 in; crescer mais só com versão da figura
  de fonte maior, que deixaria de ser idêntica à do TCC. Não fazer sem pedido.
- Resolvido em 2026-10-18 (fim de tarde): equação do slide 5 na largura toda
  com cartões embaixo; Fig. 4.3 de 5,5 para 6,2 in; subscritos reais
  (baseline -25000) em v_q, v_d, ω_PLL, ω_0, θ_PLL nos cartões do slide 6.

## Resolvidas em 2026-10-16 (entregues na rodada da noite)

1. Monofásica na Barra 7 com sintonia inadequada: slide 10 "com as duas
   sintonias"; linha nova nas tabelas dos slides 18 e 21 (Tabela 5.3 do TCC:
   0,64 / 0,55 / 70,6° / 95 ms; ver [[cenarios-simulados]]); notas 10, 18, 21.
2. Contagem: 29 cenários, 21 nominais e 8 inadequados.
3. Roteiro: 30,9 → 24,6 min (3.195 palavras), Bruno 47% / Victor 53%; só
   repetição cortada, explicações úteis à banca devolvidas pelo validador.
4. "BAD_PLL" fora da tela (slide 8) e da fala.
5. Rótulo "Justificativa de ouro:" removido das 11 caixas; a pergunta
   ficou em `accent1`.

Achados extras, também resolvidos:

- 4 figuras velhas trocadas pelas de `assets/charts/` (slides 12, 13 e 18:
  legenda "salto de fase" e par da monofásica; slide 22: escala antiga de
  P/Q, 0,87 pu antes da falta).
- Slide 14: Q 0,14 pu (escala legada ×1,5) → 0,09 pu, como no TCC.
