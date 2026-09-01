---
name: tcc-revisao-fragmento-cap5-analise
description: Regra editorial do Cap.5 do fragmento — descrição de figura não é análise; o que substituiu a enumeração de valores nos parágrafos 98 e 101, e o que ficou de fora
metadata:
  type: project
---

# Cap. 5 do Fragmento — Descrição de figura não é análise

Desmembrado de [[tcc-revisao-fragmento-cap5]] em 2026-09-01 (limite de 200
linhas). Continua a linha das remoções de métrica registradas em
[[tcc-revisao-fragmento-cap5-metricas-54]].

## O diagnóstico

Usuário, sobre o parágrafo 98 (§5.4, Figura 5.13): *"não tem nada de errado e
nada que a gente não saiba explicar, só não tem nenhum valor para uma análise
[...] algumas coisas poderiam ser apresentadas com imagens e apresentar a
análise em si"*.

**O padrão a caçar:** parágrafo que enumera valores todos legíveis na figura ao
lado. O 98 tinha **nove** (0,84 / −0,30 / −1,07 / −0,94 / 1,97 / 0,14 / 1,11 /
0,70 / 0,82) e nenhuma inferência. Número que o leitor tira do gráfico sozinho
não justifica texto; o texto tem que dizer o que o gráfico **não** diz.

É a mesma família da regra de métrica sem receita
([[tcc-revisao-fragmento-cap5-metricas]]) e da retirada das métricas de
escorregamento: número que não sustenta argumento só abre flanco.

## Os três eixos que contam como análise

Usados na reescrita do 98, e o modelo para os próximos:

1. **Sentido, não magnitude.** P não "cai", ela inverte de sinal. É o que separa
   este cenário de todos os outros do capítulo.
2. **Inversão, não degradação.** Q alterna entre absorção e injeção dentro de
   cada ciclo: o suporte de reativo não fica pior, trabalha contra parte do
   tempo. Gancho direto para a §5.5.
3. **Inversão de causalidade.** Falta eliminada, rede restabelecida, e o PAC
   continua perturbado: a perturbação virou endógena. Durante a falta a rede
   perturbava o inversor; depois é o inversor que impõe a oscilação. É a
   afirmação mais forte da seção e era a única já presente no texto antigo,
   solta na última frase.

## Aplicado (2026-09-01)

| Par. | Figura | O que mudou |
|---|---|---|
| 98 | 5.13 (P e Q) | Saíram os 9 valores; entraram os três eixos acima |
| 101 | 5.14 (correntes) | Saiu a enumeração (0,92 / −0,66 / 1,34 / −1,76 / −0,24); o mecanismo já era bom |

No **101** o mecanismo já existia e valia (projeção sobre eixos errados).
Entrou a atribuição de causa — a separação entre comando e corrente entregue
**não é falha da malha de corrente, é do referencial em que ela opera** — mais
o fecho explícito da cadeia 5.12 → 5.13 → 5.14. Cuidado tomado: não afirmar que
a malha de corrente "rastreia corretamente", porque a figura mostra ref e medido
divergindo no mesmo referencial; a redação atribui a causa sem negar a
divergência.

## Não mexidos, e por quê

- **102** — comparação 2×2 (9,2% / 98 ms contra 58,4% / 106 ms). Os números
  *são* o argumento (nem profundidade nem sintonia isoladas produzem o
  fenômeno), não descrição de figura.
- **103** — ressalva da janela de 300 ms mais a implicação operacional
  (proteção atuaria antes). Análise.
- **111** — síntese do capítulo; os números são os resultados de topo.

## Pendências

- **Parágrafo 107 (§5.5)** ainda repete "pulsando entre 0,14 pu e 1,11 pu",
  agora o único lugar do texto com esses valores. Como a §5.5 não tem figura, é
  o único apoio quantitativo da afirmação normativa ali. Deixado como estava, à
  espera de decisão do usuário.
- **Candidatos anteriores ao §5.4**, mesmo padrão, não avaliados com o usuário:
  parágrafo **87** (§5.3) tem dez valores de `t_s` e ondulação de Q em prosa;
  parágrafo **66** (§5.2) tem oito valores de retenção e pico, embora ali a
  progressão monotônica seja o argumento e a última frase dê o mecanismo.
- **Figura que carrega o conceito:** usuário quer discutir uma imagem que
  embuta os conceitos no próprio gráfico (na linha da figura didática da
  retenção, ver [[tcc-revisao-fragmento-cap5-metricas-54]]). Não iniciado.
  Nota: `bus7_3phase_bad_pll_tensao_dq_inversor` já existe em `assets/charts/`
  e nunca foi inserido — é a tensão no PAC, hoje só descrita em prosa.
