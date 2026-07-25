---
name: tabs-navegacao
description: Abas de gráficos (Resumo/Inversor/Sistema/Espectro), render preguiçoso com flags dirty e cards clicáveis (goToChart)
---

# Abas de gráficos e navegação (renderer.py)

Desde 2026-07-15 as seções de gráficos não são mais empilhadas: uma
`.tab-bar` logo após `#story-area` alterna 4 painéis (`.chart-section`):

| Aba | id | Conteúdo | Disponibilidade |
|---|---|---|---|
| Resumo | `sec-res` | `fig_res` — painéis essenciais ([[construcao-graficos]]) | `hasRes` |
| Inversor UFV | `sec-inv` | `fig_inv` | `hasInv` (sempre true) |
| Sistema 9-Bus | `sec-sys` | `fig_sys` | `hasSys` |
| Espectro FFT | `sec-spec` | `fig_spec` ([[espectro-fourier]]) | `hasSpec` |

Estado JS: `TABS = ["res","inv","sys","spec"]`, mapas `gd/secEl/tabBtn/badgeEl`
indexados pelo nome curto, `HASKEY` traduz aba → flag do `SCENARIOS`.
As chaves do `SCENARIOS` seguem o padrão `{t}Data/{t}Light/{t}Dark/{t}Idx`,
o que permite acesso genérico `sc[which + "Data"]` (também usado pelo ghost).

## Render preguiçoso (`_dirty`)

- `_dirty[t] = true` marca que o gráfico precisa de `Plotly.react`.
- `switchScenario` e `toggleTheme` sujam TODOS e renderizam só a aba ativa
  (`_renderChart(activeTab)`); `toggleGhost` reusa `switchScenario`.
- `switchTab(which)` renderiza sob demanda se a aba estiver suja e então
  reaplica pontes (`_ensureBridges`) e zoom (`_applyZoom`).
- Se a aba pedida não existe no cenário, `switchTab` cai para a 1ª
  disponível (guard no topo da função).
- Resultado: 1 `Plotly.react` por interação em vez de 3 — o ganho de
  performance que motivou as abas.

## Zoom entre abas

`TIME_TABS = ["res","inv","sys"]` (spec fora — eixo x em Hz). Tanto o
`_applyZoom` (botão "Zoom na falta") quanto a ponte de zoom manual
(`_bridgeZoom`, genérica por aba) só tocam gráficos `_plotted(t)` =
div com `.data` e não-sujo. Gráfico sujo renderiza do zero ao abrir a
aba e recebe o zoom vigente logo em seguida via `_applyZoom` — zoom
manual (arrasto) não persiste para abas sujas, só o de botão.

## Cards clicáveis (`goToChart`)

`_card(..., target="rótulo")` no Python adiciona classe `.clickable` +
`onclick="goToChart('rótulo')"`. O rótulo é um fragmento do texto da
annotation de painel gerada pelo `_label` do chart.py:

- IAE / ISE / tₛ / pico → `"Erro de fase"`
- V residual B1/B2/B3 → `"|V| Bus 1/2/3"`
- Duração → sem target (não clicável)

`goToChart` varre as figuras na ordem **res → inv → sys**, acha a primeira
annotation com `yref === "paper"` (rótulo de painel, gerado por `_label` em
chart.py) contendo o fragmento, abre a aba e rola até o painel: `_openTabAt`
usa diretamente o `y` (fração de paper) já gravado nessa annotation como
alvo do scroll, descontando header + filter-bar sticky.

Títulos de grupo (`_group_title`) usam `yref` tipo `"y domain"`/`"y3 domain"`
(contém `"domain"`) e ficam fora do filtro — só rótulos de painel têm
`yref === "paper"`.

⚠️ Bug histórico (commit `b2bbb2a`, corrigido em 2026-07-24): antes do
redesign dos títulos como barra preenchida, rótulos de painel usavam
`xref`/`yref` por eixo (`"x domain"`/`"y3 domain"`) e só os títulos de grupo
usavam `xref="paper"` — daí o filtro original ser `xref !== "paper"`. O
redesign passou os rótulos de painel também para `xref="paper", yref="paper"`,
então o filtro antigo excluía *toda* annotation e `goToChart` não fazia nada
ao clicar num card. Um segundo problema: mesmo corrigindo o filtro, o
`_openTabAt` antigo tentava extrair `yaxisN` do `yref` via regex `/^y(\d*)/`,
que não bate com `"paper"` — sempre caía em `yaxis` (linha 1). A correção usa
o `y` da própria annotation em vez de redescobrir o domínio do eixo.

⚠️ Gotchas do `_openTabAt`:
- `setTimeout(…, 60)` em vez de `requestAnimationFrame` — rAF não dispara
  com a aba do browser em segundo plano (descoberto no Claude Preview).
- `document.scrollingElement.scrollTo({behavior:"smooth"})` em vez de
  `window.scrollTo` (que era no-op no ambiente de preview).

## Badges de falta

`updateFaultUI` itera `TABS` e preenche `badgeEl[t]` (null no spec, que tem
`.spec-hint` fixo no lugar). Ver [[estrutura-html]] para a ordem vertical
completa da página.
