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

- **Partida "até 0,1 s" (slide 9, tela e notas)**: o valor não aparece no
  TCC (§4.3.4) nem no KB (slide-validator, 2026-10-16). Conferir com o Bruno
  no código das métricas; se for real, registrar em [[cenarios-simulados]].
- **Ensaiar a demo (slide 12) no notebook da defesa, sem internet**: abrir
  `output/pll_metrics.html` antes, no cenário Barra 7 trifásica nominal;
  conferir os nomes dos botões citados nas notas (Zoom na falta, aba
  Espectro FFT em dq). O cabeçalho do HTML ainda diz "UERJ 2025".
- **Crédito do template (CC BY 4.0)**: o visual vem do "Project
  Portfolio" do SlidesCarnival; falta a linha de crédito (sugestão: discreta
  no último slide do apêndice). Decisão do Victor.
- **Cosmético (slide-validator)**: ~1 in vazio no pé da capa; vão de ~0,5 in
  entre a tabela e a pergunta no slide 7.
- A capa troca de figuras do TCC para fotos de usinas (2026-10-16); o
  crédito CC BY acima vale só para o template, não para as fotos (Pexels).
- **6. Fontes**: Arial (título) + Calibri (corpo) do tema, sem mudança no
  deck. Conferir no notebook da defesa e levar o PDF de reserva.
- **Opcional**: rótulos internos da Figura 5.14 (slide 18) pequenos no
  projetor; os valores estão na tabela ao lado.

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
