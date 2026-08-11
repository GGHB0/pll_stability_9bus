"""
renderer.py — Gera o HTML final com seletor de cenário, cards e Plotly embutido.

HTMLRenderer(scenarios).render(out_path) → escreve o HTML e retorna o Path.
scenarios: dict[key, {data, label, fig_inv, fig_sys,
                      figs_spec, tms_spec, spec_harm,
                      tm_inv, tm_sys}]
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
    T_SETTLE, LVRT_THRESHOLD, F_FUND_HZ, VBUS_AVG_THRESH,
    SPEC_SEG_LIMIT_FACTOR, CURR_ODD_LIMIT_PU, CURR_ODD_LIMIT_11_16_PU, CURR_EVEN_LIMITS_PU,
    VOLT_INDIVIDUAL_LIMIT_PU, DQ_UNBALANCE_WARN_PU, DQ_UNBALANCE_HIGH_PU,
)
from ..pipeline.loader import SimData


class HTMLRenderer:
    """Renderiza relatório HTML multi-cenário com seletor e duas seções de gráficos."""

    _SPEC_MODES = ("a", "b", "c", "d", "q")
    _HARM_MODES_ABC = ("a", "b", "c")
    _HARM_MODES_DQ = ("d", "q")
    _HARM_LO_PU = 0.02   # tabela de harmônicas: apagado se amp < (pu)
    _DQ_BIN_ORDERS = {
        0: "fund. (DC)",
        1: "—",
        2: "fund. seq. neg.",
        3: "2ª/4ª",
        4: "—",
        5: "—",
        6: "5ª/7ª",
        7: "—",
        8: "—",
        9: "8ª/10ª",
        10: "—",
        11: "—",
        12: "11ª/13ª",
    }
    # Linhas com bin dq fisicamente significativo (fundamental em DC, colisão
    # de ordens, ou fundamental de sequência negativa) — as demais (k sem
    # entrada aqui) só mostrariam ruído de fundo sem critério, e ficam fora
    # da tabela dq.
    _DQ_TABLE_ROWS = tuple(k for k, v in _DQ_BIN_ORDERS.items() if v != "—")

    # Contexto de topologia por local de falta (loc = key.split("/")[0]).
    # Só as linhas cuja topologia muda o diagnóstico entram aqui: 7-8 é
    # circuito único (2 trechos em série, confirmado no .slx: 5 km + 45 km
    # com disjuntor em cada ponta); 8-9 é circuito duplo (2 trechos de
    # 100 km em paralelo, cada um ligando Bus8-Bus9 diretamente) — a falta
    # atinge só um dos dois, o outro segue em serviço.
    _LINE_TOPOLOGY = {
        "line7_8": {
            "val": "1", "unit": "circuito",
            "sub": "falta no único caminho B7–B8",
            "tip": "Linha 7-8 é um circuito único no modelo (dois trechos "
                   "em série entre as barras 7 e 8). A falta interrompe o "
                   "único caminho direto nesse trecho — não há circuito "
                   "paralelo de reserva.",
            "story": "Linha 7-8 é um circuito único entre as barras 7 e "
                      "8 — a falta interrompe o único caminho direto nesse "
                      "trecho, sem circuito paralelo de reserva.",
        },
        "line8_9": {
            "val": "2", "unit": "circuitos",
            "sub": "falta em 1 dos 2, em paralelo",
            "tip": "Linha 8-9 é um circuito duplo no modelo — dois trechos "
                   "de 100 km em paralelo entre as barras 8 e 9. A falta é "
                   "aplicada em apenas um dos dois circuitos; o outro "
                   "permanece em serviço durante o distúrbio.",
            "story": "Linha 8-9 é um circuito duplo em paralelo — a falta "
                      "atinge apenas um dos dois circuitos entre as barras "
                      "8 e 9, e o outro permanece em serviço durante o "
                      "distúrbio.",
        },
    }

    def __init__(self, scenarios: dict[str, dict]) -> None:
        # {key: {data, label, fig_inv, fig_sys, figs_spec, tm_*}}
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
            fp = sc.get("figs_spec") or {}
            ti = sc["tm_inv"]
            ts = sc["tm_sys"]
            tp = sc.get("tms_spec") or {}
            sc_js[key] = {
                "invData":   json.loads(fi.to_json()),
                "sysData":   json.loads(fs.to_json()) if fs else None,
                "specData":  {m: json.loads(f.to_json()) for m, f in fp.items()},
                "specModes": list(fp.keys()),
                "invLight":  [x[1] for x in ti],
                "invDark":   [x[2] for x in ti],
                "invIdx":    [x[0] for x in ti],
                "sysLight":  [x[1] for x in ts],
                "sysDark":   [x[2] for x in ts],
                "sysIdx":    [x[0] for x in ts],
                "specLight": {m: [x[1] for x in tm] for m, tm in tp.items()},
                "specDark":  {m: [x[2] for x in tm] for m, tm in tp.items()},
                "specIdx":   {m: [x[0] for x in tm] for m, tm in tp.items()},
                "label":     sc["label"],
                "cardsHtml": self._cards_html(d, key),
                "storyHtml": self._story_html(d, key),
                "specTableHtml": self._spec_table_html(sc.get("spec_harm") or {}),
                "metricsRow": self._table_row_data(d),
                "hasInv":    True,
                "hasSys":    fs is not None,
                "hasRes":    True,
                "hasSpec":   bool(fp),
                "badPll":    sc.get("bad_pll", False),
                "tFault":    d.t_fault,
                "tClear":    d.t_clear,
                "tEnd":      d.t[-1] if len(d.t) > 0 else None,
            }

        scenarios_js  = json.dumps(sc_js)
        select_html   = self._select_html()
        pll_toggle_html = self._pll_toggle_html() if has_bad_pll else ""
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
      <span id="lbl">Dark mode</span>
    </button>
  </div>
</header>

<div class="filter-bar">
  <span class="filter-label">Cenário</span>
  {select_html}
  {pll_toggle_html}
  <button class="toggle-btn diag-btn" id="diagram-toggle" onclick="toggleDiagram()">Mapa IEEE 9-bus</button>
  <button class="toggle-btn diag-btn" id="table-toggle" onclick="toggleTable()">Comparativo</button>
  <button class="toggle-btn diag-btn" id="zoom-fault" onclick="toggleZoomFault()">Zoom na falta</button>
</div>

<main class="main">

  <div class="diagram-section" id="diagram-section">
{self._svg_section_html()}
    <p class="diag-hint">Clique em uma barra ou linha para selecionar o cenário de falta</p>
  </div>

  <div class="table-section" id="table-section" style="display:none">
    <div class="section-header">
      <span class="section-title">Comparativo de cenários</span>
    </div>
    <div class="table-wrap">
      <table class="cmp-table" id="cmp-table">
        <thead>
          <tr>
            <th data-key="label">Cenário</th>
            <th data-key="vavg">V méd. B2 (pu)</th>
            <th data-key="vavg_b1">V méd. B1 (pu)</th>
            <th data-key="vavg_b3">V méd. B3 (pu)</th>
          </tr>
        </thead>
        <tbody id="cmp-tbody"></tbody>
      </table>
    </div>
  </div>

  <div class="tab-bar" id="tab-bar">
    <button class="tab-btn active" id="tab-res"  onclick="switchTab('res')">Resumo</button>
    <button class="tab-btn" id="tab-inv"  onclick="switchTab('inv')">Inversor UFV</button>
    <button class="tab-btn" id="tab-sys"  onclick="switchTab('sys')">Sistema 9-Bus</button>
    <button class="tab-btn" id="tab-spec" onclick="switchTab('spec')">Espectro FFT</button>
  </div>

  <div class="chart-section" id="sec-res" style="display:none">
    <div id="cards-area"></div>
    <div id="story-area"></div>
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
  // _group_title (subtítulo de barra) usa xref "paper" + yref "y.../y{{n}} domain" e
  // precisa de override manual de cor por tema (não herda layout.font). _label
  // (barra de título do painel) usa xref "paper" + yref "paper" também, mas sua
  // fonte branca é fixa (texto sobre a barra azul) e deve ficar intocada nos dois
  // temas — senão perde contraste contra o fundo escuro da barra.
  var annotations = (figData.layout.annotations || []).map(function(a) {{
    var isGroupTitle = a.xref === "paper" && a.yref !== "paper";
    if (!isGroupTitle) return a;
    var color = isDarkMode ? "#cbd5e1" : "#334155";
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
  var data = themedData(figData.data, light, dark, idx, isDark);
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
  if (which !== "res" && _dirty[which]) {{
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
  var order = ["inv", "sys"];
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
var TIME_TABS = ["inv", "sys"];
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
  zbtn.innerHTML = zoomFault ? "Visão completa" : "Zoom na falta";
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
      + _cmpCell(r.vavg) + _cmpCell(r.vavg_b1) + _cmpCell(r.vavg_b3)
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
  btn.innerHTML = hidden ? "Ocultar mapa" : "Mapa IEEE 9-bus";
  btn.style.opacity = hidden ? "1" : "0.85";
}}

function toggleTheme() {{
  isDark = !isDark;
  document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
  TABS.forEach(function(t) {{ _dirty[t] = true; }});
  _renderChart(activeTab);
  _applyZoom();
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

    def _harm_cell_tier(self, kind: str, mode: str, k: int, seg_name: str,
                         v: float) -> tuple[str, str]:
        """Classe CSS + atributo title (tooltip) de uma célula da tabela de
        harmônicas. Prioridade: fundamental (k=1 em abc; k=0/DC em dq) >
        violação normativa em abc / desequilíbrio em dq (h=2ª) > valor
        quase-zero apagado > normal. A tabela dq (`_DQ_TABLE_ROWS`) só lista
        bins com ordem correspondente, fundamental de sequência negativa, ou
        a fundamental em DC (k=0) — bins "sem ordem"
        (`_DQ_BIN_ORDERS[k] == "—"`) já ficam fora da tabela e nunca chegam
        aqui, então não há mais ramo dedicado a eles.
        Limites por ordem harmônica (IEEE 519-2014/1547-2018) só valem no
        domínio abc; em dq só o bin de 120 Hz (fundamental de sequência
        negativa, não 2ª harmônica) tem critério (patamar empírico da TeseAGP) —
        ver kb/standards/harmonic_dq_frame_mapping.md e
        kb/standards/harmonic_significance_criteria.md. A faixa ímpar 11≤h<17
        (11ª/13ª) usa valor interino herdado da IEEE 519-2014 (Tabela 17 do
        guia 1547-2018 é imagem no PDF, não extraível) — ver
        kb/standards/harmonic_significance_criteria.md. O segmento "Durante a
        falta" tem o limite abc RELAXADO em 50% (SPEC_SEG_LIMIT_FACTOR), não
        suprimido: a nota 118 do IEEE 1547.2-2023 admite exceder os limites em
        50% em "startups or unusual conditions", já que são valores de projeto
        para regime com duração acima de 1 h. O critério de desequilíbrio dq,
        ao contrário, é sobre severidade do distúrbio — vale integralmente em
        todos os segmentos (é justamente durante a falta que a sequência
        negativa é mais relevante)."""
        if k == 1 and mode in ("a", "b", "c"):
            return "harm-fund", ""
        if k == 0 and mode in ("d", "q"):
            return ("harm-fund", " title=\"fundamental representada como DC "
                    "no referencial síncrono (Yazdani §4.3) — não é ruído "
                    "nem harmônico, é o próprio ponto de operação\"")
        if k > 1 and mode in ("a", "b", "c"):
            if kind == "i":
                if k % 2:
                    if k < 11:
                        limit, norm = CURR_ODD_LIMIT_PU, "IEEE 519-2014 Tab.2 / IEEE 1547-2018 §7.3"
                    elif k < 17:
                        limit, norm = CURR_ODD_LIMIT_11_16_PU, "IEEE 519-2014 Tab.2 (11≤h<17) — valor 1547-2018 Tab.17 a confirmar"
                    else:
                        limit, norm = None, ""
                else:
                    limit = CURR_EVEN_LIMITS_PU.get(k)
                    norm = "IEEE 1547-2018 §7.3 (Relaxed Evens)"
            else:
                limit = VOLT_INDIVIDUAL_LIMIT_PU
                norm = "IEEE 519-2014 Tab.1"
            factor = SPEC_SEG_LIMIT_FACTOR.get(seg_name, 1.0)
            if limit is not None and v >= limit * factor:
                relax = ("" if factor == 1.0 else
                         f"; limite {limit * 100:.1f}% relaxado ×{factor:g} "
                         "em condição inusual, IEEE 1547.2-2023 nota 118")
                # 2ª harmônica de corrente, pré-falta/Regime: excesso é
                # majoritariamente vazamento espectral de medição (chirp de
                # frequência dentro da janela, rede ainda em resposta de
                # droop), não distorção real do inversor — achado e correção
                # em kb/standards/harmonic_frequency_leakage.md. Âmbar em vez
                # de vermelho aqui não afrouxa o limite (o número mostrado
                # continua o mesmo, sem viés) — só evita marcar como defeito
                # do inversor algo que já se sabe ser majoritariamente
                # resíduo de medição documentado.
                if kind == "i" and k == 2 and seg_name in ("Pré-falta", "Regime"):
                    return ("harm-warn",
                            f" title=\"excede {limit * factor * 100:.1f}% "
                            f"({norm}) mas é majoritariamente vazamento espectral de "
                            "medição — a rede simulada ainda está em transitório de "
                            "droop quando a janela é capturada, não distorção real do "
                            "inversor (ver nota técnica vazamento_espectral_harmonicos.pdf)\"")
                return ("harm-viol",
                        f" title=\"excede {limit * factor * 100:.1f}% "
                        f"({norm}{relax})\"")
        elif mode in ("d", "q") and k == 2:
            if v >= DQ_UNBALANCE_HIGH_PU:
                return ("harm-unb", " title=\"desequilíbrio de sequência "
                        f"negativa ≥{DQ_UNBALANCE_HIGH_PU * 100:.0f}% (TeseAGP)\"")
            if v >= DQ_UNBALANCE_WARN_PU:
                return ("harm-warn", " title=\"desequilíbrio de sequência "
                        f"negativa ≥{DQ_UNBALANCE_WARN_PU * 100:.0f}% (TeseAGP)\"")
        if v < self._HARM_LO_PU:
            return "harm-lo", ""
        return "", ""

    def _harm_legend_html(self, has_relaxed_seg: bool) -> str:
        """Legenda da tabela de harmônicas, em duas camadas: linha de swatches
        sempre visível + `<details>` "Como ler esta tabela" com um bloco por
        critério e as referências em forma curta.

        Regra editorial (kb/standards/harmonic_norm_application.md, seção "O
        que vai na tela vs. o que fica no KB"): aqui entra só a REGRA aplicada
        — o limite, a base do percentual e a norma citada. A genealogia do
        número (razão Isc/IL, nota "c" da Tab.2 do IEEE 519-2014, por que IL
        foi descartado como base) fica no KB, não na tela."""
        evens = sorted(CURR_EVEN_LIMITS_PU.items())
        ev_lim = " / ".join(f"{v * 100:g}%" for _, v in evens)
        ev_ord = " / ".join(f"{k}ª" for k, _ in evens)
        items = [
            ("a/b/c — conformidade normativa",
             "Vermelho: a amplitude daquela ordem passa do limite individual. "
             f"Corrente: {CURR_ODD_LIMIT_PU * 100:g}% nos ímpares, {ev_lim} na "
             f"{ev_ord} — percentuais da corrente nominal do inversor. "
             f"Tensão: {VOLT_INDIVIDUAL_LIMIT_PU * 100:g}%, sobre a nominal da "
             "Barra 2 (20 kV). Fontes: IEEE 1547-2018 §7.3 (corrente), "
             "IEEE 519-2014 Tabela 1 (tensão). Ímpares 11ª/13ª: 2,0% — valor interino herdado da IEEE 519-2014 (Tabela 17 da 1547-2018 ainda não confirmada, ver KB). "
             "Âmbar (só na 2ª harmônica de corrente, colunas Pré-falta/Regime): "
             "passa do limite, mas o excesso é majoritariamente vazamento espectral "
             "de medição, não distorção real do inversor — a rede simulada ainda "
             "está em transitório de droop quando a janela é capturada. O número "
             "mostrado não muda, só a cor deixa de sinalizar defeito de projeto."),
            ("Tabela dq — desequilíbrio, não conformidade",
             "0 Hz é a própria fundamental, representada como DC no "
             "referencial síncrono (não é ruído nem harmônico) — serve de "
             "referência de escala para as demais linhas. 120 Hz é a "
             "fundamental refletida em sequência negativa (não a 2ª "
             f"harmônica): âmbar ≥{DQ_UNBALANCE_WARN_PU * 100:g}%, vermelho "
             f"≥{DQ_UNBALANCE_HIGH_PU * 100:g}%. Patamar empírico (TeseAGP "
             "§5.2.2), sem base normativa. As linhas de 180/360/540/720 Hz "
             "são só informativas — a transformada de Park desloca cada "
             "ordem conforme a sequência, então cada bin dq junta duas "
             "ordens abc diferentes (coluna \"dq: ordens\": 180 Hz = 2ª+4ª, "
             "360 Hz = 5ª+7ª etc.) e não tem limite individual verificável; "
             "conformidade por ordem só existe na tabela abc. Linhas sem "
             "colisão nem fundamental (60/240/300/420/480/600/660 Hz) ficam "
             "fora da tabela dq — mostrariam só ruído de fundo."),
        ]
        if has_relaxed_seg:
            items.append((
                "O * em “Durante a falta”",
                "limite abc relaxado em 50% (ex.: 6% no lugar de 4%): a norma "
                "admite exceder os limites em condição inusual, por serem "
                "valores de projeto para regime acima de 1 h (IEEE 1547.2-2023, "
                "nota 118). O critério de desequilíbrio dq não é relaxado — é "
                "ali que a sequência negativa é maior."))
        rows = "".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in items)
        return (
            "<div class='harm-legend'>"
            "<p class='harm-leg-row'>"
            "<span class='harm-leg-sw harm-leg-viol'></span>excede limite "
            "normativo<span class='harm-leg-dot'>·</span>"
            "<span class='harm-leg-sw harm-leg-warn'></span>excesso atribuído a "
            "vazamento de medição (2ª abc) ou desequilíbrio dq intermediário"
            "<span class='harm-leg-dot'>·</span>"
            "<span class='harm-leg-sw harm-leg-unb'></span>desequilíbrio dq alto"
            "<span class='harm-leg-dot'>·</span>"
            "<span class='harm-leg-sw harm-leg-fund'></span>fundamental, sem "
            "limite<span class='harm-leg-dot'>·</span>"
            "<span class='harm-leg-sw harm-leg-lo'></span>abaixo de "
            f"{self._HARM_LO_PU * 100:g}%"
            "</p>"
            "<details class='harm-help'><summary>Como ler esta tabela</summary>"
            f"{self._harm_criteria_html(has_relaxed_seg)}"
            f"<dl>{rows}</dl>"
            "<p class='harm-refs'>IEEE Std 519-2014 · IEEE Std 1547.2-2023 · "
            "ALVES, A. G. P. Tese (Doutorado), COPPE/UFRJ, 2022.</p>"
            "</details></div>"
        )

    @staticmethod
    def _sw(*classes: str) -> str:
        """Um ou mais swatches de cor da legenda, na ordem dada. Reaproveita as
        classes `.harm-leg-*` da linha compacta, então uma troca de token de
        tema vale para a legenda e para a tabela de critérios de uma vez."""
        return "".join(f"<span class='harm-leg-sw harm-leg-{c}'></span>"
                       for c in classes)

    def _harm_criteria_html(self, has_relaxed_seg: bool) -> str:
        """Resumo tabular dos critérios de formatação condicional: por grandeza
        e ordem, o limite aplicado, a cor que a célula recebe e a norma de
        origem. Espelha a seção 6.1 da nota `output/normas_harmonicos.pdf` — as
        duas precisam continuar batendo, e por isso os números vêm todos das
        constantes de `settings.py`, nunca escritos à mão aqui."""
        evens = sorted(CURR_EVEN_LIMITS_PU.items())
        ev_lim = " / ".join(f"{v * 100:g}%" for _, v in evens)
        ev_ord = "/".join(f"{k}ª" for k, _ in evens)
        rows = [
            ("Corrente, ímpares 3ª–9ª", f"{CURR_ODD_LIMIT_PU * 100:g}%",
             self._sw("viol"), "IEEE 1547-2018 §7.3"),
            ("Corrente, ímpares 11ª–15ª", f"{CURR_ODD_LIMIT_11_16_PU * 100:g}%",
             self._sw("viol"), "IEEE 519-2014 Tab.2 (interino)"),
            (f"Corrente, {ev_ord}", ev_lim, self._sw("viol", "warn"),
             "IEEE 1547-2018 §7.3"),
            ("Tensão, qualquer ordem", f"{VOLT_INDIVIDUAL_LIMIT_PU * 100:g}%",
             self._sw("viol"), "IEEE 519-2014 Tab.1"),
            ("Desequilíbrio dq, 120 Hz",
             f"{DQ_UNBALANCE_WARN_PU * 100:g}% / {DQ_UNBALANCE_HIGH_PU * 100:g}%",
             self._sw("warn", "unb"), "TeseAGP §5.2.2 (empírico)"),
            ("Fundamental (1ª abc, 0 Hz dq)", "—", self._sw("fund"),
             "referência de escala, sem limite"),
            (f"Abaixo de {self._HARM_LO_PU * 100:g}%", "—", self._sw("lo"),
             "sem critério aplicável"),
        ]
        if has_relaxed_seg:
            factor = SPEC_SEG_LIMIT_FACTOR.get("Durante a falta", 1.0)
            rows.append(("Durante a falta", f"base ×{factor:g}", "",
                         "IEEE 1547.2-2023 nota 118"))
        body = "".join(
            f"<tr><th>{grand}</th><td>{lim}</td><td class='harm-crit-sw'>{sw}</td>"
            f"<td>{norma}</td></tr>" for grand, lim, sw, norma in rows)
        return (
            "<table class='harm-crit'><thead><tr><th>Grandeza e ordem</th>"
            "<th>Limite</th><th>Cor</th><th>Norma</th></tr></thead>"
            f"<tbody>{body}</tbody></table>"
            "<p class='harm-crit-note'>Duas cores na mesma linha indicam um "
            "segundo caso: a 2ª harmônica de corrente sai em âmbar nas colunas "
            "Pré-falta/Regime, por ser majoritariamente vazamento espectral de "
            "medição; o desequilíbrio é âmbar no patamar de alerta e vermelho "
            "no severo. Percentuais de corrente são da nominal do inversor; os "
            "de tensão, da nominal da Barra 2.</p>")

    def _harm_subtable_html(self, per_seg: dict, segs: list, kind: str,
                             title: str, domain: str, modes: tuple,
                             rows_k: tuple) -> str:
        """Uma subtabela (abc OU dq) de um bloco (Corrente/Tensão). Separadas
        porque abc e dq não compartilham semântica por linha: em abc, k é a
        k-ésima harmônica, checável por ordem contra IEEE 519/1547; em dq, k
        é um bin de colisão (duas ordens abc de sequências opostas) ou a
        fundamental refletida em sequência negativa (k=2/120 Hz) — só essa
        linha tem critério normativo. `rows_k` já vem filtrado pelo chamador
        (`range(1,13)` em abc; `_DQ_TABLE_ROWS` em dq, que descarta os bins
        sem ordem correspondente — mostrariam só ruído sem destaque). Ver
        kb/standards/harmonic_dq_frame_mapping.md."""
        if not any((per_seg.get(s) or {}).get(mo) for s in segs for mo in modes):
            return ""
        n_modes = len(modes)
        ord_label = "abc: h" if domain == "abc" else "dq: ordens"
        head1 = f"<tr><th rowspan='2'>f (Hz)</th><th rowspan='2'>{ord_label}</th>"
        head2 = "<tr>"
        for s in segs:
            star = " *" if SPEC_SEG_LIMIT_FACTOR.get(s, 1.0) != 1.0 else ""
            head1 += f"<th colspan='{n_modes}' class='harm-first'>{s}{star}</th>"
            for j, mo in enumerate(modes):
                first = " harm-first" if j == 0 else ""
                head2 += f"<th class='harm-sub{first}'>{mo}</th>"
        head1 += "</tr>"
        head2 += "</tr>"
        rows: list[str] = []
        for k in rows_k:
            ord_cell = f"{k}ª" if domain == "abc" else self._DQ_BIN_ORDERS[k]
            dqord_cls = "" if domain == "abc" else " harm-dqord"
            cells = (f"<td class='harm-h'>{k * F_FUND_HZ:.0f}</td>"
                     f"<td class='harm-h{dqord_cls}'>{ord_cell}</td>")
            for s in segs:
                mode_amps = per_seg.get(s) or {}
                for j, mo in enumerate(modes):
                    first = " harm-first" if j == 0 else ""
                    amps = mode_amps.get(mo)
                    v = amps[k] if amps else None
                    if v is None:
                        cells += f"<td class='harm-na{first}'>—</td>"
                        continue
                    tier, title_attr = self._harm_cell_tier(kind, mo, k, s, v)
                    tier_cls = f" {tier}" if tier else ""
                    cells += (f"<td class='harm-val{first}{tier_cls}'"
                              f"{title_attr}>{v:.3g}</td>")
            rows.append(f"<tr>{cells}</tr>")
        domain_label = "abc" if domain == "abc" else "d/q"
        return (
            f"<div class='harm-block'>"
            f"<p class='harm-title'>Harmônicas ({domain_label}) — {title} (pu)</p>"
            f"<div class='table-wrap'><table class='harm-table'>"
            f"<thead>{head1}{head2}</thead>"
            f"<tbody>{''.join(rows)}</tbody></table></div></div>"
        )

    def _spec_table_html(self, harm: dict) -> str:
        """Duas tabelas por bloco (Corrente UFV / Tensão UFV): uma abc
        (linhas h=1ª...12ª, checagem por ordem) e uma dq (linhas só nos bins
        fisicamente significativos — ver `_DQ_TABLE_ROWS`), separadas porque
        misturar as duas na mesma linha (mesma frequência k·60 Hz) confundia
        o significado de cada coluna — ver kb/standards/harmonic_dq_frame_mapping.md
        e `_harm_subtable_html`. Valores vêm do SpectrumBuilder (combinação RMS
        de 3 bins do espectro de janela retangular, IEEE 519-2014 §4.1);
        células comparadas a limites
        normativos reais via `_harm_cell_tier` (ver docstring lá)."""
        segs = harm.get("segs") or []
        if not segs:
            return ""
        has_relaxed_seg = any(SPEC_SEG_LIMIT_FACTOR.get(s, 1.0) != 1.0
                              for s in segs)
        blocks: list[str] = []
        for kind, title in (("i", "Corrente UFV"), ("v", "Tensão UFV")):
            per_seg = harm.get(kind) or {}
            if not any(per_seg.get(s) for s in segs):
                continue
            abc_html = self._harm_subtable_html(
                per_seg, segs, kind, title, "abc",
                self._HARM_MODES_ABC, tuple(range(1, 13)))
            dq_html = self._harm_subtable_html(
                per_seg, segs, kind, title, "dq",
                self._HARM_MODES_DQ, self._DQ_TABLE_ROWS)
            blocks.append(abc_html)
            blocks.append(dq_html)
        if blocks:
            blocks.append(self._harm_legend_html(has_relaxed_seg))
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
        """Uma linha da tabela comparativa: {métrica: {val, raw, cls}} por cenário.

        Só severidade do distúrbio (V médio por barra): as métricas derivadas do
        erro de ângulo saíram da tabela junto com os cards — ver `_cards_html`."""
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

    def _cards_html(self, data: SimData, key: str) -> str:
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

        # Grupo "Desempenho do PLL" removido (2026-08-09): IAE, ISE, tₛ,
        # |θ_err| pico e Erro R.P. eram todos derivados do erro de ângulo
        # θ̂ − θ_rede, sem fonte que sustente esses acumulados/média/pico como
        # medida de desempenho do PLL. O sinal em si continua no painel
        # "Erro de fase" do chart.py — só as métricas derivadas saíram.

        # Severidade: contexto do distúrbio — cor indica profundidade do sag.
        # "V residual" = tensão remanescente do afundamento (PRODIST/IEC),
        # aqui a MÉDIA (não o pior instante): em regime cobre o período
        # inteiro pós-T_SETTLE; numa falta, só a janela t_fault–t_clear.
        # Sem curto, o card volta a "V médio".
        vlab = "V médio" if is_regime else "V residual médio"
        janela_b2 = (f"t ≥ {T_SETTLE:.2f} s" if is_regime else
                     f"t = {data.t_fault:.2f}–{data.t_clear:.2f} s"
                     if data.t_clear is not None else f"t ≥ {data.t_fault:.2f} s")
        sev_cards = [
            _card(f"{vlab} B2", _v(m.get("vavg"), 3), "pu", "POC do inversor (UFV)",
                  f"Tensão média na Barra 2 ({janela_b2}, LVRT ≥ {LVRT_THRESHOLD} pu) — "
                  "severidade do distúrbio",
                  self._classify(m.get("vavg"), VBUS_AVG_THRESH, lower_is_better=False),
                  target="|V| Bus 2"),
        ]
        for mkey, bus, sub in (("vavg_bus1", "B1", "barra do G1 (slack)"),
                               ("vavg_bus3", "B3", "barra do G3")):
            if m.get(mkey) is not None:
                janela_txt = "todo o período" if is_regime else "durante o curto"
                sev_cards.append(
                    _card(f"{vlab} {bus}", _v(m.get(mkey), 3), "pu", sub,
                          f"Tensão média na barra {bus[1]} ({janela_txt}) — "
                          "propagação do afundamento pela rede",
                          self._classify(m.get(mkey), VBUS_AVG_THRESH,
                                         lower_is_better=False),
                          target=f"|V| Bus {bus[1]}"))
        if data.t_fault is not None and data.t_clear is not None:
            dur_ms = (data.t_clear - data.t_fault) * 1e3
            sev_cards.append(
                _card("Duração", f"{dur_ms:.0f}", "ms",
                      f"t = {data.t_fault:.2f} – {data.t_clear:.2f} s",
                      "Duração da falta aplicada", "neutral"))
        topo = self._LINE_TOPOLOGY.get(key.split("/")[0])
        if topo:
            sev_cards.append(
                _card("Topologia", topo["val"], topo["unit"], topo["sub"],
                      topo["tip"], "neutral"))
        sev_label = "Sistema 9-Bus" if is_regime else "Severidade do distúrbio"

        return _group(sev_label, "".join(sev_cards))

    # ── Narrativa ────────────────────────────────────────────────────────────

    def _story_html(self, data: SimData, key: str) -> str:
        m         = data.metrics
        is_regime = data.t_fault is None
        vavg      = m.get("vavg")

        # (classe do semáforo, rótulo, texto) — vira <li> na lista
        parts: list[tuple[str, str, str]] = []

        # ── contexto: severidade do distúrbio ────────────────────────────────
        if is_regime:
            parts.append(("neutral", "Cenário",
                          "Operação em regime permanente, sem contingência aplicada — "
                          "métricas calculadas descartando o transitório de partida "
                          f"(t ≥ {T_SETTLE:.2f} s)."))
        elif vavg is not None:
            sev = self._classify(vavg, VBUS_AVG_THRESH, lower_is_better=False)
            dur = (f" de {(data.t_clear - data.t_fault) * 1e3:.0f} ms"
                   if data.t_clear is not None else "")
            if sev == "good":
                parts.append(("good", "Distúrbio",
                              f"Falta{dur} com afundamento leve na Barra 2 "
                              f"(V residual médio = {vavg:.3f} pu)."))
            elif sev == "warn":
                parts.append(("warn", "Distúrbio",
                              f"Falta{dur} com afundamento moderado na Barra 2 "
                              f"(V residual médio = {vavg:.3f} pu, abaixo do limiar LVRT)."))
            else:
                parts.append(("bad", "Distúrbio",
                              f"Falta{dur} com afundamento severo na Barra 2 "
                              f"(V residual médio = {vavg:.3f} pu) — condição crítica de LVRT."))

        # ── topologia do trecho (só faltas em linha; contexto, sem semáforo) ──
        topo = self._LINE_TOPOLOGY.get(key.split("/")[0])
        if topo:
            parts.append(("neutral", "Topologia", topo["story"]))

        # Itens de resposta do PLL (pico de fase, acomodação, erro de regime,
        # erro acumulado) e o chip de veredito saíram em 2026-08-09 junto com
        # os cards de erro de ângulo — ver `_cards_html`. Sobra o contexto do
        # cenário: severidade do afundamento e topologia do trecho.

        if parts:
            items = "".join(
                f'<li class="{cls}"><b>{label}</b> — {text}</li>'
                for cls, label, text in parts
            )
            body = f'<ul class="story-list">{items}</ul>'
        else:
            body = ('<p class="story-text">Dados insuficientes para descrever '
                    'o cenário.</p>')
        title = "Contexto — regime permanente" if is_regime else "Contexto do cenário"

        return (
            f'<div class="story neutral">'
            f'<div class="story-body">'
            f'<p class="story-title">{title}</p>'
            f'{body}'
            f'</div>'
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
  --danger:    #dc2626;
  --warn:      #ca8a04;
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
  --danger:    #f87171;
  --warn:      #fbbf24;
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
#plot-inv, #plot-sys, #plot-spec { width: 100% }
/* Resumo não tem section-header/plot próprios — cards + diagnóstico levam
   o padding que antes vinha de .main diretamente */
#sec-res { padding: 20px 20px 4px; }

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
.harm-fund {
  font-weight: 700; color: var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, transparent);
}
.harm-viol, .harm-unb {
  font-weight: 700; color: var(--danger);
  background: color-mix(in srgb, var(--danger) 14%, transparent);
  cursor: help;
}
.harm-warn {
  font-weight: 700; color: var(--warn);
  background: color-mix(in srgb, var(--warn) 14%, transparent);
  cursor: help;
}
.harm-lo  { color: var(--muted); opacity: .5 }
.harm-na  { color: var(--muted) }
.harm-dqord { font-weight: 500; color: var(--muted); font-size: 11px }
.harm-first { border-left: 1.5px solid var(--border) }
.harm-legend {
  font-size: 11px; color: var(--muted); padding: 6px 20px 12px;
  line-height: 1.55;
}
.harm-leg-row {
  display: flex; flex-wrap: wrap; align-items: center; gap: 5px;
  margin: 0 0 6px;
}
.harm-leg-dot { opacity: .45; margin: 0 3px }
.harm-leg-sw {
  display: inline-block; width: 11px; height: 11px; border-radius: 3px;
}
.harm-leg-viol, .harm-leg-unb { background: var(--danger) }
.harm-leg-warn { background: var(--warn) }
.harm-leg-fund { background: var(--accent) }
.harm-leg-lo   { background: var(--muted); opacity: .45 }
.harm-help > summary {
  cursor: pointer; font-weight: 700; color: var(--text);
  list-style: none; display: inline-flex; align-items: center; gap: 5px;
  padding: 2px 0;
}
.harm-help > summary::-webkit-details-marker { display: none }
.harm-help > summary::before {
  content: "\\25B8"; display: inline-block; font-size: 10px;
  transition: transform .18s;
}
.harm-help[open] > summary::before { transform: rotate(90deg) }
.harm-help dl { margin: 6px 0 0; max-width: 78ch }
.harm-help dt { font-weight: 700; color: var(--text); margin-top: 9px }
.harm-help dd { margin: 2px 0 0 }
.harm-crit {
  border-collapse: collapse; margin: 9px 0 0; max-width: 78ch;
  font-size: 11px;
}
.harm-crit th, .harm-crit td {
  text-align: left; padding: 4px 12px 4px 0;
  border-bottom: 1px solid var(--border);
}
.harm-crit thead th {
  font-weight: 700; color: var(--text); white-space: nowrap;
}
.harm-crit tbody th { font-weight: 500; color: var(--text) }
.harm-crit-sw { white-space: nowrap }
.harm-crit-sw .harm-leg-sw + .harm-leg-sw { margin-left: 3px }
.harm-crit-note { margin: 7px 0 0; max-width: 78ch }
.harm-refs { margin: 11px 0 0; font-size: 10px; opacity: .75 }

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
