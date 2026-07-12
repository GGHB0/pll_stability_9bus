"""
loader.py — Carrega os CSVs exportados pelo MATLAB e calcula métricas pós-falta.

Classe principal: SimData
    .t, .P_ufv, .Q_ufv, .theta_err → arrays NumPy prontos para plotar
    .t_fast, .theta_pll_fast,   → ângulos na taxa nativa Ts (alta resolução)
    .theta_ref_fast, .theta_err_fast
    .metrics                     → dict com IAE, ISE, ts, ts_delta, settled,
                                   peak_err, dP/dQ (pós-clear), vmin
    .has_ang, .has_dq_ufv, .has_ref_ufv → flags de disponibilidade de colunas

Dois CSVs exportados pelo MATLAB:
    sim_data.csv        → P_ufv, Q_ufv, id_ufv, iq_ufv a Tsc (eixo lento)
    sim_data_angles.csv → theta_pll, theta_ref, theta_err a Ts (eixo rápido)
"""

from __future__ import annotations
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ..config import T_FAULT, T_SETTLE, TOL_RAD


class SimData:
    """Carrega sim_data.csv (+ sim_data_angles.csv se disponível) e expõe dados + métricas."""

    def __init__(self, csv_path: Path) -> None:
        self._path = Path(csv_path)
        self._df   = pd.read_csv(self._path)
        self._cols  = set(self._df.columns)

        # ── instante de falta (t_fault/t_clear reais do cenário) ───────────────
        # fault_info.json é salvo por export_sim_data.m ao lado do CSV. Regime
        # permanente não tem falta: t_fault/t_clear ficam None (sem linhas no gráfico).
        self.t_fault: float | None = T_FAULT
        self.t_clear: float | None = None
        info_path = self._path.with_name("fault_info.json")
        if info_path.exists():
            info = json.loads(info_path.read_text(encoding="utf-8"))
            if info.get("fault_type") == "regime":
                self.t_fault = self.t_clear = None
            else:
                self.t_fault = info.get("t_fault", T_FAULT)
                self.t_clear = info.get("t_clear")

        # ── flags ────────────────────────────────────────────────────────────
        self.has_ang      = {"theta_pll_rad", "theta_ref_rad"} <= self._cols  # formato legado
        self.has_dq_ufv   = {"id_ufv_pu", "iq_ufv_pu"} <= self._cols
        self.has_ref_ufv  = {"id_ufv_ref_pu", "iq_ufv_ref_pu"} <= self._cols
        self.has_vdq_ufv  = {"vd_ufv_pu", "vq_ufv_pu"} <= self._cols
        self.has_vdq_rede = {"vd_rede_pu", "vq_rede_pu"} <= self._cols

        # ── eixo de tempo e sinais principais ────────────────────────────────
        self.t     = self._df["t_s"].to_numpy()
        self.P_ufv = self._df["P_ufv_pu"].to_numpy()
        self.Q_ufv = self._df["Q_ufv_pu"].to_numpy()

        # ── ângulos: arquivo dedicado (alta resolução) ou colunas legadas ────
        angles_path = self._path.with_name("sim_data_angles.csv")
        if angles_path.exists():
            df_a = pd.read_csv(angles_path)
            self.t_fast         = df_a["t_s"].to_numpy()
            self.theta_pll_fast = df_a["theta_pll_rad"].to_numpy()
            self.theta_ref_fast = df_a["theta_ref_rad"].to_numpy()
            raw_fast            = df_a["theta_err_rad"].to_numpy()
            # Interpola o dado bruto para o eixo lento; o bloco abaixo aplica
            # wrapping e baseline correction tanto em raw (lento) quanto em fast
            raw = np.interp(self.t, self.t_fast, raw_fast)
            # theta_err_fast será preenchido após o bloco de correção abaixo
            self._raw_fast = raw_fast
            self.theta_err_fast = None   # placeholder — definido após correção
            self.has_ang = True
        elif "theta_err_rad" in self._cols:
            raw = self._df["theta_err_rad"].to_numpy()
            self.t_fast = self.theta_pll_fast = self.theta_ref_fast = self.theta_err_fast = None
        elif self.has_ang:
            raw = (self._df["theta_pll_rad"] - self._df["theta_ref_rad"]).to_numpy()
            self.t_fast = self.theta_pll_fast = self.theta_ref_fast = self.theta_err_fast = None
        else:
            raw = None
            self.t_fast = self.theta_pll_fast = self.theta_ref_fast = self.theta_err_fast = None

        # Ang_pll and Ang_Rede are sawtooth-wrapped (0→2π→0); wrapping to
        # [-π, π] removes ±2π spikes from misaligned resets.
        # Baseline = value of the error at the last sample before T_FAULT so
        # that theta_err ≈ 0 at the fault instant, making IAE/ISE/ts measure
        # only the fault-induced deviation (not pre-existing drift from the
        # Repeating-Sequence reference mismatch).
        if raw is not None:
            wrapped = np.arctan2(np.sin(raw), np.cos(raw))
            t_arr = self._df["t_s"].to_numpy()
            t_fault = self.t_fault if self.t_fault is not None else T_FAULT
            idx_fault = int(np.searchsorted(t_arr, t_fault))
            baseline = float(wrapped[idx_fault - 1]) if idx_fault > 0 else 0.0
            if baseline != 0.0:
                wrapped = np.arctan2(np.sin(wrapped - baseline), np.cos(wrapped - baseline))
            self.theta_err = wrapped

            # Aplica a mesma correção no eixo rápido quando disponível
            if hasattr(self, "_raw_fast"):
                wf = np.arctan2(np.sin(self._raw_fast), np.cos(self._raw_fast))
                if baseline != 0.0:
                    wf = np.arctan2(np.sin(wf - baseline), np.cos(wf - baseline))
                self.theta_err_fast = wf
                del self._raw_fast
        else:
            self.theta_err = None

        if self.theta_pll_fast is not None:
            # Usa o eixo rápido diretamente
            self.theta_pll = self.theta_pll_fast
            self.theta_ref = self.theta_ref_fast
        elif self.has_ang:
            self.theta_pll = self._df["theta_pll_rad"].to_numpy()
            self.theta_ref = self._df["theta_ref_rad"].to_numpy()
        else:
            self.theta_pll = self.theta_ref = None

        # ── correntes abc (sim_data_abc.csv, taxa nativa — espectro fase A) ──
        self.has_iabc_ufv = self.has_iabc_grid = False
        self.t_abc = self.ia_ufv = self.ib_ufv = self.ic_ufv = None
        self.ia_grid = self.ib_grid = self.ic_grid = None
        abc_path = self._path.with_name("sim_data_abc.csv")
        if abc_path.exists():
            df_abc = pd.read_csv(abc_path)
            cols_abc = set(df_abc.columns)
            self.t_abc = df_abc["t_s"].to_numpy()
            if {"ia_ufv_pu", "ib_ufv_pu", "ic_ufv_pu"} <= cols_abc:
                self.ia_ufv = df_abc["ia_ufv_pu"].to_numpy()
                self.ib_ufv = df_abc["ib_ufv_pu"].to_numpy()
                self.ic_ufv = df_abc["ic_ufv_pu"].to_numpy()
                self.has_iabc_ufv = True
            if {"ia_grid_pu", "ib_grid_pu", "ic_grid_pu"} <= cols_abc:
                self.ia_grid = df_abc["ia_grid_pu"].to_numpy()
                self.ib_grid = df_abc["ib_grid_pu"].to_numpy()
                self.ic_grid = df_abc["ic_grid_pu"].to_numpy()
                self.has_iabc_grid = True

        # ── geradores G1 e G3 ────────────────────────────────────────────────
        self.has_gen1 = {"ang_g1_rad", "pe_g1_pu"} <= self._cols
        self.has_gen3 = {"ang_g3_rad", "pe_g3_pu"} <= self._cols

        if self.has_gen1:
            self.ang_g1 = self._df["ang_g1_rad"].to_numpy()
            self.pe_g1  = self._df["pe_g1_pu"].to_numpy()
        else:
            self.ang_g1 = self.pe_g1 = None

        if self.has_gen3:
            self.ang_g3 = self._df["ang_g3_rad"].to_numpy()
            self.pe_g3  = self._df["pe_g3_pu"].to_numpy()
        else:
            self.ang_g3 = self.pe_g3 = None

        # ── tensões de barra ─────────────────────────────────────────────────
        self.has_vbus1 = "vbus1_pu" in self._cols
        self.vbus1 = self._df["vbus1_pu"].to_numpy() if self.has_vbus1 else None

        self.has_vbus2 = "vbus2_pu" in self._cols
        self.vbus2 = self._df["vbus2_pu"].to_numpy() if self.has_vbus2 else None

        self.has_vbus3 = "vbus3_pu" in self._cols
        self.vbus3 = self._df["vbus3_pu"].to_numpy() if self.has_vbus3 else None

        # ── P/Q de barra (coluna (1) do Mux — sinal medido) ─────────────────
        self.has_pq_bus1 = {"p_bus1_pu", "q_bus1_pu"} <= self._cols
        if self.has_pq_bus1:
            self.p_bus1 = self._df["p_bus1_pu"].to_numpy()
            self.q_bus1 = self._df["q_bus1_pu"].to_numpy()
        else:
            self.p_bus1 = self.q_bus1 = None

        self.has_pq_bus3 = {"p_bus3_pu", "q_bus3_pu"} <= self._cols
        if self.has_pq_bus3:
            self.p_bus3 = self._df["p_bus3_pu"].to_numpy()
            self.q_bus3 = self._df["q_bus3_pu"].to_numpy()
        else:
            self.p_bus3 = self.q_bus3 = None

        # ── tensões dq inversor e rede ───────────────────────────────────────
        if self.has_vdq_ufv:
            self.vd_ufv = self._df["vd_ufv_pu"].to_numpy()
            self.vq_ufv = self._df["vq_ufv_pu"].to_numpy()
        else:
            self.vd_ufv = self.vq_ufv = None

        if self.has_vdq_rede:
            self.vd_rede = self._df["vd_rede_pu"].to_numpy()
            self.vq_rede = self._df["vq_rede_pu"].to_numpy()
        else:
            self.vd_rede = self.vq_rede = None

        # ── correntes dq ─────────────────────────────────────────────────────
        if self.has_dq_ufv:
            self.id_ufv_meas = self._df["id_ufv_pu"].to_numpy()
            self.iq_ufv_meas = self._df["iq_ufv_pu"].to_numpy()
        else:
            self.id_ufv_meas = self.iq_ufv_meas = None

        if self.has_ref_ufv:
            self.id_ufv_ref = self._df["id_ufv_ref_pu"].to_numpy()
            self.iq_ufv_ref = self._df["iq_ufv_ref_pu"].to_numpy()
        else:
            self.id_ufv_ref = self.iq_ufv_ref = None

        # ── frequência estimada do PLL ───────────────────────────────────────
        self._estimate_freq()

        # ── métricas ─────────────────────────────────────────────────────────
        self.metrics = self._compute_metrics()

    # ── internos ─────────────────────────────────────────────────────────────

    def _estimate_freq(self) -> None:
        """f̂ = dθ̂/dt / 2π (Hz) por diferença central com janela ~1 ms.

        A diferença com passo largo (k amostras ≈ 0,5 ms para cada lado) já
        atua como filtro passa-baixa, suprimindo o ripple de chaveamento sem
        precisar de convolução sobre os milhões de pontos do eixo rápido.
        """
        if self.theta_pll_fast is not None:
            t, th = self.t_fast, self.theta_pll_fast
        elif self.theta_pll is not None:
            t, th = self.t, self.theta_pll
        else:
            t = th = None

        if t is None or len(t) < 3:
            self.t_freq = self.f_pll = None
            self.has_freq = False
            return

        th_u = np.unwrap(th)
        dt = float(np.median(np.diff(t[: min(len(t), 1000)])))
        k = max(1, int(round(5e-4 / dt))) if dt > 0 else 1
        if 2 * k >= len(t):
            k = 1
        self.f_pll = (th_u[2 * k:] - th_u[:-2 * k]) / (t[2 * k:] - t[:-2 * k]) / (2.0 * np.pi)
        self.t_freq = t[k:-k]
        self.has_freq = True

    def _compute_metrics(self) -> dict:
        """Métricas em duas janelas: pós-falta (t ≥ t_fault → erro de fase, V_min)
        e pós-clear (t ≥ t_clear → ΔP/ΔQ de recuperação, sem o afundamento em si).
        Nenhuma janela começa antes de T_SETTLE: o transitório de partida do PLL
        (trava em ~0.08 s) não é falta de desempenho e fica fora das integrais.
        Regime permanente (t_fault None) usa t ≥ T_SETTLE nas duas janelas."""
        is_regime = self.t_fault is None
        t_start = min(T_SETTLE, float(self.t[-1])) if is_regime \
            else max(self.t_fault, T_SETTLE)
        t_rec   = self.t_clear if (not is_regime and self.t_clear is not None) else t_start
        t_rec   = max(t_rec, T_SETTLE)
        mask     = self.t >= t_start
        mask_rec = self.t >= t_rec
        metrics: dict = {
            "IAE": None, "ISE": None, "ts": None, "ts_delta": None,
            "peak_err": None, "settled": None,
        }

        if self.theta_err is not None:
            t_pf = self.t[mask]
            e_pf = self.theta_err[mask]
            if len(t_pf):
                metrics["IAE"]      = float(np.trapezoid(np.abs(e_pf), t_pf))
                metrics["ISE"]      = float(np.trapezoid(e_pf ** 2,    t_pf))
                metrics["peak_err"] = float(np.abs(e_pf).max())
                fora = t_pf[np.abs(e_pf) > TOL_RAD]
                # "Acomodou" exige |e| dentro da tolerância até o fim da janela
                # (margem de 2 ms); sem isso o último sample fora vira ts falso
                # em cenários que nunca reacomodam dentro da simulação.
                if len(fora) == 0:
                    metrics["ts"], metrics["settled"] = float(t_pf[0]), True
                elif float(fora[-1]) >= float(t_pf[-1]) - 2e-3:
                    metrics["ts"], metrics["settled"] = None, False
                else:
                    metrics["ts"], metrics["settled"] = float(fora[-1]), True
                if metrics["ts"] is not None:
                    metrics["ts_delta"] = metrics["ts"] - t_start

        p_rec = self.P_ufv[mask_rec]
        q_rec = self.Q_ufv[mask_rec]
        metrics["dP_ufv"] = float(p_rec.max() - p_rec.min()) if len(p_rec) else None
        metrics["dQ_ufv"] = float(q_rec.max() - q_rec.min()) if len(q_rec) else None
        if self.vbus2 is not None:
            v_pf = self.vbus2[mask]
            metrics["vmin"] = float(v_pf.min()) if len(v_pf) else None
        else:
            metrics["vmin"] = None
        return metrics

    # ── __repr__ ─────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        n = len(self.t)
        m = self.metrics
        return (
            f"SimData(n={n}, "
            f"IAE={m.get('IAE')}, ISE={m.get('ISE')}, "
            f"ts={m.get('ts')}, dP_ufv={m.get('dP_ufv'):.4f}, dQ_ufv={m.get('dQ_ufv'):.4f})"
        )
