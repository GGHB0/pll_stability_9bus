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
- **Inserção da figura do plano P-Q no DOCX** (ver abaixo): gerada e aprovada
  visualmente, mas **ainda não inserida** — entra como figura da §5.4 e empurra
  a numeração seguinte. Aguardando decisão do usuário.
- `bus7_3phase_bad_pll_tensao_dq_inversor` já existe em `assets/charts/` e
  nunca foi inserido — é a tensão no PAC, hoje só descrita em prosa. Alternativa
  ou complemento ao plano P-Q.

## Figura do plano P-Q (2026-09-01)

Pedido do usuário: *"vamos fazer que nem fizemos no gráfico 5.11 [...] um svg
que consiga gerar valor dos gráficos, destacar algo do texto, faça algo que
fique bem visual"*.

Gerador `scripts/gen_plano_pq.py` → `assets/charts/plano_pq_comparacao.svg/.png`.
Painel duplo `bus7/3phase` × `bus7/3phase_bad_pll`. Detalhes de desenho em
`assets/charts/figuras_didaticas.md` e a regra generalizada em `data_charts.md` da skill
`svg-diagrams` ("trocar o eixo do tempo por um plano de estado").

**A ideia:** abandonar o eixo do tempo e plotar a trajetória no plano P-Q. O
ponto pré-falta vira o marcador "antes", a média da janela pós-falta vira
"depois". No nominal os dois coincidem; na sintonia inadequada o "depois" está
do outro lado da linha `P = 0`. É a tradução visual direta do eixo 1 ("sentido,
não magnitude") do parágrafo 98.

**Métrica nova que a figura trouxe — fração do tempo com `P < 0`:**

| Cenário | Janela | P média | Tempo com P<0 |
|---|---|---|---|
| `bus7/3phase` (nominal) | [0,45; 0,60] s | +0,799 pu | **1,1%** |
| `bus7/3phase_bad_pll` | [0,75; 1,00] s | **−0,288 pu** | **64,6%** |

Janela = `[t_clear + 50 ms, fim]`; os 50 ms removem o transitório de eliminação
(no nominal P chega a −3,4 pu por poucos ms). Vale mais que qualquer valor de
pico porque é **razão adimensional que não depende do comprimento da janela** —
exatamente a objeção que derrubou a rotação acumulada em
[[tcc-revisao-fragmento-cap5-metricas-54]]. Separa os dois cenários por quase
duas ordens de grandeza.

## Figura da potência anotada (2026-09-01)

Usuário, depois de ver o plano P-Q: *"acho que vale fazer algo em cima dos
gráficos que já existe em série temporal"*. Em vez de um gráfico novo que o
leitor precisa aprender a ler, **anotar o oscilograma que já é a Figura 5.13**.

Gerador `scripts/gen_potencia_didatica.py` → `assets/charts/potencia_didatica`.
Dois painéis (P em cima, Q embaixo), só `bus7/3phase_bad_pll`. Quatro camadas
sobre o traço bruto: área preenchida onde a potência é negativa; patamar
pré-falta tracejado; média pós-falta tracejada; e a fração do tempo em caixa.

O contraste aqui é **temporal** (antes × depois no mesmo cenário), não entre
cenários — por isso dispensa o painel do nominal e cabe como substituição direta
da imagem da Figura 5.13, **sem renumerar nada**.

| | P | Q |
|---|---|---|
| antes da falta | 0,84 pu | 0,01 pu |
| média pós-falta | **−0,26 pu** | 0,45 pu |
| tempo **entregando** | 36,2% | 60,6% |
| tempo **absorvendo** | **63,8%** | 39,4% |

**Revisão de 2026-09-01 (2ª passada na figura).** Usuário: *"você consegue
mostrar se a gente está consumindo ou entregando potência ativa"*. A primeira
versão preenchia só o lado negativo, o que dizia "absorve" mas deixava
"entrega" implícito. Passou a preencher **os dois lados** (verde acima do zero,
vermelho abaixo) e a caixa passou a dar **as duas frações**. É o que torna
visível a alternância de sentido a cada ciclo — o fenômeno que o parágrafo 98
descreve como "deixa de ter sinal definido".

Janela `[t_clear, fim]`, a mesma região sombreada, para número e desenho não
divergirem. A escala vertical ignora os 20 ms seguintes à eliminação (o
transitório de comutação levaria P a −2,4 pu e esconderia a oscilação).

### Legibilidade na página — validação pedida pelo usuário

*"Vale validar se o texto pode estar ficando ruim de enxergar por conta dos
gráficos"*. Estava mesmo: as duas figuras novas nasceram com `figsize` 10,2 e
10,4 in, o que a 6,5 in na página dava escala 0,64 e derrubava as anotações de
8,8 pt para 6,9 pt. Corrigidas para `figsize` 8,3 in com anotações em 9,5 pt,
chegando à escala 0,78 (~7,8 pt efetivos), que é o padrão do capítulo.

**As duas precisam entrar a 6,5 in**, como a Figura 5.11, e não a 5,5 in dos
oscilogramas comuns. Regra completa e procedimento de validação em
`assets/charts/figuras_didaticas.md` ("Legibilidade no DOCX"), no `data_charts.md`
da skill `svg-diagrams` e em `fragmento_externo.md` da skill `tcc-docx-editor`.

### Escolha pendente

Duas figuras geradas para o mesmo parágrafo, **nenhuma inserida ainda**:

| Figura | Contraste | Custo no documento |
|---|---|---|
| `potencia_didatica` | antes × depois, mesmo cenário | substitui a imagem da 5.13, sem renumerar |
| `plano_pq_comparacao` | nominal × inadequada, plano de estado | figura nova, renumera da 5.14 em diante |
