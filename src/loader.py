"""
loader.py — Carrega o CSV exportado pelo MATLAB e calcula métricas pós-falta.

Classe principal: SimData
    .t, .P, .Q, .theta_err      → arrays NumPy prontos para plotar
    .metrics                     → dict com IAE, ISE, ts, dP, dQ
    .has_ang, .has_dq, .has_ref  → flags de disponibilidade de colunas
"""

from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

from .config import T_FAULT, TOL_RAD


class SimData:
    """Carrega sim_data.csv e expõe dados + métricas calculadas."""

    def __init__(self, csv_path: Path) -> None:
        self._path = csv_path
        self._df   = pd.read_csv(csv_path)
        self._cols  = set(self._df.columns)

        # ── flags ────────────────────────────────────────────────────────────
        self.has_ang = {"theta_pll_rad", "theta_ref_rad"} <= self._cols
        self.has_dq  = {"id_pu", "iq_pu"} <= self._cols
        self.has_ref = {"id_ref_pu", "iq_ref_pu"} <= self._cols  # novo formato

        # ── eixo de tempo e sinais principais ────────────────────────────────
        self.t = self._df["t_s"].to_numpy()
        self.P = self._df["P_pu"].to_numpy()
        self.Q = self._df["Q_pu"].to_numpy()

        # ── ângulos ──────────────────────────────────────────────────────────
        if "theta_err_rad" in self._cols:
            self.theta_err = self._df["theta_err_rad"].to_numpy()
        elif self.has_ang:
            self.theta_err = (
                self._df["theta_pll_rad"] - self._df["theta_ref_rad"]
            ).to_numpy()
        else:
            self.theta_err = None

        if self.has_ang:
            self.theta_pll = self._df["theta_pll_rad"].to_numpy()
            self.theta_ref = self._df["theta_ref_rad"].to_numpy()
        else:
            self.theta_pll = self.theta_ref = None

        # ── correntes dq ─────────────────────────────────────────────────────
        if self.has_dq:
            self.id_meas = self._df["id_pu"].to_numpy()
            self.iq_meas = self._df["iq_pu"].to_numpy()
        else:
            self.id_meas = self.iq_meas = None

        if self.has_ref:
            self.id_ref = self._df["id_ref_pu"].to_numpy()
            self.iq_ref = self._df["iq_ref_pu"].to_numpy()
        else:
            self.id_ref = self.iq_ref = None

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

        metrics["dP"] = float(self.P[mask].max() - self.P[mask].min())
        metrics["dQ"] = float(self.Q[mask].max() - self.Q[mask].min())
        return metrics

    # ── __repr__ ─────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        n = len(self.t)
        m = self.metrics
        return (
            f"SimData(n={n}, "
            f"IAE={m.get('IAE')}, ISE={m.get('ISE')}, "
            f"ts={m.get('ts')}, dP={m.get('dP'):.4f}, dQ={m.get('dQ'):.4f})"
        )
