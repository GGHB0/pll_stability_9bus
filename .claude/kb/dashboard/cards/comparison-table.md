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

## Mudanças em `src/report/renderer.py`

### Python — `_table_row_data`

Método novo, paralelo a `_cards_html`, reaproveitando `_classify`:

```python
def _table_row_data(self, data: SimData) -> dict:
    m = data.metrics
    t_fault  = data.t_fault if data.t_fault is not None else T_FAULT
    ts_val   = m.get("ts")
    ts_delta = (ts_val - t_fault) if ts_val is not None else None

    def cell(val, decimals, thresholds, lower_is_better=True):
        return {
            "val": f"{val:.{decimals}f}" if val is not None else "—",
            "raw": val,
            "cls": self._classify(val, thresholds, lower_is_better),
        }

    return {
        "iae": cell(m.get("IAE"), 3, IAE_THRESH),
        "ise": cell(m.get("ISE"), 4, ISE_THRESH),
        "ts":  {"val": f"{ts_val:.3f}" if ts_val is not None else "—",
                "raw": ts_val, "cls": self._classify(ts_delta, TS_DELTA_THRESH)},
        "dp":  cell(m.get("dP_ufv"), 3, DP_THRESH),
        "dq":  cell(m.get("dQ_ufv"), 3, DQ_THRESH),
        "vmin": cell(m.get("vmin"), 3, VBUS2_MIN_THRESH, lower_is_better=False),
    }
```

`ts` é o único caso especial: `val`/`raw` exibem/ordenam por `ts_val` absoluto
(mesma leitura dos cards), mas `cls` classifica por `ts_delta` (margem em
relação a `t_fault`) — igual à lógica já usada em `_cards_html`.

Em `_build_html`, cada `sc_js[key]` ganha `"metricsRow": self._table_row_data(d)`.

### HTML

Botão `#table-toggle` ao lado do `#diagram-toggle` no `filter-bar`; seção
`#table-section` (`display:none` por padrão) com `<table id="cmp-table">` —
cabeçalho com `data-key` por coluna (`iae`, `ise`, `ts`, `dp`, `dq`, `vmin`,
mais `label` não-ordenável) e `<tbody id="cmp-tbody">` vazio, populado por JS.

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
      + _cmpCell(r.iae) + _cmpCell(r.ise) + _cmpCell(r.ts) + _cmpCell(r.dp) + _cmpCell(r.dq) + _cmpCell(r.vmin)
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
| Toggle "📊 Comparativo" | Só mostra/oculta a seção — não precisa re-renderizar |
