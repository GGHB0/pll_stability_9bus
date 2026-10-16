---
name: defesa-pendencias
description: Pendências do deck da defesa — divergências com o TCC, tempo de fala, decisões de conteúdo em aberto
aliases: [defesa-pendencias]
---

# Deck da defesa — pendências

> Levantadas na primeira leitura do esboço (2026-10-16). Mapa dos slides em
> [[defesa-deck-map]]; divergência de número se resolve pelo TCC canônico
> ([[tcc-pendencias]] guarda as do próprio TCC).

## P1 — divergência com o TCC

1. **Monofásica na Barra 7 com sintonia inadequada.** O deck diz que foi
   simulada "apenas com a sintonia nominal" (slide 10, texto e notas; slide
   21, notas) e a tabela do slide 21 não tem a linha. A Tabela 5.3 do TCC
   já tem: Vd média 0,64 pu, 120 Hz 0,55 pu, pico 70,6°, retorno 95 ms
   (entrou no TCC em 2026-10-14, commit `5b59750`; ver [[cenarios-simulados]]).
   Atualizar slide 10, tabela do 21 e notas dos dois.
2. **Contagem de cenários** (slide 10: "28 cenários, 21 nominais e 7
   inadequados"): muda com o item 1. A Tabela 4.1 do TCC é imagem: contar
   pelo `cenarios_simulados.md` e pela própria figura antes de reescrever.

## P2 — roteiro e regras

3. **Tempo de fala**: corpo com 4.021 palavras ≈ 30,9 min a 130 ppm, acima
   dos 30 min. Slide 13 é o mais longo (3,7 min). Mirar ~27 min.
4. **"BAD_PLL" na tela e na fala** (slide 8, cartão e notas): nome de
   código; no TCC é "sintonia inadequada".

## P3 — decidir com o Victor

5. Rótulo **"Justificativa de ouro:"** em 12 slides: soa como instrução
   interna de quem montou o esboço. Manter, trocar (ex.: "Por quê?") ou
   tirar o rótulo e deixar só a pergunta.
6. Fontes Arial (título) + Calibri (corpo) do tema; PowerPoint lista também
   Aptos. Conferir se o notebook da defesa tem as mesmas.
