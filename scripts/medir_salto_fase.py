"""Separa, no primeiro ciclo de uma falta, o salto de fase da tensao e a resposta do SRF-PLL.

    .venv\\Scripts\\python.exe scripts\\medir_salto_fase.py bus7/3phase line7_8/3phase line8_9/3phase bus6/3phase

A fase da tensao sai direto das tensoes abc do inversor (Clarke, sem passar pelo
PLL), relativa a uma referencia girando a 60 Hz e zerada no ciclo pre-falta. A fase
do PLL sai de theta_pll_rad, com a mesma referencia. O erro e o de gen_erro_fase.py
(atan2(vq, vd) da tensao no referencial do PLL).

Colunas: salto sustentado (media dos ciclos 2 a 5 da falta), faixa da fase da tensao
e do |v| no 1o ciclo, faixa da fase do PLL no 1o ciclo, pico do |erro| no 1o ciclo e
depois dele ate a eliminacao. Analise em kb/pll/contingencias/pll_phase_jump_fault_inception.md.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
W = 2 * np.pi * 60
CICLO_S = 1 / 60


def fase_rel(t, ang, tf):
    """Fase relativa a 60 Hz, em graus, zerada pela mediana do ciclo pre-falta."""
    rel = np.unwrap(ang) - W * t
    return np.degrees(rel - np.median(rel[(t > tf - CICLO_S) & (t < tf)]))


def medir(folder):
    base = ROOT / "output" / "results" / folder
    fi = json.loads((base / "fault_info.json").read_text())
    tf, tc = fi["t_fault"], fi["t_clear"]
    a = pd.read_csv(base / "sim_data_abc.csv")
    s = pd.read_csv(base / "sim_data.csv")
    g = pd.read_csv(base / "sim_data_angles.csv")

    t = a.t_s.to_numpy()
    va, vb, vc = a.va_ufv_pu.to_numpy(), a.vb_ufv_pu.to_numpy(), a.vc_ufv_pu.to_numpy()
    alfa = (2 * va - vb - vc) / 3
    beta = (vb - vc) / np.sqrt(3)
    mag = np.hypot(alfa, beta)
    fv = fase_rel(t, np.arctan2(beta, alfa), tf)

    tp = g.t_s.to_numpy()
    fp = fase_rel(tp, g.theta_pll_rad.to_numpy(), tf)

    ts = s.t_s.to_numpy()
    e = np.degrees(np.arctan2(s.vq_rede_pu.to_numpy(), s.vd_rede_pu.to_numpy()))

    c1 = (t >= tf) & (t < tf + CICLO_S)
    c25 = (t >= tf + CICLO_S) & (t < tf + 5 * CICLO_S)
    p1 = (tp >= tf) & (tp < tf + CICLO_S)
    e1 = (ts >= tf) & (ts < tf + CICLO_S)
    e2 = (ts >= tf + CICLO_S) & (ts <= tc)
    return dict(
        salto=np.mean(fv[c25]),
        fv=(fv[c1].min(), fv[c1].max()),
        mag=(mag[c1].min(), mag[c1].max()),
        fp=(fp[p1].min(), fp[p1].max()),
        e1=np.abs(e[e1]).max(),
        e2=np.abs(e[e2]).max(),
    )


def main(folders):
    print("cenario           salto  fase tensao 1o ciclo   |v| 1o ciclo   fase PLL 1o ciclo   erro 1o  erro depois")
    for f in folders:
        m = medir(f)
        print(f"{f:16s} {m['salto']:6.1f}   {m['fv'][0]:7.1f} a {m['fv'][1]:6.1f}   "
              f"{m['mag'][0]:.2f} a {m['mag'][1]:.2f}   {m['fp'][0]:6.1f} a {m['fp'][1]:5.1f}     "
              f"{m['e1']:6.1f}   {m['e2']:6.1f}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["bus7/3phase", "line7_8/3phase", "line8_9/3phase", "bus6/3phase"])
