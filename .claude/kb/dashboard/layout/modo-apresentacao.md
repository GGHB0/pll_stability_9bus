---
name: modo-apresentacao-palco
aliases: [modo-apresentacao-palco]
description: Modo apresentação do dashboard (palco branco em tela cheia da defesa) — estrutura, navegação, marcação de acomodação, passos com frase-mensagem, painel lateral (fasor, mini-mapa) e números de destaque; src/report/renderer.py e roteiro.py
---

# Modo apresentação (palco)

Botão "Modo apresentação" no cabeçalho, pedido em 2026-10-20 para dar
imersão e caber tudo na tela. O site inteiro vira um palco branco em tela
cheia (`#pres`, `position: fixed`, `requestFullscreen`), um capítulo por
tela, sem rolagem: número do capítulo, legenda, chips, gráfico ocupando a
altura que sobra, faixa de mini-cartões e os botões dos capítulos embaixo.
Os capítulos estão em [[roteiro-demonstracao-dashboard]] (até 2026-10-25 também
apareciam na aba Análise TCC, que saiu; menções a "aba" abaixo são desse período).

## Estrutura

- Os sinais de `cap.pres` ficam empilhados num só gráfico, com o mesmo eixo
  x (o zoom vale para todos): erro de fase + v_d na energização, na
  localização e no compromisso; erro de fase + P na perda de sincronismo.
- O tema claro é fixo no palco, independente do botão "Dark mode": as
  variáveis CSS são redefinidas dentro de `.pres` e a figura sai com
  `dark: false` sobre fundo branco. A primeira versão era escura; o usuário
  escolheu, entre três prévias claras, o branco puro, que também resiste
  melhor ao projetor numa sala iluminada.
- `#pres-body` é uma linha flex com `#pres-plot` e `#pres-side` (painel ao
  lado, só com `cap.lado`). Nos capítulos sem gráfico (mapa, tabela), o
  `#pres-body` inteiro some.
- `_tccFigure(cap, sinais, o)` monta a figura na aba e no palco (`o.big`).
  `_renderPres` passa altura **e largura** explícitas: o `Plotly.react`
  guardava a largura do capítulo anterior e o gráfico cobria o painel ao
  lado (achado na verificação de 2026-10-24).
- Seta ou PageDown avança, Esc sai (com tela cheia, quem fecha é o
  `fullscreenchange`). Clicar num cartão sai do palco e abre o cenário.

## Navegação em três níveis

