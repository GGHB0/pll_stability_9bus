---
name: dashboard-html-editor
description: Edita o pipeline Python que gera o relatório HTML interativo (output/pll_metrics.html) — SimData/ChartBuilder/HTMLRenderer em src/. Ativar sempre que o usuário pedir para mudar/adicionar/remover algo no dashboard: cards, métricas, gráficos, abas, tabela comparativa, tema light/dark, toggle PLL, diagrama unifilar, ou qualquer elemento visual/funcional do relatório. Também usar para regenerar e verificar o HTML após qualquer mudança em src/pipeline ou src/report.
version: 1.6.0
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
(Plotly embutido de `assets/vendor/` desde 2026-10-16); no browser, `switchScenario`/`switchTab` re-renderizam via
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
   - `preview_start` com `{url: "file:///<repo>/output/pll_metrics.html"}` —
     se `Plotly` não carregar (ver Armadilhas conhecidas), servir
     `output/` via `python -m http.server <porta>` (Bash `run_in_background`)
     e navegar para `http://localhost:<porta>/pll_metrics.html`.
   - screenshot da área afetada; `resize_window` para tema/responsivo
   - `read_page`/`javascript_tool` para conferir headers/valores da tabela
   - `form_input` no `<select>` de cenário se a mudança depender dos dados
   - Se a mudança envolve interação clicável (card, botão, toggle), clicar de
     fato e confirmar o efeito — não basta a tela renderizar sem erro no
     console. Se a verificação revelar um bug **não relacionado** à mudança
     atual, não expandir o escopo: registrar via `spawn_task` (chip de
     background) e seguir com a tarefa pedida — foi assim que o bug do
     `goToChart` (xref) foi achado em 2026-07-24, ver `tabs-navegacao.md`.
6. **Atualizar o KB**: editar o doc correspondente em
   `.claude/kb/dashboard/` (fragmentar se passar 200 linhas — ver
   `.claude/rules/limits.md`). Doc novo: `[[slug]]` para pelo menos um tema,
   linha no `kb/dashboard/index.md` e `scripts/kb_links.py all` (ver
   `.claude/rules/kb-links.md`).
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
| Redefinir cálculo de métrica existente (ex.: min→média, mudar janela) | `loader.py` (`_compute_metrics`) + toda ocorrência da chave em `renderer.py` (cards, `_table_row_data`, header `data-key`, JS `_cmpCell`, story) e `settings.py` (renomear threshold se o nome antigo não descrever mais o cálculo) | doc(s) do(s) card(s)/coluna(s) afetados |
| Card novo/removido | `renderer.py` (`_cards_html`) | `cards/cards-metricas.md` |
| Coluna da tabela comparativa | `renderer.py` (`_table_row_data` + template JS + header) | `cards/comparison-table.md` |
| Painel de gráfico / subplot | `chart.py` | `graficos/construcao-graficos.md` |
| Overlay (zoom falta, LVRT, marcador tₛ) | `chart.py`, `renderer.py` (JS) | `graficos/chart-analysis-overlays.md`, `graficos/dashboard-zoom-export.md` |
| Espectro FFT | `spectrum.py` | `graficos/espectro-fourier.md` |
| Aba de navegação | `renderer.py` (tab-bar + `switchTab`) | `layout/tabs-navegacao.md` |
| Tema light/dark | `renderer.py` (`_css`, `toggleTheme`) | `layout/dark-mode-theming.md` |
| Header/branding/botões da filter-bar | `renderer.py` | `layout/header-branding.md`, `layout/estrutura-html.md` |
| Toggle PLL nominal/sintonia inadequada | `renderer.py`, `app.py` | `layout/bad-pll-dashboard-filter.md` |
| Casos do TCC, capítulos da aba Análise TCC | `roteiro.py` (`TCC_CASOS`, `CAPITULOS`), `_TCC_JS` no `renderer.py` | `layout/roteiro-casos-tcc.md` |
| Narrativa/veredito (story) | `renderer.py` (`_story_html`) | `cards/cards-metricas.md` |
| Remover aba/gráfico inteiro (feature) | `chart.py` (método build), `app.py` (chamada + chaves do dict), `renderer.py` (chaves `SCENARIOS`, HTML da seção, `TIME_TABS`/guards de `switchTab`, ordem do `goToChart`) | doc do gráfico removido + `layout/{estrutura-html,tabs-navegacao}.md` |

(Caminhos de KB relativos a `.claude/kb/dashboard/`.)

## Armadilhas conhecidas

- **`goToChart` corrigido em 2026-10-20** (quebrado desde `b2bbb2a`): a
  barra de título do painel tem `xref`/`yref="paper"`; `_panelFrac` acha
  pelo texto e usa o `y` dela. Painel novo deve manter a barra via `_label`
  para cards e roteiro acharem. Detalhes em `tabs-navegacao.md`.

- **Sem browser pane, verificar com Edge headless**: Playwright num venv
  descartável do scratchpad, `chromium.launch(channel="msedge")` (não baixa
  browser), abrir o HTML como `file://`, avaliar JS e tirar screenshots.
  Usado em 2026-10-20 para percorrer a aba Análise TCC.
- **Pedido de gosto visual (tema, cores) → prévias antes de editar**: no
  mesmo Playwright, injetar CSS (`page.add_style_tag`) e sobrescrever a
  função de render via `page.evaluate` sobre o HTML já gerado; 2-4 variantes
  em PNG, o código só muda depois da escolha. Assim saiu o palco branco do
  modo apresentação (2026-10-20, após o escuro ser recusado).

- **Elemento novo de visual indefinido → prévia standalone** antes de
  editar `src/`: ver [previa-standalone.md](previa-standalone.md).
- Até 2026-10-16, o Plotly via CDN não carregava em `file://` no browser
  pane. Com o Plotly embutido, `file://` renderiza (detalhe em
  [historico.md](historico.md), v1.5.0).

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
- **Aba Resumo é cards + diagnóstico, sem gráfico** (desde 2026-07-24) —
  não reintroduzir uma figura ali sem que o usuário peça; era repetitivo
  com Inversor/Sistema e foi removido por esse motivo.

## Guias e histórico

- [previa-standalone.md](previa-standalone.md): elemento novo de visual
  indefinido (capítulo do palco, diagrama) prototipado num HTML do
  scratchpad, com PNG por passo no Edge headless, antes de tocar em `src/`.
- [historico.md](historico.md): versões v1.0.0 a v1.6.0 e a lição de cada
  rodada. Versão nova ganha entrada lá, não aqui.

Atualizar a tabela e as convenções conforme novas edições no dashboard
revelarem passos, armadilhas ou arquivos que valha registrar.
