"""
spectrum.py — Espectro de Fourier por segmento temporal.

SpectrumBuilder(data).build() → (fig | None, trace_map)

Cada sinal trifásico da fase A (corrente i_a, tensão v_a) vira um painel; o
tempo é partido em dois segmentos — "antes do defeito" e "depois do defeito" —
no formato do gráfico de referência (amplitude linear, curva vermelha antes /
azul depois). No referencial abc a fundamental fica em 60 Hz (não vira DC como
no dq); a média removida aqui tira só o offset, não a fundamental.
"""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..config import (
    T_SETTLE, SPEC_FMAX_HZ, SPEC_XRANGE_HZ, SPEC_MARKERS,
    SPEC_SEG_COLORS,
)
from .loader import SimData

_MIN_DUR_S   = 0.05   # janela menor que isso → df > 20 Hz, não resolve 120 Hz
_MIN_SAMPLES = 64


def _amplitude_spectrum(t: np.ndarray, y: np.ndarray,
                        fmax: float = SPEC_FMAX_HZ):
    """|FFT| de amplitude LINEAR (pu): reamostra em grade uniforme, remove a
    média (offset DC; no abc a fundamental de 60 Hz permanece) e aplica janela
    de Hann. Retorna (f, amp) com 0 < f ≤ fmax e amp em pu — escala linear
    destaca os picos discretos (60 Hz + harmônicas) sobre o piso de ruído, ao
    contrário do dB. Retorna None se o segmento for curto demais."""
    if len(t) < _MIN_SAMPLES or (t[-1] - t[0]) < _MIN_DUR_S:
        return None
    dt = float(np.median(np.diff(t)))
    if dt <= 0:
        return None
    t_u = np.arange(t[0], t[-1], dt)
    y_u = np.interp(t_u, t, y)
    y_u -= y_u.mean()
    w   = np.hanning(len(y_u))
    amp = 2.0 * np.abs(np.fft.rfft(y_u * w)) / w.sum()
    f   = np.fft.rfftfreq(len(y_u), dt)
    m   = (f > 0) & (f <= fmax)
    return f[m], amp[m]


