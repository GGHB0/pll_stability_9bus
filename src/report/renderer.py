"""
renderer.py — Gera o HTML final com seletor de cenário, cards e Plotly embutido.

HTMLRenderer(scenarios).render(out_path) → escreve o HTML e retorna o Path.
scenarios: dict[key, {data, label, fig_inv, fig_sys, fig_res,
                      figs_spec, tms_spec, spec_harm,
                      tm_inv, tm_sys, tm_res}]
figs_spec/tms_spec são dicts por fase/eixo ("a"…"q"); spec_harm alimenta a
tabela de harmônicas da aba Espectro.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import plotly
import plotly.graph_objects as go

from ..config import (
    T_SETTLE, TOL_RAD, LVRT_THRESHOLD, F_FUND_HZ,
    IAE_THRESH, ISE_THRESH, TS_DELTA_THRESH, DP_THRESH, DQ_THRESH,
    PEAK_ERR_DEG_THRESH, ERR_SS_DEG_THRESH, SYNC_LOSS_DEG, VBUS_MIN_THRESH,
)
from ..pipeline.loader import SimData


class HTMLRenderer:
    """Renderiza relatório HTML multi-cenário com seletor e duas seções de gráficos."""

    _SPEC_MODES = ("a", "b", "c", "d", "q")
    _HARM_HI_PU = 0.4    # tabela de harmônicas: destaque se amp ≥ (pu)
    _HARM_LO_PU = 0.02   # tabela de harmônicas: apagado se amp < (pu)

    def __init__(self, scenarios: dict[str, dict]) -> None:
        # {key: {data, label, fig_inv, fig_sys, fig_res, figs_spec, tm_*}}
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
            fr = sc.get("fig_res")
            fp = sc.get("figs_spec") or {}
            ti = sc["tm_inv"]
            ts = sc["tm_sys"]
            tr = sc.get("tm_res") or []
            tp = sc.get("tms_spec") or {}
            sc_js[key] = {
                "invData":   json.loads(fi.to_json()),
                "sysData":   json.loads(fs.to_json()) if fs else None,
                "resData":   json.loads(fr.to_json()) if fr else None,
                "specData":  {m: json.loads(f.to_json()) for m, f in fp.items()},
                "specModes": list(fp.keys()),
                "invLight":  [x[1] for x in ti],
                "invDark":   [x[2] for x in ti],
                "invIdx":    [x[0] for x in ti],
                "sysLight":  [x[1] for x in ts],
                "sysDark":   [x[2] for x in ts],
                "sysIdx":    [x[0] for x in ts],
                "resLight":  [x[1] for x in tr],
                "resDark":   [x[2] for x in tr],
                "resIdx":    [x[0] for x in tr],
                "specLight": {m: [x[1] for x in tm] for m, tm in tp.items()},
                "specDark":  {m: [x[2] for x in tm] for m, tm in tp.items()},
                "specIdx":   {m: [x[0] for x in tm] for m, tm in tp.items()},
                "label":     sc["label"],
                "cardsHtml": self._cards_html(d),
                "storyHtml": self._story_html(d),
                "specTableHtml": self._spec_table_html(sc.get("spec_harm") or {}),
                "metricsRow": self._table_row_data(d),
                "hasInv":    True,
                "hasSys":    fs is not None,
                "hasRes":    fr is not None,
                "hasSpec":   bool(fp),
                "badPll":    sc.get("bad_pll", False),
                "tFault":    d.t_fault,
                "tClear":    d.t_clear,
                "tEnd":      d.t[-1] if len(d.t) > 0 else None,
            }

        scenarios_js  = json.dumps(sc_js)
        select_html   = self._select_html()
        pll_toggle_html = self._pll_toggle_html() if has_bad_pll else ""
        ghost_btn_html = (
            '<button class="toggle-btn diag-btn" id="ghost-toggle" '
            'onclick="toggleGhost()">👻&nbsp;Comparar PLL</button>'
        ) if has_bad_pll else ""
        uerj_logo_html = self._uerj_logo_html()

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
    {uerj_logo_html}
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
  <button class="toggle-btn diag-btn" id="table-toggle" onclick="toggleTable()">📊 Comparativo</button>
  <button class="toggle-btn diag-btn" id="zoom-fault" onclick="toggleZoomFault()">🔍&nbsp;Zoom na falta</button>
  {ghost_btn_html}
</div>

<main class="main">

  <div class="diagram-section" id="diagram-section">
{self._svg_section_html()}
    <p class="diag-hint">Clique em uma barra ou linha para selecionar o cenário de falta</p>
  </div>

  <div id="cards-area"></div>
  <div id="story-area"></div>

  <div class="table-section" id="table-section" style="display:none">
    <div class="section-header">
      <span class="section-title">Comparativo de cenários</span>
    </div>
    <div class="table-wrap">
      <table class="cmp-table" id="cmp-table">
        <thead>
          <tr>
            <th data-key="label">Cenário</th>
            <th data-key="iae">IAE (rad·s)</th>
            <th data-key="ise">ISE (rad²·s)</th>
            <th data-key="ts">tₛ (s)</th>
            <th data-key="peak">|θ_err| pico (°)</th>
            <th data-key="dp">ΔP (pu)</th>
            <th data-key="dq">ΔQ (pu)</th>
            <th data-key="vmin">Vmin B2 (pu)</th>
            <th data-key="vmin_b1">Vmin B1 (pu)</th>
            <th data-key="vmin_b3">Vmin B3 (pu)</th>
          </tr>
        </thead>
        <tbody id="cmp-tbody"></tbody>
      </table>
    </div>
  </div>

  <div class="tab-bar" id="tab-bar">
    <button class="tab-btn active" id="tab-res"  onclick="switchTab('res')">📌 Resumo</button>
    <button class="tab-btn" id="tab-inv"  onclick="switchTab('inv')">⚡ Inversor UFV</button>
    <button class="tab-btn" id="tab-sys"  onclick="switchTab('sys')">🔌 Sistema 9-Bus</button>
    <button class="tab-btn" id="tab-spec" onclick="switchTab('spec')">📈 Espectro FFT</button>
  </div>

  <div class="chart-section" id="sec-res" style="display:none">
    <div class="section-header">
      <span class="section-title">Resumo — resposta essencial</span>
      <span class="fault-badge" id="badge-res"></span>
    </div>
    <div id="plot-res"></div>
  </div>

  <div class="chart-section" id="sec-inv" style="display:none">
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

  <div class="chart-section" id="sec-spec" style="display:none">
    <div class="section-header">
      <span class="section-title">Espectro de amplitude (FFT) — <span id="spec-mode-lbl">fase a (abc)</span></span>
      <span class="spec-hint">amplitude linear · pré × durante × pós-falta · duplo-clique expande até 2 kHz</span>
    </div>
    <div class="spec-phase-bar">
      <span class="filter-label">Fase / eixo</span>
      <div class="pll-toggle">
        <button class="pll-btn spec-ph-btn active" data-phase="a" onclick="setSpecPhase('a')">a</button>
        <button class="pll-btn spec-ph-btn" data-phase="b" onclick="setSpecPhase('b')">b</button>
        <button class="pll-btn spec-ph-btn" data-phase="c" onclick="setSpecPhase('c')">c</button>
        <button class="pll-btn spec-ph-btn" data-phase="d" onclick="setSpecPhase('d')">d</button>
        <button class="pll-btn spec-ph-btn" data-phase="q" onclick="setSpecPhase('q')">q</button>
      </div>
      <span class="spec-hint" id="spec-phase-hint"></span>
    </div>
    <div id="plot-spec"></div>
    <div id="spec-harm-area"></div>
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

// Abas: cada gráfico vive num painel; só o ativo é renderizado (lazy) e os
// demais ficam "sujos" até serem abertos — _dirty[t] = precisa de Plotly.react.
var TABS = ["res", "inv", "sys", "spec"];
var HASKEY = {{ res: "hasRes", inv: "hasInv", sys: "hasSys", spec: "hasSpec" }};
var activeTab = "res";
var _dirty = {{ res: true, inv: true, sys: true, spec: true }};

var gd = {{}}, secEl = {{}}, tabBtn = {{}}, badgeEl = {{}};
TABS.forEach(function(t) {{
  gd[t]     = document.getElementById("plot-" + t);
  secEl[t]  = document.getElementById("sec-" + t);
  tabBtn[t] = document.getElementById("tab-" + t);
  badgeEl[t] = document.getElementById("badge-" + t);  // null no spec
}});
var headerSub = document.getElementById("header-sub");

// Cores por tema, aplicadas ANINHADAS em themedLayout — chave dotted
// ("font.color") é ignorada por Plotly.react (só relayout aceita).
var BASE_LIGHT = {{
  paper: "#ffffff", plot: "#ffffff", font: "#0f172a",
  legendInnerBg: "rgba(255,255,255,0.8)",
  hoverBg: "#ffffff", hoverBorder: "#e2e8f0",
}};
var BASE_DARK = {{
  paper: "#111827", plot: "#1a2436", font: "#f9fafb",
  legendInnerBg: "rgba(26,36,54,0.85)",
  hoverBg: "#1f2937", hoverBorder: "#374151",
}};

var PLOTLY_CFG = {{
  responsive: true, displaylogo: false,
  modeBarButtonsToRemove: ["select2d", "lasso2d", "autoScale2d"],
  // PNG em alta resolução (scale 3) pronto para as figuras do TCC DOCX
  toImageButtonOptions: {{ format: "png", scale: 3 }},
}};

function themedLayout(figData, isDarkMode) {{
  var C = isDarkMode ? BASE_DARK : BASE_LIGHT;
  var base = {{
    paper_bgcolor: C.paper, plot_bgcolor: C.plot,
    font: Object.assign({{}}, figData.layout.font, {{ color: C.font }}),
    hoverlabel: Object.assign({{}}, figData.layout.hoverlabel,
                              {{ bgcolor: C.hoverBg, bordercolor: C.hoverBorder }}),
  }};
  var axUpd = {{}};
  Object.keys(figData.layout).forEach(function(k) {{
    if (k.startsWith("xaxis") || k.startsWith("yaxis")) {{
      axUpd[k] = Object.assign({{}}, figData.layout[k], {{
        gridcolor:     isDarkMode ? "#31425c" : "#f1f5f9",
        zerolinecolor: isDarkMode ? "#4b5d7a" : "#e5e7eb",
      }});
    }}
    // legendas múltiplas (legend, legend2, …): fonte segue o tema; só a bgcolor
    // das internas (semi-opaca, painéis pareados) é re-temada — externas ficam
    // transparentes como vieram do chart.py
    if (k.startsWith("legend")) {{
      var lg = figData.layout[k] || {{}};
      var upd = {{ font: Object.assign({{}}, lg.font, {{ color: C.font }}) }};
      if (lg.bgcolor && lg.bgcolor !== "rgba(0,0,0,0)") upd.bgcolor = C.legendInnerBg;
      axUpd[k] = Object.assign({{}}, lg, upd);
    }}
  }});
  // _label (rótulo de painel) usa xref "x.../x{{n}} domain"; _group_title (subtítulo
  // de barra) usa xref "paper" — só essas duas cores vêm fixas do chart.py (não
  // herdam layout.font, então precisam de override manual por tema aqui.
  var annotations = (figData.layout.annotations || []).map(function(a) {{
    var isGroupTitle = a.xref === "paper";
    var color = isDarkMode
      ? (isGroupTitle ? "#cbd5e1" : "#9ca3af")
      : (isGroupTitle ? "#334155" : "#6b7280");
    return Object.assign({{}}, a, {{ font: Object.assign({{}}, a.font, {{ color: color }}) }});
  }});
  // Só a divisória do _group_title (xref "paper") é re-temada. Os demais shapes
  // (vlines/vrect de falta, hlines LVRT, banda de tolerância) vêm de add_vline/
  // add_hline/add_vrect do chart.py e devem MANTER a cor semântica própria.
  var shapes = (figData.layout.shapes || []).map(function(s) {{
    if (s.xref !== "paper") return s;
    return Object.assign({{}}, s, {{
      line: Object.assign({{}}, s.line, {{ color: isDarkMode ? "#374151" : "#e2e8f0" }})
    }});
  }});
  return Object.assign({{}}, figData.layout, base, axUpd, {{ annotations: annotations, shapes: shapes }});
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

function _renderChart(which) {{
  var sc = SCENARIOS[currentKey];
  var figData, light, dark, idx;
  if (which === "spec") {{
    var s = _specFig(sc);
    if (!s) return;
    _syncSpecPhaseUI();
    figData = s.fig; light = s.light; dark = s.dark; idx = s.idx;
  }} else {{
    figData = sc[which + "Data"];
    light = sc[which + "Light"]; dark = sc[which + "Dark"];
    idx   = sc[which + "Idx"];
  }}
  if (!figData) return;
  PLOTLY_CFG.toImageButtonOptions.filename =
    "pll_" + currentKey.split("/").join("_") + "_" + which
    + (which === "spec" ? "_" + specPhase : "");
  var data = themedData(figData.data, light, dark, idx, isDark)
    .concat(_ghostData(which));
  Plotly.react(gd[which], data, themedLayout(figData, isDark), PLOTLY_CFG);
  _dirty[which] = false;
}}

// ── Espectro: seletor de fase (abc) / eixo (dq) ────────────────────────────
// Cada fase/eixo é uma figura própria em specData[modo]; o seletor só troca
// qual delas o painel spec renderiza — mesmo lazy render das abas.

var specPhase = "a";
var SPEC_MODE_LBL = {{ a: "fase a (abc)", b: "fase b (abc)", c: "fase c (abc)",
                       d: "eixo d (dq)",  q: "eixo q (dq)" }};

function _specFig(sc) {{
  var modes = sc.specModes || [];
  if (!modes.length) return null;
  if (modes.indexOf(specPhase) === -1) specPhase = modes[0];
  return {{
    fig:   sc.specData[specPhase],
    light: sc.specLight[specPhase],
    dark:  sc.specDark[specPhase],
    idx:   sc.specIdx[specPhase],
  }};
}}

function setSpecPhase(p) {{
  specPhase = p;
  _dirty.spec = true;
  _syncSpecPhaseUI();
  if (activeTab === "spec") _renderChart("spec");
}}

function _syncSpecPhaseUI() {{
  var sc = SCENARIOS[currentKey];
  var modes = sc.specModes || [];
  if (modes.length && modes.indexOf(specPhase) === -1) specPhase = modes[0];
  document.querySelectorAll(".spec-ph-btn").forEach(function(b) {{
    var ph = b.dataset.phase;
    b.style.display = (modes.indexOf(ph) === -1) ? "none" : "";
    b.classList.toggle("active", ph === specPhase);
  }});
  var lbl = document.getElementById("spec-mode-lbl");
  if (lbl) lbl.textContent = SPEC_MODE_LBL[specPhase] || specPhase;
  var hint = document.getElementById("spec-phase-hint");
  if (hint) hint.textContent = (specPhase === "d" || specPhase === "q")
    ? "no dq a fundamental vira DC; seq. negativa aparece em 120 Hz"
    : "no abc a fundamental fica em 60 Hz";
}}

// ── Abas: mostra/esconde painéis e renderiza sob demanda ──────────────────

function switchTab(which) {{
  var sc = SCENARIOS[currentKey];
  if (!sc[HASKEY[which]]) {{
    which = TABS.filter(function(t) {{ return sc[HASKEY[t]]; }})[0];
  }}
  activeTab = which;
  TABS.forEach(function(t) {{
    var avail = !!sc[HASKEY[t]];
    tabBtn[t].style.display = avail ? "" : "none";
    tabBtn[t].classList.toggle("active", t === which);
    secEl[t].style.display = (t === which && avail) ? "" : "none";
  }});
  if (_dirty[which]) {{
    _renderChart(which);
    _ensureBridges();
    _applyZoom();
  }}
}}

// ── Cards clicáveis: pula para o painel da métrica ────────────────────────
// Procura o rótulo do painel (annotation do chart.py) nas figuras na ordem
// res → inv → sys; abre a aba e rola até o painel usando o domínio do eixo Y.

function goToChart(labelFrag) {{
  var sc = SCENARIOS[currentKey];
  var order = ["res", "inv", "sys"];
  for (var i = 0; i < order.length; i++) {{
    var t = order[i];
    if (!sc[HASKEY[t]]) continue;
    var fig = sc[t + "Data"];
    var anns = (fig.layout && fig.layout.annotations) || [];
    for (var j = 0; j < anns.length; j++) {{
      if (anns[j].xref !== "paper" && (anns[j].text || "").indexOf(labelFrag) !== -1) {{
        _openTabAt(t, fig, anns[j].yref);
        return;
      }}
    }}
  }}
}}

function _openTabAt(t, fig, yref) {{
  switchTab(t);
  var m = (yref || "").match(/^y(\\d*)/);
  var axName = "yaxis" + (m && m[1] ? m[1] : "");
  var lay = fig.layout[axName];
  var frac = (lay && lay.domain) ? lay.domain[1] : 1;   // topo do painel (0–1, base→topo)
  // setTimeout (não rAF): dá tempo do layout assentar após switchTab e
  // funciona mesmo com a aba do browser em segundo plano
  setTimeout(function() {{
    var sticky = document.querySelector(".header").offsetHeight
               + document.querySelector(".filter-bar").offsetHeight;
    var secTop = secEl[t].getBoundingClientRect().top + window.scrollY;
    var headerH = secEl[t].querySelector(".section-header").offsetHeight;
    var y = secTop + headerH + (1 - frac) * (fig.layout.height || 0) - sticky - 12;
    document.scrollingElement.scrollTo({{ top: Math.max(0, y), behavior: "smooth" }});
  }}, 60);
}}

// ── Fantasma: sobrepõe o cenário equivalente do outro modo PLL ────────────

var ghostMode = false;

function _exactEquiv(key) {{
  var sc = SCENARIOS[key];
  if (!sc) return null;
  var other = sc.badPll ? key.replace("_bad_pll", "") : key + "_bad_pll";
  return SCENARIOS[other] ? other : null;
}}

function _ghostData(which) {{
  if (!ghostMode) return [];
  var other = _exactEquiv(currentKey);
  if (!other) return [];
  var o = SCENARIOS[other];
  var fig, idx, colors;
  if (which === "spec") {{
    if (!o.specModes || o.specModes.indexOf(specPhase) === -1) return [];
    fig    = o.specData[specPhase];
    idx    = o.specIdx[specPhase];
    colors = isDark ? o.specDark[specPhase] : o.specLight[specPhase];
  }} else {{
    fig    = o[which + "Data"];
    idx    = o[which + "Idx"];
    colors = isDark ? o[which + "Dark"] : o[which + "Light"];
  }}
  if (!fig) return [];
  var tag = o.badPll ? " (sintonia inadequada)" : " (nominal)";
  // mesma cor do traço principal; pontilhado + opacidade marcam o fantasma
  return idx.map(function(i, pos) {{
    var tr = fig.data[i];
    return Object.assign({{}}, tr, {{
      opacity: 0.5,
      line: Object.assign({{}}, tr.line, {{ color: colors[pos], dash: "dot", width: 1.2 }}),
      name: (tr.name || "") + tag,
      showlegend: false,
      hoverinfo: "skip",
    }});
  }});
}}

function toggleGhost() {{
  ghostMode = !ghostMode;
  switchScenario(currentKey);
}}

// ── Zoom na janela de falta ───────────────────────────────────────────────

var zoomFault = false;

function toggleZoomFault() {{
  zoomFault = !zoomFault;
  _syncCtrlButtons();
  _applyZoom();
}}

// Todos os eixos X têm matches="x" (setado no chart.py) — basta atualizar o
// eixo raiz de cada figura que os demais painéis seguem. O spec fica de fora
// (eixo x em Hz); gráficos sujos (nunca renderizados nesta aba) também.
var TIME_TABS = ["res", "inv", "sys"];
var _syncingZoom = false;

function _plotted(t) {{
  return gd[t] && gd[t].data && !_dirty[t];
}}

function _applyZoom() {{
  var sc = SCENARIOS[currentKey];
  var upd = (zoomFault && sc.tFault != null)
    ? {{
        "xaxis.range": [
          sc.tFault - 0.1,
          Math.min((sc.tClear != null ? sc.tClear : sc.tFault) + 0.5,
                   sc.tEnd != null ? sc.tEnd : Infinity)
        ],
        "xaxis.autorange": false
      }}
    : {{ "xaxis.autorange": true }};
  _syncingZoom = true;
  var ps = [];
  TIME_TABS.forEach(function(t) {{
    if (_plotted(t)) ps.push(Plotly.relayout(gd[t], upd));
  }});
  Promise.all(ps).then(function() {{ _syncingZoom = false; }});
}}

// ── Sincroniza zoom manual (arrasto/duplo-clique) entre Inversor e Sistema ──

function _extractXZoom(ev) {{
  var keys = Object.keys(ev);
  for (var i = 0; i < keys.length; i++) {{
    if (/^xaxis\\d*\\.autorange$/.test(keys[i]) && ev[keys[i]]) return {{ auto: true }};
  }}
  for (var i = 0; i < keys.length; i++) {{
    var m = keys[i].match(/^(xaxis\\d*)\\.range(\\[0\\])?$/);
    if (m) {{
      var ax = m[1];
      var range = ev[ax + ".range"] ||
                  [ev[ax + ".range[0]"], ev[ax + ".range[1]"]];
      return {{ range: range }};
    }}
  }}
  return null;
}}

function _bridgeZoom(srcWhich) {{
  gd[srcWhich].on("plotly_relayout", function(ev) {{
    if (_syncingZoom) return;
    var z = _extractXZoom(ev || {{}});
    if (!z) return;
    var upd = z.auto ? {{ "xaxis.autorange": true }}
                     : {{ "xaxis.range": z.range, "xaxis.autorange": false }};
    _syncingZoom = true;
    var ps = [];
    TIME_TABS.forEach(function(t) {{
      if (t !== srcWhich && _plotted(t)) ps.push(Plotly.relayout(gd[t], upd));
    }});
    Promise.all(ps).then(function() {{ _syncingZoom = false; }});
  }});
}}

// .on só existe depois do 1º plot de cada div — registra sob demanda
function _ensureBridges() {{
  TIME_TABS.forEach(function(t) {{
    if (gd[t].on && !gd[t]._zoomBridged) {{
      gd[t]._zoomBridged = true;
      _bridgeZoom(t);
    }}
  }});
}}

function _syncCtrlButtons() {{
  var sc = SCENARIOS[currentKey];
  var zbtn = document.getElementById("zoom-fault");
  if (sc.tFault == null) zoomFault = false;
  zbtn.disabled = (sc.tFault == null);
  zbtn.classList.toggle("active", zoomFault);
  zbtn.innerHTML = zoomFault ? "🔍&nbsp;Visão completa" : "🔍&nbsp;Zoom na falta";
  var gbtn = document.getElementById("ghost-toggle");
  if (gbtn) {{
    if (_exactEquiv(currentKey) == null) ghostMode = false;
    gbtn.disabled = (_exactEquiv(currentKey) == null);
    gbtn.classList.toggle("active", ghostMode);
    gbtn.innerHTML = ghostMode ? "👻&nbsp;Ocultar comparação" : "👻&nbsp;Comparar PLL";
  }}
}}

function updateFaultUI(sc) {{
  var isRegime = (sc.tFault == null);
  var txt = "";
  if (isRegime) {{
    headerSub.textContent = "Análise em regime permanente";
  }} else {{
    headerSub.innerHTML = "Análise pós-falta &nbsp;·&nbsp; T<sub>fault</sub> = "
      + sc.tFault.toFixed(2) + " s";
    txt = (sc.tClear != null)
      ? "Falta: t = " + sc.tFault.toFixed(2) + " – " + sc.tClear.toFixed(2) + " s"
      : "Falta em t = " + sc.tFault.toFixed(2) + " s";
  }}
  TABS.forEach(function(t) {{
    if (!badgeEl[t]) return;
    badgeEl[t].textContent = txt;
    badgeEl[t].style.display = isRegime ? "none" : "";
  }});
}}

function switchScenario(key) {{
  currentKey = key;
  var sc = SCENARIOS[key];

  _syncCtrlButtons();
  updateFaultUI(sc);

  // todos os gráficos ficam sujos; só a aba ativa renderiza agora
  // (switchTab cai para a 1ª aba disponível se a ativa não existir no cenário)
  TABS.forEach(function(t) {{ _dirty[t] = true; }});
  switchTab(activeTab);

  document.getElementById("cards-area").innerHTML = sc.cardsHtml;
  document.getElementById("story-area").innerHTML = sc.storyHtml;
  document.getElementById("spec-harm-area").innerHTML = sc.specTableHtml || "";
  _syncSpecPhaseUI();

  highlightSVG(key);
  renderComparisonTable();
}}

// ── Tabela comparativa ────────────────────────────────────────────────────

var sortState = {{ key: null, dir: 1 }};

function toggleTable() {{
  var sec = document.getElementById("table-section");
  var btn = document.getElementById("table-toggle");
  var hidden = sec.style.display === "none";
  sec.style.display = hidden ? "" : "none";
  btn.style.opacity = hidden ? "1" : "0.85";
}}

function _sortVal(key, k) {{
  return (key === "label") ? SCENARIOS[k].label : SCENARIOS[k].metricsRow[key].raw;
}}

function _cmpCell(cell) {{
  return "<td class=\\"cmp-" + cell.cls + "\\">" + cell.val + "</td>";
}}

function renderComparisonTable() {{
  var keys = Object.keys(SCENARIOS).filter(function(k) {{
    return SCENARIOS[k].badPll === (pllMode === "bad");
  }});
  if (sortState.key) {{
    keys.sort(function(a, b) {{
      var ra = _sortVal(sortState.key, a), rb = _sortVal(sortState.key, b);
      if (ra == null) return 1;
      if (rb == null) return -1;
      if (ra < rb) return -sortState.dir;
      if (ra > rb) return sortState.dir;
      return 0;
    }});
  }}
  document.getElementById("cmp-tbody").innerHTML = keys.map(function(k) {{
    var sc = SCENARIOS[k], r = sc.metricsRow;
    var active = (k === currentKey) ? " cmp-active" : "";
    return "<tr class=\\"cmp-row" + active + "\\" onclick=\\"_pickTableRow('" + k + "')\\">"
      + "<td class=\\"cmp-label\\">" + sc.label + "</td>"
      + _cmpCell(r.iae) + _cmpCell(r.ise) + _cmpCell(r.ts) + _cmpCell(r.peak) + _cmpCell(r.dp) + _cmpCell(r.dq) + _cmpCell(r.vmin) + _cmpCell(r.vmin_b1) + _cmpCell(r.vmin_b3)
      + "</tr>";
  }}).join("");
}}

function _pickTableRow(k) {{
  document.getElementById("scenario-picker").value = k;
  switchScenario(k);
}}

document.querySelectorAll("#cmp-table thead th[data-key]").forEach(function(th) {{
  th.addEventListener("click", function() {{
    var key = th.getAttribute("data-key");
    sortState.dir = (sortState.key === key) ? -sortState.dir : 1;
    sortState.key = key;
    renderComparisonTable();
  }});
}});

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
  btn.innerHTML = hidden ? "🗺&nbsp;Ocultar mapa" : "🗺&nbsp;Mapa IEEE 9-bus";
  btn.style.opacity = hidden ? "1" : "0.85";
}}

function toggleTheme() {{
  isDark = !isDark;
  document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
  TABS.forEach(function(t) {{ _dirty[t] = true; }});
  _renderChart(activeTab);
  _applyZoom();
  document.getElementById("ico").textContent = isDark ? "☀️" : "🌙";
  document.getElementById("lbl").textContent = isDark ? "Light mode" : "Dark mode";
}}

switchScenario(currentKey);
</script>

</body>
</html>"""

    # ── Logo UERJ ───────────────────────────────────────────────────────────

    def _uerj_logo_html(self) -> str:
        from ..config import PROJ_ROOT
        import base64
        logo_path = PROJ_ROOT / "assets" / "uerj.png"
        try:
            b64 = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        except FileNotFoundError:
            return ""
        return f'<img class="h-uerj-logo" src="data:image/png;base64,{b64}" alt="UERJ">'

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
            'onclick="setPllMode(\'bad\')">Sintonia inadequada</button>'
            '</div>'
        )

    # ── Tabela de harmônicas (aba Espectro) ──────────────────────────────────

    def _spec_table_html(self, harm: dict) -> str:
        """Tabelas de amplitude das harmônicas 1–7 (k·60 Hz), colunas
        agrupadas por segmento (pré/durante/pós-falta) × fase/eixo (a b c d q)
        — uma tabela para corrente, outra para tensão UFV. Valores vêm do
        SpectrumBuilder (pico local do espectro de Hann em cada k·60 Hz)."""
        segs = harm.get("segs") or []
        if not segs:
            return ""
        n_modes = len(self._SPEC_MODES)
        blocks: list[str] = []
        for kind, title in (("i", "Corrente UFV"), ("v", "Tensão UFV")):
            per_seg = harm.get(kind) or {}
            if not any(per_seg.get(s) for s in segs):
                continue
            head1 = "<tr><th rowspan='2'>h</th><th rowspan='2'>f (Hz)</th>"
            head2 = "<tr>"
            for s in segs:
                head1 += f"<th colspan='{n_modes}' class='harm-first'>{s}</th>"
                for j, mo in enumerate(self._SPEC_MODES):
                    first = " harm-first" if j == 0 else ""
                    head2 += f"<th class='harm-sub{first}'>{mo}</th>"
            head1 += "</tr>"
            head2 += "</tr>"
            rows: list[str] = []
            for k in range(1, 8):
                cells = (f"<td class='harm-h'>{k}ª</td>"
                         f"<td class='harm-h'>{k * F_FUND_HZ:.0f}</td>")
                for s in segs:
                    mode_amps = per_seg.get(s) or {}
                    for j, mo in enumerate(self._SPEC_MODES):
                        first = " harm-first" if j == 0 else ""
                        amps = mode_amps.get(mo)
                        v = amps[k - 1] if amps else None
                        if v is None:
                            cells += f"<td class='harm-na{first}'>—</td>"
                            continue
                        # limiares absolutos em pu: destaque só para amplitude
                        # na ordem da nominal; quase-zero fica apagado
                        tier = (" harm-top" if v >= self._HARM_HI_PU
                                else " harm-lo" if v < self._HARM_LO_PU
                                else "")
                        cells += f"<td class='harm-val{first}{tier}'>{v:.3g}</td>"
                rows.append(f"<tr>{cells}</tr>")
            blocks.append(
                f"<div class='harm-block'>"
                f"<p class='harm-title'>Harmônicas — {title} (pu)</p>"
                f"<div class='table-wrap'><table class='harm-table'>"
                f"<thead>{head1}{head2}</thead>"
                f"<tbody>{''.join(rows)}</tbody></table></div></div>"
            )
        return "".join(blocks)

    # ── Cards ────────────────────────────────────────────────────────────────

    @staticmethod
    def _classify(val, thresholds, lower_is_better=True):
        if val is None:
            return "neutral"
        lo, hi = thresholds
        if lower_is_better:
            return "good" if val <= lo else ("warn" if val <= hi else "bad")
        return "good" if val >= lo else ("warn" if val >= hi else "bad")

    def _table_row_data(self, data: SimData) -> dict:
        """Uma linha da tabela comparativa: {métrica: {val, raw, cls}} por cenário."""
        m = data.metrics
        ts_val   = m.get("ts")
        peak_deg = float(np.degrees(m["peak_err"])) if m.get("peak_err") is not None else None

        def cell(val, decimals, thresholds, lower_is_better=True):
            return {
                "val": f"{val:.{decimals}f}" if val is not None else "—",
                "raw": val,
                "cls": self._classify(val, thresholds, lower_is_better),
            }

        if m.get("settled") is False:
            # não acomodou na janela simulada: ordena pelo fim da simulação
            ts_cell = {"val": f"&gt; {data.t[-1]:.2f}", "raw": float(data.t[-1]), "cls": "bad"}
        else:
            ts_cell = {
                "val": f"{ts_val:.3f}" if ts_val is not None else "—",
                "raw": ts_val,
                "cls": self._classify(m.get("ts_delta"), TS_DELTA_THRESH),
            }

        return {
            "iae":  cell(m.get("IAE"), 3, IAE_THRESH),
            "ise":  cell(m.get("ISE"), 4, ISE_THRESH),
            "ts":   ts_cell,
            "peak": cell(peak_deg, 1, PEAK_ERR_DEG_THRESH),
            "dp":   cell(m.get("dP_ufv"), 3, DP_THRESH),
            "dq":   cell(m.get("dQ_ufv"), 3, DQ_THRESH),
            "vmin":    cell(m.get("vmin"),      3, VBUS_MIN_THRESH, lower_is_better=False),
            "vmin_b1": cell(m.get("vmin_bus1"), 3, VBUS_MIN_THRESH, lower_is_better=False),
            "vmin_b3": cell(m.get("vmin_bus3"), 3, VBUS_MIN_THRESH, lower_is_better=False),
        }

    def _cards_html(self, data: SimData) -> str:
        m = data.metrics

        def _v(val, decimals):
            return f"{val:.{decimals}f}" if val is not None else "—"

        def _card(name, val, unit, sub, tip, status, target=None):
            # target = fragmento do rótulo de painel (annotation do chart.py);
            # o clique abre a aba certa e rola até o painel (goToChart no JS)
            click = f' onclick="goToChart(\'{target}\')"' if target else ""
            cls   = f"card {status}" + (" clickable" if target else "")
            return (
                f'\n    <div class="{cls}" title="{tip}"{click}>'
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

        is_regime = data.t_fault is None
        ts_val    = m.get("ts")
        peak_deg  = float(np.degrees(m["peak_err"])) if m.get("peak_err") is not None else None

        # tₛ: três estados — acomodou, não acomodou na janela, sem dado.
        # Em regime não há distúrbio para acomodar → card omitido.
        if is_regime:
            ts_card = ""
        elif m.get("settled") is False:
            ts_card = _card("tₛ", f"&gt; {data.t[-1]:.2f}", "s", "não acomodou",
                            f"Erro de fase ainda fora de ±{np.degrees(TOL_RAD):.2f}° "
                            "ao fim da janela simulada", "bad", target="Erro de fase")
        else:
            ts_card = _card("tₛ", _v(ts_val, 3), "s",
                            f"±{np.degrees(TOL_RAD):.2f}°",
                            "Tempo de acomodação do PLL",
                            self._classify(m.get("ts_delta"), TS_DELTA_THRESH),
                            target="Erro de fase")

        peak_win  = "em regime" if is_regime else "pós-falta"
        sync_loss = peak_deg is not None and peak_deg >= SYNC_LOSS_DEG
        peak_card = _card("|θ_err| pico", _v(peak_deg, 1), "°",
                          "perda de sincronismo" if sync_loss else "pico transitório",
                          f"Pico (máx instantâneo) do erro de fase {peak_win} — pior "
                          f"excursão, distinto do erro sustentado de R.P. "
                          f"(≥ {SYNC_LOSS_DEG:.0f}° indica escorregamento do PLL)",
                          self._classify(peak_deg, PEAK_ERR_DEG_THRESH),
                          target="Erro de fase")

        # Erro de regime permanente: erro de fase SUSTENTADO (média de |e|) na
        # janela após a acomodação (t ≥ t_ss). Só existe quando há regime a
        # medir — falta que não reacomodou fica sem este card.
        err_ss_deg = float(np.degrees(m["err_ss_mean"])) if m.get("err_ss_mean") is not None else None
        t_ss       = m.get("t_ss")
        if err_ss_deg is not None and t_ss is not None:
            ss_card = _card("Erro R.P.", _v(err_ss_deg, 2), "°",
                            f"média |e|, t ≥ {t_ss:.3f} s",
                            f"Erro de fase sustentado em regime permanente — média de "
                            f"|θ̂ − θ_rede| a partir de t = {t_ss:.3f} s "
                            f"({'PLL travado' if is_regime else 'após a acomodação tₛ'}). "
                            f"Não confundir com o pico transitório.",
                            self._classify(err_ss_deg, ERR_SS_DEG_THRESH),
                            target="Erro de fase")
        else:
            ss_card = ""

        pll = "".join([
            _card("IAE", _v(m.get("IAE"), 3), "rad·s", "∫|e| dt",
                  "Erro de fase acumulado",
                  self._classify(m.get("IAE"), IAE_THRESH),
                  target="Erro de fase"),
            _card("ISE", _v(m.get("ISE"), 4), "rad²·s", "∫e² dt",
                  "Energia do erro de fase",
                  self._classify(m.get("ISE"), ISE_THRESH),
                  target="Erro de fase"),
            ts_card,
            peak_card,
            ss_card,
        ])

        rec_sub = "regime" if is_regime else "pós-clear"
        rec_ctx = ("em regime (oscilação sustentada)" if is_regime
                   else "na recuperação")
        inv = "".join([
            _card("ΔP UFV", _v(m.get("dP_ufv"), 3), "pu", rec_sub,
                  f"Excursão de potência ativa {rec_ctx} (UFV)",
                  self._classify(m.get("dP_ufv"), DP_THRESH),
                  target="P / Q UFV"),
            _card("ΔQ UFV", _v(m.get("dQ_ufv"), 3), "pu", rec_sub,
                  f"Excursão de potência reativa {rec_ctx} (UFV)",
                  self._classify(m.get("dQ_ufv"), DQ_THRESH),
                  target="P / Q UFV"),
        ])

        # Severidade: contexto do distúrbio — cor indica profundidade do sag,
        # mas não entra no veredito de desempenho
        # "V residual" = tensão remanescente do afundamento (PRODIST/IEC);
        # em regime não há curto, então o card volta a "V min"
        vlab = "V min" if is_regime else "V residual"
        sev_cards = [
            _card(f"{vlab} B2", _v(m.get("vmin"), 3), "pu", "POC do inversor (UFV)",
                  f"Tensão mínima na Barra 2 (LVRT ≥ {LVRT_THRESHOLD} pu) — "
                  "severidade do distúrbio",
                  self._classify(m.get("vmin"), VBUS_MIN_THRESH, lower_is_better=False),
                  target="|V| Bus 2"),
        ]
        for key, bus, sub in (("vmin_bus1", "B1", "barra do G1 (slack)"),
                              ("vmin_bus3", "B3", "barra do G3")):
            if m.get(key) is not None:
                sev_cards.append(
                    _card(f"{vlab} {bus}", _v(m.get(key), 3), "pu", sub,
                          f"Tensão mínima na barra {bus[1]} durante o curto — "
                          "propagação do afundamento pela rede",
                          self._classify(m.get(key), VBUS_MIN_THRESH,
                                         lower_is_better=False),
                          target=f"|V| Bus {bus[1]}"))
        if data.t_fault is not None and data.t_clear is not None:
            dur_ms = (data.t_clear - data.t_fault) * 1e3
            sev_cards.append(
                _card("Duração", f"{dur_ms:.0f}", "ms",
                      f"t = {data.t_fault:.2f} – {data.t_clear:.2f} s",
                      "Duração da falta aplicada", "neutral"))
        sev_label = "Sistema 9-Bus" if is_regime else "Severidade do distúrbio"
        inv_label = ("Estabilidade de potência" if is_regime
                     else "Recuperação do inversor")

        return (
            _group(sev_label, "".join(sev_cards)) + "\n"
            + _group("Desempenho do PLL", pll) + "\n"
            + _group(inv_label, inv)
        )

    # ── Narrativa ────────────────────────────────────────────────────────────

    def _story_html(self, data: SimData) -> str:
        m         = data.metrics
        is_regime = data.t_fault is None
        iae      = m.get("IAE")
        ts       = m.get("ts")
        ts_delta = m.get("ts_delta")
        settled  = m.get("settled")
        dp       = m.get("dP_ufv")
        dq       = m.get("dQ_ufv")
        vmin     = m.get("vmin")
        peak_deg = float(np.degrees(m["peak_err"])) if m.get("peak_err") is not None else None
        tol      = round(float(np.degrees(TOL_RAD)), 2)

        # (classe do semáforo, rótulo, texto) — vira <li> na lista do diagnóstico
        parts: list[tuple[str, str, str]] = []

        # ── contexto: severidade do distúrbio (não entra no veredito) ────────
        if is_regime:
            parts.append(("neutral", "Cenário",
                          "Operação em regime permanente, sem contingência aplicada — "
                          "métricas calculadas descartando o transitório de partida "
                          f"(t ≥ {T_SETTLE:.2f} s)."))
        elif vmin is not None:
            sev = self._classify(vmin, VBUS_MIN_THRESH, lower_is_better=False)
            dur = (f" de {(data.t_clear - data.t_fault) * 1e3:.0f} ms"
                   if data.t_clear is not None else "")
            if sev == "good":
                parts.append(("good", "Distúrbio",
                              f"Falta{dur} com afundamento leve na Barra 2 "
                              f"(V residual = {vmin:.3f} pu)."))
            elif sev == "warn":
                parts.append(("warn", "Distúrbio",
                              f"Falta{dur} com afundamento moderado na Barra 2 "
                              f"(V residual = {vmin:.3f} pu, abaixo do limiar LVRT)."))
            else:
                parts.append(("bad", "Distúrbio",
                              f"Falta{dur} com afundamento severo na Barra 2 "
                              f"(V residual = {vmin:.3f} pu) — condição crítica de LVRT."))

        # ── resposta do PLL ──────────────────────────────────────────────────
        peak_cls = self._classify(peak_deg, PEAK_ERR_DEG_THRESH)
        if peak_deg is not None:
            if peak_deg >= SYNC_LOSS_DEG:
                parts.append(("bad", "Pico de fase",
                              f"{peak_deg:.0f}° — perda de sincronismo do PLL "
                              "(escorregamento)."))
            elif peak_cls == "bad":
                parts.append(("bad", "Pico de fase",
                              f"Excursão elevada, de até {peak_deg:.0f}°."))
            elif peak_cls == "warn":
                ctx = "em regime" if is_regime else "durante o distúrbio"
                parts.append(("warn", "Pico de fase",
                              f"Excursão de até {peak_deg:.0f}° {ctx}."))

        ts_cls = "bad" if settled is False else self._classify(ts_delta, TS_DELTA_THRESH)
        if settled is False:
            parts.append(("bad", "Acomodação",
                          "O PLL não reacomodou dentro da janela simulada "
                          f"(erro fora de ±{tol:.2f}° em t = {data.t[-1]:.2f} s)."))
        elif ts is not None:
            if ts_cls == "good":
                parts.append(("good", "Acomodação",
                              f"Δt = {ts_delta:.2f} s (tₛ = {ts:.3f} s), "
                              f"dentro do critério ±{tol:.2f}°."))
            elif ts_cls == "warn":
                parts.append(("warn", "Acomodação",
                              f"Δt = {ts_delta:.2f} s (tₛ = {ts:.3f} s) — "
                              "dentro dos limites, margem reduzida."))
            else:
                parts.append(("bad", "Acomodação",
                              f"Δt = {ts_delta:.2f} s (tₛ = {ts:.3f} s) — "
                              "resposta lenta."))

        # ── erro sustentado em regime permanente (após a acomodação) ─────────
        err_ss_deg = float(np.degrees(m["err_ss_mean"])) if m.get("err_ss_mean") is not None else None
        t_ss       = m.get("t_ss")
        if err_ss_deg is not None and t_ss is not None:
            ss_cls = self._classify(err_ss_deg, ERR_SS_DEG_THRESH)
            win = "regime permanente" if is_regime else "regime pós-falta"
            if ss_cls == "good":
                parts.append(("good", "Erro de regime",
                              f"Erro de fase sustentado de {err_ss_deg:.2f}° "
                              f"(média para t ≥ {t_ss:.3f} s) — desprezível."))
            elif ss_cls == "warn":
                parts.append(("warn", "Erro de regime",
                              f"Erro de fase sustentado de {err_ss_deg:.2f}° em {win} "
                              f"(t ≥ {t_ss:.3f} s) — moderado."))
            else:
                parts.append(("bad", "Erro de regime",
                              f"Erro de fase sustentado de {err_ss_deg:.2f}° em {win} "
                              f"(t ≥ {t_ss:.3f} s) — elevado para regime permanente."))

        iae_cls = self._classify(iae, IAE_THRESH)
        if iae is not None:
            if iae_cls == "good":
                parts.append(("good", "Erro acumulado",
                              f"IAE = {iae:.3f} rad·s, baixo."))
            elif iae_cls == "warn":
                parts.append(("warn", "Erro acumulado",
                              f"IAE = {iae:.3f} rad·s — acúmulo moderado."))
            else:
                parts.append(("bad", "Erro acumulado",
                              f"IAE = {iae:.3f} rad·s — acumulação significativa."))

        # ── recuperação (pós-clear) ou estabilidade de P/Q (regime) ──────────
        dp_cls = self._classify(dp, DP_THRESH)
        if dp is not None:
            label = "Oscilação de potência" if is_regime else "Recuperação"
            if dp_cls == "good":
                if is_regime:
                    parts.append(("good", label,
                                  f"ΔP = {dp:.3f} pu — estável em operação normal."))
                else:
                    parts.append(("good", label,
                                  f"ΔP = {dp:.3f} pu, sem oscilação residual após a falta."))
            elif dp_cls == "warn":
                parts.append(("warn", label,
                              f"Oscilação moderada de potência ativa "
                              f"(ΔP = {dp:.3f} pu)."))
            else:
                if is_regime:
                    parts.append(("bad", label,
                                  f"Oscilação sustentada em regime "
                                  f"(ΔP = {dp:.3f} pu) — risco de atuação de proteção."))
                else:
                    parts.append(("bad", label,
                                  f"Oscilação severa após a falta "
                                  f"(ΔP = {dp:.3f} pu) — risco de atuação de proteção."))

        # Veredito: só métricas de desempenho/recuperação — a severidade do
        # afundamento (V min) é contexto e fica de fora
        statuses = [
            iae_cls,
            self._classify(m.get("ISE"), ISE_THRESH),
            ts_cls,
            peak_cls,
            dp_cls,
            self._classify(dq, DQ_THRESH),
        ]
        if "bad" in statuses:
            verdict_cls, verdict_txt = "bad",     "Desempenho crítico"
        elif "warn" in statuses:
            verdict_cls, verdict_txt = "warn",    "Desempenho em atenção"
        elif "good" in statuses:
            verdict_cls, verdict_txt = "good",    "Desempenho bom"
        else:
            verdict_cls, verdict_txt = "neutral", "Dados insuficientes"

        if parts:
            items = "".join(
                f'<li class="{cls}"><b>{label}</b> — {text}</li>'
                for cls, label, text in parts
            )
            body = f'<ul class="story-list">{items}</ul>'
        else:
            body = ('<p class="story-text">Dados insuficientes para análise '
                    'narrativa.</p>')
        title = "Diagnóstico — regime permanente" if is_regime else "Diagnóstico pós-falta"

        return (
            f'<div class="story {verdict_cls}">'
            f'<div class="story-body">'
            f'<p class="story-title">{title}</p>'
            f'{body}'
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
.h-uerj-logo { height: 36px; width: auto; flex-shrink: 0 }
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
.story-list {
  list-style: none; margin: 0; padding: 0;
  font-size: 13px; color: var(--text); line-height: 1.55;
  display: flex; flex-direction: column; gap: 6px;
}
.story-list li { position: relative; padding-left: 18px }
.story-list li::before {
  content: ""; position: absolute; left: 0; top: .42em;
  width: 9px; height: 9px; border-radius: 50%;
  background: var(--muted);
}
.story-list li.good::before { background: #16a34a }
.story-list li.warn::before { background: #d97706 }
.story-list li.bad::before  { background: #dc2626 }
[data-theme="dark"] .story-list li.good::before { background: #4ade80 }
[data-theme="dark"] .story-list li.warn::before { background: #fbbf24 }
[data-theme="dark"] .story-list li.bad::before  { background: #f87171 }
.story-list b { font-weight: 600 }
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
.spec-hint { font-size: 10.5px; color: var(--muted); letter-spacing: .2px }
#plot-res, #plot-inv, #plot-sys, #plot-spec { width: 100% }

/* ── Abas de gráficos ── */
.tab-bar {
  display: flex; gap: 4px;
  border-bottom: 1.5px solid var(--border);
  margin-bottom: 16px;
}
.tab-btn {
  font-family: inherit; font-size: 13px; font-weight: 600;
  padding: 9px 16px 8px;
  background: transparent; border: none;
  border-bottom: 2.5px solid transparent;
  margin-bottom: -1.5px;
  color: var(--muted); cursor: pointer;
  transition: color .18s, border-color .18s;
  white-space: nowrap;
}
.tab-btn:hover  { color: var(--text) }
.tab-btn.active { color: var(--accent); border-bottom-color: var(--accent) }

/* ── Cards clicáveis ── */
.card.clickable { cursor: pointer }
.card.clickable:hover { border-color: var(--accent) }

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
.diag-btn.active { background: var(--accent); color: #fff; border-color: var(--accent) }
[data-theme="dark"] .diag-btn.active { color: #0f172a }
.diag-btn:disabled { opacity: .4; cursor: not-allowed; pointer-events: none }

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

/* ── Tabela comparativa ── */
.table-wrap { overflow-x: auto; padding: 4px 4px 8px }
.cmp-table { width: 100%; border-collapse: collapse; font-size: 12.5px }
.cmp-table th, .cmp-table td { padding: 9px 14px; text-align: right; white-space: nowrap }
.cmp-table th:first-child, .cmp-table td:first-child { text-align: left }
.cmp-table thead th {
  font-size: 10.5px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .5px; color: var(--muted);
  border-bottom: 1.5px solid var(--border);
  cursor: pointer; user-select: none;
}
.cmp-table thead th:hover { color: var(--text) }
.cmp-table tbody tr { border-bottom: 1px solid var(--border); cursor: pointer }
.cmp-table tbody tr:hover { background: var(--bg) }
.cmp-table tbody tr.cmp-active { background: var(--badge-bg) }
.cmp-label { font-weight: 600; color: var(--text) }
.cmp-good    { color: #16a34a; font-weight: 600 }
.cmp-warn    { color: #b45309; font-weight: 600 }
.cmp-bad     { color: #dc2626; font-weight: 600 }
.cmp-neutral { color: var(--muted) }
[data-theme="dark"] .cmp-good { color: #4ade80 }
[data-theme="dark"] .cmp-warn { color: #fbbf24 }
[data-theme="dark"] .cmp-bad  { color: #f87171 }

/* ── Espectro: seletor de fase e tabela de harmônicas ── */
.spec-phase-bar {
  display: flex; align-items: center; gap: 12px;
  padding: 10px 20px;
  border-bottom: 1px solid var(--border);
}
.harm-block { padding: 4px 20px 14px }
.harm-title {
  font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .6px; color: var(--muted);
  margin: 12px 0 6px;
}
.harm-table { width: 100%; border-collapse: collapse; font-size: 12px }
.harm-table th, .harm-table td {
  padding: 5px 9px; text-align: right; white-space: nowrap;
}
.harm-table thead th {
  font-size: 10.5px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .5px; color: var(--muted);
  border-bottom: 1.5px solid var(--border); text-align: center;
}
.harm-table thead th.harm-sub {
  text-transform: none; font-style: italic; font-size: 11px;
  border-bottom: 1px solid var(--border);
}
.harm-table tbody tr { border-bottom: 1px solid var(--border) }
.harm-table tbody tr:hover { background: var(--bg) }
.harm-h   { font-weight: 600; color: var(--text); text-align: center !important }
.harm-val { color: var(--text) }
.harm-top {
  font-weight: 700; color: var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, transparent);
}
.harm-lo  { color: var(--muted); opacity: .5 }
.harm-na  { color: var(--muted) }
.harm-first { border-left: 1.5px solid var(--border) }

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
