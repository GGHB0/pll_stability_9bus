---
name: faltas-destacadas
aliases: [faltas-destacadas]
description: Capítulo "Faltas destacadas" (1º do modo apresentação) — unifilar com os quatro pontos de falta (B7, L7-8, L8-9 dupla, B6), passos por seta ou clique, régua de severidade; implementado em 2026-10-21 (kind "mapa")
source: prévia standalone de 2026-10-21; Zbarra do notebook (ver ieee9bus-thevenin)
---

# Capítulo "Faltas destacadas"

Pedido de 2026-10-21: antes dos resultados, o modo apresentação
([[roteiro-demonstracao-dashboard]]) mostra **onde** as faltas foram
aplicadas e por que esses pontos. Foi aprovado em três prévias standalone e
implementado no mesmo dia como 1º capítulo (no palco aparece como "1/8").

## Implementação

- `roteiro.py`: entrada `id="faltas"`, `kind="mapa"`, com `passos` (id do
  ponto, `rotulo`, `pos` na régua, `cenario` do botão, `faltas`,
  `inadequada`, `tom` da etiqueta, `texto`, `papel`; `resumo=True` acende
  tudo). Textos e cobertura ficam ali, não no JS.
- `src/report/js/mapa.js`: `_mapaSvg` monta o unifilar como string a
  cada passo; `_mapaHtml(cap, gid)` monta SVG, cartão e régua (o `gid`
  evita id de gradiente repetido entre aba e palco). Os containers são
  `#tcc-mapa` e `#pres-mapa`.
- Navegação: `tccStep`/`presStep` (teclado e botões ‹ ›) chamam
  `_mapaStep` e só trocam de capítulo no último passo; voltando pela seta,
  `_mapaEnter(i, back)` abre no último passo, e pelo botão do capítulo,
  no primeiro.
- Cores por variáveis de tema (`--text`, `--surface`, `--accent`): funciona
  na aba em dark mode e no palco branco.
- Conferido no Edge headless (Playwright): sem erro de JS, palco em
  1920×1080 sem rolagem, clique no ponto, setas, botão abre `bus7/3phase`.

## Os quatro pontos (definidos pelo usuário)

| Ponto | Papel | Faltas simuladas | Sintonia inadequada |
|---|---|---|---|
| Barra 7 | mais próxima da usina (só T2 no meio) | 3φ, 2φ, 1φ | sim |
| Linha 7-8 | circuito simples | 3φ | sim |
| Linha 8-9 | **circuito duplo**, falta em um só | 3φ | não |
| Barra 6 | mais distante (3 linhas em qualquer caminho) | 3φ, 2φ, 1φ | sim |

O SVG do dashboard (`ieee9bus_unifilar.svg`) desenha a 8-9 simples. No palco,
ela aparece como dois circuitos ("circuito com falta" / "sem falta"). A
cobertura de faltas segue [[cenarios-simulados]].

Na primeira mensagem, a Barra 8 apareceu como a mais distante. Era a 6
(correção do usuário). A Barra 8 segue fora do TCC.

## Layout (palco branco, 1600×900 conferido)

- Cabeçalho: "Capítulo 0 · Antes dos resultados", título **Faltas
  destacadas**, subtítulo "Quatro pontos de falta, do mais próximo ao mais
  distante da usina fotovoltaica".
- Esquerda: unifilar simplificado, sem R/X/B nem cargas. Cinza = rede; azul
  = ponto ativo; raio vermelho num círculo = local da falta. Rótulos "mais
  perto/longe da usina" na B7 e na B6.
- Direita: cartão com etiqueta colorida (vermelho = perto, âmbar = linha,
  azul = longe), título, dois parágrafos e uma linha "No estudo". Abaixo,
  etiquetas de faltas e sintonias (tachado = não simulado) e o botão
  "Abrir no painel →", que sai do palco e abre a trifásica nominal do ponto.
- Régua "afundamento mais profundo → mais raso" com os quatro pinos. A
  posição é proporcional à tensão residual na Barra 2 (0 / 0,06 / ~0,23 /
  0,36 pu; ver [[ieee9bus-thevenin]]). **Número nunca aparece na tela**:
  não está no TCC ([[defesa-deck-map]] segue a regra do deck exato).
- Navegação: seta → / ← (6 passos), clique na barra/linha ou no pino da
  régua pula para o passo daquele ponto.

## Textos aprovados

| Passo | Título | Conteúdo resumido |
|---|---|---|
| 1 | Quatro pontos, uma pergunta | outros pontos também receberam falta, a análise se concentra nestes quatro; cada um tem uma particularidade e juntos vão do afundamento mais profundo ao mais raso, com linha de circuito simples e de circuito duplo (2026-10-24: não listar os outros curtos, só anunciar a lógica da escolha). Pergunta: como a distância muda a resposta do SRF-PLL? |
| 2 | Barra 7 | logo depois do T2; caso mais severo, afundamento mais profundo; ponto de partida da perda de sincronismo |
| 3 | Linha 7-8 | sai da B7; sem circuito paralelo, a linha inteira sob falta; ainda perto da usina |
| 4 | Linha 8-9 | dois circuitos, falta em um; o outro segue conduzindo |
| 5 | Barra 6 | ramo inferior, entre B4 e B9; caso mais brando; contraponto da B7 |
| 6 | Faltas destacadas (resumo) | ordem B7, L7-8, L8-9, B6; todos com 3φ; B7 e B6 também 1φ e 2φ (capítulo de sequência negativa) |

Texto literal completo: `passos` do capítulo `faltas` em `roteiro.py`.

Cuidados na revisão do texto:
- Não afirmar que só a B7 perde o sincronismo: a
  `line7_8/3phase_bad_pll` da safra de 01/10 também perde
  ([[cenarios-simulados]]), e o §5.4 ainda está para ser refeito.
- "Usina" em vez de "UFV" no texto corrido. Na legenda do desenho, UFV.
- Sem em-dash e sem a sigla de transitórios eletromagnéticos (regras do deck).

## Relacionados

- [[roteiro-demonstracao-dashboard]] — o modo apresentação que recebe o capítulo
- [[ieee9bus-thevenin]] — cálculo da ordem de severidade da régua
