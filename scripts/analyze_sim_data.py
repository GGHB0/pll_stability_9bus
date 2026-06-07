"""
analyze_sim_data.py
Lê output/sim_data.csv → gera output/pll_metrics.html

HTML totalmente customizado: header, cards de métricas, Plotly embutido,
toggle Light / Dark com transição suave.

Uso:
    .venv/Scripts/python.exe scripts/analyze_sim_data.py
"""

import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path
import json
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

PROJ_ROOT = Path(__file__).resolve().parent.parent
CSV       = PROJ_ROOT / "output" / "sim_data.csv"
T_FAULT   = 0.5
TOL_RAD   = 0.02

# ── Paletas de traço ───────────────────────────────────────────────────────────
L_CLR = ["#2563eb", "#dc2626", "#16a34a", "#ea580c", "#9333ea", "#0891b2"]
D_CLR = ["#60a5fa", "#f87171", "#4ade80", "#fb923c", "#c084fc", "#22d3ee"]

# ── Leitura ────────────────────────────────────────────────────────────────────
print(f"Lendo: {CSV}")
df = pd.read_csv(CSV)
print(f"Colunas: {list(df.columns)}")

t = df["t_s"].to_numpy()
P = df["P_pu"].to_numpy()
Q = df["Q_pu"].to_numpy()

has_ang = {"theta_pll_rad", "theta_ref_rad"} <= set(df.columns)
cols = set(df.columns)
has_dq     = {"id_pu", "iq_pu"} <= cols          # qualquer formato
has_dq_ref = {"id_ref_pu", "iq_ref_pu"} <= cols  # novo formato (ref + medido)

if "theta_err_rad" in df.columns:
    theta_err = df["theta_err_rad"].to_numpy()
elif has_ang:
    theta_err = (df["theta_pll_rad"] - df["theta_ref_rad"]).to_numpy()
else:
    theta_err = None

# ── Métricas ───────────────────────────────────────────────────────────────────
mask = t >= T_FAULT
print("\n=== Métricas pós-falta ===")

if theta_err is not None:
    t_pf, e_pf = t[mask], theta_err[mask]
    IAE = float(np.trapezoid(np.abs(e_pf), t_pf))
    ISE = float(np.trapezoid(e_pf**2,      t_pf))
    fora = t_pf[np.abs(e_pf) > TOL_RAD]
    ts   = float(fora[-1]) if len(fora) else float(t_pf[0])
    print(f"  IAE = {IAE:.4f} rad·s")
    print(f"  ISE = {ISE:.4f} rad²·s")
    print(f"  ts  = {ts:.4f} s")
else:
    IAE = ISE = ts = None
    print("  (sem ângulos — IAE/ISE/ts indisponíveis)")

dP = float(P[mask].max() - P[mask].min())
dQ = float(Q[mask].max() - Q[mask].min())
print(f"  ΔP  = {dP:.4f} pu")
print(f"  ΔQ  = {dQ:.4f} pu")

# ── Subplots Plotly ────────────────────────────────────────────────────────────
panels = []
if has_ang:               panels.append(("ang", "Ângulo (°)"))
if theta_err is not None: panels.append(("err", "Erro de fase (°)"))
panels.append(("P", "P (pu)"))
panels.append(("Q", "Q (pu)"))
if has_dq:
    if has_dq_ref:
        panels.append(("id",  "i_d (pu)"))
        panels.append(("iq",  "i_q (pu)"))
    else:
        panels.append(("dq_legacy", "Corrente dq (pu)"))
n = len(panels)

fig = make_subplots(rows=n, cols=1, shared_xaxes=True, vertical_spacing=0.05)

ci = 0
trace_map = []   # (trace_index, light_color, dark_color)

def add(trace, row, lc, dc):
    fig.add_trace(trace, row=row, col=1)
    trace_map.append((len(fig.data) - 1, lc, dc))

