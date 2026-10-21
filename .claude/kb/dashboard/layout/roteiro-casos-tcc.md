---
name: roteiro-demonstracao-dashboard
aliases: [roteiro-demonstracao-dashboard]
description: Casos do Cap. 5 destacados no dashboard (seletor por seção, mapa azul/cinza, comparativo "Só casos do TCC"), aba "Análise TCC" (7 capítulos com cenários sobrepostos) e modo apresentação em tela cheia da defesa — src/report/roteiro.py
---

# Casos do TCC e aba Análise TCC

Motivação (2026-10-20): na defesa, o slide 16 abre o painel ao vivo
([[defesa-deck-map]]). O painel tem 34 cenários, e o TCC discute 17. A banca
precisa ver de cara quais são os do TCC, e a demonstração não pode depender
de achar o cenário certo no `<select>` durante a fala.

## Fonte: `src/report/roteiro.py`

- `TCC_SECOES`: grupos do seletor, na ordem do Cap. 5 (§5.1 Regime
  permanente, §5.2 Faltas simétricas, §5.3 Faltas assimétricas, §5.4 Perda de
  sincronismo). O resto vai para "Outros cenários (fora do TCC)".
- `TCC_CASOS`: caso → seção, na ordem das Tabelas 5.1 a 5.3, conferidos no
  VFinal. Na §5.4 ficam a Barra 7 trifásica inadequada e as trifásicas
  inadequadas da Linha 7-8 (9,7% de retenção) e da Barra 6 (106 ms), que o
  texto usa como contraste.
- Fora do TCC: Barras 4, 5, 8 e 9 (todas as faltas) e Linha 8-9 bifásica.
- `CAPITULOS`: os capítulos da aba "Análise TCC". Cada um tem `id`,
  `curto` (botão), `titulo`, `ref`, `texto` (pode ter `<sub>`), `kind`
  (`time`, `spec`, `ons`, `tabela`), `casos` com cor (light, dark),
  `sinais` (o 1º é o padrão), `xrange` e `metricas` (mini-cartões).

Caso novo no TCC → entrada em `TCC_CASOS`. Número de legenda alterado → ele
tem de bater com o card do mesmo cenário ([[indicadores-tcc-dashboard]]).

## Destaque no seletor, no mapa e no comparativo

- **Seletor**: `<optgroup>` por seção. Com o toggle PLL, grupos sem opção
  visível somem; na sintonia inadequada aparecem §5.1, §5.3 e §5.4.
- **Mapa unifilar**: o JS marca `.tcc-loc` (linha e rótulo em azul) onde
  algum caso do ponto está no TCC e `.svg-extra` (opacidade 0,45) no resto,
  que segue clicável. Legenda abaixo do mapa. É a convenção do slide 13 do
  deck (azul = analisado, cinza = consultável no painel).
- **Comparativo**: etiqueta `§5.x` ao lado do nome, linhas fora do TCC
  esmaecidas e botão "Só casos do TCC". Com o filtro ligado e sem coluna
  escolhida, as linhas seguem a ordem do Cap. 5 (`tccOrd`). Ver
  [[comparison-table]].
- `_locOf(key)` tira o `_bad_pll` antes do `split`: `regime_bad_pll` passou
  a acender o título do mapa, o que antes não acontecia.

## Aba "Análise TCC"

Histórico: em 2026-10-20 a demonstração começou como uma faixa de 9 passos
sobre as abas por cenário (commit `d1a8e8c`). No mesmo dia virou esta aba,
a pedido do usuário, para comparar os cenários num painel só.

A aba é a primeira e a página abre nela. Cada capítulo sobrepõe no mesmo
eixo os cenários que o TCC compara: azul = nominal, laranja = inadequada,
e na localização um degradê de azul do mais perto ao mais longe da usina.

| # | Capítulo | Casos | Gráfico |
|---|---|---|---|
| 1 | Energização | regime × regime inadequada | erro de fase / v_d (0-0,2 s) |
| 2 | Localização | 4 trifásicas nominais | erro / v_d / P |
| 3 | Perda de sincronismo | B7 trifásica nas duas sintonias | erro (±180° fixo) / P / Q / v_d |
| 4 | Sequência negativa | 4 assimétricas + B7 trifásica (cinza) | espectro de v_d na falta |
| 5 | Compromisso da sintonia | B6 bifásica nas duas sintonias | erro / v_d |
| 6 | Código de rede | 4 trifásicas | rampa ONS (i_q × V) com o ponto de cada caso |
| 7 | Todos os casos | 17 casos do TCC | tabela (colunas do comparativo) |

