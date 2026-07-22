"""
chart.py — Constrói figuras Plotly por seção (Resumo / Inversor / Sistema 9-Bus).

ChartBuilder.build_sections() → (fig_inv, fig_sys, trace_map_inv, trace_map_sys)
ChartBuilder.build_resume()   → (fig_res, trace_map_res) — painéis essenciais
fig_sys/fig_res é None se não houver dados disponíveis.
"""
from __future__ import annotations

import re

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..config import TOL_RAD, LVRT_THRESHOLD, LIGHT_COLORS, DARK_COLORS
from .loader import SimData

_S = "single"   # linha inteira (colspan 2)
_P = "pair"     # dois painéis lado a lado

_MAX_POINTS = 5000  # cap de pontos/trace no HTML — ver kb/simulation/python_pipeline.md
# A figura Resumo duplica traces já presentes nas seções completas; decimação
# mais agressiva limita o custo extra no tamanho do HTML.
_RES_MAX_POINTS = 2000


class ChartBuilder:
    """Monta subplots Plotly separados por seção temática."""

    def __init__(self, data: SimData) -> None:
        self._d = data
        self._fig: go.Figure | None = None
        self._ci = 0
        self._trace_map: list[tuple[int, str, str]] = []
        self._legend_key = "legend"
        self._max_points = _MAX_POINTS

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

    def build_resume(self) -> tuple[go.Figure | None, list[tuple[int, str, str]]]:
        """Figura Resumo: painéis essenciais do cenário, decimação reduzida."""
        rows = self._res_rows()
        if len(rows) < 2:
            return None, []
        self._max_points = _RES_MAX_POINTS
        try:
            return self._make_figure(rows)
        finally:
            self._max_points = _MAX_POINTS

    # ── Definição de linhas ──────────────────────────────────────────────────

    def _res_rows(self) -> list:
        """A história essencial em uma tela: erro do PLL, frequência, P/Q e V no POC."""
        d = self._d
        rows: list = []
        if d.theta_err is not None:
            rows.append((_S, "err", "Erro de fase (°)"))
        if d.has_freq:
            rows.append((_S, "freq", "Frequência PLL (Hz)"))
        rows.append((_S, "pq_combined", "P / Q UFV (pu)"))
        if d.has_vbus2:
            rows.append((_S, "vbus2", "|V| Bus 2 (pu)"))
        return rows

    def _inv_rows(self) -> list:
        d = self._d
        rows: list = []
        if d.has_ang:
            rows.append((_S, "ang", "Ângulo (°)"))
        if d.theta_err is not None:
            rows.append((_S, "err", "Erro de fase (°)"))
        if d.has_freq:
            rows.append((_S, "freq", "Frequência PLL (Hz)"))
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
        self._n_rows_fig = n
        specs = [
            [{"type": "scatter", "colspan": 2}, None] if r[0] == _S
            else [{"type": "scatter"}, {"type": "scatter"}]
            for r in rows
        ]
        self._fig = make_subplots(
            rows=n, cols=2,
            shared_xaxes=True,
            vertical_spacing=0.11,
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

    @staticmethod
    def _split_label(text: str) -> tuple[str, str]:
        """"Nome (unid)" → ("Nome", "unid"). Sem parêntese final → (text, "")."""
        m = re.match(r"^(.*?)\s*\(([^()]*)\)\s*$", text)
        if m:
            return m.group(1).strip(), m.group(2).strip()
        return text, ""

    _BAR_COLOR = "#185FA5"   # barra de título (estilo header Power BI)

    def _label(self, text: str, ax_idx: int) -> None:
        """Barra de título no topo do painel + unidade no eixo Y (vertical).
        Responde ao Ponto 2 do professor: o rótulo deixa de ser annotation
        horizontal no canto — o nome vira uma barra de título preenchida
        (texto branco centralizado) encostada no topo do painel, e a unidade
        vira o título do eixo Y, rotacionada e encostada no eixo."""
        title, unit = self._split_label(text)
        n = self._n_rows_fig
        xname = "xaxis" if ax_idx == 1 else f"xaxis{ax_idx}"
        yname = "yaxis" if ax_idx == 1 else f"yaxis{ax_idx}"
        ax_dom = self._fig.layout[xname].domain
        y_top  = float(self._fig.layout[yname].domain[1])
        xc     = float((ax_dom[0] + ax_dom[1]) / 2)
        bar_h  = 22.0 / (240 * n)   # altura da barra (fração de paper)
        # barra preenchida encostada no topo do painel
        self._fig.add_shape(
            type="rect", xref="paper", yref="paper",
            x0=ax_dom[0], x1=ax_dom[1], y0=y_top, y1=y_top + bar_h,
            fillcolor=self._BAR_COLOR, line_width=0, layer="above",
        )
        # nome centralizado, branco, dentro da barra
        self._fig.add_annotation(
            text=f"<b>{title}</b>", xref="paper", yref="paper",
            x=xc, y=y_top + bar_h / 2, xanchor="center", yanchor="middle",
            font=dict(size=11, color="#ffffff"), showarrow=False,
        )
        # unidade no eixo Y, na vertical
        self._fig.layout[yname].title.text = unit
        self._fig.layout[yname].title.font = dict(size=10, color="#6b7280")
        self._fig.layout[yname].title.standoff = 4

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
        """Destaca a janela de falta: faixa sombreada + vlines de início (vermelha)
        e limpeza (verde). Nenhuma marca em regime permanente."""
        d = self._d
        if d.t_fault is not None and d.t_clear is not None:
            self._fig.add_vrect(
                x0=d.t_fault, x1=d.t_clear,
                fillcolor="rgba(220,50,50,0.07)", line_width=0, layer="below",
                row=row, col=col,
            )
        if d.t_fault is not None:
            self._fig.add_vline(
                x=d.t_fault,
                line=dict(color="rgba(220,50,50,0.75)", width=2.0, dash="dash"),
                row=row, col=col,
            )
        if d.t_clear is not None:
            self._fig.add_vline(
                x=d.t_clear,
                line=dict(color="rgba(22,163,74,0.65)", width=2.0, dash="dash"),
                row=row, col=col,
            )

    def _ts_marker(self, t_err: np.ndarray, err: np.ndarray, row: int, col: int) -> None:
        """Marca no gráfico de erro o instante de acomodação tₛ calculado no loader."""
        d = self._d
        ts_val = d.metrics.get("ts")
        if ts_val is None or d.t_fault is None:
            return
        y_ts = float(np.interp(ts_val, t_err, np.degrees(err)))
        marker = go.Scatter(
            x=[ts_val], y=[y_ts], mode="markers+text",
            text=["t<sub>s</sub>"], textposition="top right",
            textfont=dict(size=11, color="#16a34a"),
            marker=dict(size=9, symbol="diamond", color="#16a34a",
                        line=dict(width=1, color="#ffffff")),
            name="tₛ", showlegend=False,
            hovertemplate="tₛ = %{x:.3f} s<extra></extra>",
        )
        marker.legend = self._legend_key
        self._fig.add_trace(marker, row=row, col=col)

    # Envelope LVRT IEEE 1547-2018 Categoria II: (Δt após a falta, V mínimo de
    # ride-through obrigatório) — 0.30 pu/0.16 s, 0.45 pu/0.32 s, 0.65 pu/3 s,
    # 0.88 pu operação contínua.
    _LVRT_STEPS = ((0.16, 0.30), (0.32, 0.45), (3.0, 0.65))

    def _lvrt_envelope(self, row: int, col: int) -> None:
        """Curva degrau V×t de ride-through, ancorada em t_fault (só no |V| Bus 2)."""
        d = self._d
        t0, t_end = d.t_fault, float(d.t[-1])
        xs, ys = [t0], [self._LVRT_STEPS[0][1]]
        for i, (dt_step, _v) in enumerate(self._LVRT_STEPS):
            next_v = self._LVRT_STEPS[i + 1][1] if i + 1 < len(self._LVRT_STEPS) else 0.88
            xs.append(min(t0 + dt_step, t_end))
            ys.append(next_v)
        xs.append(t_end)
        ys.append(0.88)
        env = go.Scatter(
            x=xs, y=ys, mode="lines", line_shape="hv",
            line=dict(color="rgba(220,50,50,0.7)", width=1.6, dash="dash"),
            name="LVRT 1547 Cat II", hoverinfo="skip",
        )
        env.legend = self._legend_key
        self._fig.add_trace(env, row=row, col=col)

    def _apply_layout(self, n_rows: int, extra_top: bool = False) -> None:
        self._fig.update_xaxes(
            title_text="Tempo (s)", gridcolor="#f0f2f5",
            zerolinecolor="#e5e7eb", tickfont_size=10,
        )
        # shared_xaxes só liga eixos por coluna; linkar TODOS ao eixo raiz faz
        # qualquer zoom (botão, arrasto, duplo-clique) valer para todos os painéis
        for ax_name in self._fig.layout:
            if ax_name.startswith("xaxis") and ax_name != "xaxis":
                self._fig.layout[ax_name].matches = "x"
        # pu é adimensional — sem prefixo SI (µ/k/M) nos ticks do eixo Y
        self._fig.update_yaxes(exponentformat="none")
        # espaço extra no topo: título de cada painel (+ subtítulo "Barra N" no grupo)
        top_margin = 54 if extra_top else 34
        self._fig.update_layout(
            margin=dict(t=top_margin, b=16, l=64, r=100),
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
        x, y = np.asarray(trace.x), np.asarray(trace.y)
        if len(x) > self._max_points:
            step = int(np.ceil(len(x) / self._max_points))
            trace.x, trace.y = x[::step], y[::step]
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
            # θ̂ PLL é o protagonista (sólido, mais grosso, 1ª cor da paleta);
            # θ Rede vira referência de fundo (fino, tracejado)
            t_ang = d.t_fast if d.t_fast is not None else t
            self._add(go.Scatter(x=t_ang, y=np.degrees(d.theta_pll),
                                 name="θ̂ PLL", mode="lines", line=dict(width=2.4)), row, col)
            self._add(go.Scatter(x=t_ang, y=np.degrees(d.theta_ref),
                                 name="θ Rede", mode="lines", line=dict(width=1.1, dash="dash")), row, col)

        elif kind == "err":
            t_err = d.t_fast if d.t_fast is not None else t
            err   = d.theta_err_fast if d.theta_err_fast is not None else d.theta_err
            self._add(go.Scatter(x=t_err, y=np.degrees(err),
                                 name="Erro de fase", mode="lines", line=dict(width=1.8)), row, col)
            tol_deg = np.degrees(TOL_RAD)
            self._fig.add_hrect(y0=-tol_deg, y1=tol_deg,
                                fillcolor="rgba(22,163,74,0.08)", line_width=0, layer="below",
                                row=row, col=col)
            for sign in (+1, -1):
                self._fig.add_hline(y=sign * tol_deg,
                                    line=dict(color="rgba(22,163,74,0.4)", width=1.0, dash="dot"),
                                    row=row, col=col)
            self._ts_marker(t_err, err, row, col)

        elif kind == "freq":
            self._add(go.Scatter(x=d.t_freq, y=d.f_pll,
                                 name="f̂ PLL", mode="lines", line=dict(width=1.8)), row, col)
            self._fig.add_hline(y=60.0,
                                line=dict(color="rgba(100,100,100,0.35)", width=1.0, dash="dot"),
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
            if kind == "vbus2" and d.t_fault is not None:
                self._lvrt_envelope(row, col)
            else:
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