for i, (kind, _) in enumerate(panels, 1):
    lc, dc = L_CLR[ci % len(L_CLR)], D_CLR[ci % len(D_CLR)]

    if kind == "ang":
        add(go.Scatter(x=t, y=np.degrees(df["theta_pll_rad"]),
                       name="θ̂ PLL",  mode="lines",
                       line=dict(width=1.8, color=lc)), i, lc, dc)
        ci += 1
        lc2, dc2 = L_CLR[ci % len(L_CLR)], D_CLR[ci % len(D_CLR)]
        add(go.Scatter(x=t, y=np.degrees(df["theta_ref_rad"]),
                       name="θ rede", mode="lines",
                       line=dict(width=1.4, color=lc2, dash="dash")), i, lc2, dc2)
        ci += 1

    elif kind == "err":
        add(go.Scatter(x=t, y=np.degrees(theta_err),
                       name="Erro de fase", mode="lines",
                       line=dict(width=1.8, color=lc)), i, lc, dc)
        tol_deg = np.degrees(TOL_RAD)
        for sign in (+1, -1):
            fig.add_hline(y=sign * tol_deg,
                          line=dict(color="rgba(220,50,50,0.45)", width=1.1, dash="dash"),
                          row=i, col=1)
        ci += 1

    elif kind == "P":
        add(go.Scatter(x=t, y=P, name="P ativa", mode="lines",
                       line=dict(width=1.8, color=lc)), i, lc, dc)
        ci += 1

    elif kind == "Q":
        add(go.Scatter(x=t, y=Q, name="Q reativa", mode="lines",
                       line=dict(width=1.8, color=lc)), i, lc, dc)
        ci += 1

    elif kind == "dq_legacy":
        add(go.Scatter(x=t, y=df["id_pu"], name="i<sub>d</sub>", mode="lines",
                       line=dict(width=1.8, color=lc)), i, lc, dc)
        ci += 1
        lc2, dc2 = L_CLR[ci % len(L_CLR)], D_CLR[ci % len(D_CLR)]
        add(go.Scatter(x=t, y=df["iq_pu"], name="i<sub>q</sub>", mode="lines",
                       line=dict(width=1.4, color=lc2, dash="dot")), i, lc2, dc2)
        ci += 1

    elif kind == "id":
        # Sinal real (com ruído) — linha sólida
        add(go.Scatter(x=t, y=df["id_pu"],
                       name="i<sub>d</sub> medido", mode="lines",
                       line=dict(width=1.4, color=lc)), i, lc, dc)
        ci += 1
        lc2, dc2 = L_CLR[ci % len(L_CLR)], D_CLR[ci % len(D_CLR)]
        # Referência — tracejado, mais espesso
        add(go.Scatter(x=t, y=df["id_ref_pu"],
                       name="i<sub>d</sub> ref", mode="lines",
                       line=dict(width=2.0, color=lc2, dash="dash")), i, lc2, dc2)
        ci += 1

    elif kind == "iq":
        add(go.Scatter(x=t, y=df["iq_pu"],
                       name="i<sub>q</sub> medido", mode="lines",
                       line=dict(width=1.4, color=lc)), i, lc, dc)
        ci += 1
        lc2, dc2 = L_CLR[ci % len(L_CLR)], D_CLR[ci % len(D_CLR)]
        add(go.Scatter(x=t, y=df["iq_ref_pu"],
                       name="i<sub>q</sub> ref", mode="lines",
                       line=dict(width=2.0, color=lc2, dash="dash")), i, lc2, dc2)
        ci += 1

    # Rótulo do painel como anotação
    fig.add_annotation(
        text=f"<b>{panels[i-1][1]}</b>",
        xref="paper", yref=f"y{'' if i==1 else i} domain",
        x=0, y=1.0, xanchor="left", yanchor="bottom",
        font=dict(size=10, color="#6b7280"), showarrow=False,
    )
    fig.add_vline(x=T_FAULT,
                  line=dict(color="rgba(100,100,100,0.25)", width=1.1, dash="dot"),
                  row=i, col=1)
    fig.update_yaxes(gridcolor="#f0f2f5", zerolinecolor="#e5e7eb",
                     tickfont_size=10, row=i, col=1)

fig.update_xaxes(title_text="Tempo (s)", gridcolor="#f0f2f5",
                 zerolinecolor="#e5e7eb", tickfont_size=10)

