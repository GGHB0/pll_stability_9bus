---
name: construcao-graficos
description: ChartBuilder (chart.py) — subplots por seção, linhas single/pair, legendas por eixo, decimação, paletas e eixos X linkados
---

# Construção dos Gráficos (src/pipeline/chart.py)

`ChartBuilder(data).build_sections()` → `(fig_inv, fig_sys, tm_inv, tm_sys)`.
`fig_sys = None` quando o cenário não tem sinais de sistema.

`ChartBuilder(data).build_resume()` → `(fig_res, tm_res)` — figura da aba
Resumo ([[tabs-navegacao]]): `_res_rows()` = erro de fase, frequência PLL,
P/Q UFV e |V| Bus 2, reusando os mesmos kinds/overlays das seções completas.
Como duplica traces já presentes em inv/sys, usa decimação mais agressiva
(`_RES_MAX_POINTS = 2000` via `self._max_points`). Retorna `None` com menos
de 2 painéis disponíveis.

## Linhas: single vs pair

Cada figura é um `make_subplots(rows=n, cols=2, shared_xaxes=True)`. Uma linha
é declarada como tupla:

- `(_S, kind, label[, grupo])` — painel de linha inteira (`colspan 2`);
- `(_P, (k1, l1), (k2, l2)[, grupo])` — dois painéis lado a lado (P/Q de barra).

`_inv_rows()` monta a seção Inversor (ang, err, freq, dq, vdq, P/Q UFV) e
`_sys_rows()` a seção Sistema (|V| e P/Q das barras 1/2/3) — cada painel só
entra se a flag `has_*` do [[pipeline-dados]] estiver ligada. O 4º elemento
opcional (`"Barra N"`) vira subtítulo de grupo (`_group_title`, annotation com
`xref="paper"` + shape divisória).

## `_add`: decimação, paleta e trace_map

Todo trace de dados passa por `_add(trace, row, col)`:

1. **Decimação**: se o trace tem > `self._max_points` pontos (padrão
   `_MAX_POINTS = 5000`; `_RES_MAX_POINTS = 2000` no resumo), faz slicing
   `[::step]` — o HTML caiu de ~570 MB para ~24 MB.
2. **Paleta**: cor light atribuída na construção; o par
   `(idx, light, dark)` entra no `trace_map`, que o renderer usa para
   re-colorir por tema no JS (`themedData`). `LIGHT_COLORS`/`DARK_COLORS`
   vivem em `config/settings.py`.
3. **Legenda por eixo**: `trace.legend = self._legend_key`.

⚠️ Traces adicionados FORA de `_add` (marcador tₛ, envelope LVRT) não entram
no `trace_map` → o JS nunca os re-colore → a cor fixa precisa funcionar nos
dois temas. E `trace.legend` deve ser setado manualmente. Ver
[[chart-analysis-overlays]].

## Legendas múltiplas (`_place_legends`)

Cada painel tem a própria legenda nomeada (`legend`, `legend2`, …, indexada
pelo nº do eixo):

- **Single**: fora da área de plot, à direita (`x=1.01`, `y` no meio do domínio
  do eixo Y), `bgcolor` transparente.
- **Pair**: dentro do painel, canto superior direito, `bgcolor`
  `rgba(255,255,255,0.8)` (semi-opaca para legibilidade sobre as curvas) —
  re-temada no dark pelo renderer (ver [[dark-mode-theming]], Fix 4).

## Eixos X linkados (`_apply_layout`)

`shared_xaxes=True` só liga eixos **por coluna**; todo eixo não-raiz recebe
`matches="x"` para a figura inteira seguir qualquer zoom — detalhes e a ponte
entre as duas figuras em [[dashboard-zoom-ghost]].

Outros pontos do layout: `exponentformat="none"` nos eixos Y (pu é
adimensional — sem prefixo SI), `hovermode="x unified"`, altura
`240 px × n_rows`, margem superior extra quando há subtítulos de grupo.
