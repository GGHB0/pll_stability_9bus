---
name: tabs-navegacao
description: Abas de gráficos (Resumo/Inversor/Sistema/Espectro), render preguiçoso com flags dirty e cards clicáveis (goToChart)
---

# Abas de gráficos e navegação (renderer.py)

Desde 2026-07-15 as seções de gráficos não são mais empilhadas: uma
`.tab-bar` alterna 4 painéis (`.chart-section`):

| Aba | id | Conteúdo | Disponibilidade |
|---|---|---|---|
| Resumo | `sec-res` | `#cards-area` + `#story-area` (sem gráfico) | `hasRes` (sempre true) |
| Inversor UFV | `sec-inv` | `fig_inv` | `hasInv` (sempre true) |
| Barras de Geração | `sec-sys` | `fig_sys` | `hasSys` |
| Espectro FFT | `sec-spec` | `fig_spec` ([[espectro-fourier]]) | `hasSpec` |

> Desde 2026-07-24 a aba Resumo **não tem gráfico próprio** — `build_resume`
> foi removido (duplicava painéis já presentes em Inversor/Sistema e o
> usuário achou repetitivo). Cards+diagnóstico, que antes ficavam soltos
> acima da tab-bar (visíveis em toda aba), moraram para dentro de `sec-res`
> e só aparecem quando essa aba está ativa.

Estado JS: `TABS = ["res","inv","sys","spec"]`, mapas `gd/secEl/tabBtn/badgeEl`
indexados pelo nome curto, `HASKEY` traduz aba → flag do `SCENARIOS`.
As chaves do `SCENARIOS` seguem o padrão `{t}Data/{t}Light/{t}Dark/{t}Idx`
para `t ∈ {inv, sys, spec}` — `res` não tem essas chaves (sem figura).
`switchTab` tem guard explícito (`which !== "res"`) para nunca chamar
`_renderChart`/`_ensureBridges`/`_applyZoom` na aba Resumo.

## Render preguiçoso (`_dirty`)

- `_dirty[t] = true` marca que o gráfico precisa de `Plotly.react`.
- `switchScenario` e `toggleTheme` sujam TODOS e renderizam só a aba ativa
  (`_renderChart(activeTab)`).
- `switchTab(which)` renderiza sob demanda se a aba estiver suja e então
  reaplica pontes (`_ensureBridges`) e zoom (`_applyZoom`).
- Se a aba pedida não existe no cenário, `switchTab` cai para a 1ª
  disponível (guard no topo da função).
- Resultado: 1 `Plotly.react` por interação em vez de 3 — o ganho de
  performance que motivou as abas.

## Zoom entre abas

`TIME_TABS = ["inv","sys"]` (res não tem gráfico; spec fora — eixo x em Hz). Tanto o
`_applyZoom` (botão "Zoom na falta") quanto a ponte de zoom manual
(`_bridgeZoom`, genérica por aba) só tocam gráficos `_plotted(t)` =
div com `.data` e não-sujo. Gráfico sujo renderiza do zero ao abrir a
aba e recebe o zoom vigente logo em seguida via `_applyZoom` — zoom
manual (arrasto) não persiste para abas sujas, só o de botão.

## Cards clicáveis (`goToChart`)

`_card(..., target="rótulo")` no Python adiciona classe `.clickable` +
`onclick="goToChart('rótulo')"`. O rótulo é um fragmento do texto da
annotation de painel gerada pelo `_label` do chart.py:

- V residual B1/B2/B3 → `"|V| Bus 1/2/3"`
- Duração / Topologia → sem target (não clicáveis)

Os cards que apontavam para `"Erro de fase"` (IAE, ISE, tₛ, \|θ_err\| pico,
Erro R.P.) foram removidos em 2026-08-09 — ver [[cards-metricas]]. Hoje só os
cards de tensão são clicáveis.

`goToChart` varre as figuras na ordem **inv → sys** (res saiu da busca em
2026-07-24 — não tem mais figura), acha a primeira annotation (não-`paper`)
contendo o fragmento, abre a aba e rola até o painel: `_openTabAt` converte
o `yref` da annotation em `yaxisN`, lê o `domain` do layout (estático,
pré-computado no Python) e calcula o y do scroll descontando header +
filter-bar sticky.

⚠️ Gotchas do `_openTabAt`:
- `setTimeout(…, 60)` em vez de `requestAnimationFrame` — rAF não dispara
  com a aba do browser em segundo plano (descoberto no Claude Preview).
- `document.scrollingElement.scrollTo({behavior:"smooth"})` em vez de
  `window.scrollTo` (que era no-op no ambiente de preview).
- ⚠️ **Bug conhecido (desde b2bbb2a, 2026-07-24)**: o redesign dos títulos
  de painel (barra preenchida) fez `_label` em `chart.py` passar a usar
  `xref="paper"` também para a annotation do rótulo (antes era
  `"x/y domain"`). O filtro `anns[j].xref !== "paper"` em `goToChart` ficou
  obsoleto — nunca mais casa nada, então clique em card não navega mais.
  Fix sugerido: filtrar por `yref` (`"paper"` = rótulo de painel,
  `"y... domain"` = `_group_title`) e usar o `y` da própria annotation
  como fração de scroll, em vez de resolver via domain do yaxis.

## Badges de falta

`updateFaultUI` itera `TABS` e preenche `badgeEl[t]` (null no spec, que tem
`.spec-hint` fixo no lugar). Ver [[estrutura-html]] para a ordem vertical
completa da página.
