"""
renderer.py — Gera o HTML final com header, cards de métricas e Plotly embutido.

Classe principal: HTMLRenderer
    .render(out_path)  → escreve o arquivo HTML e retorna o Path
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import plotly
import plotly.graph_objects as go

from .config import T_FAULT, TOL_RAD
from .loader import SimData


class HTMLRenderer:
    """Renderiza o relatório HTML completo a partir de SimData + figura Plotly."""

    def __init__(
        self,
        data: SimData,
        fig: go.Figure,
        trace_map: list[tuple[int, str, str]],
    ) -> None:
        self._d = data
        self._fig = fig
        self._trace_map = trace_map

    # ── API pública ──────────────────────────────────────────────────────────

    def render(self, out_path: Path) -> Path:
        """Gera o HTML e salva em out_path. Retorna o Path."""
        html = self._build_html()
        out_path.write_text(html, encoding="utf-8")
        return out_path

    # ── internos: composição do HTML ─────────────────────────────────────────

    def _build_html(self) -> str:
        fig_json   = self._fig.to_json()
        n_panels   = self._count_panels()
        light_cols = json.dumps([c for _, c, _ in self._trace_map])
        dark_cols  = json.dumps([c for _, _, c in self._trace_map])
        trace_idx  = json.dumps([i for i, _, _ in self._trace_map])
        cards_html = self._cards_html()

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

<!-- ── Header ── -->
<header class="header">
  <div class="h-left">
    <div class="h-logo">φ</div>
    <div>
      <div class="h-title">SRF-PLL &nbsp;·&nbsp; IEEE 9-Bus</div>
      <div class="h-sub">Análise pós-falta &nbsp;·&nbsp; T<sub>fault</sub> = {T_FAULT} s</div>
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

<!-- ── Main ── -->
<main class="main">

  <div class="cards">{cards_html}
  </div>

  <div class="chart-wrap">
    <div class="chart-header">
      <span class="chart-title">Sinais temporais</span>
      <span class="fault-badge">⚡ Falta em t = {T_FAULT} s</span>
    </div>
    <div id="plot"></div>
  </div>

  <div class="footer">
    <span>SRF-PLL Analyzer</span>
    <span class="footer-dot"></span>
    <span>Plotly {plotly.__version__}</span>
    <span class="footer-dot"></span>
    <span>TCC UERJ 2025</span>
  </div>

</main>

<!-- ── Scripts ── -->
<script>
var figData = {fig_json};
var gd = document.getElementById("plot");

Plotly.newPlot(gd, figData.data, figData.layout, {{
  responsive: true,
  displaylogo: false,
  modeBarButtonsToRemove: ["select2d","lasso2d","autoScale2d"],
  toImageButtonOptions: {{ format: "svg", filename: "pll_metrics" }},
}});

var isDark = false;

var LAYOUT_LIGHT = {{
  paper_bgcolor: "#ffffff", plot_bgcolor: "#ffffff",
  "font.color": "#0f172a",
  "legend.bgcolor": "rgba(0,0,0,0)",
  "hoverlabel.bgcolor": "#ffffff", "hoverlabel.bordercolor": "#e2e8f0",
}};
var LAYOUT_DARK = {{
  paper_bgcolor: "#111827", plot_bgcolor: "#111827",
  "font.color": "#f9fafb",
  "legend.bgcolor": "rgba(0,0,0,0)",
  "hoverlabel.bgcolor": "#1f2937", "hoverlabel.bordercolor": "#374151",
}};

var n = {n_panels};
for (var i = 1; i <= n; i++) {{
  var s = i === 1 ? "" : String(i);
  LAYOUT_LIGHT["xaxis" + s + ".gridcolor"]     = "#f1f5f9";
  LAYOUT_LIGHT["xaxis" + s + ".zerolinecolor"] = "#e2e8f0";
  LAYOUT_LIGHT["yaxis" + s + ".gridcolor"]     = "#f1f5f9";
  LAYOUT_LIGHT["yaxis" + s + ".zerolinecolor"] = "#e2e8f0";
  LAYOUT_DARK ["xaxis" + s + ".gridcolor"]     = "#1f2937";
  LAYOUT_DARK ["xaxis" + s + ".zerolinecolor"] = "#374151";
  LAYOUT_DARK ["yaxis" + s + ".gridcolor"]     = "#1f2937";
  LAYOUT_DARK ["yaxis" + s + ".zerolinecolor"] = "#374151";
}}

var lightColors = {light_cols};
var darkColors  = {dark_cols};
var traceIdx    = {trace_idx};

function toggleTheme() {{
  isDark = !isDark;
  document.documentElement.setAttribute("data-theme", isDark ? "dark" : "light");
  Plotly.relayout(gd, isDark ? LAYOUT_DARK : LAYOUT_LIGHT);
  var cols = isDark ? darkColors : lightColors;
  traceIdx.forEach(function(ti, i) {{
    Plotly.restyle(gd, {{"line.color": [cols[i]]}}, [ti]);
  }});
  document.getElementById("ico").textContent = isDark ? "☀️" : "🌙";
  document.getElementById("lbl").textContent = isDark ? "Light mode" : "Dark mode";
}}
</script>

</body>
</html>"""

    # ── internos: cards ──────────────────────────────────────────────────────

    def _cards_html(self) -> str:
        m = self._d.metrics

        def _v(val, decimals):
            return f"{val:.{decimals}f}" if val is not None else "—"

        cards = [
            ("IAE",  _v(m.get("IAE"), 3), "rad·s",  "∫|e| dt",
             "Erro de fase acumulado (pós-falta)"),
            ("ISE",  _v(m.get("ISE"), 4), "rad²·s", "∫e² dt",
             "Energia do erro de fase"),
            ("tₛ",   _v(m.get("ts"),  3), "s",
             f"±{np.degrees(TOL_RAD):.1f}°",
             "Tempo de acomodação do PLL"),
            ("ΔP",   _v(m.get("dP"),  3), "pu",     "pós-falta",
             "Oscilação de potência ativa"),
            ("ΔQ",   _v(m.get("dQ"),  3), "pu",     "pós-falta",
             "Oscilação de potência reativa"),
        ]

        return "\n".join(
            f"""
    <div class="card" title="{tip}">
      <p class="c-name">{name}</p>
      <p class="c-val">{val}<span class="c-unit">{unit}</span></p>
      <p class="c-sub">{sub}</p>
    </div>"""
            for name, val, unit, sub, tip in cards
        )

    # ── internos: contagem de painéis ────────────────────────────────────────

    def _count_panels(self) -> int:
        """Reconta quantos subplots existem na figura."""
        layout = self._fig.layout
        count = 1
        i = 2
        while getattr(layout, f"yaxis{i}", None) is not None:
            count += 1
            i += 1
        return count

    # ── internos: CSS ────────────────────────────────────────────────────────

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
body, .card, .header, .chart-wrap, .badge, .toggle-btn,
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

