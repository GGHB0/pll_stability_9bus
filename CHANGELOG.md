# Changelog — Dashboard HTML (src/)

Registro das alterações no pipeline Python e no relatório `output/pll_metrics.html`,
para revisão posterior. Detalhes técnicos de cada item estão nos patterns do KB
(`.claude/kb/python/patterns/`).

## 2026-07-05 — Zoom na falta em todos os painéis

Arquivo: `src/report/renderer.py`

- **Fix**: o zoom só alcançava a cadeia de eixos da coluna 1 — os painéis
  pareados P/Q Bus 1/3 (coluna 2 da seção Sistema 9-Bus) têm cadeia de
  `matches` própria e não zoomavam. `_zoomUpd()` agora varre todas as chaves
  `xaxis*` do layout de cada figura.

## 2026-07-05 — Overlays de análise e controles novos (`bc428d7`)

Arquivos: `src/pipeline/loader.py`, `src/pipeline/chart.py`, `src/report/renderer.py`

### Novos recursos de análise
- **Painel "Frequência PLL (Hz)"**: `SimData._estimate_freq()` calcula
  `f̂ = dθ̂/dt / 2π` por diferença central com janela ~1 ms sobre o eixo rápido.
  Novos atributos: `f_pll`, `t_freq`, flag `has_freq`. Hline de 60 Hz no painel.
- **Envelope LVRT IEEE 1547-2018 Cat II** no painel |V| Bus 2: curva degrau V×t
  ancorada em `t_fault` (0.30 pu/0.16 s → 0.45/0.32 s → 0.65/3 s → 0.88 contínuo).
  Substitui a hline fixa de `LVRT_THRESHOLD` (mantida em Bus 1/3 e em regime).
- **Marcador de tₛ** no gráfico de erro de fase: diamante verde no instante de
  acomodação + banda de tolerância ±1.15° sombreada em verde translúcido.

### Melhorias de visualização
- **Janela de falta em destaque**: faixa vermelha translúcida entre
  `t_fault`/`t_clear` + vlines mais grossas (2.0) — vermelha no início da falta,
  verde na limpeza (era cinza fina).
- **Hierarquia no painel de ângulo**: θ̂ PLL agora é sólido, largura 2.4 e
  primeira cor da paleta; θ Rede fino e tracejado (antes era o inverso).

### Controles novos na filter-bar
- **🔍 Zoom na falta**: enquadra o eixo X de todos os subplots em
  `[t_fault−0.1, t_clear+0.5]`; persiste entre cenários/temas; desabilita em regime.
- **👻 Comparar PLL**: sobrepõe o cenário BAD_PLL equivalente como fantasma
  pontilhado (mesma cor, opacidade 0.5); desabilita quando não há par exato.
- **Export PNG 3×**: botão de câmera do modebar exporta em alta resolução com
  filename por cenário/seção (era SVG sem nome).

### Correção
- **Re-tema de shapes repintava linhas semânticas de cinza**: o `themedLayout`
  repintava TODAS as shapes (incluindo vlines de falta, hlines LVRT e bandas)
  com a cor da divisória de grupo, a cada troca de tema ou cenário, nos dois
  temas. Agora só shapes com `xref === "paper"` são re-temadas.
  Ver `kb/python/patterns/dark-mode-theming.md` (Fix 3).

## 2026-07-05 — Remoção do símbolo φ do header (`8b24f47`)

- Removido o quadrado roxo com "φ" do header (`<div class="h-logo">` + bloco CSS);
  o logo da UERJ passou a ser a única marca visual, ao lado do título.

## 2026-07-05 — Fix real do dark mode (`6af6e3e`)

- **Causa raiz**: `themedLayout` construía chaves flat `"xaxis.gridcolor"`
  (dotted string) que `Plotly.react` ignora silenciosamente — gridlines nunca
  foram re-temadas e ficavam quase brancas sobre fundo escuro. Corrigido
  aninhando o objeto do eixo (`axUpd[k] = Object.assign({}, layout[k], {...})`).
- `plot_bgcolor` do dark mode clareado para `#1a2436` (antes idêntico ao card),
  com grid `#31425c` e zeroline `#4b5d7a` recalibrados.
  Ver `kb/python/patterns/dark-mode-theming.md` (Fix 2).

## 2026-07-05 — Contraste de rótulos no dark mode (`7626d19`)

- Annotations (`_label`, `_group_title`) e shape divisória re-temadas por tema
  via `xref` como discriminador (cores fixas do `chart.py` não herdam do layout).

## 2026-07-05 — Logo UERJ no header (`45ff9c7`)

- `_uerj_logo_html()`: embute `assets/uerj.png` como base64 (HTML segue
  portátil); degrada silenciosamente se o arquivo não existir.

## 2026-07-05 — Label do toggle de mapa (`0d2541c`)

- Corrigido ternário invertido em `toggleDiagram()`; regra adotada: o label de
  um botão toggle descreve sempre a **próxima ação**, nunca o estado atual.

## 2026-07-05 — Decimação + tabela comparativa (`46f08c3`)

- Decimação de traces (`_MAX_POINTS = 5000` por trace) em `chart.py`:
  HTML caiu de ~570 MB para ~23,7 MB.
- Seção "Comparativo de cenários": tabela ordenável com IAE/ISE/tₛ/ΔP/ΔQ/Vmin
  por cenário, filtrada pelo modo PLL, clique na linha troca o cenário.

## 2026-07-01 — Reestruturação do pacote (`1d19283` … `992e4e3`)

- `src/` dividido em `config/` (settings), `pipeline/` (loader, chart) e
  `report/` (renderer); entry point `app.py`.
- Linhas de falta dinâmicas por cenário lendo `fault_info.json` (t_fault/t_clear
  reais exportados pelo MATLAB); base de normalização de P/Q de barra corrigida
  para MVA.
