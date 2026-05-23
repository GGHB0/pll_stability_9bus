"""
Illustrative plots: short-circuit with reduced machine inertia
Shows why the inverter output goes to zero after fault clearance.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'lines.linewidth': 2,
    'figure.facecolor': 'white',
    'axes.facecolor': '#f8f9fa',
    'axes.grid': True,
    'grid.alpha': 0.4,
})

t = np.linspace(0, 1.5, 3000)
t_fault_on  = 0.3   # fault starts
t_fault_off = 0.5   # fault cleared

def sigmoid(t, t0, k=40):
    return 1 / (1 + np.exp(-k * (t - t0)))

# ── 1. Bus voltage ──────────────────────────────────────────────────────────
def bus_voltage(t, H, t_on=t_fault_on, t_off=t_fault_off):
    v = np.ones_like(t)
    # sag during fault
    sag = 0.15
    v -= sag * (sigmoid(t, t_on) - sigmoid(t, t_off))
    # oscillation after clearance; amplitude ∝ 1/H
    amp = 0.18 / H
    decay = np.exp(-2.0 * (t - t_off))
    decay = np.where(t < t_off, 0.0, decay)
    osc_freq = 8.0  # Hz
    v += amp * decay * np.cos(2 * np.pi * osc_freq * (t - t_off)) * (t > t_off)
    return np.clip(v, 0, 1.15)

# ── 2. Grid frequency ────────────────────────────────────────────────────────
def grid_freq(t, H, t_on=t_fault_on, t_off=t_fault_off):
    f = np.zeros_like(t)
    # During fault: freq drops (Pe < Pm → generators accelerate → freq rises,
    # but for a 3-phase bolted fault close to load: freq initially drops)
    # simplified: freq dips then swings after clearance
    for i, ti in enumerate(t):
        if ti < t_on:
            f[i] = 60.0
        elif ti < t_off:
            # rapid drop, steeper for lower H
            dt = ti - t_on
            f[i] = 60.0 - (2.5 / H) * (1 - np.exp(-dt * 8))
        else:
            dt = ti - t_off
            df_min = -(2.5 / H) * (1 - np.exp(-(t_off - t_on) * 8))
            # recovery with oscillation
            f[i] = 60.0 + df_min * np.exp(-1.8 * dt) * np.cos(2 * np.pi * 6 * dt)
    return f

# ── 3. PLL angle error ───────────────────────────────────────────────────────
def pll_angle_error(t, H, t_on=t_fault_on, t_off=t_fault_off):
    """Phase error between PLL estimate and actual grid angle."""
    f = grid_freq(t, H)
    # PLL bandwidth: ~200 rad/s → natural freq ~32 Hz
    omega_n = 2 * np.pi * 25  # PLL natural freq
    xi = 0.707
    err = np.zeros_like(t)
    dt = t[1] - t[0]
    # simple 2nd order PLL simulation
    theta_err = 0.0
    dtheta_err = 0.0
    for i in range(1, len(t)):
        dfreq = 2 * np.pi * (f[i] - 60.0)
        ddtheta = -2 * xi * omega_n * dtheta_err - omega_n**2 * theta_err + omega_n**2 * dfreq
        dtheta_err += ddtheta * dt
        theta_err  += dtheta_err * dt
        err[i] = theta_err
    return err

# ── 4. Active power ──────────────────────────────────────────────────────────
def active_power(t, pll_err, H, t_on=t_fault_on, t_off=t_fault_off):
    P = np.ones_like(t)
    # drop during fault
    P -= 0.85 * (sigmoid(t, t_on) - sigmoid(t, t_off))
    # after clearance: if PLL loses lock (large angle error), power goes to zero
    threshold = np.pi / 3  # 60° error → control diverges
    for i in range(len(t)):
        if t[i] > t_off:
            if abs(pll_err[i]) > threshold:
                # progressive collapse
                decay_i = np.exp(-5 * (t[i] - (t_off + 0.05)))
                P[i] = max(0.0, P[i] * decay_i)
    return np.clip(P, 0, 1.05)

# ── Compute for two H values ─────────────────────────────────────────────────
H_high = 6.0   # normal inertia
H_low  = 1.0   # reduced inertia

V_high = bus_voltage(t, H_high)
V_low  = bus_voltage(t, H_low)

F_high = grid_freq(t, H_high)
F_low  = grid_freq(t, H_low)

RoCoF_high = np.gradient(F_high, t)
RoCoF_low  = np.gradient(F_low,  t)

PLL_high = pll_angle_error(t, H_high)
PLL_low  = pll_angle_error(t, H_low)

P_high = active_power(t, PLL_high, H_high)
P_low  = active_power(t, PLL_low,  H_low)

# ── Figure ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 12))
fig.suptitle(
    'Curto-Circuito com Baixa Inércia: Por que a Potência Vai a Zero?',
    fontsize=13, fontweight='bold', y=0.98
)
gs = GridSpec(4, 2, figure=fig, hspace=0.55, wspace=0.35)

colors = {'high': '#2196F3', 'low': '#F44336'}
fault_color = '#FF9800'

def add_fault_band(ax):
    ax.axvspan(t_fault_on, t_fault_off, alpha=0.12, color=fault_color, zorder=0)
    ax.axvline(t_fault_on,  color=fault_color, lw=1.2, ls='--', alpha=0.7)
    ax.axvline(t_fault_off, color=fault_color, lw=1.2, ls='--', alpha=0.7)

# ── Plot 1: Bus Voltage ───────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t, V_high, color=colors['high'], label=f'H = {H_high} s (normal)')
ax1.plot(t, V_low,  color=colors['low'],  label=f'H = {H_low} s (reduzida)', ls='--')
add_fault_band(ax1)
ax1.set_ylabel('Tensão (pu)')
ax1.set_title('① Tensão na Barra do Inversor')
ax1.legend(fontsize=8)
ax1.set_ylim(0, 1.25)
ax1.text(0.4, 0.08, 'CURTO', fontsize=8, color=fault_color, ha='center',
         transform=ax1.get_xaxis_transform())

# ── Plot 2: Frequency ─────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(t, F_high, color=colors['high'], label=f'H = {H_high} s')
ax2.plot(t, F_low,  color=colors['low'],  label=f'H = {H_low} s', ls='--')
add_fault_band(ax2)
ax2.set_ylabel('Frequência (Hz)')
ax2.set_title('② Frequência da Rede')
ax2.legend(fontsize=8)
ax2.set_ylim(56, 63)
ax2.axhline(60, color='gray', lw=0.8, ls=':')

# ── Plot 3: RoCoF ─────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
ax3.plot(t, RoCoF_high, color=colors['high'], label=f'H = {H_high} s')
ax3.plot(t, RoCoF_low,  color=colors['low'],  label=f'H = {H_low} s', ls='--')
add_fault_band(ax3)
ax3.set_ylabel('RoCoF (Hz/s)')
ax3.set_title('③ Taxa de Variação de Frequência (RoCoF)')
ax3.legend(fontsize=8)
ax3.axhline(0, color='gray', lw=0.8, ls=':')
# IEEE 1547 limit
ax3.axhline(2.0,  color='purple', lw=1, ls=':', alpha=0.7)
ax3.axhline(-2.0, color='purple', lw=1, ls=':', alpha=0.7)
ax3.text(1.35, 2.2, 'Limite IEEE 1547', fontsize=7, color='purple')

# ── Plot 4: PLL phase error ────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
pll_deg_high = np.degrees(PLL_high)
pll_deg_low  = np.degrees(PLL_low)
ax4.plot(t, pll_deg_high, color=colors['high'], label=f'H = {H_high} s')
ax4.plot(t, pll_deg_low,  color=colors['low'],  label=f'H = {H_low} s', ls='--')
add_fault_band(ax4)
ax4.axhline( 60, color='red', lw=1, ls=':', alpha=0.8)
ax4.axhline(-60, color='red', lw=1, ls=':', alpha=0.8)
ax4.text(1.35,  65, 'Perda de lock', fontsize=7, color='red')
ax4.set_ylabel('Erro de Fase PLL (°)')
ax4.set_title('④ Erro de Fase da SRF-PLL')
ax4.legend(fontsize=8)

# ── Plot 5: Active power ───────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[2, :])
ax5.plot(t, P_high, color=colors['high'], lw=2.5, label=f'H = {H_high} s — PLL mantém lock → potência recupera')
ax5.plot(t, P_low,  color=colors['low'],  lw=2.5, ls='--', label=f'H = {H_low} s — PLL perde lock → potência vai a ZERO')
add_fault_band(ax5)
ax5.set_ylabel('Potência Ativa (pu)')
ax5.set_xlabel('Tempo (s)')
ax5.set_title('⑤ Potência Ativa Injetada pelo Inversor', fontweight='bold')
ax5.legend(fontsize=9, loc='upper right')
ax5.set_ylim(-0.05, 1.15)
ax5.fill_between(t, 0, P_low, where=(P_low < 0.05) & (t > t_fault_off),
                 alpha=0.15, color='red', label='_')
ax5.annotate('Potência vai a zero:\nPLL perdeu sincronismo',
             xy=(0.75, 0.03), xytext=(0.9, 0.25),
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
             color='red', fontsize=9, fontweight='bold')

# ── Plot 6: Equal-area criterion (conceptual) ──────────────────────────────────
ax6 = fig.add_subplot(gs[3, :])
delta = np.linspace(0, np.pi, 500)
Pm = 0.7
Pmax_pre  = 1.0
Pmax_fault= 0.2  # fault reduces transfer capacity
Pmax_post = 0.9  # post-fault (slightly reduced)

Pe_pre  = Pmax_pre  * np.sin(delta)
Pe_fault= Pmax_fault* np.sin(delta)
Pe_post = Pmax_post * np.sin(delta)

delta_0  = np.arcsin(Pm / Pmax_pre)
delta_cl_high = delta_0 + 0.45  # small swing for high H
delta_cl_low  = delta_0 + 1.1   # large swing for low H (may exceed critical angle)
delta_cr = np.pi - np.arcsin(Pm / Pmax_post)  # critical clearing angle

ax6.plot(np.degrees(delta), Pe_pre,   'b-',  lw=1.5, label='$P_e$ pré-falta')
ax6.plot(np.degrees(delta), Pe_fault, 'r--', lw=1.5, label='$P_e$ durante curto')
ax6.plot(np.degrees(delta), Pe_post,  'g-',  lw=1.5, label='$P_e$ pós-falta')
ax6.axhline(Pm, color='gray', lw=1.2, ls=':', label=f'$P_m$ = {Pm} pu')

# Mark angles
ax6.axvline(np.degrees(delta_0),  color='blue',  lw=1, ls=':')
ax6.axvline(np.degrees(delta_cr), color='orange', lw=1.5, ls='--', alpha=0.8)
ax6.axvline(np.degrees(delta_cl_high), color=colors['high'], lw=1.5, ls='-.')
ax6.axvline(np.degrees(delta_cl_low),  color=colors['low'],  lw=1.5, ls='-.')

ax6.fill_between(np.degrees(delta),
                 Pm, Pe_fault,
                 where=(delta >= delta_0) & (delta <= delta_cl_low),
                 alpha=0.15, color='red', label='Área acelerante (H baixo)')
ax6.fill_between(np.degrees(delta),
                 Pe_post, Pm,
                 where=(delta >= delta_cl_low) & (delta <= delta_cr),
                 alpha=0.15, color='green', label='Área desacelerante')

ax6.text(np.degrees(delta_0) + 1, 0.03, '$\\delta_0$', color='blue', fontsize=9)
ax6.text(np.degrees(delta_cr) + 1, 0.03, '$\\delta_{cr}$', color='orange', fontsize=9)
ax6.text(np.degrees(delta_cl_high) + 1, 1.05, 'H alto', color=colors['high'], fontsize=8)
ax6.text(np.degrees(delta_cl_low)  + 1, 1.05, 'H baixo\n(instável!)', color=colors['low'], fontsize=8)

ax6.set_xlabel('Ângulo do Rotor δ (°)')
ax6.set_ylabel('Potência (pu)')
ax6.set_title('⑥ Critério das Áreas Iguais — Por que Baixa Inércia Causa Instabilidade')
ax6.legend(fontsize=8, ncol=3, loc='upper right')
ax6.set_xlim(0, 180)
ax6.set_ylim(0, 1.15)

plt.savefig('../assets/inertia_fault_analysis.png', dpi=150, bbox_inches='tight')
print("Saved: assets/inertia_fault_analysis.png")
plt.close()

# ── Second figure: mechanism chain ──────────────────────────────────────────
fig2, ax = plt.subplots(figsize=(12, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis('off')
ax.set_facecolor('white')
fig2.patch.set_facecolor('white')

boxes = [
    (0.2, "H ↓\n(baixa\ninércia)", '#E53935'),
    (2.0, "Oscilação\nde ângulo\nampliada", '#E91E63'),
    (3.8, "RoCoF alto\napós\nclearance", '#9C27B0'),
    (5.6, "SRF-PLL perde\nsincronismo\n(erro > 60°)", '#3F51B5'),
    (7.4, "Controle dq\ncorrompido →\nId, Iq errados", '#2196F3'),
    (9.0, "Pinv → 0\n(colapso)", '#F44336'),
]

for i, (x, label, color) in enumerate(boxes):
    rect = mpatches.FancyBboxPatch((x, 0.8), 1.5, 1.4,
                                    boxstyle="round,pad=0.05",
                                    facecolor=color, edgecolor='white',
                                    alpha=0.85, linewidth=2)
    ax.add_patch(rect)
    ax.text(x + 0.75, 1.5, label, ha='center', va='center',
            color='white', fontsize=9, fontweight='bold')
    if i < len(boxes) - 1:
        ax.annotate('', xy=(x + 1.6, 1.5), xytext=(x + 1.5, 1.5),
                    arrowprops=dict(arrowstyle='->', color='#333', lw=2))

ax.set_title('Cadeia de Causa e Efeito: Baixa Inércia → Potência Zero',
             fontsize=12, fontweight='bold', pad=10)
plt.savefig('../assets/inertia_chain.png', dpi=150, bbox_inches='tight')
print("Saved: assets/inertia_chain.png")
plt.close()