`presStep(d)`: primeiro os passos do mapa (`_mapaStep`, capítulo "Faltas
destacadas", [[faltas-destacadas]]), depois os passos do palco
(`_presPassoStep`), e só então o capítulo vizinho. Entrando num capítulo
pela seta ←, cai no último passo.

## Marcação de acomodação (Energização, 2026-10-24)

`_marcaPartida` marca, por caso, linha tracejada na cor da curva, tempo no
topo (40/79 ms no erro, 34/42 ms em v_d) e ponto onde a curva entra de vez
na faixa. O painel de v_d ganhou a faixa de ±5% do valor final, uma por
caso em volta do próprio valor final (0,983 nominal, 0,996 inadequada; com
uma só, o ponto da inadequada caía fora dela, achado do code-reviewer). O eixo do
erro fica em ±20°: em ±150° a faixa de 2° sumia. Valores de
`tccInd.partida` ([[indicadores-tcc-dashboard]]). Vale no palco e na aba.
Escolhida entre três prévias (linha + ponto, etiqueta só no erro, setas de
duração).

## Retorno à faixa de 2° (capítulos com falta, 2026-10-24)

`_marcaRetorno` (`tcc.js`) vale em todo capítulo com a métrica `ts`
(Localização, Perda de sincronismo, Compromisso), no palco e na aba:
tracejado e ponto no instante em que o erro volta de vez à faixa, e uma
seta de duas pontas **da eliminação até esse instante**, com o tempo do
cartão (98, 112, 76 ms...). A seta existe porque o retorno é contado de
t_clear (`pico_e_retorno`), e um rótulo solto "98 ms" num eixo que começa
em 0,25 s seria lido como instante. Caso que não retorna fica sem marca.
Desde 2026-10-25 as setas ficam numa faixa própria acima do eixo do erro
(o domínio do eixo desce), fora das curvas. `tccInd.retorno` ([[indicadores-tcc-dashboard]]).

O campo `faixa_err` do capítulo fixa o eixo do erro: ±60° na Localização,
que corta só o salto do 1º ciclo (o TCC já o descarta no pico). O
Compromisso fica em escala automática, porque o pico de 96° é a mensagem;
a Perda de sincronismo segue em ±180°. Eixo fixo leva `ticktext`: sem ele,
o Plotly escreve os ticks com o `hoverformat` (".3f", "60.000").

## Vírgula decimal

Os textos de `tccInd` (cartões do palco e da aba) saem com vírgula
(`_tcc_ind`), como as legendas; a tabela "Todos os casos" troca na hora de
desenhar (`tcc_ui.js`). A tabela comparativa das abas por cenário segue
com ponto.

## Elementos só do palco (2026-10-24)

Pedidos para "enriquecer a apresentação além dos gráficos"; quatro prévias
injetadas no palco real, aprovadas juntas. Configurados em `CAPITULOS`
(`roteiro.py`), sem nada fixo no JS.

- **Passos com frase-mensagem** (`passos_pres`, Energização e Localização): cada passo
  troca o parágrafo da legenda por uma frase grande (`.pres-msg`) e esconde
  os casos de `ocultar`. Passo 1 só a nominal ("40 ms"), passo 2 entra a
  inadequada ("79 ms: quase o dobro"). Indicador de passo no cabeçalho
  (`_passoInd`, 2026-10-25): barra em segmentos que enche até o atual, com
  "k de n" embaixo; o mesmo no mapa de "Faltas destacadas". Escolhido entre
  três prévias (pílulas, segmentos, pílulas + tecla) no lugar do texto
  "passo N de M · seta → avança". `_presPassoReset` devolve os casos à aba ao sair.
  Na Localização (2026-10-24) os passos trocam o painel ao lado: campo
  `lado` do passo, resolvido por `_presLado()` (o do passo, senão o do
  capítulo). Passo 1 mini-mapa e retenção de v_d (9,2% a 58,4%), passo 2
  fasor e pico do erro (37,3° a 7,3°), Tabela 5.1. O usuário não quis
  perder o mini-mapa e recusou os dois empilhados (espremidos em 1280×720).
- **Foco do passo** (`foco=[t0, t1]` no passo, 2026-10-25, `_foco` em
  `tcc.js`): o gráfico fora da janela fica sob um véu branco (72%) e a
  janela ganha contorno pontilhado azul. Escolhido entre três prévias
  (trilha de frases no topo empurrava o gráfico sobre os cartões; balão com
  seta exigia coordenada à mão por passo). Compromisso e Perda de
  sincronismo têm 3 passos: nominal sozinha com foco, entra a inadequada,
  frase-ponte ("E numa falta mais severa?") e fecho ("O ganho que filtrava
  o 120 Hz na Barra 6 é o que perde o sincronismo aqui"). Em capítulo com
  passos, o `destaque` só aparece no passo com `destaque=True`
  (`_capDestaque`). A Perda de sincronismo ficou sem número de destaque desde
  2026-10-28 (o 66,8% de P absorvida saiu do palco a pedido do usuário).
  Estendido no mesmo dia: Energização (foco na partida), Localização
  (foco na falta; passo 3 novo, retorno em até 112 ms no pós-falta) e
  Sequência negativa (refeita em 2026-10-28 em cinco passos, abc → dq →
  espectro: [[palco-sequencia-negativa]]). **O último passo fica sem foco**
  (pedido de 2026-10-25): o capítulo começa no detalhe e fecha com o
  gráfico inteiro, em todos os capítulos com passos.
- **Fasor** (`lado="fasor"`, Energização, Perda de sincronismo e passo 2
  da Localização): círculo
  com a rede (marca preta no topo, cunha verde de ±2°) e um vetor por caso,
  no ângulo do erro de fase. O instante segue o mouse no gráfico
  (`plotly_hover`) e o play percorre a janela do capítulo em 20 s
  (`FASOR_MS`, 20 s desde 2026-10-24: 8 s ficou rápido demais), **sempre a partir do início** (pedido de 2026-10-24: na
  Energização, t = 0, o PLL girando até travar); trocar de capítulo zera
  `fasorT`. Na Energização os passos também valem no fasor (passo 1 só o
  vetor nominal). Cursor vertical cinza tracejado
  (`#fs-cursor`) posicionado por `xaxis.l2p`. Os ângulos vêm de
  `gd._fullData` (os `x`/`y` em `SCENARIOS` estão em base64 e não têm
  `.length`). O fasor não mostra número. Legenda: "PLL nominal/inadequada"
  quando o capítulo mistura sintonias, senão o rótulo do ponto no mapa (B7...).
- **Mini-mapa** (`lado="minimapa"`, Localização): o unifilar de
  `_mapaSvg` (capítulo "Faltas destacadas"), com cada ponto na cor da curva
  e a retenção de v_d (`tccInd.ret`) em grande. As notas pequenas do mapa
  (`.mp-note`) somem; posição dos rótulos em `MINI_ROT`. Clicar no ponto
  ou no número chama `_tccChip` (liga/desliga o caso, como o chip); caso
  desligado fica com opacidade 0,3 e segue clicável (2026-10-24).
- **Número de destaque** (`destaque`): caixa vermelha com o número em 46 px
  sobre o gráfico (`_destaque`, só com `o.big`), com seta até o alvo. "> 250×"
  aponta para o pico de 120 Hz da menor assimétrica. Com `lado=True`, o
  número vai para o painel ao lado, sob o play do fasor (usado pelo "66,8%"
  da perda de sincronismo até 2026-10-28, quando saiu).
- **Notas** (`notas`, 2026-10-24): caixas menores com seta (`_nota`, só com
  `o.big`), para curva que some no gráfico. Na Sequência negativa, a
  trifásica da Barra 7 (0,0002 pu, do cartão) colada no zero em 120 Hz.
- **Estilo por caso** (3º item opcional de `casos`: `dash`, `larg`, `grupo`,
  `frente`; vale para aba e palco). Na Sequência negativa a cor diz a barra
  (laranja = 7, verde-azulado = 6), o traço diz o curto (contínuo = bifásica,
  tracejado = monofásica) e a trifásica vai grafite, grossa e por cima. Com
  `grupo`, os chips saem sob o rótulo "Barra 7"/"Barra 6" (sem o prefixo no
  chip) e os cartões ganham um respiro entre os grupos.
- **Matriz no lugar dos cartões** (`matriz`, 2026-10-24; aba e palco,
  `_tccMatrizHtml`): linhas × colunas de cenário (chave = prefixo da
  linha + "/" + sufixo da coluna), 1ª métrica grande e as outras ao lado, coluna
  `realce` sombreada, clique abre o cenário. Na Sequência negativa: Barra
  7/6 × trifásica/bifásica/monofásica; a trifásica da Barra 6 (0,0011 pu, o
  "maior valor das trifásicas" do texto) entra só na matriz, sem curva,
  porque ficaria sobre a da Barra 7 no zero. Escolhida entre duas prévias
  (a outra: barras horizontais no painel ao lado).

Regra: todo número escrito no palco vem da legenda ou de `tccInd`, que
batem com o TCC ([[defesa-deck-map]]). Nada de número calculado só para a
tela. Os termos também são os do deck e do TCC (revisão de 2026-10-25):
"escorregamento de ciclo", "sintonia nominal" na 1ª menção do capítulo,
nominal antes da inadequada nos pares de números.

## Telas menores que 1920×1080 (2026-10-24)

O palco foi desenhado em 1920×1080, mas o navegador pode enxergar bem
menos: notebook Full HD com escala de 150% no Windows entrega 1280×720, e
projetor espelhado costuma baixar a resolução. Em 1366×768 o
`palco-validator` achou a dica de passo sobre os botões, os rótulos de
retorno sobrepostos, o fasor espremido e a tabela final cortada. Correções:

- Dica "passo N de M" no cabeçalho, ao lado do título, fora da barra de
  capítulos.
- Painel ao lado proporcional: fasor `clamp(340px, 30vw, 430px)`, mini-mapa
  `clamp(320px, 31vw, 600px)`. O SVG do fasor ocupa a altura que sobra.
- `@media (max-height: 900px), (max-width: 1500px)`: cabeçalho, cartões,
  botões e tabela mais compactos; cabeçalho da tabela quebra linha.
- Setas de retorno a 22 px uma da outra (calculado pela altura do painel)
  e casos com o mesmo tempo dividem uma seta só, em cor neutra (B7 e L7-8,
  98 ms).

Em 1920×1080 nada mudou.

## Verificação

`scripts/verifica_palco.py` percorre o palco com a seta em 1920×1080 e
1280×720 (`--telas` muda a lista) e falha em erro de JS, tela que rola,
gráfico sobre o painel ao lado, painel ao lado que transborda, tabela que
não cabe, ← fora do último passo, fasor parado e caso escondido depois de sair do palco
depois de sair. Os PNGs vão para `output/verifica_palco/<L>x<A>/`; quem lê
é o agente `palco-validator`. O JS está
em `src/report/js/` (`tcc.js`, `palco.js`, `fasor.js`, `minimapa.js` etc.,
ordem em `TCC_JS_FILES`), com `node --check` no pre-commit.

## Relacionados

- [[roteiro-demonstracao-dashboard]] — capítulos, casos e cores
- [[indicadores-tcc-dashboard]] — origem dos números (`tccInd`)
- [[palco-codigo-de-rede]] — Código de rede em cinco passos, com fecho
