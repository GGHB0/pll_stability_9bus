"""
spectrum.py — Espectro de Fourier por segmento temporal.

SpectrumBuilder(data).build() → (figs, tms, harm)

figs/tms são dicts indexados por modo ("a", "b", "c", "d", "q"): cada modo é
uma figura com um painel de corrente e um de tensão UFV, com o tempo partido
em três segmentos — pré-falta, durante a falta e pós-falta. No referencial
abc a fundamental fica em 60 Hz; no dq ela vira DC (removida com a média) e
a sequência negativa da falta assimétrica aparece em 120 Hz. harm carrega a
amplitude das harmônicas 1–7 (k·60 Hz) por segmento/modo para a tabela do
relatório.
"""
from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..config import (
    T_SETTLE, SPEC_FMAX_HZ, SPEC_XRANGE_HZ, SPEC_MARKERS, SPEC_MARKERS_DQ,
    SPEC_SEG_COLORS, F_FUND_HZ,
)
from .loader import SimData

_MIN_DUR_S   = 0.05   # janela menor que isso → df > 20 Hz, não resolve 120 Hz
_MIN_SAMPLES = 64
_N_HARM      = 7      # harmônicas 1–7 extraídas para a tabela do relatório


def _amplitude_spectrum(t: np.ndarray, y: np.ndarray,
                        fmax: float = SPEC_FMAX_HZ):
    """|FFT| de amplitude LINEAR (pu): reamostra em grade uniforme, trunca a
    janela para um número INTEIRO de ciclos da fundamental (60 Hz cai exato
    num bin — sem vazamento por janela cortada no meio do ciclo), remove a
    média (offset DC; no abc a fundamental de 60 Hz permanece) e aplica janela
    de Hann. Retorna (f, amp) com 0 < f ≤ fmax e amp em pu — escala linear
    destaca os picos discretos (60 Hz + harmônicas) sobre o piso de ruído, ao
    contrário do dB. Retorna None se o segmento for curto demais."""
    if len(t) < _MIN_SAMPLES or (t[-1] - t[0]) < _MIN_DUR_S:
        return None
    dt = float(np.median(np.diff(t)))
    if dt <= 0:
        return None
    n_cyc = int(np.floor((t[-1] - t[0]) * F_FUND_HZ))
    if n_cyc < 1:
        return None
    n = int(round(n_cyc / F_FUND_HZ / dt))
    if n < _MIN_SAMPLES:
        return None
    t_u = t[0] + np.arange(n) * dt
    y_u = np.interp(t_u, t, y)
    y_u -= y_u.mean()
    w   = np.hanning(len(y_u))
    amp = 2.0 * np.abs(np.fft.rfft(y_u * w)) / w.sum()
    f   = np.fft.rfftfreq(len(y_u), dt)
    m   = (f > 0) & (f <= fmax)
    return f[m], amp[m]


def _harmonics(f: np.ndarray, amp: np.ndarray) -> list[float | None]:
    """Amplitude nas harmônicas k·60 Hz (k = 1…_N_HARM): pico local em
    ±1,5 bin em torno da frequência alvo — a janela de Hann espalha um tom
    bin-centrado em 3 bins, com o pico verdadeiro no bin central."""
    if len(f) < 2:
        return [None] * _N_HARM
    df  = float(f[1] - f[0])
    out: list[float | None] = []
    for k in range(1, _N_HARM + 1):
        m = np.abs(f - k * F_FUND_HZ) <= 1.5 * df
        out.append(float(amp[m].max()) if m.any() else None)
    return out