fig.update_layout(
    margin=dict(t=16, b=16, l=66, r=16),
    paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
    font=dict(family="Inter, Segoe UI, system-ui, sans-serif", size=12, color="#111827"),
    legend=dict(orientation="h", x=0, y=-0.06, font_size=11,
                bgcolor="rgba(0,0,0,0)", borderwidth=0),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e5e7eb",
                    font_family="Inter, Segoe UI, system-ui, sans-serif",
                    font_size=11),
    height=248 * n,
)

fig_json   = fig.to_json()
light_cols = json.dumps([c for _, c, _ in trace_map])
dark_cols  = json.dumps([c for _, _, c in trace_map])
trace_idx  = json.dumps([idx for idx, _, _ in trace_map])

# ── Cards de métricas ──────────────────────────────────────────────────────────
def _v(v, d): return f"{v:.{d}f}" if v is not None else "—"

CARDS = [
    ("IAE",  _v(IAE, 3), "rad·s",  "∫|e| dt",    "Erro de fase acumulado"),
    ("ISE",  _v(ISE, 4), "rad²·s", "∫e² dt",     "Energia do erro"),
    ("tₛ",   _v(ts,  3), "s",      f"±{np.degrees(TOL_RAD):.1f}°", "Tempo de acomodação"),
    ("ΔP",   _v(dP,  3), "pu",     "pós-falta",   "Oscilação de potência ativa"),
    ("ΔQ",   _v(dQ,  3), "pu",     "pós-falta",   "Oscilação de potência reativa"),
]

cards_html = "\n".join(f"""
    <div class="card" title="{tip}">
      <p class="c-name">{name}</p>
      <p class="c-val">{val}<span class="c-unit">{unit}</span></p>
      <p class="c-sub">{sub}</p>
    </div>""" for name, val, unit, sub, tip in CARDS)

# ── HTML final ─────────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SRF-PLL · IEEE 9-Bus · UERJ 2025</title>
<script src="https://cdn.plot.ly/plotly-2.35.0.min.js" charset="utf-8"></script>
<style>
/* ── Tokens ──────────────────────────────────────────────────── */
:root {{
  --bg:        #f1f5f9;
  --surface:   #ffffff;
  --border:    #e2e8f0;
  --text:      #0f172a;
  --muted:     #64748b;
  --accent:    #2563eb;
  --accent-s:  #dbeafe;
  --badge-bg:  #eff6ff;
  --badge-fg:  #1d4ed8;
  --card-bg:   #ffffff;
  --sh:        0 1px 3px rgba(0,0,0,.08),0 1px 2px rgba(0,0,0,.05);
  --sh-md:     0 4px 12px rgba(0,0,0,.09);
  --sh-lg:     0 10px 30px rgba(0,0,0,.11);
  --radius:    14px;
  --plot-bg:   #ffffff;
  --grid:      #f1f5f9;
  --zero:      #e2e8f0;
  --btn-bg:    #ffffff;
  --btn-fg:    #374151;
  --btn-bdr:   #d1d5db;
}}
[data-theme="dark"] {{
  --bg:        #0a0f1e;
  --surface:   #111827;
  --border:    #1f2937;
  --text:      #f9fafb;
  --muted:     #9ca3af;
  --accent:    #60a5fa;
  --accent-s:  #1e3050;
  --badge-bg:  #1e3050;
  --badge-fg:  #93c5fd;
  --card-bg:   #111827;
  --sh:        0 1px 3px rgba(0,0,0,.5),0 1px 2px rgba(0,0,0,.4);
  --sh-md:     0 4px 12px rgba(0,0,0,.5);
  --sh-lg:     0 10px 30px rgba(0,0,0,.5);
  --plot-bg:   #111827;
  --grid:      #1f2937;
  --zero:      #374151;
  --btn-bg:    #1f2937;
  --btn-fg:    #d1d5db;
  --btn-bdr:   #374151;
}}

/* ── Reset & base ────────────────────────────────────────────── */
*,*::before,*::after {{ box-sizing:border-box; margin:0; padding:0 }}
body {{
  font-family: Inter,'Segoe UI',system-ui,sans-serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}}
body, .card, .header, .chart-wrap, .badge, .toggle-btn,
.c-val, .c-name, .c-sub, .c-unit {{
  transition: background .28s, color .28s, border-color .28s,
              box-shadow .28s;
}}

