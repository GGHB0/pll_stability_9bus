---
name: palco-codigo-de-rede
aliases: [palco-codigo-de-rede]
description: Capítulo "Código de rede" do palco da defesa (kind "ons") em seis passos — regra, curtos próximos, distantes, dilema Q = V·iq (0,09 pu), outros curtos e fecho com a frase da Conclusão; campos realce, outros, fecho, cartoes_pres
---

# Palco: Código de rede em seis passos

Continuação de [[modo-apresentacao-palco]]. Pedido em 2026-10-25: a tela
mostrava tudo de uma vez (parágrafo, dois gráficos, quatro cartões) e não
tinha os dois argumentos mais fortes do slide do deck sobre o Submódulo
2.10: a potência reativa de 0,09 pu com corrente saturada e o "permanecer
conectado não basta". É o penúltimo capítulo e fecha a defesa com a tese
do trabalho.

## Passos

| Passo | Em cena | Fonte da frase |
|---|---|---|
| 1 | Só a região (Fig. 2.1) e a rampa (Fig. 2.2), sem casos | §5.5, 1º parágrafo |
| 2 | Barra 7 e Linha 7-8: abaixo de 0,2 pu, i<sub>q</sub> = 1 pu | Tabela 5.2 |
| 3 | Os quatro casos; Barra 6 a 0,72 contra 0,76 pu da rampa | Tabela 5.2 |
| 4 | Barra 7 realçada, outros esmaecidos; caixa "0,09 pu" com seta ao ponto na rampa | texto da Fig. 5.8 (§5.2) |
| 5 | Outros curtos acesos (assimétricas e inadequada) | §5.5, 2º e 3º parágrafos |
| 6 | Gráfico velado, cartão "O que a verificação de hoje pergunta / O que os resultados mostram" | Conclusão (Cap. 6) |

O passo 6 é a única exceção à regra "último passo sem foco, gráfico
inteiro": o cartão vela o gráfico de propósito. Foi escolhido entre três
prévias (só a frase; cartão central; dois cartões "conectado × serviço",
recusado por citar "28 de 28 não desconectaram", que não está no TCC).

## Campos (roteiro.py, kind "ons")

- `realce` no passo: casos em cena; os outros ficam com opacidade 0,15 nas
  curvas e 0,2 nos pontos (`esm` em `_onsFigure`).
- `outros=True` no passo: liga `st.outros` (os demais curtos), como o botão
  "Mostrar os outros curtos"; `palco.js` aplica a cada passo e
  `_presPassoReset` desliga ao sair do palco.
- `fecho = {pergunta, resposta}` no passo: `palco.js` acrescenta
  `#pres-fecho` dentro de `#pres-body` (CSS `.pres-fecho` em `renderer.py`,
  tamanhos em `clamp`/`vw`).
- `destaque.key` no capítulo: a caixa aponta o ponto (V<sub>méd</sub>,
  i<sub>q,ref</sub>) do caso no painel da rampa; com destaque, a nota
  "abaixo de 0,5 pu, i<sub>q</sub> = 1 pu" some para não colidir.
- `cartoes_pres=False`: sem cartões embaixo no palco (a aba Análise TCC,
  que os mostrava, saiu em 2026-10-25). O veredito por cenário fica no card
  "Suportabilidade ONS" do Resumo ([[indicadores-tcc-dashboard]]).

## Relacionados

- [[ons-voltage-ride-through]] — região de suportabilidade e rampa do Submódulo 2.10
- [[roteiro-demonstracao-dashboard]] — capítulos, casos e cores
