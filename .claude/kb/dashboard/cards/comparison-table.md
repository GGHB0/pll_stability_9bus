---
name: comparison-table
description: Tabela comparativa de cenários no dashboard HTML — coluna de métricas ordenável, filtrada por modo PLL
---

# Tabela Comparativa de Cenários

## Contexto

O dashboard mostrava só **um cenário por vez** (troca via `<select>` ou clique
no mapa SVG). Com 12+ cenários, faltava uma visão de conjunto para comparar
severidade entre barras/linhas de falta. Adicionado em 2026-07 como seção
oculta por padrão (`table-toggle`), mesma UX do `diagram-toggle` existente.

Colunas removidas ao longo do tempo:

- ΔP/ΔQ (`dp`/`dq`) em 2026-07-24 — ver [[cards-metricas]].
- **`iae`, `ise`, `ts`, `peak` em 2026-08-09**, junto com o grupo de cards
  "Desempenho do PLL": eram todas derivadas do erro de ângulo
  `θ̂ − θ_rede`, sem fonte que sustente acúmulo/média/pico como medida de
  desempenho do PLL. Sumiram também os casos especiais que essas colunas
  exigiam (a célula `"&gt; t_end"` do cenário que não acomodava, e a
  classificação de `ts` por `ts_delta` em vez do valor exibido). Detalhe da
  decisão em [[cards-metricas]].

Sobraram as três colunas de tensão — a tabela hoje compara **severidade do
distúrbio** entre cenários, não desempenho.

## Mudanças em `src/report/renderer.py`

### Python — `_table_row_data`

Método paralelo a `_cards_html`, reaproveitando `_classify`:

```python
def _table_row_data(self, data: SimData) -> dict:
    m = data.metrics

    def cell(val, decimals, thresholds, lower_is_better=True):
        return {
            "val": f"{val:.{decimals}f}" if val is not None else "—",
            "raw": val,
            "cls": self._classify(val, thresholds, lower_is_better),
        }

    return {
        "vavg":    cell(m.get("vavg"),      3, VBUS_AVG_THRESH, lower_is_better=False),
        "vavg_b1": cell(m.get("vavg_bus1"), 3, VBUS_AVG_THRESH, lower_is_better=False),
        "vavg_b3": cell(m.get("vavg_bus3"), 3, VBUS_AVG_THRESH, lower_is_better=False),
    }
```

`vavg*` (2026-07-25, ex-`vmin*`) é média de |V|, não mínimo — ver
[[cards-metricas]] pela regra de janela (regime = período inteiro, falta =
só o período do curto). Threshold renomeado de `VBUS_MIN_THRESH` para
`VBUS_AVG_THRESH` (mesmos valores 0.90/0.50 pu).

Em `_build_html`, cada `sc_js[key]` ganha `"metricsRow": self._table_row_data(d)`.

### HTML

Botão `#table-toggle` ao lado do `#diagram-toggle` no `filter-bar`; seção
`#table-section` (`display:none` por padrão) com `<table id="cmp-table">` —
cabeçalho com `data-key` por coluna (`vavg`, `vavg_b1`, `vavg_b3`, mais
`label` não-ordenável) e
`<tbody id="cmp-tbody">` vazio, populado por JS. As três colunas de tensão
são "V méd. B2/B1/B3 (pu)" — B2 primeiro por ser o POC do inversor; B1/B3
mostram a propagação do afundamento pela rede ("—" em CSVs antigos sem
`vbus1_pu`/`vbus3_pu`).

### JS — render e ordenação

```javascript
var sortState = { key: null, dir: 1 };

function renderComparisonTable() {
  var keys = Object.keys(SCENARIOS).filter(function(k) {
    return SCENARIOS[k].badPll === (pllMode === "bad");
  });
  if (sortState.key) {
    keys.sort(function(a, b) {
      var ra = _sortVal(sortState.key, a), rb = _sortVal(sortState.key, b);
      if (ra == null) return 1;
      if (rb == null) return -1;
      if (ra < rb) return -sortState.dir;
      if (ra > rb) return sortState.dir;
      return 0;
    });
  }
  document.getElementById("cmp-tbody").innerHTML = keys.map(function(k) {
    var sc = SCENARIOS[k], r = sc.metricsRow;
    var active = (k === currentKey) ? " cmp-active" : "";
    return "<tr class=\"cmp-row" + active + "\" onclick=\"_pickTableRow('" + k + "')\">"
      + "<td class=\"cmp-label\">" + sc.label + "</td>"
      + _cmpCell(r.vavg) + _cmpCell(r.vavg_b1) + _cmpCell(r.vavg_b3)
      + "</tr>";
  }).join("");
}
```

Cabeçalhos com `data-key` recebem `addEventListener("click", ...)` que alterna
`sortState.dir` (toggle asc/desc no mesmo header) e re-renderiza.

**Ponto de integração**: `renderComparisonTable()` é chamado no fim de
`switchScenario()` (não em `toggleTable()`) — assim a tabela já nasce
populada no load inicial (`switchScenario(currentKey)` roda no fim do script)
e se mantém sincronizada com o filtro PLL sempre que `setPllMode()` troca de
cenário via `_findEquiv`, sem precisar de uma segunda chamada explícita.

### CSS

Reaproveita os tokens de cor dos cards (`.cmp-good/.warn/.bad/.neutral` ==
mesma paleta de `.card.good/.warn/.bad`), linha ativa com `background:
var(--badge-bg)`.

## Comportamento

| Situação | Comportamento |
|---|---|
| Clique em linha da tabela | `switchScenario` — sincroniza dropdown, mapa SVG e gráficos |
| Clique em header ordenável | Ordena asc; clique de novo no mesmo header inverte para desc |
| Toggle PLL (nominal/bad) | Filtra linhas visíveis, mesma regra do `<select>` |
| Toggle "Comparativo" | Só mostra/oculta a seção — não precisa re-renderizar |