class SpectrumBuilder:
    """Monta as figuras de espectro segmentado (uma por fase/eixo) e a
    tabela de harmônicas a partir de um SimData."""

    def __init__(self, data: SimData) -> None:
        self._d = data

    # ── API pública ──────────────────────────────────────────────────────────

    def build(self) -> tuple[dict[str, go.Figure],
                             dict[str, list[tuple[int, str, str]]],
                             dict]:
        modes = self._modes()
        segs  = self._segments()
        if not modes or not segs:
            return {}, {}, {}

        # harm["i"|"v"][segmento][modo] = [amp h1 … h7] (pu)
        harm: dict = {"segs": [s[0] for s in segs], "i": {}, "v": {}}
        figs: dict[str, go.Figure] = {}
        tms:  dict[str, list[tuple[int, str, str]]] = {}
        for mode, sigs in modes.items():
            figs[mode], tms[mode] = self._mode_fig(mode, sigs, segs, harm)
        return figs, tms, harm

    # ── Segmentos e sinais ───────────────────────────────────────────────────

    def _segments(self) -> list[tuple[str, float, float]]:
        """Três janelas: pré-falta, durante a falta e pós-falta, cortadas em
        t_fault/t_clear (reais do cenário, via fault_info.json). A janela de
        pré-falta começa em T_SETTLE (config) para descartar o transitório de
        partida do PLL — não é falta de desempenho, é o PLL ainda travando na
        rede. Sem t_clear (falta permanente ou ausente), "durante a falta" vai
        até o fim da simulação e não há segmento pós-falta."""
        d = self._d
        t_end = float(d.t[-1])
        if d.t_fault is None:
            return [("Regime", min(T_SETTLE, t_end), t_end)]
        segs = [("Pré-falta", min(T_SETTLE, d.t_fault), d.t_fault)]
        if d.t_clear is not None and d.t_clear < t_end:
            segs.append(("Durante a falta", d.t_fault, d.t_clear))
            segs.append(("Pós-falta", d.t_clear, t_end))
        else:
            segs.append(("Durante a falta", d.t_fault, t_end))
        return segs

    def _modes(self) -> dict[str, list[tuple[str, str, np.ndarray, np.ndarray]]]:
        """{modo: [(kind, label, t, y), …]} com kind ∈ {"i", "v"} ligando o
        sinal à tabela de harmônicas. Fases abc usam t_abc (Ts rápido); eixos
        d/q usam t (Tsc). No dq a seq. negativa aparece isolada em 120 Hz —
        assinatura da falta assimétrica que no abc cai junto com os 60 Hz."""
        d = self._d
        modes: dict[str, list] = {}
        for ph in ("a", "b", "c"):
            rows = []
            if d.has_iabc_ufv:
                rows.append(("i", f"Corrente i<sub>{ph}</sub> UFV (abc)",
                             d.t_abc, getattr(d, f"i{ph}_ufv")))
            if d.has_vabc_ufv:
                rows.append(("v", f"Tensão v<sub>{ph}</sub> UFV (abc)",
                             d.t_abc, getattr(d, f"v{ph}_ufv")))
            if rows:
                modes[ph] = rows
        for ax in ("d", "q"):
            rows = []
            if d.has_dq_ufv:
                rows.append(("i", f"Corrente i<sub>{ax}</sub> UFV (dq)",
                             d.t, getattr(d, f"i{ax}_ufv_meas")))
            if d.has_vdq_ufv:
                rows.append(("v", f"Tensão v<sub>{ax}</sub> UFV (dq)",
                             d.t, getattr(d, f"v{ax}_ufv")))
            if rows:
                modes[ax] = rows
        return modes

    # ── Figura de um modo ────────────────────────────────────────────────────

    def _mode_fig(self, mode: str, sigs: list, segs: list,
                  harm: dict) -> tuple[go.Figure, list[tuple[int, str, str]]]:
        n = len(sigs)
        fig = make_subplots(rows=n, cols=1, shared_xaxes=True,
                            vertical_spacing=0.13)
        tm: list[tuple[int, str, str]] = []

        for ri, (kind, label, t, y) in enumerate(sigs, 1):
            for seg_name, t0, t1 in segs:
                mask = (t >= t0) & (t <= t1)
                res = _amplitude_spectrum(t[mask], y[mask])
                if res is None:
                    continue
                f, amp = res
                harm[kind].setdefault(seg_name, {})[mode] = _harmonics(f, amp)
                lc, dc = SPEC_SEG_COLORS[seg_name]
                fig.add_trace(go.Scatter(
                    x=f, y=amp, name=seg_name, mode="lines",
                    line=dict(width=1.6, color=lc),
                    legendgroup=seg_name, showlegend=(ri == 1),
                    hovertemplate="%{x:.0f} Hz · %{y:.3g} pu<extra>" + seg_name + "</extra>",
                ), row=ri, col=1)
                tm.append((len(fig.data) - 1, lc, dc))
            self._label(fig, label, ri, n)

        markers = SPEC_MARKERS if mode in ("a", "b", "c") else SPEC_MARKERS_DQ
        self._marker_lines(fig, n, markers)
        self._apply_layout(fig, n)
        return fig, tm

    # ── Helpers de figura ────────────────────────────────────────────────────

    @staticmethod
    def _label(fig: go.Figure, text: str, ax_idx: int, n_rows: int) -> None:
        """Barra de título (nome do sinal) no topo do painel, acima das
        marcações de frequência. A unidade "Amplitude (pu)" fica no eixo Y, na
        vertical (setada em _apply_layout) — Ponto 2 do professor."""
        xname = "xaxis" if ax_idx == 1 else f"xaxis{ax_idx}"
        yname = "yaxis" if ax_idx == 1 else f"yaxis{ax_idx}"
        ax_dom = fig.layout[xname].domain
        y_top  = float(fig.layout[yname].domain[1])
        xc     = float((ax_dom[0] + ax_dom[1]) / 2)
        y0 = y_top + 16.0 / (240 * n_rows)   # acima dos marcadores (y=1.05)
        y1 = y0 + 22.0 / (240 * n_rows)
        fig.add_shape(
            type="rect", xref="paper", yref="paper",
            x0=ax_dom[0], x1=ax_dom[1], y0=y0, y1=y1,
            fillcolor="#185FA5", line_width=0, layer="above",
        )
        fig.add_annotation(
            text=f"<b>{text}</b>", xref="paper", yref="paper",
            x=xc, y=(y0 + y1) / 2, xanchor="center", yanchor="middle",
            font=dict(size=11, color="#ffffff"), showarrow=False,
        )

    @staticmethod
    def _marker_lines(fig: go.Figure, n_rows: int, markers) -> None:
        """Linhas tracejadas nas frequências características: no abc,
        fundamental + harmônicas ímpares (SPEC_MARKERS); no dq, 2f₁/6f₁/12f₁
        (SPEC_MARKERS_DQ). Ressonância LCL nos dois."""
        color = "rgba(120,120,130,0.45)"
        for freq, text in markers:
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
            margin=dict(t=64, b=16, l=64, r=100),
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
                        y=1.22, yanchor="bottom", font_size=10,
                        bgcolor="rgba(0,0,0,0)", borderwidth=0),
        )
