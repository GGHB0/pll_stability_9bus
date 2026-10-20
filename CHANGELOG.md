# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão em
`.claude/kb/dashboard/` (docs separados por dados/graficos/cards/layout).
Entradas antigas: `docs/changelog/` (arquivadas pelo limite de 200 linhas).

## 2026-10-20 — Indicadores do Cap. 5 do TCC no painel

Arquivos: `src/pipeline/indicadores.py` (novo), `src/pipeline/loader.py`,
`src/pipeline/chart.py`, `src/pipeline/spectrum.py`, `src/report/renderer.py`,
`src/config/settings.py`, `src/config/__init__.py`, `src/__init__.py`,
`scripts/medir_tabelas_cap5.py`, `scripts/gen_erro_fase.py`

A defesa passa do slide 14 para o HTML ao vivo, e o painel não batia com o TCC.
O erro de fase era `θ̂ − θ_rede` com faixa ±1,15° (pico de 53,1° contra
37,3° na Barra 7 trifásica, e `bus6/2phase` aparecia como "não acomoda", contra
48 ms no TCC), e faltavam os indicadores das Tabelas 5.1-5.3. Mudanças:

- As receitas do Cap. 5 viraram o módulo `indicadores.py`, usado pelo
  dashboard e pelos scripts do TCC. `tabelas_cap5.csv` regenerado com
  diferença zero.
- O erro de fase passa a ser `atan2(v_q, v_d)` da rede, com faixa de 2°, 1º
  ciclo sombreado e linha quebrada nos saltos de ±180°. `TOL_RAD` foi removido.
- Cards novos: "Sincronismo do SRF-PLL", "Tensão e suporte de reativo" e
  "Energização do inversor" (regime), além do item "Sincronismo" na narrativa.
- A tabela comparativa ganhou 9 colunas das Tabelas 5.1-5.3, geradas de
  `_CMP_COLS`.
- A aba Espectro ganhou um destaque com o 120 Hz pela receita do TCC; a tabela
  de harmônicas, que é outro instrumento, continua igual.
- O cabeçalho passou de "UERJ 2025" para "UERJ 2026".

Detalhes em `.claude/kb/dashboard/cards/indicadores-tcc.md`.

## 2026-10-16 — Plotly embutido no HTML (abre sem internet)

Arquivos: `src/report/renderer.py`, `assets/vendor/plotly-2.35.0.min.js` (novo)

O painel vai ser aberto ao vivo na defesa do TCC, e a sala pode não ter
internet: com o `<script src>` do CDN, os gráficos ficavam em branco. O
`_plotly_js_html` embute o plotly.js 2.35.0 (mesma versão do CDN, 4,5 MB) a
partir de `assets/vendor/`; sem o arquivo, volta ao CDN. O HTML passa de
~68 MB para ~73 MB e também renderiza aberto como `file://`.

## 2026-10-03 — Fix: escala de P e Q do UFV

Arquivos: `src/pipeline/pq.py` (novo), `src/pipeline/loader.py`

O subsistema do `.slx` que calcula P e Q (SID 4055) usava ganho 1/√3 nos
dois: P saía ×√3/2 (0,87 pu pré-falta com i_d = 1) e Q ×1,5. O `.slx` foi
corrigido, mas as rodadas existentes não foram re-simuladas: o `SimData`
passa o CSV por `corrige_pq`, que reescala quando o `fault_info.json` não
traz `pq_ganho_p` (P ×2/√3, Q ×2/3). Os gráficos e métricas de potência do
dashboard mudam de valor, não de forma. Detalhe em
`.claude/kb/simulation/export_workflow.md`.

## 2026-08-18 — Fix: filtro do toggle PLL não aplicado na carga inicial do HTML

Arquivos: `src/report/renderer.py`

Bug reportado pelo usuário: ao abrir o HTML pela primeira vez, com o toggle
"Nominal" ativo, o `<select>` de cenário mostrava (e permitia abrir) todos
os casos de sintonia inadequada (`_bad_pll`) também. Só depois de alternar
manualmente para "Sintonia inadequada" e voltar para "Nominal" é que o
filtro passava a funcionar corretamente.

Causa: o script de inicialização só chamava `switchScenario(currentKey)` no
final da página — nunca `setPllMode(pllMode)`. A filtragem das `<option>`
do `<select>` (`opt.hidden = ...`) só acontece dentro de `setPllMode`, então
nunca rodava na carga inicial, mesmo com a variável `pllMode` já valendo
`"nominal"` e o botão correspondente marcado como ativo.

Fix: trocado `switchScenario(currentKey);` por `setPllMode(pllMode);` na
inicialização (linha final do `<script>`). `setPllMode("nominal")` já
reencontra o cenário equivalente (o próprio `currentKey`, pois os cenários
nominais vêm primeiro na ordenação) e chama `switchScenario` internamente,
então o cenário inicial exibido não muda — só passa a aplicar o filtro do
`<select>` desde o primeiro carregamento.

Verificado no browser pane (via `http.server` local): na carga inicial,
30 opções totais, 22 visíveis, 0 `_bad_pll` visíveis (as 8 corretamente
ocultas). Alternância manual "Sintonia inadequada" ↔ "Nominal" continua
funcionando nos dois sentidos.

