"""
chart.py — Constrói a figura Plotly multi-painel a partir de um SimData.

Classe principal: ChartBuilder
    .build()   → retorna (fig, trace_map)
    trace_map  → lista de (trace_index, light_color, dark_color)
                 usada pelo JS para o toggle de tema
"""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .config import T_FAULT, TOL_RAD, LVRT_THRESHOLD, LIGHT_COLORS, DARK_COLORS
from .loader import SimData


class ChartBuilder:
    """Monta os subplots Plotly para os sinais do inversor."""

    def __init__(self, data: SimData) -> None:
        self._d = data
        self._ci = 0          # índice de cor atual
        self._trace_map: list[tuple[int, str, str]] = []
        self._fig: go.Figure | None = None

    # ── API pública ──────────────────────────────────────────────────────────

    def build(self) -> tuple[go.Figure, list[tuple[int, str, str]]]:
        """Constrói e retorna (fig, trace_map)."""
        panels = self._define_panels()
        n = len(panels)

        self._fig = make_subplots(
            rows=n, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
        )
        self._ci = 0
        self._trace_map = []

        for row, (kind, label) in enumerate(panels, 1):
            self._add_panel(kind, row)
            self._add_panel_annotations(label, row, n)

        self._apply_layout(n)
        return self._fig, self._trace_map

    # ── internos: definição de painéis ───────────────────────────────────────

    def _define_panels(self) -> list[tuple[str, str]]:
        d = self._d
        panels: list[tuple[str, str]] = []
        if d.has_ang:
            panels.append(("ang", "Ângulo (°)"))
        if d.theta_err is not None:
            panels.append(("err", "Erro de fase (°)"))
        if d.has_vbus2:
            panels.append(("vbus", "|V| Barra 2 (pu)"))
        panels.append(("P", "P (pu)"))
        panels.append(("Q", "Q (pu)"))
        if d.has_dq_ufv:
            if d.has_ref_ufv:
                panels.append(("id", "iₓ UFV (pu)"))
                panels.append(("iq", "iᵱ UFV (pu)"))
            else:
                panels.append(("dq_legacy", "Corrente dq UFV (pu)"))
        if d.has_vdq_ufv or d.has_vdq_rede:
            panels.append(("vd_track", "V<sub>d</sub> (pu)"))
            panels.append(("vq_track", "V<sub>q</sub> (pu)"))
        if d.has_gen1 or d.has_gen3:
            panels.append(("ang_gen", "Ângulo rotor (°)"))
            panels.append(("pe_gen", "Pe geradores (pu)"))
        return panels

    # ── internos: renderização de cada painel ─────────────────────────────────

    def _add_panel(self, kind: str, row: int) -> None:
        d = self._d
        t = d.t

        if kind == "ang":
            t_ang = d.t_fast if d.t_fast is not None else t
            self._add(go.Scatter(
                x=t_ang, y=np.degrees(d.theta_ref),
                name="θ Rede", mode="lines",
                line=dict(width=2.0)),
                row)
            self._add(go.Scatter(
                x=t_ang, y=np.degrees(d.theta_pll),
                name="θ̂ PLL", mode="lines",
                line=dict(width=1.4, dash="dot")),
                row)

        elif kind == "err":
            t_err = d.t_fast if d.t_fast is not None else t
            err   = d.theta_err_fast if d.theta_err_fast is not None else d.theta_err
            self._add(go.Scatter(
                x=t_err, y=np.degrees(err),
                name="Erro de fase", mode="lines",
                line=dict(width=1.8)),
                row)
            tol_deg = np.degrees(TOL_RAD)
            for sign in (+1, -1):
                self._fig.add_hline(
                    y=sign * tol_deg,
                    line=dict(color="rgba(220,50,50,0.45)",
                              width=1.1, dash="dash"),
                    row=row, col=1)

        elif kind == "vbus":
            self._add(go.Scatter(
                x=t, y=d.vbus2,
                name="|V| Bus 2", mode="lines",
                line=dict(width=1.8)),
                row)
            self._fig.add_hline(
                y=1.0,
                line=dict(color="rgba(100,100,100,0.25)", width=1.0, dash="dot"),
                row=row, col=1)
            self._fig.add_hline(
                y=LVRT_THRESHOLD,
                line=dict(color="rgba(220,50,50,0.45)", width=1.1, dash="dash"),
                row=row, col=1)

        elif kind == "P":
            self._add(go.Scatter(
                x=t, y=d.P_ufv,
                name="P UFV", mode="lines",
                line=dict(width=1.8)),
                row)

        elif kind == "Q":
            self._add(go.Scatter(
                x=t, y=d.Q_ufv,
                name="Q UFV", mode="lines",
                line=dict(width=1.8)),
                row)

        elif kind == "dq_legacy":
            self._add(go.Scatter(
                x=t, y=d.id_ufv_meas,
                name="i<sub>d</sub> UFV", mode="lines",
                line=dict(width=1.8)),
                row)
            self._add(go.Scatter(
                x=t, y=d.iq_ufv_meas,
                name="i<sub>q</sub> UFV", mode="lines",
                line=dict(width=1.4, dash="dot")),
                row)

        elif kind == "id":
            self._add(go.Scatter(
                x=t, y=d.id_ufv_meas,
                name="i<sub>d</sub> UFV medido", mode="lines",
                line=dict(width=1.4)),
                row)
            self._add(go.Scatter(
                x=t, y=d.id_ufv_ref,
                name="i<sub>d</sub> UFV ref", mode="lines",
                line=dict(width=2.0, dash="dash")),
                row)

        elif kind == "iq":
            self._add(go.Scatter(
                x=t, y=d.iq_ufv_meas,
                name="i<sub>q</sub> UFV medido", mode="lines",
                line=dict(width=1.4)),
                row)
            self._add(go.Scatter(
                x=t, y=d.iq_ufv_ref,
                name="i<sub>q</sub> UFV ref", mode="lines",
                line=dict(width=2.0, dash="dash")),
                row)

        elif kind == "vd_track":
            if d.has_vdq_rede:
                self._add(go.Scatter(
                    x=t, y=d.vd_rede,
                    name="V<sub>d</sub> Rede", mode="lines",
                    line=dict(width=2.0)),
                    row)
            if d.has_vdq_ufv:
                self._add(go.Scatter(
                    x=t, y=d.vd_ufv,
                    name="V<sub>d</sub> Inv (PLL)", mode="lines",
                    line=dict(width=1.4, dash="dot")),
                    row)

        elif kind == "vq_track":
            if d.has_vdq_rede:
                self._add(go.Scatter(
                    x=t, y=d.vq_rede,
                    name="V<sub>q</sub> Rede", mode="lines",
                    line=dict(width=2.0)),
                    row)
            if d.has_vdq_ufv:
                self._add(go.Scatter(
                    x=t, y=d.vq_ufv,
                    name="V<sub>q</sub> Inv (PLL)", mode="lines",
                    line=dict(width=1.4, dash="dot")),
                    row)
            self._fig.add_hline(
                y=0.0,
                line=dict(color="rgba(100,100,100,0.25)", width=1.0, dash="dot"),
                row=row, col=1)

        elif kind == "ang_gen":
            if d.has_gen1:
                self._add(go.Scatter(
                    x=t, y=np.degrees(d.ang_g1),
                    name="δ G1", mode="lines",
                    line=dict(width=1.8)),
                    row)
            if d.has_gen3:
                self._add(go.Scatter(
                    x=t, y=np.degrees(d.ang_g3),
                    name="δ G3", mode="lines",
                    line=dict(width=1.8)),
                    row)

        elif kind == "pe_gen":
            if d.has_gen1:
                self._add(go.Scatter(
                    x=t, y=d.pe_g1,
                    name="Pe G1", mode="lines",
                    line=dict(width=1.8)),
                    row)
            if d.has_gen3:
                self._add(go.Scatter(
                    x=t, y=d.pe_g3,
                    name="Pe G3", mode="lines",
                    line=dict(width=1.8)),
                    row)

    def _add_panel_annotations(self, label: str, row: int, n: int) -> None:
        yref = "y domain" if row == 1 else f"y{row} domain"
        self._fig.add_annotation(
            text=f"<b>{label}</b>",
            xref="paper", yref=yref,
            x=0, y=1.0, xanchor="left", yanchor="bottom",
            font=dict(size=10, color="#6b7280"),
            showarrow=False,
        )
        self._fig.add_vline(
            x=T_FAULT,
            line=dict(color="rgba(100,100,100,0.25)", width=1.1, dash="dot"),
            row=row, col=1,
        )
        self._fig.update_yaxes(
            gridcolor="#f0f2f5", zerolinecolor="#e5e7eb",
            tickfont_size=10, row=row, col=1,
        )

    # ── internos: helpers ────────────────────────────────────────────────────

    def _next_colors(self) -> tuple[str, str]:
        lc = LIGHT_COLORS[self._ci % len(LIGHT_COLORS)]
        dc = DARK_COLORS [self._ci % len(DARK_COLORS)]
        self._ci += 1
        return lc, dc

    def _add(self, trace: go.BaseTraceType, row: int) -> None:
        lc, dc = self._next_colors()
        trace.line.color = lc
        self._fig.add_trace(trace, row=row, col=1)
        self._trace_map.append((len(self._fig.data) - 1, lc, dc))

    # ── internos: layout ────────────────────────────────────────────────────

    def _apply_layout(self, n: int) -> None:
        self._fig.update_xaxes(
            title_text="Tempo (s)",
            gridcolor="#f0f2f5",
            zerolinecolor="#e5e7eb",
            tickfont_size=10,
        )
        self._fig.update_layout(
            margin=dict(t=16, b=16, l=66, r=16),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(
                family="Inter, Segoe UI, system-ui, sans-serif",
                size=12, color="#111827",
            ),
            legend=dict(
                orientation="h", x=0, y=-0.06,
                font_size=11,
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
            ),
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor="#ffffff",
                bordercolor="#e5e7eb",
                font_family="Inter, Segoe UI, system-ui, sans-serif",
                font_size=11,
            ),
            height=248 * n,
        )
