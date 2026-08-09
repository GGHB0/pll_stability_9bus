# KB — Dashboard HTML (output/pll_metrics.html)

Documentação do relatório interativo gerado por `app.py`
(`SimData → ChartBuilder → HTMLRenderer`), separada por parte do dashboard.
Histórico de mudanças por commit: `CHANGELOG.md` na raiz do repo.

## Mapa da pasta

| Pasta | Arquivo | Cobre |
|---|---|---|
| `dados/` | [pipeline-dados.md](dados/pipeline-dados.md) | SimData: CSV, interpolação, métricas na janela pós-falta, frequência PLL, fault_info.json |
| `graficos/` | [construcao-graficos.md](graficos/construcao-graficos.md) | ChartBuilder: subplots, paletas, legendas por eixo, decimação, eixos linkados |
| `graficos/` | [chart-analysis-overlays.md](graficos/chart-analysis-overlays.md) | Janela de falta, hierarquia θ̂ PLL, marcador tₛ, envelope LVRT, painel de frequência |
| `graficos/` | [dashboard-zoom-export.md](graficos/dashboard-zoom-export.md) | Zoom na falta sincronizado, export PNG 3× |
| `graficos/` | [espectro-fourier.md](graficos/espectro-fourier.md) | SpectrumBuilder: FFT segmentada pré-falta/falta/pós-falta no dq, escala dB, marcadores 120 Hz e f_res LCL |
| `cards/` | [cards-metricas.md](cards/cards-metricas.md) | Cards de severidade (V médio, duração, topologia); remoção do grupo de erro de ângulo e do veredito (2026-08-09) |
| `cards/` | [cards-explainer-notebook.md](cards/cards-explainer-notebook.md) | Notebook didático que reimplementa o cálculo de cada card, com verificação cruzada |
| `cards/` | [comparison-table.md](cards/comparison-table.md) | Tabela comparativa de cenários, ordenável, filtrada por modo PLL |
| `layout/` | [estrutura-html.md](layout/estrutura-html.md) | Esqueleto do HTML, filter-bar, SCENARIOS/switchScenario, mapa SVG |
| `layout/` | [tabs-navegacao.md](layout/tabs-navegacao.md) | Abas Resumo (cards+contexto, sem gráfico)/Inversor/Sistema/Espectro, lazy render, cards clicáveis |
| `layout/` | [dark-mode-theming.md](layout/dark-mode-theming.md) | Temas light/dark: themedLayout, Fix 1-3 (annotations/shapes/eixos, gotcha dotted-key) |
| `layout/` | [dark-mode-legend-title-fixes.md](layout/dark-mode-legend-title-fixes.md) | Continuação: Fix 4 (legenda invisível) e Fix 5 (barra de título re-temada por engano) |
| `layout/` | [header-branding.md](layout/header-branding.md) | Logo UERJ base64, regra de label de toggle |
| `layout/` | [bad-pll-dashboard-filter.md](layout/bad-pll-dashboard-filter.md) | Toggle PLL nominal/sintonia inadequada |

## Visão geral do fluxo

1. `app.py` varre `output/` por cenários (CSV + `fault_info.json`), instancia um
   `SimData` por cenário e monta `fig_inv`/`fig_sys` com `ChartBuilder`.
2. `HTMLRenderer` serializa cada figura para JSON (`SCENARIOS` no JS), gera
   cards/story/linha-da-tabela por cenário em Python e embute tudo num único
   HTML portátil (Plotly via CDN, logo em base64).
3. No browser, `switchScenario(key)` re-renderiza tudo client-side via
   `Plotly.react` — sem servidor.

## Regras da casa

- Máx. 200 linhas por `.md` — fragmentar por subtema quando crescer.
- Toda mudança aprovada no dashboard ganha entrada no `CHANGELOG.md` e
  atualização no doc correspondente desta pasta.
- Links `[[nome]]` referenciam o `name:` do frontmatter de outro doc do KB.
