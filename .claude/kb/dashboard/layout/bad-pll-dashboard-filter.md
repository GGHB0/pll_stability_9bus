---
name: bad-pll-dashboard-filter
description: Design do filtro BAD_PLL no dashboard HTML — app.py + renderer.py, toggle PLL, SVG e select
---

# Filtro BAD_PLL no Dashboard

## Contexto

Quando `BAD_PLL=true` no MATLAB, os CSVs vão para pastas com sufixo `_bad_pll`
(ex.: `bus5/3phase_bad_pll/`). O `scan_scenarios` do `app.py` os varre junto com
os nominais → chaves coexistem no dict `SCENARIOS` do JS.

O dashboard precisa de um **toggle PLL** para:
- exibir label limpa (sem `_bad_pll` no texto)
- filtrar o `<select>` por modo ativo (nominal / mal dimensionado)
- trocar automaticamente para o cenário equivalente ao mudar o modo
- filtrar o tooltip do SVG pelo modo ativo

## Mudanças em `app.py`

```python
def _is_bad_pll(key: str) -> bool:
    return key.split("/")[-1].endswith("_bad_pll")

def _scenario_label(key: str) -> str:
    clean = key.replace("_bad_pll", "")
    if clean == "regime":
        return "Regime permanente"
    parts = clean.split("/")
    if len(parts) == 2:
        loc, fault = parts
        fl = FAULT_LABELS.get(fault, fault)
        if loc.startswith("bus"):  return f"Barra {loc[3:]} — {fl}"
        if loc.startswith("line"): return f"Linha {loc[4:].replace('_', '-')} — {fl}"
    return clean

def _sort_key(key: str) -> tuple:
    bad   = 1 if key.endswith("_bad_pll") else 0
    clean = key.replace("_bad_pll", "")
    # mesmo sort anterior, com `bad` como último critério
    # → nominal vem antes de bad_pll dentro do mesmo cenário
    ...
    return (..., bad)
```

Em `main()`, adicionar ao dict do cenário:

```python
scenarios[key] = {
    ...
    "bad_pll": _is_bad_pll(key),
}
```

## Mudanças em `src/report/renderer.py`

### Python

```python
# Em _build_html():
has_bad_pll = any(sc.get("bad_pll", False) for sc in self._scenarios.values())

# No sc_js[key]:
sc_js[key]["badPll"] = sc.get("bad_pll", False)
```

`_select_html` adiciona `data-pll="nominal"|"bad"` em cada `<option>`.
Classificação de optgroups usa `clean_loc = key.replace("_bad_pll","").split("/")[0]`
para que `regime_bad_pll` caia no grupo "Regime".

### JS — variável global e inicialização

```javascript
var pllMode = "nominal";  // "nominal" | "bad"
```

Toggle só é renderizado se `has_bad_pll == True`:

```html
<button class="pll-btn active" data-mode="nominal" onclick="setPllMode('nominal')">
  PLL Nominal
</button>
<button class="pll-btn" data-mode="bad" onclick="setPllMode('bad')">
  PLL Mal dimensionado
</button>
```

### JS — setPllMode

```javascript
function setPllMode(mode) {
  pllMode = mode;
  document.querySelectorAll(".pll-btn").forEach(function(b) {
    b.classList.toggle("active", b.dataset.mode === mode);
  });
  // Filtra options e optgroups
  document.querySelectorAll("#scenario-picker option").forEach(function(opt) {
    var isBad = SCENARIOS[opt.value] && SCENARIOS[opt.value].badPll;
    opt.hidden = (mode === "nominal") ? isBad : !isBad;
  });
  document.querySelectorAll("#scenario-picker optgroup").forEach(function(og) {
    og.hidden = !Array.from(og.querySelectorAll("option")).some(function(o) {
      return !o.hidden;
    });
  });
  // Troca para cenário equivalente no novo modo
  var equiv = _findEquiv(currentKey, mode);
  if (equiv) {
    document.getElementById("scenario-picker").value = equiv;
    switchScenario(equiv);
  }
}
```

### JS — _findEquiv e _firstOfMode

```javascript
function _findEquiv(key, mode) {
  if (mode === "bad") {
    var parts = key.split("/");
    var badKey = parts.length === 2
      ? parts[0] + "/" + parts[1] + "_bad_pll"
      : key + "_bad_pll";
    return SCENARIOS[badKey] ? badKey : _firstOfMode(true);
  } else {
    var nomKey = key.replace("_bad_pll", "");
    return SCENARIOS[nomKey] ? nomKey : _firstOfMode(false);
  }
}

function _firstOfMode(isBad) {
  return Object.keys(SCENARIOS).find(function(k) {
    return SCENARIOS[k].badPll === isBad;
  }) || null;
}
```

### JS — selectLocation (SVG) filtrado por modo

```javascript
function selectLocation(loc, el) {
  var keys = (svgLocMap[loc] || []).filter(function(k) {
    return SCENARIOS[k].badPll === (pllMode === "bad");
  });
  if (!keys.length) return;
  if (keys.length === 1) {
    _closeTip();
    document.getElementById("scenario-picker").value = keys[0];
    switchScenario(keys[0]);
  } else {
    _showTip(keys, el);
  }
}
```

### CSS — botões pill do toggle PLL

```css
.pll-btn {
  /* herda .toggle-btn */
  opacity: 0.6;
}
.pll-btn.active {
  opacity: 1;
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}
```

## Comportamento

| Situação | Comportamento |
|---|---|
| Sem dados BAD_PLL | Botões não aparecem |
| BAD_PLL=true, cenário equivalente existe | Troca diretamente para o equivalente |
| BAD_PLL=true, sem equivalente | Salta para o 1° cenário do modo |
| Clique no SVG no modo "bad" | Tooltip lista apenas os `_bad_pll` daquele local |
