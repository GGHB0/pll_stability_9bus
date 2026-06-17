"""
loader.py — Carrega os CSVs exportados pelo MATLAB e calcula métricas pós-falta.

Classe principal: SimData
    .t, .P_ufv, .Q_ufv, .theta_err → arrays NumPy prontos para plotar
    .t_fast, .theta_pll_fast,   → ângulos na taxa nativa Ts (alta resolução)
    .theta_ref_fast, .theta_err_fast
    .metrics                     → dict com IAE, ISE, ts, dP, dQ
    .has_ang, .has_dq_ufv, .has_ref_ufv → flags de disponibilidade de colunas

Dois CSVs exportados pelo MATLAB:
    sim_data.csv        → P_ufv, Q_ufv, id_ufv, iq_ufv a Tsc (eixo lento)
    sim_data_angles.csv → theta_pll, theta_ref, theta_err a Ts (eixo rápido)
"""

from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

from .config import T_FAULT, TOL_RAD


class SimData:
    """Carrega sim_data.csv (+ sim_data_angles.csv se disponível) e expõe dados + métricas."""

    def __init__(self, csv_path: Path) -> None:
        self._path = Path(csv_path)
        self._df   = pd.read_csv(self._path)
        self._cols  = set(self._df.columns)

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
            idx_fault = int(np.searchsorted(t_arr, T_FAULT))
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

        # ── tensão Barra 2 ───────────────────────────────────────────────────
        self.has_vbus2 = "vbus2_pu" in self._cols
        self.vbus2 = self._df["vbus2_pu"].to_numpy() if self.has_vbus2 else None

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

        # ── métricas ─────────────────────────────────────────────────────────
        self.metrics = self._compute_metrics()

    # ── internos ─────────────────────────────────────────────────────────────

    def _compute_metrics(self) -> dict:
        mask = self.t >= T_FAULT
        metrics: dict = {}

        if self.theta_err is not None:
            t_pf = self.t[mask]
            e_pf = self.theta_err[mask]
            metrics["IAE"] = float(np.trapezoid(np.abs(e_pf), t_pf))
            metrics["ISE"] = float(np.trapezoid(e_pf ** 2,    t_pf))
            fora = t_pf[np.abs(e_pf) > TOL_RAD]
            metrics["ts"]  = float(fora[-1]) if len(fora) else float(t_pf[0])
        else:
            metrics["IAE"] = metrics["ISE"] = metrics["ts"] = None

        metrics["dP_ufv"] = float(self.P_ufv[mask].max() - self.P_ufv[mask].min())
        metrics["dQ_ufv"] = float(self.Q_ufv[mask].max() - self.Q_ufv[mask].min())
        metrics["vmin"] = float(self.vbus2[mask].min()) if self.vbus2 is not None else None
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