/* ── Layout ── */
.main {
  max-width: 1200px; margin: 0 auto;
  padding: 28px 24px 48px;
}

/* ── Cards ── */
.cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px; margin-bottom: 22px;
}
@media(max-width: 720px){ .cards { grid-template-columns: repeat(3,1fr) } }
@media(max-width: 460px){ .cards { grid-template-columns: repeat(2,1fr) } }

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
[data-theme="dark"] .card::before {
  background: linear-gradient(90deg, #60a5fa, #a78bfa);
}
.card:hover {
  box-shadow: var(--sh-md); transform: translateY(-2px);
  transition: box-shadow .18s, transform .18s,
              background .28s, border-color .28s;
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

/* ── Chart ── */
.chart-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--sh);
  overflow: hidden; padding: 4px 4px 0;
}
.chart-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px 10px;
  border-bottom: 1px solid var(--border);
}
.chart-title {
  font-size: 13px; font-weight: 600; color: var(--text);
  display: flex; align-items: center; gap: 8px;
}
.fault-badge {
  font-size: 10px; font-weight: 600; color: #b45309;
  background: #fef3c7; border-radius: 6px; padding: 2px 8px;
}
[data-theme="dark"] .fault-badge { color: #fcd34d; background: #451a03 }
#plot { width: 100% }

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
"""
