"""
analyze_sim_data.py
Lê sim_data.csv exportado pelo export_sim_data.m e calcula métricas do PLL.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

CSV = "sim_data.csv"
T_FAULT = 0.5      # instante da falta (s) — ajustar conforme cenário
T_END   = None     # None = até o final
TOL_RAD = 0.02     # tolerância para tempo de acomodação (rad ≈ 1,15°)

# ── Leitura ──────────────────────────────────────────────────────────────────
df = pd.read_csv(CSV)
t  = df["t_s"].to_numpy()

theta_err = df["theta_err_rad"].to_numpy()
P         = df["P_pu"].to_numpy()
Q         = df["Q_pu"].to_numpy()
id_       = df["id_pu"].to_numpy()
iq        = df["iq_pu"].to_numpy()

# ── Métricas (janela pós-falta) ───────────────────────────────────────────────
mask = t >= T_FAULT
t_pf = t[mask]
e_pf = theta_err[mask]

IAE = np.trapz(np.abs(e_pf), t_pf)
ISE = np.trapz(e_pf**2, t_pf)

fora_tol = t_pf[np.abs(e_pf) > TOL_RAD]
ts = float(fora_tol[-1]) if len(fora_tol) > 0 else float(t_pf[0])

delta_P = P[mask].max() - P[mask].min()
delta_Q = Q[mask].max() - Q[mask].min()

print("=== Métricas PLL (pós-falta) ===")
print(f"  IAE           = {IAE:.4f} rad·s")
print(f"  ISE           = {ISE:.4f} rad²·s")
print(f"  ts (±{TOL_RAD} rad) = {ts:.4f} s")
print(f"  ΔP            = {delta_P:.4f} pu")
print(f"  ΔQ            = {delta_Q:.4f} pu")

# ── Gráficos ─────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(3, 2, figsize=(12, 9), sharex=True)

axes[0, 0].plot(t, np.degrees(df["theta_pll_rad"]), label="θ̂ PLL")
axes[0, 0].plot(t, np.degrees(df["theta_ref_rad"]), "--", label="θ rede")
axes[0, 0].set_ylabel("Ângulo (°)")
axes[0, 0].legend()

axes[0, 1].plot(t, np.degrees(theta_err))
axes[0, 1].axhline(np.degrees(TOL_RAD), color="r", linestyle="--", linewidth=0.8)
axes[0, 1].axhline(-np.degrees(TOL_RAD), color="r", linestyle="--", linewidth=0.8)
axes[0, 1].set_ylabel("Erro de fase (°)")

axes[1, 0].plot(t, P)
axes[1, 0].set_ylabel("P (pu)")

axes[1, 1].plot(t, Q)
axes[1, 1].set_ylabel("Q (pu)")

axes[2, 0].plot(t, id_, label="id")
axes[2, 0].plot(t, iq, label="iq")
axes[2, 0].set_ylabel("Corrente dq (pu)")
axes[2, 0].set_xlabel("Tempo (s)")
axes[2, 0].legend()

axes[2, 1].axis("off")

for ax in axes.flat:
    ax.axvline(T_FAULT, color="k", linestyle=":", linewidth=0.8)
    ax.grid(True, linewidth=0.4)

plt.tight_layout()
plt.savefig("pll_metrics.png", dpi=150)
plt.show()
print("Figura salva: pll_metrics.png")