- As curvas vêm das figuras já embutidas em `SCENARIOS` (traço "Erro de
  fase", "V<sub>d</sub> Rede", "P UFV", "Q UFV" do Inversor; "Durante a
  falta" em `y2` do espectro dq). O HTML não cresce.
- Os chips ligam e desligam cenários e fazem de legenda (a do Plotly fica
  oculta). "+ comparar com…" acrescenta qualquer cenário, em linha
  pontilhada.
- Os mini-cartões vêm de `tccInd` (`_tcc_ind` no renderer, mesmas receitas
  dos cards). Clicar abre o cenário na aba Inversor.
- Na aba, o cabeçalho diz "Análise comparativa", o seletor e o toggle PLL
  ficam esmaecidos e o "Zoom na falta" some.
- Teclas, só com a aba ativa e fora de `<select>`: seta → ou PageDown
  avança, seta ← ou PageUp volta (um passador de slides funciona).
- O JS mora em `_TCC_JS`, uma string comum no fim do `renderer.py`, e entra
  no f-string do HTML por `{tcc_js}`, sem precisar dobrar chaves.

Os números das legendas foram conferidos contra os mini-cartões no Edge
headless (Playwright em venv descartável), nos 7 capítulos, sem erro de JS.

## Modo apresentação

Botão "Modo apresentação" no cabeçalho, pedido em 2026-10-20 para dar
imersão e caber tudo na tela. O site inteiro vira um palco branco em tela
cheia (`#pres`, `position: fixed`, `requestFullscreen`), um capítulo por
tela, sem rolagem: número do capítulo, legenda, chips, gráfico ocupando a
altura que sobra, faixa de mini-cartões e os botões dos capítulos embaixo.

- Os sinais de `cap.pres` ficam empilhados num só gráfico, com o mesmo eixo
  x (o zoom vale para todos): erro de fase + v_d na energização, na
  localização e no compromisso; erro de fase + P na perda de sincronismo.
- O tema claro é fixo no palco, independente do botão "Dark mode": as
  variáveis CSS são redefinidas dentro de `.pres` e a figura sai com
  `dark: false` sobre fundo branco. A primeira versão era escura; o usuário
  não gostou e escolheu, entre três prévias claras (branco puro, cinza com
  cartões, faixa azul-marinho no topo como o deck), o branco puro. O claro
  também resiste melhor ao projetor numa sala iluminada.
- Os chips e cartões reaproveitam as classes da aba.
- Seta ou PageDown avança, Esc sai. Com a tela cheia, o navegador consome o
  Esc, e quem fecha o modo é o `fullscreenchange`. O capítulo é o mesmo da
  aba (`tccCap`), e clicar num cartão sai do palco e abre o cenário.
- `_tccFigure(cap, sinais, o)` monta a figura nos dois casos (aba com um
  sinal, palco com vários), e `_renderPres` mede a altura do `#pres-plot`
  e redesenha no `resize`.

Na mesma rodada:

- **Capítulo do ONS** trocado de barras (três coladas em 1 pu) pela rampa
  do Submódulo 2.10 (i_q contra V) com o ponto de operação de cada trifásica
  (V médio, i_q,ref médio). Mostra onde cada caso cai na curva e a Barra 6
  um pouco abaixo dela.
- **Cores dos capítulos só com casos nominais**: escala amarelo → verde →
  ciano → índigo, do mais perto ao mais longe da usina. Os tons de azul se
  confundiam no fundo escuro e seguem distintos no branco.
- **Rótulo do mouse**: "x unified" com fundo sólido, borda azul, fonte 13 e
  3 casas decimais, também nas abas por cenário (`themedLayout`).

Conferido no Edge headless em 1920×1080: os 7 capítulos cabem na tela
(`scrollHeight` = altura da janela) e não houve erro de JS.

## `goToChart` consertado junto

A faixa de passos rolava até o painel com a mesma rotina dos cards clicáveis, que
estava quebrada desde 2026-07-24 ([[tabs-navegacao]]). `_panelFrac` acha a
barra de título pelo texto e usa o `y` dela (`yref="paper"`), e
`_openTabAt` desconta as margens da figura.

## Relacionados

- [[bad-pll-dashboard-filter]]: o toggle PLL, que o clique num mini-cartão
  aciona por `_applyPllFilter`
- [[tcc-revisao-fragmento-cap5-metricas]]: os números das tabelas do Cap. 5