/* ── Header ──────────────────────────────────────────────────── */
.header {{
  position: sticky; top: 0; z-index: 200;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  box-shadow: var(--sh);
  padding: 0 28px;
  height: 64px;
  display: flex; align-items: center; justify-content: space-between;
}}
.h-left {{ display:flex; align-items:center; gap:14px }}
.h-logo {{
  width:40px; height:40px; border-radius:11px;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  display:flex; align-items:center; justify-content:center;
  color:#fff; font-size:20px; font-weight:800;
  flex-shrink:0; user-select:none;
  box-shadow: 0 2px 8px rgba(37,99,235,.35);
}}
.h-title {{ font-size:15px; font-weight:700; letter-spacing:-.2px; line-height:1.2 }}
.h-sub   {{ font-size:12px; color:var(--muted); margin-top:2px }}
.badge {{
  background: var(--badge-bg); color: var(--badge-fg);
  font-size:11px; font-weight:600; padding:4px 11px;
  border-radius:999px; letter-spacing:.3px;
}}
.h-right {{ display:flex; align-items:center; gap:10px }}
.toggle-btn {{
  display:flex; align-items:center; gap:8px;
  background: var(--btn-bg); color: var(--btn-fg);
  border: 1.5px solid var(--btn-bdr);
  padding: 7px 16px; border-radius:999px;
  font-size:13px; font-weight:600; font-family:inherit;
  cursor:pointer; box-shadow:var(--sh);
  transition: box-shadow .2s, transform .2s, background .28s, color .28s, border-color .28s;
}}
.toggle-btn:hover {{
  box-shadow: var(--sh-md); transform: translateY(-1px);
}}
.toggle-btn:active {{ transform:translateY(0) }}

/* ── Main layout ─────────────────────────────────────────────── */
.main {{
  max-width: 1200px; margin: 0 auto;
  padding: 28px 24px 48px;
}}

/* ── Metric cards ────────────────────────────────────────────── */
.cards {{
  display: grid;
  grid-template-columns: repeat(5,1fr);
  gap: 14px;
  margin-bottom: 22px;
}}
@media(max-width:720px){{ .cards {{ grid-template-columns:repeat(3,1fr) }} }}
@media(max-width:460px){{ .cards {{ grid-template-columns:repeat(2,1fr) }} }}

