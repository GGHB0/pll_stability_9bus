"""
renderer.py — Gera o HTML final com seletor de cenário, cards e Plotly embutido.

HTMLRenderer(scenarios).render(out_path) → escreve o HTML e retorna o Path.
scenarios: dict[key, {data, label, fig_inv, fig_sys, tm_inv, tm_sys}]
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import plotly
import plotly.graph_objects as go

from ..config import (
    T_FAULT, TOL_RAD, LVRT_THRESHOLD,
    IAE_THRESH, ISE_THRESH, TS_DELTA_THRESH, DP_THRESH, DQ_THRESH, VBUS2_MIN_THRESH,
)
from ..pipeline.loader import SimData


class HTMLRenderer:
    """Renderiza relatório HTML multi-cenário com seletor e duas seções de gráficos."""

    def __init__(self, scenarios: dict[str, dict]) -> None:
        # {key: {data, label, fig_inv, fig_sys, tm_inv, tm_sys}}
        self._scenarios = scenarios

    # ── API pública ──────────────────────────────────────────────────────────

    def render(self, out_path: Path) -> Path:
        out_path.write_text(self._build_html(), encoding="utf-8")
        return out_path

    # ── HTML ─────────────────────────────────────────────────────────────────

    def _build_html(self) -> str:
        first_key    = next(iter(self._scenarios))
        first_key_js = json.dumps(first_key)

        has_bad_pll = any(sc.get("bad_pll", False) for sc in self._scenarios.values())

        sc_js: dict = {}
        for key, sc in self._scenarios.items():
            d  = sc["data"]
            fi = sc["fig_inv"]
            fs = sc["fig_sys"]
            ti = sc["tm_inv"]
            ts = sc["tm_sys"]
            sc_js[key] = {
                "invData":   json.loads(fi.to_json()),
                "sysData":   json.loads(fs.to_json()) if fs else None,
                "invLight":  [x[1] for x in ti],
                "invDark":   [x[2] for x in ti],
                "invIdx":    [x[0] for x in ti],
                "sysLight":  [x[1] for x in ts],
                "sysDark":   [x[2] for x in ts],
                "sysIdx":    [x[0] for x in ts],
                "label":     sc["label"],
                "cardsHtml": self._cards_html(d),
                "storyHtml": self._story_html(d),
                "hasSys":    fs is not None,
                "badPll":    sc.get("bad_pll", False),
                "tFault":    d.t_fault,
                "tClear":    d.t_clear,
            }

        scenarios_js  = json.dumps(sc_js)
        select_html   = self._select_html()
        pll_toggle_html = self._pll_toggle_html() if has_bad_pll else ""

        return f"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SRF-PLL · IEEE 9-Bus · UERJ 2025</title>
<script src="https://cdn.plot.ly/plotly-2.35.0.min.js" charset="utf-8"></script>
<style>
{self._css()}
</style>
</head>
<body>

<header class="header">
  <div class="h-left">
    <div class="h-logo">φ</div>
    <div>
      <div class="h-title">SRF-PLL &nbsp;·&nbsp; IEEE 9-Bus</div>
      <div class="h-sub" id="header-sub">Análise pós-falta</div>
    </div>
    <span class="badge">UERJ 2025</span>
  </div>
  <div class="h-right">
    <button class="toggle-btn" onclick="toggleTheme()">
      <span id="ico">🌙</span>
      <span id="lbl">Dark mode</span>
    </button>
  </div>
</header>

<div class="filter-bar">
  <span class="filter-label">Cenário</span>
  {select_html}
  {pll_toggle_html}
  <button class="toggle-btn diag-btn" id="diagram-toggle" onclick="toggleDiagram()">🗺 Mapa IEEE 9-bus</button>
</div>

<main class="main">

  <div class="diagram-section" id="diagram-section">
{self._svg_section_html()}
    <p class="diag-hint">Clique em uma barra ou linha para selecionar o cenário de falta</p>
  </div>

  <div id="cards-area"></div>
  <div id="story-area"></div>

  <div class="chart-section" id="sec-inv">
    <div class="section-header">
      <span class="section-title">Inversor UFV</span>
      <span class="fault-badge" id="badge-inv"></span>
    </div>
    <div id="plot-inv"></div>
  </div>

  <div class="chart-section" id="sec-sys" style="display:none">
    <div class="section-header">
      <span class="section-title">Sistema 9-Bus</span>
      <span class="fault-badge" id="badge-sys"></span>
    </div>
    <div id="plot-sys"></div>
  </div>

  <div class="footer">
    <span>SRF-PLL Analyzer</span>
    <span class="footer-dot"></span>
    <span>Plotly {plotly.__version__}</span>
    <span class="footer-dot"></span>
    <span>TCC UERJ 2025</span>
  </div>

</main>

<script>
var SCENARIOS = {scenarios_js};
var currentKey = {first_key_js};
var isDark = false;
var pllMode = "nominal";

var gdInv  = document.getElementById("plot-inv");
var gdSys  = document.getElementById("plot-sys");
var secSys = document.getElementById("sec-sys");
var headerSub = document.getElementById("header-sub");
var badgeInv  = document.getElementById("badge-inv");
var badgeSys  = document.getElementById("badge-sys");

var BASE_LIGHT = {{
  paper_bgcolor: "#ffffff", plot_bgcolor: "#ffffff",
  "font.color": "#0f172a",
  "legend.bgcolor": "rgba(0,0,0,0)",
  "hoverlabel.bgcolor": "#ffffff", "hoverlabel.bordercolor": "#e2e8f0",
}};
var BASE_DARK = {{
  paper_bgcolor: "#111827", plot_bgcolor: "#111827",
  "font.color": "#f9fafb",
  "legend.bgcolor": "rgba(0,0,0,0)",
  "hoverlabel.bgcolor": "#1f2937", "hoverlabel.bordercolor": "#374151",
}};

var PLOTLY_CFG = {{
  responsive: true, displaylogo: false,
  modeBarButtonsToRemove: ["select2d", "lasso2d", "autoScale2d"],
  toImageButtonOptions: {{ format: "svg" }},
}};

function themedLayout(figData, isDarkMode) {{
  var base = isDarkMode ? BASE_DARK : BASE_LIGHT;
  var axUpd = {{}};
  Object.keys(figData.layout).forEach(function(k) {{
    if (k.startsWith("xaxis") || k.startsWith("yaxis")) {{
      axUpd[k + ".gridcolor"]     = isDarkMode ? "#1f2937" : "#f1f5f9";
      axUpd[k + ".zerolinecolor"] = isDarkMode ? "#374151" : "#e5e7eb";
    }}
  }});
  return Object.assign({{}}, figData.layout, base, axUpd);
}}

function themedData(data, lightC, darkC, tIdx, isDarkMode) {{
  var colors = isDarkMode ? darkC : lightC;
  return data.map(function(trace, i) {{
    var pos = tIdx.indexOf(i);
    if (pos === -1) return trace;
    return Object.assign({{}}, trace, {{
      line: Object.assign({{}}, trace.line, {{ color: colors[pos] }})
    }});
  }});
}}

function reactThemedChart(gd, figData, lightC, darkC, tIdx) {{
  Plotly.react(gd,
    themedData(figData.data, lightC, darkC, tIdx, isDark),
    themedLayout(figData, isDark),
    PLOTLY_CFG);
}}

function updateFaultUI(sc) {{
  if (sc.tFault == null) {{
    headerSub.textContent = "Análise em regime permanente";
    badgeInv.style.display = "none";
    badgeSys.style.display = "none";
    return;
  }}
  headerSub.innerHTML = "Análise pós-falta &nbsp;·&nbsp; T<sub>fault</sub> = "
    + sc.tFault.toFixed(2) + " s";
  var txt = (sc.tClear != null)
    ? "Falta: t = " + sc.tFault.toFixed(2) + " – " + sc.tClear.toFixed(2) + " s"
    : "Falta em t = " + sc.tFault.toFixed(2) + " s";
  badgeInv.textContent = txt;
  badgeInv.style.display = "";
  badgeSys.textContent = txt;
  badgeSys.style.display = "";
}}

function switchScenario(key) {{
  currentKey = key;
  var sc = SCENARIOS[key];

  updateFaultUI(sc);
  reactThemedChart(gdInv, sc.invData, sc.invLight, sc.invDark, sc.invIdx);

  if (sc.hasSys) {{
    secSys.style.display = "";
    reactThemedChart(gdSys, sc.sysData, sc.sysLight, sc.sysDark, sc.sysIdx);
  }} else {{
    secSys.style.display = "none";
  }}

  document.getElementById("cards-area").innerHTML = sc.cardsHtml;
  document.getElementById("story-area").innerHTML = sc.storyHtml;

  highlightSVG(key);
}}

// ── SVG diagram interactivity ─────────────────────────────────────────────

var svgLocMap = {{}};
(function() {{
  Object.keys(SCENARIOS).forEach(function(k) {{
    var loc = (k === "regime") ? "regime" : k.split("/")[0];
    if (!svgLocMap[loc]) svgLocMap[loc] = [];
    svgLocMap[loc].push(k);
  }});
  document.querySelectorAll("[data-loc]").forEach(function(el) {{
    var loc = el.getAttribute("data-loc");
    if (svgLocMap[loc]) {{
      el.classList.add("has-data");
      el.addEventListener("click", function(e) {{
        e.stopPropagation();
        selectLocation(loc, el);
      }});
    }}
  }});
}})();

var _tip = null;

function setPllMode(mode) {{
  pllMode = mode;
  document.querySelectorAll(".pll-btn").forEach(function(b) {{
    b.classList.toggle("active", b.dataset.mode === mode);
  }});
  document.querySelectorAll("#scenario-picker option").forEach(function(opt) {{
    var isBad = SCENARIOS[opt.value] && SCENARIOS[opt.value].badPll;
    opt.hidden = (mode === "nominal") ? isBad : !isBad;
  }});
  document.querySelectorAll("#scenario-picker optgroup").forEach(function(og) {{
    og.hidden = !Array.from(og.querySelectorAll("option")).some(function(o) {{ return !o.hidden; }});
  }});
  var equiv = _findEquiv(currentKey, mode);
  if (equiv) {{
    document.getElementById("scenario-picker").value = equiv;
    switchScenario(equiv);
  }}
}}

function _findEquiv(key, mode) {{
  if (mode === "bad") {{
    var parts = key.split("/");
    var badKey = parts.length === 2
      ? parts[0] + "/" + parts[1] + "_bad_pll"
      : key + "_bad_pll";
    return SCENARIOS[badKey] ? badKey : _firstOfMode(true);
  }} else {{
    var nomKey = key.replace("_bad_pll", "");
    return SCENARIOS[nomKey] ? nomKey : _firstOfMode(false);
  }}
}}

function _firstOfMode(isBad) {{
  return Object.keys(SCENARIOS).find(function(k) {{
    return SCENARIOS[k].badPll === isBad;
  }}) || null;
}}

function selectLocation(loc, el) {{
  var allKeys = svgLocMap[loc] || [];
  var keys = allKeys.filter(function(k) {{
    return SCENARIOS[k].badPll === (pllMode === "bad");
  }});
  if (!keys.length) return;
  if (keys.length === 1) {{
    _closeTip();
    document.getElementById("scenario-picker").value = keys[0];
    switchScenario(keys[0]);
  }} else {{
    _showTip(keys, el);
  }}
}}

function _showTip(keys, el) {{
  _closeTip();
  var d = document.createElement("div");
  d.className = "svg-tip";
  var h = document.createElement("p");
  h.className = "svg-tip-h";
  h.textContent = "Tipo de falta";
  d.appendChild(h);
  keys.forEach(function(k) {{
    var lbl = (SCENARIOS[k] && SCENARIOS[k].label) ? SCENARIOS[k].label : k;
    var btn = document.createElement("button");
    btn.className = "svg-tip-btn";
    btn.textContent = lbl;
    btn.onclick = (function(key) {{ return function() {{ _pickKey(key); }}; }})(k);
    d.appendChild(btn);
  }});
  document.body.appendChild(d);
  var r = el.getBoundingClientRect();
  var tx = r.right + window.scrollX + 10;
  if (tx + 210 > window.innerWidth) tx = r.left + window.scrollX - 220;
  d.style.left = Math.max(4, tx) + "px";
  d.style.top  = (r.top + window.scrollY) + "px";
  _tip = d;
  setTimeout(function() {{ document.addEventListener("click", _outsideClick); }}, 50);
}}

function _outsideClick(e) {{
  if (_tip && !_tip.contains(e.target)) _closeTip();
}}

function _closeTip() {{
  if (_tip) {{ _tip.remove(); _tip = null; }}
  document.removeEventListener("click", _outsideClick);
}}

function _pickKey(k) {{
  _closeTip();
  document.getElementById("scenario-picker").value = k;
  switchScenario(k);
}}

function highlightSVG(key) {{
  document.querySelectorAll("[data-loc].svg-active").forEach(function(el) {{
    el.classList.remove("svg-active");
  }});
  var loc = (key === "regime") ? "regime" : key.split("/")[0];
  var el = document.querySelector("[data-loc='" + loc + "']");
  if (el) el.classList.add("svg-active");
}}

function toggleDiagram() {{
  var sec = document.getElementById("diagram-section");
  var btn = document.getElementById("diagram-toggle");
  var hidden = sec.style.display === "none";
  sec.style.display = hidden ? "" : "none";
  btn.innerHTML = hidden ? "🗺&nbsp;Mapa IEEE 9-bus" : "🗺&nbsp;Ocultar mapa";
  btn.style.opacity = hidden ? "1" : "0.85";
}}

function toggleTheme() {{
  isDark = !isDark;
  document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
  var sc = SCENARIOS[currentKey];
  reactThemedChart(gdInv, sc.invData, sc.invLight, sc.invDark, sc.invIdx);
  if (sc.hasSys) {{
    reactThemedChart(gdSys, sc.sysData, sc.sysLight, sc.sysDark, sc.sysIdx);
  }}
  document.getElementById("ico").textContent = isDark ? "☀️" : "🌙";
  document.getElementById("lbl").textContent = isDark ? "Light mode" : "Dark mode";
}}

switchScenario(currentKey);
</script>

</body>
</html>"""

    # ── SVG diagram ─────────────────────────────────────────────────────────

    def _svg_section_html(self) -> str:
        from ..config import PROJ_ROOT
        svg_path = PROJ_ROOT / "assets" / "diagrams" / "ieee9bus_unifilar.svg"
        try:
            return svg_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ""

    # ── Select ───────────────────────────────────────────────────────────────

    def _select_html(self) -> str:
        regime_opts: list[str] = []
        bus_opts:    list[str] = []
        line_opts:   list[str] = []

        for key, sc in self._scenarios.items():
            pll_attr = 'data-pll="bad"' if sc.get("bad_pll", False) else 'data-pll="nominal"'
            opt = f'<option value="{key}" {pll_attr}>{sc["label"]}</option>'
            clean_loc = key.replace("_bad_pll", "").split("/")[0]
            if clean_loc == "regime":
                regime_opts.append(opt)
            elif clean_loc.startswith("bus"):
                bus_opts.append(opt)
            elif clean_loc.startswith("line"):
                line_opts.append(opt)

        groups: list[str] = []
        if regime_opts:
            groups.append(f'<optgroup label="Regime">{"".join(regime_opts)}</optgroup>')
        if bus_opts:
            groups.append(f'<optgroup label="Barras">{"".join(bus_opts)}</optgroup>')
        if line_opts:
            groups.append(f'<optgroup label="Linhas">{"".join(line_opts)}</optgroup>')

        return (
            '<select id="scenario-picker" onchange="switchScenario(this.value)">'
            + "".join(groups)
            + "</select>"
        )

    def _pll_toggle_html(self) -> str:
        return (
            '<span class="filter-label" style="margin-left:8px">PLL</span>'
            '<div class="pll-toggle">'
            '<button class="pll-btn active" data-mode="nominal" '
            'onclick="setPllMode(\'nominal\')">Nominal</button>'
            '<button class="pll-btn" data-mode="bad" '
            'onclick="setPllMode(\'bad\')">Mal dimensionado</button>'
            '</div>'
        )

    # ── Cards ────────────────────────────────────────────────────────────────

    @staticmethod
    def _classify(val, thresholds, lower_is_better=True):
        if val is None:
            return "neutral"
        lo, hi = thresholds
        if lower_is_better:
            return "good" if val <= lo else ("warn" if val <= hi else "bad")
        return "good" if val >= lo else ("warn" if val >= hi else "bad")

    def _cards_html(self, data: SimData) -> str:
        m = data.metrics

        def _v(val, decimals):
            return f"{val:.{decimals}f}" if val is not None else "—"

        def _card(name, val, unit, sub, tip, status):
            return (
                f'\n    <div class="card {status}" title="{tip}">'
                f'\n      <p class="c-name">{name}</p>'
                f'\n      <p class="c-val">{val}<span class="c-unit">{unit}</span></p>'
                f'\n      <p class="c-sub">{sub}</p>'
                f'\n    </div>'
            )

        def _group(label, cards_inner):
            return (
                f'\n  <div class="card-section">'
                f'\n    <p class="cg-label">{label}</p>'
                f'\n    <div class="cards-row">{cards_inner}\n    </div>'
                f'\n  </div>'
            )

        t_fault  = data.t_fault if data.t_fault is not None else T_FAULT
        ts_val   = m.get("ts")
        ts_delta = (ts_val - t_fault) if ts_val is not None else None

        pll = "".join([
            _card("IAE", _v(m.get("IAE"), 3), "rad·s", "∫|e| dt",
                  "Erro de fase acumulado",
                  self._classify(m.get("IAE"), IAE_THRESH)),
            _card("ISE", _v(m.get("ISE"), 4), "rad²·s", "∫e² dt",
                  "Energia do erro de fase",
                  self._classify(m.get("ISE"), ISE_THRESH)),
            _card("tₛ", _v(ts_val, 3), "s",
                  f"±{np.degrees(TOL_RAD):.1f}°",
                  "Tempo de acomodação do PLL",
                  self._classify(ts_delta, TS_DELTA_THRESH)),
        ])

        inv = "".join([
            _card("ΔP UFV", _v(m.get("dP_ufv"), 3), "pu", "pós-falta",
                  "Oscilação de potência ativa (UFV)",
                  self._classify(m.get("dP_ufv"), DP_THRESH)),
            _card("ΔQ UFV", _v(m.get("dQ_ufv"), 3), "pu", "pós-falta",
                  "Oscilação de potência reativa (UFV)",
                  self._classify(m.get("dQ_ufv"), DQ_THRESH)),
        ])

        sys = "".join([
            _card("V min", _v(m.get("vmin"), 3), "pu", "Barra 2",
                  f"Tensão mínima pós-falta (LVRT ≥ {LVRT_THRESHOLD} pu)",
                  self._classify(m.get("vmin"), VBUS2_MIN_THRESH, lower_is_better=False)),
        ])

        return (
            _group("Desempenho do PLL", pll) + "\n"
            + _group("Inversor UFV", inv) + "\n"
            + _group("Sistema 9-Bus", sys)
        )

    # ── Narrativa ────────────────────────────────────────────────────────────

    def _story_html(self, data: SimData) -> str:
        m       = data.metrics
        t_fault = data.t_fault if data.t_fault is not None else T_FAULT
        iae  = m.get("IAE")
        ts   = m.get("ts")
        dp   = m.get("dP_ufv")
        vmin = m.get("vmin")

        parts: list[str] = []

        if iae is not None:
            cls = self._classify(iae, IAE_THRESH)
            if cls == "good":
                parts.append(f"Erro de fase acumulado baixo (IAE = {iae:.3f} rad·s) — resposta rápida do PLL.")
            elif cls == "warn":
                parts.append(f"IAE de {iae:.3f} rad·s — desempenho moderado, PLL recuperou em tempo razoável.")
            else:
                parts.append(f"IAE elevado de {iae:.3f} rad·s — acumulação significativa de erro de fase.")

        if ts is not None:
            dt  = ts - t_fault
            cls = self._classify(dt, TS_DELTA_THRESH)
            tol = np.degrees(TOL_RAD)
            if cls == "good":
                parts.append(f"Acomodação em Δt = {dt:.2f} s (tₛ = {ts:.3f} s), dentro do critério ±{tol:.1f}°.")
            elif cls == "warn":
                parts.append(f"Acomodação em Δt = {dt:.2f} s (tₛ = {ts:.3f} s) — dentro dos limites, margem reduzida.")
            else:
                parts.append(f"PLL levou Δt = {dt:.2f} s para recuperar (tₛ = {ts:.3f} s) — resposta lenta.")

        if vmin is not None:
            cls = self._classify(vmin, VBUS2_MIN_THRESH, lower_is_better=False)
            if cls == "good":
                parts.append(f"Tensão na Barra 2 próxima do nominal (V_min = {vmin:.3f} pu).")
            elif cls == "warn":
                parts.append(f"Afundamento moderado na Barra 2 (V_min = {vmin:.3f} pu) — abaixo do limiar LVRT.")
            else:
                parts.append(f"Afundamento severo na Barra 2 (V_min = {vmin:.3f} pu) — condição crítica de LVRT.")

        if dp is not None:
            cls = self._classify(dp, DP_THRESH)
            if cls == "good":
                parts.append(f"Potência ativa pouco afetada (ΔP = {dp:.3f} pu).")
            elif cls == "warn":
                parts.append(f"Oscilação moderada de potência ativa (ΔP = {dp:.3f} pu).")
            else:
                parts.append(f"Oscilação severa de potência ativa (ΔP = {dp:.3f} pu) — risco de disparo de proteção.")

        statuses = [
            self._classify(iae, IAE_THRESH),
            self._classify((ts - t_fault) if ts is not None else None, TS_DELTA_THRESH),
            self._classify(vmin, VBUS2_MIN_THRESH, lower_is_better=False),
            self._classify(dp, DP_THRESH),
        ]
        if "bad" in statuses:
            verdict_cls, verdict_txt = "bad",     "Desempenho crítico"
        elif "warn" in statuses:
            verdict_cls, verdict_txt = "warn",    "Desempenho satisfatório"
        elif "good" in statuses:
            verdict_cls, verdict_txt = "good",    "Desempenho excelente"
        else:
            verdict_cls, verdict_txt = "neutral", "Dados insuficientes"

        text = " ".join(parts) or "Dados insuficientes para análise narrativa."

        return (
            f'<div class="story {verdict_cls}">'
            f'<div class="story-body">'
            f'<p class="story-title">Diagnóstico pós-falta</p>'
            f'<p class="story-text">{text}</p>'
            f'</div>'
            f'<div class="story-verdict {verdict_cls}">{verdict_txt}</div>'
            f'</div>'
        )

    # ── CSS ──────────────────────────────────────────────────────────────────

    @staticmethod
    def _css() -> str:
        return """
/* ── Tokens ── */
:root {
  --bg:        #f1f5f9;
  --surface:   #ffffff;
  --border:    #e2e8f0;
  --text:      #0f172a;
  --muted:     #64748b;
  --accent:    #2563eb;
  --badge-bg:  #eff6ff;
  --badge-fg:  #1d4ed8;
  --card-bg:   #ffffff;
  --sh:        0 1px 3px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.05);
  --sh-md:     0 4px 12px rgba(0,0,0,.09);
  --radius:    14px;
  --btn-bg:    #ffffff;
  --btn-fg:    #374151;
  --btn-bdr:   #d1d5db;
}
[data-theme="dark"] {
  --bg:        #0a0f1e;
  --surface:   #111827;
  --border:    #1f2937;
  --text:      #f9fafb;
  --muted:     #9ca3af;
  --accent:    #60a5fa;
  --badge-bg:  #1e3050;
  --badge-fg:  #93c5fd;
  --card-bg:   #111827;
  --sh:        0 1px 3px rgba(0,0,0,.5),0 1px 2px rgba(0,0,0,.4);
  --sh-md:     0 4px 12px rgba(0,0,0,.5);
  --btn-bg:    #1f2937;
  --btn-fg:    #d1d5db;
  --btn-bdr:   #374151;
}
*,*::before,*::after { box-sizing: border-box; margin: 0; padding: 0 }
body {
  font-family: Inter, "Segoe UI", system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}
body, .card, .header, .chart-section, .badge, .toggle-btn,
.c-val, .c-name, .c-sub, .c-unit {
  transition: background .28s, color .28s, border-color .28s, box-shadow .28s;
}

/* ── Header ── */
.header {
  position: sticky; top: 0; z-index: 200;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--sh);
  padding: 0 28px; height: 64px;
  display: flex; align-items: center; justify-content: space-between;
}
.h-left { display: flex; align-items: center; gap: 14px }
.h-logo {
  width: 40px; height: 40px; border-radius: 11px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 20px; font-weight: 800;
  flex-shrink: 0; user-select: none;
  box-shadow: 0 2px 8px rgba(37,99,235,.35);
}
.h-title { font-size: 15px; font-weight: 700; letter-spacing: -.2px; line-height: 1.2 }
.h-sub   { font-size: 12px; color: var(--muted); margin-top: 2px }
.badge {
  background: var(--badge-bg); color: var(--badge-fg);
  font-size: 11px; font-weight: 600; padding: 4px 11px;
  border-radius: 999px; letter-spacing: .3px;
}
.h-right { display: flex; align-items: center; gap: 10px }
.toggle-btn {
  display: flex; align-items: center; gap: 8px;
  background: var(--btn-bg); color: var(--btn-fg);
  border: 1.5px solid var(--btn-bdr);
  padding: 7px 16px; border-radius: 999px;
  font-size: 13px; font-weight: 600; font-family: inherit;
  cursor: pointer; box-shadow: var(--sh);
  transition: box-shadow .2s, transform .2s, background .28s,
              color .28s, border-color .28s;
}
.toggle-btn:hover  { box-shadow: var(--sh-md); transform: translateY(-1px) }
.toggle-btn:active { transform: translateY(0) }

/* ── Filter bar ── */
.filter-bar {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 10px 28px;
  display: flex; align-items: center; gap: 12px;
  position: sticky; top: 64px; z-index: 100;
  box-shadow: 0 2px 4px rgba(0,0,0,.04);
  transition: background .28s, border-color .28s;
}
.filter-label {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .7px; color: var(--muted); white-space: nowrap;
}
#scenario-picker {
  font-family: inherit; font-size: 13px; font-weight: 500;
  color: var(--text); background: var(--btn-bg);
  border: 1.5px solid var(--btn-bdr); border-radius: 8px;
  padding: 7px 12px; cursor: pointer;
  min-width: 260px; max-width: 480px;
  transition: border-color .2s, background .28s, color .28s;
}
#scenario-picker:focus { outline: none; border-color: var(--accent); }

/* ── Layout ── */
.main {
  max-width: 1200px; margin: 0 auto;
  padding: 28px 24px 48px;
}

/* ── Card sections ── */
.card-section { margin-bottom: 18px }
.cg-label {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .7px; color: var(--muted);
  margin-bottom: 9px;
}
.cards-row {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 14px;
}
.card {
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 16px 14px;
  box-shadow: var(--sh);
  position: relative; overflow: hidden; cursor: default;
}
.card::before {
  content: "";
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, #2563eb, #7c3aed);
  border-radius: var(--radius) var(--radius) 0 0;
}
[data-theme="dark"] .card::before { background: linear-gradient(90deg,#60a5fa,#a78bfa) }
.card:hover {
  box-shadow: var(--sh-md); transform: translateY(-2px);
  transition: box-shadow .18s, transform .18s, background .28s, border-color .28s;
}
.c-name {
  font-size: 11px; font-weight: 600; text-transform: uppercase;
  letter-spacing: .6px; color: var(--muted); margin-bottom: 8px;
}
.c-val {
  font-size: 24px; font-weight: 800; color: var(--accent);
  letter-spacing: -.5px; line-height: 1;
  display: flex; align-items: baseline; gap: 4px;
}
.c-unit { font-size: 11px; font-weight: 500; color: var(--muted); letter-spacing: .3px }
.c-sub  { font-size: 10.5px; color: var(--muted); margin-top: 6px }

/* ── Card status ── */
.card.good::before  { background: linear-gradient(90deg,#16a34a,#15803d) }
.card.warn::before  { background: linear-gradient(90deg,#d97706,#b45309) }
.card.bad::before   { background: linear-gradient(90deg,#dc2626,#991b1b) }
[data-theme="dark"] .card.good::before { background: linear-gradient(90deg,#4ade80,#16a34a) }
[data-theme="dark"] .card.warn::before { background: linear-gradient(90deg,#fbbf24,#d97706) }
[data-theme="dark"] .card.bad::before  { background: linear-gradient(90deg,#f87171,#dc2626) }
.card.good .c-val { color: #16a34a }
.card.warn .c-val { color: #b45309 }
.card.bad  .c-val { color: #dc2626 }
[data-theme="dark"] .card.good .c-val { color: #4ade80 }
[data-theme="dark"] .card.warn .c-val { color: #fbbf24 }
[data-theme="dark"] .card.bad  .c-val { color: #f87171 }

/* ── Story ── */
.story {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--sh);
  padding: 16px 20px;
  margin-bottom: 22px;
  display: flex; align-items: center; justify-content: space-between; gap: 20px;
}
.story.good { border-left-color: #16a34a }
.story.warn { border-left-color: #d97706 }
.story.bad  { border-left-color: #dc2626 }
[data-theme="dark"] .story.good { border-left-color: #4ade80 }
[data-theme="dark"] .story.warn { border-left-color: #fbbf24 }
[data-theme="dark"] .story.bad  { border-left-color: #f87171 }
.story-title {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .6px; color: var(--muted); margin-bottom: 6px;
}
.story-text { font-size: 13px; color: var(--text); line-height: 1.6 }
.story-verdict {
  flex-shrink: 0; white-space: nowrap;
  font-size: 12px; font-weight: 700;
  padding: 8px 18px; border-radius: 999px;
}
.story-verdict.good    { background: #dcfce7; color: #15803d }
.story-verdict.warn    { background: #fef3c7; color: #b45309 }
.story-verdict.bad     { background: #fee2e2; color: #991b1b }
.story-verdict.neutral { background: var(--border); color: var(--muted) }
[data-theme="dark"] .story-verdict.good    { background: #14532d; color: #4ade80 }
[data-theme="dark"] .story-verdict.warn    { background: #451a03; color: #fbbf24 }
[data-theme="dark"] .story-verdict.bad     { background: #450a0a; color: #f87171 }
[data-theme="dark"] .story-verdict.neutral { background: var(--border); color: var(--muted) }

/* ── Chart sections ── */
.chart-section {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--sh);
  overflow: hidden;
  margin-bottom: 20px;
}
.section-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 20px 12px;
  border-bottom: 1px solid var(--border);
}
.section-title {
  font-size: 13px; font-weight: 700; color: var(--text);
  letter-spacing: -.1px;
}
.fault-badge {
  font-size: 10px; font-weight: 600; color: #b45309;
  background: #fef3c7; border-radius: 6px; padding: 3px 9px;
}
[data-theme="dark"] .fault-badge { color: #fcd34d; background: #451a03 }
#plot-inv, #plot-sys { width: 100% }

/* ── Footer ── */
.footer {
  margin-top: 20px; text-align: center;
  font-size: 11px; color: var(--muted);
  display: flex; align-items: center; justify-content: center; gap: 12px;
}
.footer-dot {
  width: 3px; height: 3px; border-radius: 50%;
  background: var(--muted); flex-shrink: 0;
}

/* ── Filter bar extras ── */
.diag-btn { font-size: 12px; padding: 6px 14px; opacity: 1; transition: opacity .2s, box-shadow .2s, transform .2s, background .28s, color .28s, border-color .28s }

/* ── PLL toggle ── */
.pll-toggle {
  display: flex; border: 1.5px solid var(--btn-bdr);
  border-radius: 999px; overflow: hidden;
  background: var(--btn-bg);
  transition: border-color .28s, background .28s;
}
.pll-btn {
  font-family: inherit; font-size: 12px; font-weight: 600;
  padding: 6px 14px; background: transparent;
  border: none; cursor: pointer;
  color: var(--muted);
  transition: background .18s, color .18s;
  white-space: nowrap;
}
.pll-btn:hover { color: var(--text) }
.pll-btn.active {
  background: var(--accent); color: #fff;
}
[data-theme="dark"] .pll-btn.active { color: #0f172a }

/* ── Diagram section ── */
.diagram-section {
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--sh);
  padding: 12px 16px 8px;
  margin-bottom: 20px;
  overflow: hidden;
  transition: background .28s, border-color .28s;
}
.diagram-section svg {
  width: 100%; max-width: 920px; height: auto;
  display: block; margin: 0 auto; border-radius: 8px;
}
.diag-hint {
  text-align: center; font-size: 10.5px; color: var(--muted);
  margin-top: 4px; letter-spacing: .2px;
}

/* ── SVG tooltip ── */
.svg-tip {
  position: absolute;
  background: var(--surface);
  border: 1.5px solid var(--border);
  border-radius: 10px;
  box-shadow: var(--sh-md);
  padding: 10px 8px;
  z-index: 500;
  min-width: 190px;
  transition: background .28s, border-color .28s;
}
.svg-tip-h {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .6px; color: var(--muted); margin-bottom: 6px; padding: 0 6px;
}
.svg-tip-btn {
  display: block; width: 100%; text-align: left;
  padding: 7px 10px; background: transparent; border: none;
  border-radius: 7px; font-family: inherit; font-size: 12.5px;
  font-weight: 500; color: var(--text); cursor: pointer;
}
.svg-tip-btn:hover { background: var(--bg) }
"""
