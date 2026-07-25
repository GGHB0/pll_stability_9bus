---
name: dashboard-html-editor
description: Edita o pipeline Python que gera o relatório HTML interativo (output/pll_metrics.html) — SimData/ChartBuilder/HTMLRenderer em src/. Ativar sempre que o usuário pedir para mudar/adicionar/remover algo no dashboard: cards, métricas, gráficos, abas, tabela comparativa, tema light/dark, toggle PLL, diagrama unifilar, ou qualquer elemento visual/funcional do relatório. Também usar para regenerar e verificar o HTML após qualquer mudança em src/pipeline ou src/report.
version: 1.1.0
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
   - Se a mudança envolve interação clicável (card, botão, toggle), clicar de
     fato e confirmar o efeito — não basta a tela renderizar sem erro no
     console. Se a verificação revelar um bug **não relacionado** à mudança
     atual, não expandir o escopo: registrar via `spawn_task` (chip de
     background) e seguir com a tarefa pedida — foi assim que o bug do
     `goToChart` (xref) foi achado em 2026-07-24, ver `tabs-navegacao.md`.
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
| Redefinir cálculo de métrica existente (ex.: min→média, mudar janela) | `loader.py` (`_compute_metrics`) + toda ocorrência da chave em `renderer.py` (cards, `_table_row_data`, header `data-key`, JS `_cmpCell`, story) e `settings.py` (renomear threshold se o nome antigo não descrever mais o cálculo) | doc(s) do(s) card(s)/coluna(s) afetados |
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
| Remover aba/gráfico inteiro (feature) | `chart.py` (método build), `app.py` (chamada + chaves do dict), `renderer.py` (chaves `SCENARIOS`, HTML da seção, `TIME_TABS`/guards de `switchTab`, ordem do `goToChart`) | doc do gráfico removido + `layout/{estrutura-html,tabs-navegacao}.md` |

(Caminhos de KB relativos a `.claude/kb/dashboard/`.)

## Armadilhas conhecidas

- **`goToChart`/`_label` (chart.py) desde o redesign dos títulos de painel
  (`b2bbb2a`, 2026-07-21)**: os rótulos de painel agora usam
  `xref="paper"`, igual aos subtítulos de grupo (`_group_title`) — o filtro
  antigo em `goToChart` (`xref !== "paper"`) ficou obsoleto e clique em card
  não navega mais até o gráfico. Fix disparado numa sessão de background
  separada em 2026-07-24; se ainda não tiver sido aplicado, qualquer edição
  futura em `_label`/`goToChart`/`_openTabAt` deve resolver isso junto, não
  ignorar. Detalhes em `tabs-navegacao.md`.

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

## Evolução desta skill

v1.0.0 (2026-07-24): criada a partir do padrão observado na remoção das
métricas ΔP/ΔQ e dos emoji dos botões/abas.

v1.1.0 (2026-07-24): adicionada a linha "remover aba/gráfico inteiro" na
tabela (padrão da remoção do `build_resume`); nova seção "Armadilhas
conhecidas" com o bug do `goToChart`/`xref` achado durante a verificação
desta mesma mudança; passo de verificação reforçado para interações
clicáveis, com a regra de não expandir escopo ao achar bugs não
relacionados (usar `spawn_task`).

v1.2.0 (2026-07-25): nova linha "redefinir cálculo de métrica existente" na
tabela — padrão da troca de V min→V médio (mínimo instantâneo virou média
numa janela por regra de cenário), que tocou `loader.py`, `settings.py`
(threshold renomeado) e toda referência à chave antiga em `renderer.py`
(cards, tabela comparativa, JS de ordenação, story) simultaneamente — grepar
o nome da chave/threshold no `src/` inteiro antes de considerar a renomeação
completa, não só nos arquivos "óbvios".

Atualizar a tabela e as convenções conforme novas edições no dashboard
revelarem passos, armadilhas ou arquivos que valha registrar — esta skill
deve crescer com o uso, não ser escrita de uma vez.