.card {{
  background: var(--card-bg);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 16px 14px;
  box-shadow: var(--sh);
  cursor: default;
  position: relative; overflow: hidden;
}}
.card::before {{
  content:'';
  position:absolute; top:0; left:0; right:0; height:3px;
  background: linear-gradient(90deg,#2563eb,#7c3aed);
  border-radius: var(--radius) var(--radius) 0 0;
}}
[data-theme="dark"] .card::before {{
  background: linear-gradient(90deg,#60a5fa,#a78bfa);
}}
.card:hover {{
  box-shadow: var(--sh-md);
  transform: translateY(-2px);
  transition: box-shadow .18s, transform .18s, background .28s, border-color .28s;
}}
.c-name {{
  font-size:11px; font-weight:600; text-transform:uppercase;
  letter-spacing:.6px; color:var(--muted); margin-bottom:8px;
}}
.c-val {{
  font-size:24px; font-weight:800; color:var(--accent);
  letter-spacing:-.5px; line-height:1;
  display:flex; align-items:baseline; gap:4px;
}}
.c-unit {{
  font-size:11px; font-weight:500; color:var(--muted); letter-spacing:.3px;
}}
.c-sub {{
  font-size:10.5px; color:var(--muted); margin-top:6px;
}}

/* ── Chart container ─────────────────────────────────────────── */
.chart-wrap {{
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--sh);
  overflow: hidden;
  padding: 4px 4px 0;
}}
.chart-header {{
  display:flex; align-items:center; justify-content:space-between;
  padding: 14px 18px 10px;
  border-bottom: 1px solid var(--border);
}}
.chart-title {{
  font-size:13px; font-weight:600; color:var(--text);
  display:flex; align-items:center; gap:8px;
}}
.fault-badge {{
  font-size:10px; font-weight:600; color:#b45309;
  background:#fef3c7; border-radius:6px; padding:2px 8px;
}}
[data-theme="dark"] .fault-badge {{
  color:#fcd34d; background:#451a03;
}}
#plot {{ width:100% }}

/* ── Footer ──────────────────────────────────────────────────── */
.footer {{
  margin-top:20px; text-align:center;
  font-size:11px; color:var(--muted);
  display:flex; align-items:center; justify-content:center; gap:12px;
}}
.footer-dot {{
  width:3px; height:3px; border-radius:50%;
  background:var(--muted); flex-shrink:0;
}}
</style>
</head>

<body>

<!-- ── Header ────────────────────────────────────────────────── -->
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

<!-- ── Main ──────────────────────────────────────────────────── -->
<main class="main">

  <!-- Cards -->
  <div class="cards">{cards_html}
  </div>

  <!-- Chart -->
  <div class="chart-wrap">
    <div class="chart-header">
      <span class="chart-title">
        Sinais temporais
      </span>
      <span class="fault-badge">⚡ Falta em t = {T_FAULT} s</span>
    </div>
    <div id="plot"></div>
  </div>

  <!-- Footer -->
  <div class="footer">
    <span>analyze_sim_data.py</span>
    <span class="footer-dot"></span>
    <span>Plotly {plotly.__version__}</span>
    <span class="footer-dot"></span>
    <span>TCC UERJ 2025</span>
  </div>

</main>

<!-- ── Scripts ───────────────────────────────────────────────── -->
<script>
/* ── Plotly init ── */
var figData = {fig_json};
var gd = document.getElementById('plot');

Plotly.newPlot(gd, figData.data, figData.layout, {{
  responsive: true,
  displaylogo: false,
  modeBarButtonsToRemove: ['select2d','lasso2d','autoScale2d','toImage'],
  toImageButtonOptions: {{ format:'svg', filename:'pll_metrics' }},
}});

/* ── Theme toggle ── */
var isDark = false;

var LAYOUT_LIGHT = {{
  paper_bgcolor: '#ffffff', plot_bgcolor: '#ffffff',
  'font.color': '#0f172a',
  'legend.bgcolor': 'rgba(0,0,0,0)',
  'hoverlabel.bgcolor': '#ffffff', 'hoverlabel.bordercolor': '#e2e8f0',
}};
var LAYOUT_DARK = {{
  paper_bgcolor: '#111827', plot_bgcolor: '#111827',
  'font.color': '#f9fafb',
  'legend.bgcolor': 'rgba(0,0,0,0)',
  'hoverlabel.bgcolor': '#1f2937', 'hoverlabel.bordercolor': '#374151',
}};

var n = {n};
for (var i = 1; i <= n; i++) {{
  var s = i === 1 ? '' : String(i);
  LAYOUT_LIGHT['xaxis'+s+'.gridcolor']     = '#f1f5f9';
  LAYOUT_LIGHT['xaxis'+s+'.zerolinecolor'] = '#e2e8f0';
  LAYOUT_LIGHT['yaxis'+s+'.gridcolor']     = '#f1f5f9';
  LAYOUT_LIGHT['yaxis'+s+'.zerolinecolor'] = '#e2e8f0';
  LAYOUT_DARK ['xaxis'+s+'.gridcolor']     = '#1f2937';
  LAYOUT_DARK ['xaxis'+s+'.zerolinecolor'] = '#374151';
  LAYOUT_DARK ['yaxis'+s+'.gridcolor']     = '#1f2937';
  LAYOUT_DARK ['yaxis'+s+'.zerolinecolor'] = '#374151';
}}

var lightColors = {light_cols};
var darkColors  = {dark_cols};
var traceIdx    = {trace_idx};

function toggleTheme() {{
  isDark = !isDark;
  document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
  Plotly.relayout(gd, isDark ? LAYOUT_DARK : LAYOUT_LIGHT);
  var cols = isDark ? darkColors : lightColors;
  traceIdx.forEach(function(ti, i) {{
    Plotly.restyle(gd, {{'line.color': [cols[i]]}}, [ti]);
  }});
  document.getElementById('ico').textContent = isDark ? '☀️' : '🌙';
  document.getElementById('lbl').textContent = isDark ? 'Light mode' : 'Dark mode';
}}
</script>

</body>
</html>
"""

out = PROJ_ROOT / "output" / "pll_metrics.html"
out.write_text(html, encoding="utf-8")
print(f"\nHTML salvo: {out}")
