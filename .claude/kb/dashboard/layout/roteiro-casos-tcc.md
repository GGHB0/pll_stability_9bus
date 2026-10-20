---
name: roteiro-demonstracao-dashboard
aliases: [roteiro-demonstracao-dashboard]
description: Casos do Cap. 5 destacados no dashboard (seletor por seção, mapa azul/cinza, comparativo "Só casos do TCC") e modo roteiro da demonstração da defesa (9 passos, seta/PageDown) — src/report/roteiro.py
---

# Casos do TCC e modo roteiro

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
- `ROTEIRO`: os passos da demonstração. Cada um tem `key`, `tab`, `zoom`,
  `panel` (fragmento do título do painel), `phase` (eixo do espectro),
  `table` (comparativo filtrado), `titulo` e `texto` (a legenda).

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

## Modo roteiro

Botão "Roteiro" na filter-bar. Abre uma faixa (dentro da filter-bar, então
fica fixa no topo) com ‹ n/9 › e a legenda do passo. Teclas, só com o modo
ligado e fora do `<select>`: seta → ou PageDown avança, seta ← ou PageUp
volta, Esc sai. Um passador de slides manda PageDown/PageUp.

`_rtApply(i)` aplica o passo sem renderizar duas vezes: `_applyPllFilter`
(o filtro do toggle sem trocar de cenário), depois `specPhase`, `zoomFault`
e `activeTab`, e só então `switchScenario`. O comparativo aparece só no
passo `table` e a rolagem vai ao painel pedido por `_panelFrac` +
`_openTabAt`.

| # | Cenário | Aba | O que a legenda diz |
|---|---|---|---|
| 1 | Regime | Inversor | trava em 40 ms; inadequada em 79 ms |
| 2 | B7 trifásica | Inversor, zoom | 9,2%; 37,3°; 98 ms |
| 3 | B6 trifásica | Inversor, zoom | 58,4%; 7,3°; 76 ms |
| 4 | B7 trifásica inadequada | Inversor, zoom | 8,2%; ±180° contínuo |
| 5 | idem, painel P/Q | Inversor, zoom | absorve P em 66,8% do pós-falta |
| 6 | B6 bifásica | Espectro, eixo d | 0,39 pu × 0,0011 pu das trifásicas |
| 7 | B6 bifásica | Inversor, zoom | 96,0°; 48 ms |
| 8 | B6 bifásica inadequada | Inversor, zoom | 34,5°; 30 ms |
| 9 | B7 trifásica | Resumo + comparativo | casos do TCC |

As legendas dizem "durante a falta" no pico: no passo 8 o transitório da
eliminação desce a cerca de −100°, fora da janela do pico.

Conferido em 2026-10-20 no Edge headless (Playwright em venv descartável):
os 9 passos sem erro de JS, os números das legendas iguais aos cards, o modo
dark, Esc e a ordem do comparativo.

## `goToChart` consertado junto

O roteiro rola até o painel com a mesma rotina dos cards clicáveis, que
estava quebrada desde 2026-07-24 ([[tabs-navegacao]]). `_panelFrac` acha a
barra de título pelo texto e usa o `y` dela (`yref="paper"`), e
`_openTabAt` desconta as margens da figura.

## Relacionados

- [[bad-pll-dashboard-filter]]: o toggle PLL, que o roteiro aciona por
  `_applyPllFilter`
- [[tcc-revisao-fragmento-cap5-metricas]]: os números das tabelas do Cap. 5
