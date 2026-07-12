"""
spectrum.py — Espectro de Fourier por segmento temporal.

SpectrumBuilder(data).build() → (fig | None, trace_map)

Cada sinal (θ_err, i_q, Q) vira um painel; cada segmento (pré-falta / falta /
pós-falta, ou janela única em regime) vira um traço de amplitude |FFT|.
No referencial dq a fundamental vira DC (removida com a média) e a sequência
negativa da falta assimétrica aparece como pico em 120 Hz (2ª harmônica).
"""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..config import (
    T_SETTLE, SPEC_FMAX_HZ, SPEC_XRANGE_HZ, F_2H_HZ, F_RES_LCL_HZ,
    SPEC_SEG_COLORS,
)
from .loader import SimData

_MIN_DUR_S   = 0.05   # janela menor que isso → df > 20 Hz, não resolve 120 Hz
_MIN_SAMPLES = 64
_AMP_FLOOR   = 1e-5   # piso de amplitude → −100 dB (evita log(0) e ruído numérico)


def _amplitude_spectrum(t: np.ndarray, y: np.ndarray,
                        fmax: float = SPEC_FMAX_HZ):
    """|FFT| de amplitude em dB: reamostra em grade uniforme, remove a média
    (fundamental → DC no dq) e aplica janela de Hann. Retorna (f, amp_db) com
    0 < f ≤ fmax e amp_db = 20·log10(amp) re 1 pu/rad (piso −100 dB), ou None
    se o segmento for curto demais."""
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
    amp_db = 20.0 * np.log10(np.maximum(amp[m], _AMP_FLOOR))
    return f[m], amp_db


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
                f, amp_db = res
                lc, dc = SPEC_SEG_COLORS[seg_name]
                fig.add_trace(go.Scatter(
                    x=f, y=amp_db, name=seg_name, mode="lines",
                    line=dict(width=1.6, color=lc),
                    legendgroup=seg_name, showlegend=(ri == 1),
                    hovertemplate="%{x:.0f} Hz · %{y:.1f} dB<extra>" + seg_name + "</extra>",
                ), row=ri, col=1)
                tm.append((len(fig.data) - 1, lc, dc))
            self._label(fig, f"{label} — dB re 1 {unit}", ri)

        self._marker_lines(fig, n)
        self._apply_layout(fig, n)
        return fig, tm

    # ── Segmentos e sinais ───────────────────────────────────────────────────

    def _segments(self) -> list[tuple[str, float, float]]:
        """Janelas de análise. Pré-falta começa em T_SETTLE (config) para
        descartar o transitório de partida do PLL — não é falta de desempenho,
        é o PLL ainda travando na rede."""
        d = self._d
        t_end = float(d.t[-1])
        if d.t_fault is None:
            return [("Regime", min(T_SETTLE, t_end), t_end)]
        segs = [("Pré-falta", min(T_SETTLE, d.t_fault), d.t_fault)]
        if d.t_clear is not None and d.t_clear < t_end:
            segs.append(("Falta", d.t_fault, d.t_clear))
            segs.append(("Pós-falta", d.t_clear, t_end))
        else:
            segs.append(("Falta", d.t_fault, t_end))
        return segs

    def _signals(self) -> list[tuple[str, np.ndarray, np.ndarray, str]]:
        d = self._d
        sigs: list[tuple[str, np.ndarray, np.ndarray, str]] = []
        if d.theta_err is not None:
            if d.theta_err_fast is not None:
                sigs.append(("Erro de fase θ<sub>err</sub>",
                             d.t_fast, d.theta_err_fast, "rad"))
            else:
                sigs.append(("Erro de fase θ<sub>err</sub>",
                             d.t, d.theta_err, "rad"))
        if d.has_dq_ufv:
            sigs.append(("Corrente i<sub>q</sub> UFV", d.t, d.iq_ufv_meas, "pu"))
        sigs.append(("Potência reativa Q UFV", d.t, d.Q_ufv, "pu"))
        if d.has_iabc_ufv:
            # abc: fundamental fica em 60 Hz (não vira DC como no dq); a
            # seq. negativa cai TAMBÉM em 60 Hz — usar junto com os painéis dq
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
        """Linhas de referência: 120 Hz (2ª harm. no dq) e ressonância LCL."""
        markers = ((F_2H_HZ, "rgba(220,50,50,0.55)", "2f = 120 Hz"),
                   (F_RES_LCL_HZ, "rgba(147,51,234,0.5)", "f<sub>res</sub> LCL"))
        for freq, color, text in markers:
            if freq > SPEC_FMAX_HZ:
                continue
            for ri in range(1, n_rows + 1):
                fig.add_vline(x=freq,
                              line=dict(color=color, width=1.2, dash="dash"),
                              row=ri, col=1)
            fig.add_annotation(
                text=text, x=freq, xref="x", yref="y domain", y=1.06,
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
            title_text="Amplitude (dB)", title_font_size=11,
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