## 2026-08-18 — Fix: título do eixo X do espectro FFT sobrepondo painel abaixo

Arquivos: `src/pipeline/spectrum.py`

Bug reportado pelo usuário: no painel de espectro FFT (abc), quando o modo
tem 2 linhas (corrente + tensão), o texto "Frequência (Hz)" do eixo x da
linha de cima (corrente) aparecia sobreposto à barra de título azul da linha
de baixo ("Tensão v̂ₐ UFV (abc)").

Causa: `_apply_layout` setava `title_text="Frequência (Hz)"` via
`fig.update_xaxes(...)` sem filtrar por linha — `shared_xaxes=True` já
esconde os números do eixo de cima, mas não some com o **título** do eixo
(propriedade independente dos ticks), que ficava caindo no vão estreito
reservado só para a barra de título da linha seguinte.

Fix: título em branco no `update_xaxes` geral; "Frequência (Hz)" setado só
no eixo x da última linha (`fig.layout[last_ax].title.text`). Verificado
regenerando os 30 cenários (sem exceptions) e inspecionando
`gd._fullLayout` no browser pane (servido via `python -m http.server`):
`xaxis.title.text === ""` / `xaxis2.title.text === "Frequência (Hz)"` no
modo `a` do cenário `bus4/1phase`; posição das duas barras de título
("Corrente"/"Tensão") sem sobreposição no DOM.

## 2026-08-17 — Aba "Sistema 9-Bus" renomeada para "Barras de Geração"

Arquivos: `src/report/renderer.py`, `src/pipeline/chart.py`

A pedido do usuário. Três ocorrências do rótulo trocadas:

- Botão da `tab-bar` (`#tab-sys`).
- Cabeçalho `.section-title` da seção `#sec-sys`.
- Título do grupo de cards de topologia/severidade na aba Resumo, exibido
  quando o cenário é regime permanente (`sev_label` em `_group_severidade`,
  antes idêntico ao nome da aba) — confirmado com o usuário que também
  deveria mudar, já que reutilizava o mesmo texto.

Comentário de docstring em `chart.py` atualizado por consistência. Nenhuma
mudança de comportamento — só rótulo. Verificado no browser pane (servido
via `python -m http.server`): botão, cabeçalho da seção e grupo de cards do
Resumo (cenário `regime`) todos exibindo "Barras de Geração".

## Entradas anteriores

- [2026-08-11](docs/changelog/2026-08-11.md) — tabela de critérios na legenda
  da tabela de harmônicas; FFT mede a frequência real por segmento (abc).
- [2026-08-09](docs/changelog/2026-08-09.md) — medição de harmônicas pelo
  IEEE 519 §4.1 (3 bins RMS, janela retangular) e relaxamento ×1,5 na falta;
  remoção dos cards de erro de
  ângulo (grupo "Desempenho do PLL": IAE/ISE/tₛ/pico/Erro R.P.), sem base
  bibliográfica que os sustentasse como métrica de desempenho.
- [2026-08-05](docs/changelog/2026-08-05.md) — linha de 0 Hz (fundamental em
  DC) na tabela dq, tabela de harmônicas separada em abc e dq.
- [2026-08-03](docs/changelog/2026-08-03.md) — card e item de diagnóstico
  "Topologia" (line7_8 vs. line8_9, circuito único vs. duplo).
- [2026-08-02](docs/changelog/2026-08-02.md) — teto fixo em 1 pu no eixo Y
  do espectro FFT, legenda explicada da tabela de harmônicas.
- [2026-07-28 a 2026-07-30](docs/changelog/2026-07-28_30.md) — faixa de
  frequência ONS §5.2.1 no painel "Frequência PLL" (depois removido),
  destaque normativo (IEEE 519/1547) na tabela de harmônicas, remoção do
  painel "Frequência PLL".
- [2026-07-25](docs/changelog/2026-07-25.md) — eixo Y com nome+unidade,
  título branco fix, remoção do overlay "Comparar PLL", cards de tensão
  mínimo → média (V médio / V residual médio).
- [2026-07-18 a 2026-07-24](docs/changelog/2026-07-18_24.md) — terminologia
  "sintonia inadequada", remoção dos ícones emoji dos botões/abas, remoção
  das métricas ΔP/ΔQ UFV, cards/diagnóstico movidos para a aba Resumo.
- [2026-07-15](docs/changelog/2026-07-15.md) — espectro FFT multi-modo
  (a/b/c/d/q) + tabela de harmônicas, abas de gráficos + aba Resumo + cards
  clicáveis.
- [2026-07-14](docs/changelog/2026-07-14.md) — regime sem tₛ, cards de
  severidade renomeados para "V residual", Vmin das Barras 1 e 3.
- [2026-07-12](docs/changelog/2026-07-12.md) — export de correntes/tensões
  abc, T_SETTLE fora de todos os cálculos, espectro de Fourier segmentado.
- [2026-07-01 a 2026-07-05](docs/changelog/2026-07-early.md) — reestruturação
  do pacote `src/`, decimação (570 MB → 23,7 MB), tabela comparativa, fixes de
  dark mode, overlays de análise (LVRT, tₛ, frequência PLL), zoom sincronizado,
  reavaliação dos cards e veredito.