class SpectrumBuilder:
    """Monta a figura de espectros segmentados a partir de um SimData."""

    def __init__(self, data: SimData) -> None:
        self._d = data

    # ── API pública ──────────────────────────────────────────────────────────

    def build(self) -> tuple[go.Figure | None, list[tuple[int, str, str]]]:
        sigs = self._signals()
        segs = self._segments()
        if not sigs or not segs:
            return None, []

        n = len(sigs)
        fig = make_subplots(rows=n, cols=1, shared_xaxes=True,
                            vertical_spacing=0.09)
        tm: list[tuple[int, str, str]] = []

        for ri, (label, t, y, unit) in enumerate(sigs, 1):
            for seg_name, t0, t1 in segs:
                mask = (t >= t0) & (t <= t1)
                res = _amplitude_spectrum(t[mask], y[mask])
                if res is None:
                    continue
                f, amp = res
                lc, dc = SPEC_SEG_COLORS[seg_name]
                fig.add_trace(go.Scatter(
                    x=f, y=amp, name=seg_name, mode="lines",
                    line=dict(width=1.6, color=lc),
                    legendgroup=seg_name, showlegend=(ri == 1),
                    hovertemplate="%{x:.0f} Hz · %{y:.3g} " + unit + "<extra>" + seg_name + "</extra>",
                ), row=ri, col=1)
                tm.append((len(fig.data) - 1, lc, dc))
            self._label(fig, f"{label} — amplitude ({unit})", ri)

        self._marker_lines(fig, n)
        self._apply_layout(fig, n)
        return fig, tm

    # ── Segmentos e sinais ───────────────────────────────────────────────────

    def _segments(self) -> list[tuple[str, float, float]]:
        """Duas janelas no formato do gráfico de referência: "antes do defeito"
        e "depois do defeito", cortadas em t_fault. A janela de antes começa em
        T_SETTLE (config) para descartar o transitório de partida do PLL — não é
        falta de desempenho, é o PLL ainda travando na rede. A de depois junta
        falta + pós-falta numa curva só."""
        d = self._d
        t_end = float(d.t[-1])
        if d.t_fault is None:
            return [("Regime", min(T_SETTLE, t_end), t_end)]
        return [
            ("Antes do defeito",  min(T_SETTLE, d.t_fault), d.t_fault),
            ("Depois do defeito", d.t_fault, t_end),
        ]

    def _signals(self) -> list[tuple[str, np.ndarray, np.ndarray, str]]:
        """Só os sinais trifásicos da fase A (corrente i_a e tensão v_a). No abc
        a fundamental fica em 60 Hz e a seq. negativa da falta assimétrica cai
        TAMBÉM em 60 Hz — daí o marcador em F_FUND_HZ."""
        d = self._d
        sigs: list[tuple[str, np.ndarray, np.ndarray, str]] = []
        if d.has_iabc_ufv:
            sigs.append(("Corrente i<sub>a</sub> UFV (abc)",
                         d.t_abc, d.ia_ufv, "pu"))
        if d.has_vabc_ufv:
            sigs.append(("Tensão v<sub>a</sub> UFV (abc)",
                         d.t_abc, d.va_ufv, "pu"))
        return sigs

    # ── Helpers de figura ────────────────────────────────────────────────────

    @staticmethod
    def _label(fig: go.Figure, text: str, ax_idx: int) -> None:
        xref = "x domain" if ax_idx == 1 else f"x{ax_idx} domain"
        yref = "y domain" if ax_idx == 1 else f"y{ax_idx} domain"
        fig.add_annotation(
            text=f"<b>{text}</b>", xref=xref, yref=yref,
            x=0.01, y=0.97, xanchor="left", yanchor="top",
            font=dict(size=10, color="#6b7280"), showarrow=False,
        )

    @staticmethod
    def _marker_lines(fig: go.Figure, n_rows: int) -> None:
        """Linhas tracejadas nas principais frequências (SPEC_MARKERS):
        fundamental 60 Hz, harmônicas ímpares e ressonância LCL."""
        color = "rgba(120,120,130,0.45)"
        for freq, text in SPEC_MARKERS:
            if freq > SPEC_FMAX_HZ:
                continue
            for ri in range(1, n_rows + 1):
                fig.add_vline(x=freq,
                              line=dict(color=color, width=1.1, dash="dash"),
                              row=ri, col=1)
            fig.add_annotation(
                text=text, x=freq, xref="x", yref="y domain", y=1.05,
                xanchor="left", font=dict(size=9, color="#6b7280"),
                showarrow=False,
            )

    @staticmethod
    def _apply_layout(fig: go.Figure, n_rows: int) -> None:
        fig.update_xaxes(
            title_text="Frequência (Hz)", range=[0, SPEC_XRANGE_HZ],
            gridcolor="#f0f2f5", zerolinecolor="#e5e7eb", tickfont_size=10,
        )
        for ax_name in fig.layout:
            if ax_name.startswith("xaxis") and ax_name != "xaxis":
                fig.layout[ax_name].matches = "x"
        fig.update_yaxes(
            title_text="Amplitude (pu)", title_font_size=11,
            rangemode="tozero",
            gridcolor="#f0f2f5", zerolinecolor="#e5e7eb",
            tickfont_size=10,
        )
        fig.update_layout(
            margin=dict(t=34, b=16, l=60, r=100),
            paper_bgcolor="#ffffff", plot_bgcolor="#ffffff",
            font=dict(family="Inter, Segoe UI, system-ui, sans-serif",
                      size=12, color="#111827"),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="#ffffff", bordercolor="#e5e7eb",
                            font_family="Inter, Segoe UI, system-ui, sans-serif",
                            font_size=11),
            height=240 * n_rows,
            showlegend=True,
            legend=dict(orientation="h", x=1.0, xanchor="right",
                        y=1.12, yanchor="bottom", font_size=10,
                        bgcolor="rgba(0,0,0,0)", borderwidth=0),
        )
