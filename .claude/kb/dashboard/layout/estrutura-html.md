---
name: estrutura-html
description: Esqueleto do relatório HTML — header, filter-bar, seções, objeto SCENARIOS, fluxo switchScenario e mapa SVG clicável
---

# Estrutura do HTML (renderer.py)

Arquivo único e portátil: Plotly 2.35 via CDN, logo UERJ em base64
([[header-branding]]), CSS em `_css()` (string plana — **chaves simples**),
JS no template f-string (**chaves duplas** `{{}}`). Todo estado por cenário é
pré-computado em Python e embutido no objeto `SCENARIOS`.

## Ordem vertical

1. `header` — título, subtítulo dinâmico (`#header-sub`), badge UERJ, toggle
   de tema.
2. `.filter-bar` — `<select>` de cenário, toggle PLL
   ([[bad-pll-dashboard-filter]], só se houver cenário BAD_PLL), botões:
   🗺 Mapa IEEE 9-bus, 📊 Comparativo, 🔍 Zoom na falta, 👻 Comparar PLL
   ([[dashboard-zoom-ghost]]).
3. `#diagram-section` — SVG unifilar clicável.
4. `#cards-area` / `#story-area` — HTML pré-gerado ([[cards-metricas]]).
5. `#table-section` — comparativo, oculto por padrão ([[comparison-table]]).
6. `#sec-inv` (`#plot-inv`) e `#sec-sys` (`#plot-sys`) — as duas figuras
   Plotly; `#sec-sys` some quando `hasSys` é falso.
7. `.footer`.

## Objeto SCENARIOS

`{key: {invData, sysData, invLight/invDark/invIdx (trace_map), sysLight/…,
label, cardsHtml, storyHtml, metricsRow, hasSys, badPll, tFault, tClear}}`.
`key` = pasta do cenário, ex. `"bus7/3phase"`, `"line7_8/3phase_bad_pll"`.

## Fluxo `switchScenario(key)`

1. `_syncCtrlButtons()` — habilita/desabilita zoom (sem `tFault`) e ghost
   (sem par exato nominal↔bad_pll).
2. `updateFaultUI(sc)` — subtítulo do header + badges "Falta: t = …" das
   seções (ocultos em regime).
3. `reactThemedChart` para inv e sys (re-colore por tema + concatena ghost).
4. `_ensureBridges()` + `_applyZoom()` — sincronização de zoom.
5. Injeta `cardsHtml`/`storyHtml`, `highlightSVG(key)`,
   `renderComparisonTable()`.

Toggles de UI (`toggleDiagram`, `toggleTable`, tema): o label do botão sempre
descreve a **próxima ação** — regra registrada em [[header-branding]].

## Mapa SVG clicável

SVG unifilar embutido (autoral, ver `kb/power-system/ieee9bus_topology.md`).
Na carga, `svgLocMap` agrupa os keys de `SCENARIOS` por local
(prefixo antes da `/`, ex. `bus7`, `line7_8`); elementos do SVG com
`data-loc` correspondente ganham `.has-data` + listener de clique →
`selectLocation(loc, el)` seleciona o cenário daquele local.
`highlightSVG(key)` marca o local da falta ativa com `.svg-active`.

Temas via atributo `data-theme` no `<html>` + CSS vars (`--accent`, cores de
card etc.); o re-tema das figuras Plotly é à parte — [[dark-mode-theming]].
