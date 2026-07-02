"""
chart.py — Constrói figuras Plotly por seção (Inversor / Sistema 9-Bus).

ChartBuilder.build_sections() → (fig_inv, fig_sys, trace_map_inv, trace_map_sys)
fig_sys é None se não houver dados de sistema disponíveis.
"""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..config import T_FAULT, TOL_RAD, LVRT_THRESHOLD, LIGHT_COLORS, DARK_COLORS
from .loader import SimData

_S = "single"   # linha inteira (colspan 2)
_P = "pair"     # dois painéis lado a lado


class ChartBuilder:
    """Monta subplots Plotly separados por seção temática."""

    def __init__(self, data: SimData) -> None:
        self._d = data
        self._fig: go.Figure | None = None
        self._ci = 0
        self._trace_map: list[tuple[int, str, str]] = []
        self._legend_key = "legend"

    # ── API pública ──────────────────────────────────────────────────────────

    def build_sections(self) -> tuple[
        go.Figure,
        go.Figure | None,
        list[tuple[int, str, str]],
        list[tuple[int, str, str]],
    ]:
        """Retorna (fig_inv, fig_sys, trace_map_inv, trace_map_sys)."""
        fig_inv, tm_inv = self._make_figure(self._inv_rows())
        sys_rows = self._sys_rows()
        if sys_rows:
            fig_sys, tm_sys = self._make_figure(sys_rows)
        else:
            fig_sys, tm_sys = None, []
        return fig_inv, fig_sys, tm_inv, tm_sys

    # ── Definição de linhas ──────────────────────────────────────────────────

    def _inv_rows(self) -> list:
        d = self._d
        rows: list = []
        if d.has_ang:
            rows.append((_S, "ang", "Ângulo (°)"))
        if d.theta_err is not None:
            rows.append((_S, "err", "Erro de fase (°)"))
        if d.has_dq_ufv:
            rows.append((_S, "dq_combined", "Corrente dq UFV (pu)"))
        if d.has_vdq_ufv or d.has_vdq_rede:
            rows.append((_S, "vdq_combined", "Tensão dq (pu)"))
        rows.append((_S, "pq_combined", "P / Q UFV (pu)"))
        return rows

    def _sys_rows(self) -> list:
        d = self._d
        rows: list = []
        if d.has_vbus2:
            rows.append((_S, "vbus2", "|V| Bus 2 (pu)", "Barra 2"))

        grp1 = "Barra 1"
        if d.has_vbus1:
            rows.append((_S, "vbus1", "|V| Bus 1 (pu)", grp1))
            grp1 = None
        if d.has_pq_bus1:
            rows.append((_P,
                ("p_bus1", "P Bus 1 (pu)"),
                ("q_bus1", "Q Bus 1 (pu)"), grp1))

        grp3 = "Barra 3"
        if d.has_vbus3:
            rows.append((_S, "vbus3", "|V| Bus 3 (pu)", grp3))
            grp3 = None
        if d.has_pq_bus3:
            rows.append((_P,
                ("p_bus3", "P Bus 3 (pu)"),
                ("q_bus3", "Q Bus 3 (pu)"), grp3))
        return rows

    # ── Construção da figura ─────────────────────────────────────────────────

    def _make_figure(self, rows: list) -> tuple[go.Figure, list]:
        n = len(rows)
        specs = [
            [{"type": "scatter", "colspan": 2}, None] if r[0] == _S
            else [{"type": "scatter"}, {"type": "scatter"}]
            for r in rows
        ]
        self._fig = make_subplots(
            rows=n, cols=2,
            shared_xaxes=True,
            vertical_spacing=0.07,
            specs=specs,
        )
        self._ci = 0
        self._trace_map = []

        has_groups = any(len(r) == 4 and r[-1] for r in rows)

        ax = 0
        for ri, row_spec in enumerate(rows, 1):
            group = row_spec[-1] if len(row_spec) == 4 else None
            if row_spec[0] == _S:
                _, kind, label = row_spec[:3]
                ax += 1
                if group:
                    self._group_title(group, ax)
                self._legend_key = "legend" if ax == 1 else f"legend{ax}"
                self._add_panel(kind, ri, 1)
                self._label(label, ax)
                self._vline(ri, 1)
                self._fig.update_yaxes(gridcolor="#f0f2f5", zerolinecolor="#e5e7eb",
                                       tickfont_size=10, row=ri, col=1)
            else:
                _, (k1, l1), (k2, l2) = row_spec[:3]
                ax1, ax2 = ax + 1, ax + 2
                ax += 2
                if group:
                    self._group_title(group, ax1)
                self._legend_key = "legend" if ax1 == 1 else f"legend{ax1}"
                self._add_panel(k1, ri, 1)
                self._label(l1, ax1)
                self._vline(ri, 1)
                self._fig.update_yaxes(gridcolor="#f0f2f5", zerolinecolor="#e5e7eb",
                                       tickfont_size=10, row=ri, col=1)

                self._legend_key = f"legend{ax2}"
                self._add_panel(k2, ri, 2)
                self._label(l2, ax2)
                self._vline(ri, 2)
                self._fig.update_yaxes(gridcolor="#f0f2f5", zerolinecolor="#e5e7eb",
                                       tickfont_size=10, row=ri, col=2)

        self._apply_layout(n, extra_top=has_groups)
        self._place_legends(rows)
        return self._fig, self._trace_map

    # ── Helpers de figura ────────────────────────────────────────────────────

    def _label(self, text: str, ax_idx: int) -> None:
        xref = "x domain" if ax_idx == 1 else f"x{ax_idx} domain"
        yref = "y domain" if ax_idx == 1 else f"y{ax_idx} domain"
        self._fig.add_annotation(
            text=f"<b>{text}</b>", xref=xref, yref=yref,
            x=0.01, y=0.97, xanchor="left", yanchor="top",
            font=dict(size=10, color="#6b7280"), showarrow=False,
        )

    def _group_title(self, text: str, ax_idx: int) -> None:
        """Subtítulo de divisão por barra, ancorado acima da 1ª linha do grupo."""
        yref = "y domain" if ax_idx == 1 else f"y{ax_idx} domain"
        self._fig.add_annotation(
            text=text.upper(), xref="paper", yref=yref,
            x=0, y=1.16, xanchor="left", yanchor="bottom",
            font=dict(size=11, color="#334155", family="Inter, Segoe UI, system-ui, sans-serif"),
            showarrow=False,
        )
        self._fig.add_shape(
            type="line", xref="paper", yref=yref,
            x0=0, x1=1, y0=1.08, y1=1.08,
            line=dict(color="#e2e8f0", width=1),
        )

    def _vline(self, row: int, col: int) -> None:
        self._fig.add_vline(
            x=T_FAULT,
            line=dict(color="rgba(100,100,100,0.25)", width=1.1, dash="dot"),
            row=row, col=col,
        )

    def _apply_layout(self, n_rows: int, extra_top: bool = False) -> None:
        self._fig.update_xaxes(
            title_text="Tempo (s)", gridcolor="#f0f2f5",
            zerolinecolor="#e5e7eb", tickfont_size=10,
        )
        # pu é adimensional — sem prefixo SI (µ/k/M) nos ticks do eixo Y
        self._fig.update_yaxes(exponentformat="none")
        # espaço extra no topo para o subtítulo "Barra N" da 1ª linha do grupo
        top_margin = 34 if extra_top else 16
        self._fig.update_layout(
            margin=dict(t=top_margin, b=16, l=60, r=100),
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font=dict(family="Inter, Segoe UI, system-ui, sans-serif", size=12, color="#111827"),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e5e7eb",
                            font_family="Inter, Segoe UI, system-ui, sans-serif", font_size=11),
            height=240 * n_rows,
            showlegend=True,
        )

    def _place_legends(self, rows: list) -> None:
        """Legenda fora (direita) para single; dentro (topo-direito) para pair."""
        updates: dict = {}
        ax = 0
        for r in rows:
            if r[0] == _S:
                ax += 1
                yname = "yaxis" if ax == 1 else f"yaxis{ax}"
                ly = getattr(self._fig.layout, yname, None)
                if ly:
                    y_mid = float((ly.domain[0] + ly.domain[1]) / 2)
                    key = "legend" if ax == 1 else f"legend{ax}"
                    updates[key] = dict(
                        x=1.01, y=y_mid, yanchor="middle", xanchor="left",
                        font_size=10, bgcolor="rgba(0,0,0,0)", borderwidth=0, tracegroupgap=2,
                    )
            else:
                ax1, ax2 = ax + 1, ax + 2
                ax += 2
                for ai in (ax1, ax2):
                    yname = "yaxis" if ai == 1 else f"yaxis{ai}"
                    xname = "xaxis" if ai == 1 else f"xaxis{ai}"
                    ly = getattr(self._fig.layout, yname, None)
                    lx = getattr(self._fig.layout, xname, None)
                    if ly and lx:
                        x_right = float(lx.domain[1]) - 0.01
                        y_top   = float(ly.domain[1]) - 0.02
                        key = "legend" if ai == 1 else f"legend{ai}"
                        updates[key] = dict(
                            x=x_right, y=y_top, yanchor="top", xanchor="right",
                            font_size=10, bgcolor="rgba(255,255,255,0.8)",
                            borderwidth=0, tracegroupgap=2,
                        )
        self._fig.update_layout(**updates)

    # ── _add ────────────────────────────────────────────────────────────────

    def _add(self, trace: go.BaseTraceType, row: int, col: int = 1) -> None:
        lc = LIGHT_COLORS[self._ci % len(LIGHT_COLORS)]
        dc = DARK_COLORS[self._ci % len(DARK_COLORS)]
        self._ci += 1
        trace.line.color = lc
        trace.legend = self._legend_key
        self._fig.add_trace(trace, row=row, col=col)
        self._trace_map.append((len(self._fig.data) - 1, lc, dc))

    # ── Painéis ─────────────────────────────────────────────────────────────

    def _add_panel(self, kind: str, row: int, col: int) -> None:
        d = self._d
        t = d.t

        if kind == "ang":
            t_ang = d.t_fast if d.t_fast is not None else t
            self._add(go.Scatter(x=t_ang, y=np.degrees(d.theta_ref),
                                 name="θ Rede", mode="lines", line=dict(width=2.0)), row, col)
            self._add(go.Scatter(x=t_ang, y=np.degrees(d.theta_pll),
                                 name="θ̂ PLL", mode="lines", line=dict(width=1.4, dash="dot")), row, col)

        elif kind == "err":
            t_err = d.t_fast if d.t_fast is not None else t
            err   = d.theta_err_fast if d.theta_err_fast is not None else d.theta_err
            self._add(go.Scatter(x=t_err, y=np.degrees(err),
                                 name="Erro de fase", mode="lines", line=dict(width=1.8)), row, col)
            tol_deg = np.degrees(TOL_RAD)
            for sign in (+1, -1):
                self._fig.add_hline(y=sign * tol_deg,
                                    line=dict(color="rgba(220,50,50,0.45)", width=1.1, dash="dash"),
                                    row=row, col=col)

        elif kind in ("vbus1", "vbus2", "vbus3"):
            vbus_map = {"vbus1": (d.vbus1, "|V| Bus 1"), "vbus2": (d.vbus2, "|V| Bus 2"),
                        "vbus3": (d.vbus3, "|V| Bus 3")}
            vbus, name = vbus_map[kind]
            self._add(go.Scatter(x=t, y=vbus,
                                 name=name, mode="lines", line=dict(width=1.8)), row, col)
            self._fig.add_hline(y=1.0,
                                line=dict(color="rgba(100,100,100,0.25)", width=1.0, dash="dot"),
                                row=row, col=col)
            self._fig.add_hline(y=LVRT_THRESHOLD,
                                line=dict(color="rgba(220,50,50,0.45)", width=1.1, dash="dash"),
                                row=row, col=col)

        elif kind == "pq_combined":
            self._add(go.Scatter(x=t, y=d.P_ufv,
                                 name="P UFV", mode="lines", line=dict(width=1.8)), row, col)
            self._add(go.Scatter(x=t, y=d.Q_ufv,
                                 name="Q UFV", mode="lines", line=dict(width=1.8)), row, col)

        elif kind == "dq_combined":
            if d.has_ref_ufv:
                self._add(go.Scatter(x=t, y=d.id_ufv_meas,
                                     name="i<sub>d</sub> med.", mode="lines", line=dict(width=1.4)), row, col)
                self._add(go.Scatter(x=t, y=d.id_ufv_ref,
                                     name="i<sub>d</sub> ref", mode="lines", line=dict(width=2.0, dash="dash")), row, col)
                self._add(go.Scatter(x=t, y=d.iq_ufv_meas,
                                     name="i<sub>q</sub> med.", mode="lines", line=dict(width=1.4)), row, col)
                self._add(go.Scatter(x=t, y=d.iq_ufv_ref,
                                     name="i<sub>q</sub> ref", mode="lines", line=dict(width=2.0, dash="dash")), row, col)
            else:
                self._add(go.Scatter(x=t, y=d.id_ufv_meas,
                                     name="i<sub>d</sub> UFV", mode="lines", line=dict(width=1.8)), row, col)
                self._add(go.Scatter(x=t, y=d.iq_ufv_meas,
                                     name="i<sub>q</sub> UFV", mode="lines", line=dict(width=1.4, dash="dot")), row, col)

        elif kind == "vdq_combined":
            if d.has_vdq_rede:
                self._add(go.Scatter(x=t, y=d.vd_rede,
                                     name="V<sub>d</sub> Rede", mode="lines", line=dict(width=2.0)), row, col)
                self._add(go.Scatter(x=t, y=d.vq_rede,
                                     name="V<sub>q</sub> Rede", mode="lines", line=dict(width=2.0)), row, col)
            if d.has_vdq_ufv:
                self._add(go.Scatter(x=t, y=d.vd_ufv,
                                     name="V<sub>d</sub> Inv", mode="lines", line=dict(width=1.4, dash="dot")), row, col)
                self._add(go.Scatter(x=t, y=d.vq_ufv,
                                     name="V<sub>q</sub> Inv", mode="lines", line=dict(width=1.4, dash="dot")), row, col)
            self._fig.add_hline(y=0.0,
                                line=dict(color="rgba(100,100,100,0.25)", width=1.0, dash="dot"),
                                row=row, col=col)

        elif kind in ("p_bus1", "q_bus1", "p_bus3", "q_bus3"):
            pq_map = {"p_bus1": (d.p_bus1, "P Bus 1"), "q_bus1": (d.q_bus1, "Q Bus 1"),
                      "p_bus3": (d.p_bus3, "P Bus 3"), "q_bus3": (d.q_bus3, "Q Bus 3")}
            pq, name = pq_map[kind]
            self._add(go.Scatter(x=t, y=pq,
                                 name=name, mode="lines", line=dict(width=1.8)), row, col)
