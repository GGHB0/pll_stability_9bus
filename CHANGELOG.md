# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

## 2026-10-25 — Palco: foco também na Energização, Localização e Sequência negativa

Arquivos: `src/report/roteiro.py`, `src/report/js/navegacao.js`,
`src/report/js/palco.js`, `src/report/js/mapa.js`, `src/report/renderer.py`

A mesma dinâmica de passos com foco foi para os outros capítulos com
gráfico. Energização: foco na partida (0 a 60 ms, depois 0 a 100 ms).
Localização: foco na falta nos passos 1 e 2 e um passo 3 novo, "o erro
sempre volta à faixa de 2°: em até 112 ms", com foco no pós-falta.
Sequência negativa: dois passos novos, a trifásica sozinha e depois as
assimétricas com o "> 250×", foco em 100 a 140 Hz. Em todos os
capítulos, o último passo fica sem foco, com o gráfico inteiro. O texto
"passo N de M · seta → avança" virou uma barra em segmentos que enche até
o passo atual, com "k de n" embaixo, no palco e no mapa (`_passoInd` em
`navegacao.js`, CSS `.passo-*` no `renderer.py`; escolhida entre três
prévias). Revisão dos textos contra o deck e o TCC: "escorregamento de
ciclo", "sintonia nominal" na 1ª menção, retenção de v<sub>d</sub> na ordem
nominal/inadequada, i<sub>q,ref</sub> explícito no Código de rede e cartão
"Pico do erro de fase", como no slide 19. `verifica_palco.py` sem falhas.

## 2026-10-25 — Palco: passos com foco no Compromisso e na Perda de sincronismo

Arquivos: `src/report/roteiro.py`, `src/report/js/tcc.js`,
`src/report/js/navegacao.js`, `src/report/js/fasor.js`

As duas telas apareciam inteiras de uma vez, e a do Compromisso já
anunciava a perda de sincronismo no cabeçalho. Agora cada uma tem 3 passos
(nominal sozinha, entra a inadequada, frase-ponte ou fecho). Campo novo
`foco` no passo esmaece o gráfico fora da janela que importa; campo
`destaque` no passo faz o 66,8% aparecer só no fecho da Perda de
sincronismo. O texto corrido da aba Análise TCC não mudou.

## 2026-10-24 — Palco: Perda de sincronismo depois do Compromisso

Arquivos: `src/report/roteiro.py`

O palco mostrava a perda de sincronismo da sintonia inadequada (§5.4) antes
do capítulo em que ela filtra melhor o 120 Hz (§5.3), e o capítulo favorável
soava como defesa de algo já derrubado. A ordem passou a seguir o TCC:
Sequência negativa → Compromisso → Perda de sincronismo. O título do
Compromisso virou "Ganho menor filtra melhor o 120 Hz" e a última frase
virou ponte ("Mas, na trifásica da Barra 7, a mesma sintonia perde o
sincronismo").

## 2026-10-24 — Sequência negativa: trifásica visível, casos agrupados por barra

Arquivos: `src/report/roteiro.py`, `src/report/js/tcc.js`,
`src/report/js/tcc_ui.js`, `src/report/renderer.py`

Na tela 5 do palco, a trifásica da Barra 7 (cinza-claro, colada no zero)
não aparecia. Agora é grafite, grossa e desenhada por cima, com uma caixa
"Barra 7 trifásica, 0,0002 pu" apontando para ela em 120 Hz (campo novo
`notas`, `_nota`). Cor = barra (laranja = 7, verde-azulado = 6), traço =
curto (contínuo = bifásica, tracejado = monofásica); chips agrupados sob
"Barra 7"/"Barra 6" e cartões na mesma ordem, com respiro entre as barras
(3º item opcional de `casos`: `dash`, `larg`, `grupo`, `frente`). A caixa
"> 250×" passou a dizer "contra as trifásicas". Os cartões da tela viraram
uma matriz Barra 7/6 × trifásica/bifásica/monofásica (campo `matriz`,
`_tccMatrizHtml`), com a trifásica da Barra 6 (0,0011 pu) só na tabela;
escolhida entre duas prévias.

## 2026-10-24 — Fasor mais lento; mini-mapa liga e desliga casos

Arquivos: `src/report/js/fasor.js`, `src/report/js/minimapa.js`

O play do fasor estava rápido demais para acompanhar na defesa: passou de
8 s para 20 s por janela (`FASOR_MS`), em todos os capítulos com fasor. No
mini-mapa da Localização, clicar num ponto (traço ou número de retenção)
liga ou desliga o caso no gráfico e nos cartões, como o chip; o caso
desligado fica esmaecido no mapa e continua clicável. O estado vale também
no passo do fasor. `verifica_palco.py` sem falhas em 1920×1080 e 1280×720.

## 2026-10-24 — Localização em dois passos: mini-mapa, depois fasor

Arquivos: `src/report/roteiro.py`, `src/report/js/palco.js`,
`src/report/js/fasor.js`, `scripts/verifica_palco.py`

O capítulo Localização ganhou dois passos no palco, sem perder o mini-mapa.
Passo 1: mini-mapa ao lado e a frase da retenção de v_d (9,2% na Barra 7,
58,4% na Barra 6). Passo 2: o painel ao lado vira o fasor com os quatro
casos e a frase do pico do erro (37,3° e 7,3°), números da Tabela 5.1. Cada
passo pode ter `lado` próprio, resolvido por `_presLado()`; o
`verifica_palco.py` usa a mesma função para achar o fasor. Sem mistura de
sintonias, a legenda do fasor usa o rótulo do mapa (B7, L7-8, L8-9, B6) em
vez de "PLL nominal" repetido. `verifica_palco.py` sem falhas em 1920×1080
e 1280×720.

## 2026-10-24 — Fasor também na Energização; play sempre do início

Arquivos: `src/report/roteiro.py`, `src/report/js/fasor.js`, `src/report/js/palco.js`

O fasor da Perda de sincronismo foi para o capítulo Energização
(`lado="fasor"`): o play mostra o vetor do PLL girando até travar na marca
da rede, em 8 s para a janela de 0 a 0,2 s. Os passos valem também no
fasor: no passo 1 só o vetor nominal, no passo 2 entra o da inadequada. O
play passou a recomeçar sempre do início da janela do capítulo (antes
continuava de onde tinha parado), e o instante volta ao início ao trocar
de capítulo. `verifica_palco.py` sem falhas em 1920×1080 e 1280×720.

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

## Entradas anteriores

- [2026-10-24](docs/changelog/2026-10-24.md) — palco com passos, fasor,
  mini-mapa e números de destaque; marcação da acomodação na Energização.
- [2026-10-21](docs/changelog/2026-10-21.md) — capítulo "Faltas destacadas"
  (unifilar com os quatro pontos) e curva de suportabilidade no "Código de rede".
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
