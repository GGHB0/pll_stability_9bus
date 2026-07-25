---
name: dashboard-html-editor
description: Edita o pipeline Python que gera o relatório HTML interativo (output/pll_metrics.html) — SimData/ChartBuilder/HTMLRenderer em src/. Ativar sempre que o usuário pedir para mudar/adicionar/remover algo no dashboard: cards, métricas, gráficos, abas, tabela comparativa, tema light/dark, toggle PLL, diagrama unifilar, ou qualquer elemento visual/funcional do relatório. Também usar para regenerar e verificar o HTML após qualquer mudança em src/pipeline ou src/report.
version: 1.0.0
---

# Dashboard HTML Editor — Skill de Edição do Relatório Interativo

Workflow padronizado para editar `src/pipeline/` e `src/report/renderer.py`
(pipeline `SimData → ChartBuilder/SpectrumBuilder → HTMLRenderer`, orquestrado
por `app.py`, saída `output/pll_metrics.html`). Esta skill é sobre o
**processo** de edição; o conteúdo técnico de cada parte do dashboard vive em
`.claude/kb/dashboard/` — não duplicar aqui.

## Arquitetura em uma frase

`app.py` varre `output/` por cenário, monta `SimData`/`fig_inv`/`fig_sys` e o
`HTMLRenderer` embute tudo (JSON das figuras + JS) num único HTML portátil
(Plotly via CDN); no browser, `switchScenario`/`switchTab` re-renderizam via
`Plotly.react`, sem servidor.

## Workflow padrão

1. **Mapear**: achar o arquivo-fonte certo (tabela abaixo) e o doc de KB
   correspondente via [`.claude/kb/dashboard/index.md`](../../kb/dashboard/index.md).
2. **Plano**: se a mudança não for cosmética/trivial, apresentar o plano e
   **aguardar aprovação explícita** antes de editar.
3. **Editar** o(s) arquivo(s) fonte.
4. **Regenerar**: `.venv\Scripts\python.exe app.py` — deve rodar limpo, sem
   exceptions, para todos os cenários.
5. **Verificar no browser pane** (`mcp__Claude_Browser__*`):
   - `preview_start` com `{url: "file:///<repo>/output/pll_metrics.html"}`
   - screenshot da área afetada; `resize_window` para tema/responsivo
   - `read_page`/`javascript_tool` para conferir headers/valores da tabela
   - `form_input` no `<select>` de cenário se a mudança depender dos dados
6. **Atualizar o KB**: editar o doc correspondente em
   `.claude/kb/dashboard/` (fragmentar se passar 200 linhas — ver
   `.claude/rules/limits.md`).
7. **CHANGELOG**: nova entrada no topo de `CHANGELOG.md` (motivação, arquivos,
   o que mudou — mesmo formato das entradas existentes); se ultrapassar 200
   linhas, arquivar as entradas mais antigas em `docs/changelog/<data>.md`
   antes de adicionar a nova (padrão já usado em `docs/changelog/2026-07-12.md`).
8. **Commit/push**: só quando o usuário pedir explicitamente. Ao stagear,
   listar arquivos explicitamente (nunca `git add -A`/`.`), excluindo
   qualquer mudança não relacionada já presente na working tree.

## Onde mexer para cada tipo de mudança

| Mudança pedida | Arquivo(s) fonte | Doc de KB |
|---|---|---|
| Métrica nova/removida (IAE, ISE, tₛ, ΔX...) | `loader.py` (`_compute_metrics`), `settings.py` (thresholds) | `dados/pipeline-dados.md` |
| Card novo/removido | `renderer.py` (`_cards_html`) | `cards/cards-metricas.md` |
| Coluna da tabela comparativa | `renderer.py` (`_table_row_data` + template JS + header) | `cards/comparison-table.md` |
| Painel de gráfico / subplot | `chart.py` | `graficos/construcao-graficos.md` |
| Overlay (zoom falta, LVRT, marcador tₛ, fantasma) | `chart.py`, `renderer.py` (JS) | `graficos/chart-analysis-overlays.md`, `graficos/dashboard-zoom-ghost.md` |
| Espectro FFT | `spectrum.py` | `graficos/espectro-fourier.md` |
| Aba de navegação | `renderer.py` (tab-bar + `switchTab`) | `layout/tabs-navegacao.md` |
| Tema light/dark | `renderer.py` (`_css`, `toggleTheme`) | `layout/dark-mode-theming.md` |
| Header/branding/botões da filter-bar | `renderer.py` | `layout/header-branding.md`, `layout/estrutura-html.md` |
| Toggle PLL nominal/sintonia inadequada | `renderer.py`, `app.py` | `layout/bad-pll-dashboard-filter.md` |
| Narrativa/veredito (story) | `renderer.py` (`_story_html`) | `cards/cards-metricas.md` |

(Caminhos de KB relativos a `.claude/kb/dashboard/`.)

## Convenções fixas do projeto

- **Sem emoji decorativo** em botões/abas/labels do HTML (removido em
  2026-07-24) — texto puro, sem exceção.
- Decimação de pontos (`_MAX_POINTS` em `chart.py`) evita HTML gigante — não
  remover sem entender o motivo (ficou 570 MB sem ela).
- Nunca commitar `output/pll_metrics.html` (gitignored, gerado em runtime).
- Qualquer `.md` do repo (exceto `README.md`), incluindo os do KB: máx. 200
  linhas — fragmentar proativamente.
- Mudança aprovada sempre ganha entrada no `CHANGELOG.md` **e** atualização
  do doc de KB correspondente — nunca só uma das duas.

## Evolução desta skill

v1.0.0 (2026-07-24): criada a partir do padrão observado na remoção das
métricas ΔP/ΔQ e dos emoji dos botões/abas. Atualizar a tabela e as
convenções conforme novas edições no dashboard revelarem passos, armadilhas
ou arquivos que valha registrar — esta skill deve crescer com o uso, não ser
escrita de uma vez.
