# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

## 2026-10-24 — Faltas destacadas: por que estes quatro pontos

Arquivos: `src/report/roteiro.py`

O primeiro passo do capítulo "Faltas destacadas" dava a entender que só
quatro pontos receberam falta. O texto passou a dizer que outros pontos
também foram simulados e que a análise se concentra nestes quatro, cada um
com uma particularidade: juntos, vão do afundamento mais profundo ao mais
raso e incluem uma linha de circuito simples e outra de circuito duplo.
`verifica_palco.py` sem falhas em 1920×1080 e 1280×720.

## 2026-10-24 — Palco legível em telas menores que 1920×1080

Arquivos: `src/report/renderer.py` (CSS e estrutura do palco),
`src/report/js/tcc.js`, `src/report/js/fasor.js`, `scripts/verifica_palco.py`

Um notebook Full HD com escala de 150% no Windows entrega 1280×720 ao
navegador. Nessa faixa a dica de passo cobria os botões dos capítulos, os
rótulos de retorno se sobrepunham, o fasor ficava espremido e a tabela
"Todos os casos" cortava linhas e colunas. A dica foi para o cabeçalho, o
painel ao lado ficou proporcional à largura, uma regra `@media` compacta
cabeçalho, cartões e tabela, e casos com o mesmo tempo de retorno dividem
uma seta. Em 1920×1080 nada muda. O `verifica_palco.py` passou a rodar em
1920×1080 e 1280×720 e a acusar painel ao lado e tabela que não cabem.

## 2026-10-24 — JS em arquivos, verificação do palco, vírgula e retorno à faixa

Arquivos: `src/report/renderer.py`, `src/report/js/` (novo, 9 arquivos),
`src/report/roteiro.py`, `src/pipeline/indicadores.py`,
`scripts/verifica_palco.py` (novo), `.githooks/pre-commit`, `requirements.txt`

- O JS da aba Análise TCC e do palco saiu da string `_TCC_JS` para
  `src/report/js/`, lido na geração na ordem de `TCC_JS_FILES`. O HTML
  gerado ficou idêntico byte a byte; o pre-commit roda `node --check`.
- `scripts/verifica_palco.py` percorre o palco no Edge headless e falha em
  erro de JS, tela que rola, gráfico sobre o painel ao lado e navegação
  errada; PNGs em `output/verifica_palco/`. Playwright entrou no
  `requirements.txt`.
- Cartões e tabela "Todos os casos" com vírgula decimal, como as legendas.
- Retorno à faixa de 2° marcado nos capítulos com falta: tracejado, ponto
  e seta da eliminação até o retorno, com o tempo do cartão. Eixo do erro
  em ±60° na Localização (`faixa_err`). `indicadores_falta` devolve também
  `err_ts`.

## 2026-10-24 — Palco: passos, fasor, mini-mapa e números de destaque

Arquivos: `src/report/roteiro.py`, `src/report/renderer.py`

Elementos só do modo apresentação, para enriquecer a defesa além dos
gráficos, configurados por capítulo em `CAPITULOS`:
- `passos_pres` (Energização): a seta mostra primeiro só a nominal e
  depois a inadequada, com a legenda trocada por uma frase grande por passo.
- `lado="fasor"` (Perda de sincronismo): círculo com o ângulo do PLL de cada
  sintonia contra a rede, seguindo o mouse ou um play de 8 s.
- `lado="minimapa"` (Localização): unifilar com os pontos na cor das curvas
  e a retenção de v_d.
- `destaque`: "> 250×" sobre o espectro e "66,8%" sob o fasor.
O gráfico do palco passou a receber largura explícita no `Plotly.react`.
Detalhes em `.claude/kb/dashboard/layout/modo-apresentacao.md`.

## 2026-10-24 — Marcação da acomodação no capítulo "Energização"

Arquivos: `src/pipeline/indicadores.py`, `src/report/renderer.py`

No palco e na aba Análise TCC, o capítulo de energização marca onde cada
curva entra de vez na faixa: linha tracejada na cor do caso, tempo no topo
(40/79 ms no erro, 34/42 ms em v_d) e ponto na curva. O painel de v_d ganhou
a faixa de ±5% do valor final (uma por caso), e o eixo do erro fica em ±20°: em ±150° a
faixa de 2° não aparecia. `indicadores_partida` passou a devolver o valor
final de v_d e o valor de cada sinal no instante de acomodação
(`tccInd.partida`). Escolhida entre três prévias (linha + ponto, etiqueta só
no erro, setas de duração).

## 2026-10-21 — Curva de suportabilidade no capítulo "Código de rede"

Arquivos: `src/pipeline/indicadores.py`, `src/pipeline/loader.py`,
`src/report/renderer.py`, `src/report/roteiro.py`

O capítulo do ONS ganhou, ao lado da rampa de corrente reativa, a curva de
suportabilidade a subtensões (Figura 2.1) com a tensão da fase mais
afundada no inversor de cada caso. Etiqueta "dentro/fora da região" nos
chips e cartões; anel vermelho na rampa para os casos fora; faixas por
regime na rampa. "+ Mostrar os outros curtos" acende os demais cenários sem
destaque, e o mouse sobre "Fora/Dentro da região · N casos" lista e filtra
os casos no gráfico. Nova receita `suportabilidade_ons` (60 Hz por fase,
janela de 1 ciclo); a série entra em `tccInd.lvrt` (~0,2 MB no HTML).

## 2026-10-21 — Capítulo "Faltas destacadas"

Arquivos: `src/report/roteiro.py`, `src/report/renderer.py`

Primeiro capítulo da aba Análise TCC e do modo apresentação: antes dos
resultados, o unifilar mostra onde as faltas foram aplicadas (Barra 7, Linha
7-8, Linha 8-9 em circuito duplo, Barra 6). Seis passos: visão geral, um
por ponto e resumo. Cada passo traz um cartão com texto, as faltas e
sintonias simuladas e "Abrir no painel →", além de uma régua do
afundamento mais profundo ao mais raso. A seta → percorre os passos antes de
trocar de capítulo. Clicar na barra, na linha ou no pino da régua pula para
o ponto. Saiu de três prévias standalone aprovadas pelo usuário.

## Entradas anteriores

- [2026-10-20](docs/changelog/2026-10-20.md) — indicadores do Cap. 5 no painel,
  casos do TCC em destaque, aba "Análise TCC", modo apresentação (palco branco),
  rampa do ONS e rótulo do mouse.
- [2026-10-03 a 2026-10-16](docs/changelog/2026-10-03_16.md) — Plotly embutido
  no HTML (abre sem internet); fix da escala de P e Q do UFV.
- [2026-08-17 a 2026-08-18](docs/changelog/2026-08-17_18.md) — fix do filtro
  do toggle PLL na carga inicial, título do eixo X do espectro, aba "Sistema
  9-Bus" renomeada para "Barras de Geração".
- [2026-08-11](docs/changelog/2026-08-11.md) — tabela de critérios na legenda
  da tabela de harmônicas; FFT mede a frequência real por segmento (abc).
- [2026-08-09](docs/changelog/2026-08-09.md) — medição de harmônicas pelo
  IEEE 519 §4.1 (3 bins RMS, janela retangular) e relaxamento ×1,5 na falta;
  remoção dos cards de erro de
  ângulo (grupo "Desempenho do PLL": IAE/ISE/tₛ/pico/Erro R.P.), sem base
  bibliográfica que os sustentasse como métrica de desempenho.
- [2026-08-05](docs/changelog/2026-08-05.md) — linha de 0 Hz (fundamental em
  DC) na tabela dq, tabela de harmônicas separada em abc e dq.
- [2026-08-03](docs/changelog/2026-08-03.md) — card e item de diagnóstico
  "Topologia" (line7_8 vs. line8_9, circuito único vs. duplo).
- [2026-08-02](docs/changelog/2026-08-02.md) — teto fixo em 1 pu no eixo Y
  do espectro FFT, legenda explicada da tabela de harmônicas.
- [2026-07-28 a 2026-07-30](docs/changelog/2026-07-28_30.md) — faixa de
  frequência ONS §5.2.1 no painel "Frequência PLL" (depois removido),
  destaque normativo (IEEE 519/1547) na tabela de harmônicas, remoção do
  painel "Frequência PLL".
- [2026-07-25](docs/changelog/2026-07-25.md) — eixo Y com nome+unidade,
  título branco fix, remoção do overlay "Comparar PLL", cards de tensão
  mínimo → média (V médio / V residual médio).
- [2026-07-18 a 2026-07-24](docs/changelog/2026-07-18_24.md) — terminologia
  "sintonia inadequada", remoção dos ícones emoji dos botões/abas, remoção
  das métricas ΔP/ΔQ UFV, cards/diagnóstico movidos para a aba Resumo.
- [2026-07-15](docs/changelog/2026-07-15.md) — espectro FFT multi-modo
  (a/b/c/d/q) + tabela de harmônicas, abas de gráficos + aba Resumo + cards
  clicáveis.
- [2026-07-14](docs/changelog/2026-07-14.md) — regime sem tₛ, cards de
  severidade renomeados para "V residual", Vmin das Barras 1 e 3.
- [2026-07-12](docs/changelog/2026-07-12.md) — export de correntes/tensões
  abc, T_SETTLE fora de todos os cálculos, espectro de Fourier segmentado.
- [2026-07-01 a 2026-07-05](docs/changelog/2026-07-early.md) — reestruturação
  do pacote `src/`, decimação (570 MB → 23,7 MB), tabela comparativa, fixes de
  dark mode, overlays de análise (LVRT, tₛ, frequência PLL), zoom sincronizado,
  reavaliação dos cards e veredito.
