"""
Análise pós-simulação: IAE, ISE, settling time e plots matplotlib.
Importar após run_simulation() retornar os dados.
"""

import numpy as np
import matplotlib.pyplot as plt

W0 = 2 * np.pi * 60  # frequência nominal (rad/s)


# ── métricas de erro ─────────────────────────────────────────────────────────

def freq_from_angle(t, angle_rad):
    """Derivada numérica do ângulo → frequência instantânea (rad/s)."""
    return np.gradient(np.asarray(angle_rad), np.asarray(t))

def _window(t, signal, t_start):
    if t_start is None:
        return np.asarray(t), np.asarray(signal)
    t, signal = np.asarray(t), np.asarray(signal)
    mask = t >= t_start
    return t[mask], signal[mask]

def compute_iae(t, error, t_start=None):
    t, e = _window(t, error, t_start)
    return float(np.trapz(np.abs(e), t))

def compute_ise(t, error, t_start=None):
    t, e = _window(t, error, t_start)
    return float(np.trapz(e ** 2, t))

def compute_settling_time(t, signal, nominal, threshold=0.02, t_start=None):
    """
    Menor t após t_start em que o sinal permanece dentro de ±threshold*|nominal|.
    Retorna None se nunca acomodar dentro da janela.
    """
    t, sig = _window(t, signal, t_start)
    band = abs(nominal) * threshold if nominal != 0 else threshold
    outside = np.abs(sig - nominal) > band
    idx = np.where(outside)[0]
    if len(idx) == 0:
        return 0.0
    if idx[-1] == len(t) - 1:
        return None
    return float(t[idx[-1]] - t[0])


# ── métricas PLL ─────────────────────────────────────────────────────────────

def pll_metrics(t, ang_pll, fault_time=None):
    """
    Retorna dict com métricas de desempenho do PLL.

    Parâmetros
    ----------
    t         : array de tempo (s)
    ang_pll   : ângulo estimado pelo PLL (rad)
    fault_time: instante da falta (s); integração começa aqui
    """
    t, ang = np.asarray(t), np.asarray(ang_pll)
    freq     = freq_from_angle(t, ang)
    freq_err = freq - W0

    ts = compute_settling_time(t, freq, W0, threshold=0.02, t_start=fault_time)
    return {
        'max_freq_deviation_hz': float(np.max(np.abs(freq_err)) / (2 * np.pi)),
        'iae_freq_rad':          compute_iae(t, freq_err, t_start=fault_time),
        'ise_freq_rad2s':        compute_ise(t, freq_err, t_start=fault_time),
        'settling_time_s':       ts,
    }


# ── plots ─────────────────────────────────────────────────────────────────────

def _vline(axes, t_fault):
    if t_fault is not None:
        for ax in axes:
            ax.axvline(t_fault, color='orange', ls='--', lw=1, alpha=0.8,
                       label='Falta')

def plot_pll(t, ang_pll, fault_time=None, save_path=None):
    """Ângulo PLL e frequência estimada em dois painéis."""
    t, ang = np.asarray(t), np.asarray(ang_pll)
    freq_hz = freq_from_angle(t, ang) / (2 * np.pi)

    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    axes[0].plot(t, np.unwrap(ang) * 180 / np.pi, 'b')
    axes[0].set_ylabel('Ângulo PLL (°)')
    axes[0].set_title('Resposta do SRF-PLL')
    axes[0].grid(alpha=0.3)

    axes[1].plot(t, freq_hz, 'r')
    axes[1].axhline(60, color='k', ls='--', lw=0.8, alpha=0.6, label='60 Hz')
    axes[1].set_ylabel('Frequência estimada (Hz)')
    axes[1].set_xlabel('Tempo (s)')
    axes[1].grid(alpha=0.3)
    axes[1].legend(fontsize=8)

    _vline(axes, fault_time)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig

def plot_power(t, p, q, fault_time=None, save_path=None):
    """Potências ativa e reativa."""
    fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
    axes[0].plot(t, p, 'b');  axes[0].set_ylabel('P ativo (pu)');  axes[0].grid(alpha=0.3)
    axes[1].plot(t, q, 'r');  axes[1].set_ylabel('Q reativo (pu)'); axes[1].grid(alpha=0.3)
    axes[1].set_xlabel('Tempo (s)')
    _vline(axes, fault_time)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig

def plot_currents(t, iabc_inv, iabc_grid=None, fault_time=None, save_path=None):
    """Correntes trifásicas do inversor (e da rede, se disponível)."""
    n = 2 if iabc_grid is not None else 1
    fig, axes = plt.subplots(n, 1, figsize=(10, 3 * n), sharex=True)
    if n == 1:
        axes = [axes]
    axes[0].plot(t, iabc_inv);  axes[0].set_ylabel('Iabc Inversor (pu)'); axes[0].grid(alpha=0.3)
    if iabc_grid is not None:
        axes[1].plot(t, iabc_grid); axes[1].set_ylabel('Iabc Rede (pu)'); axes[1].grid(alpha=0.3)
    axes[-1].set_xlabel('Tempo (s)')
    _vline(axes, fault_time)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig

def print_metrics(metrics):
    """Imprime tabela de métricas formatada."""
    print("─" * 45)
    print(f"  Desvio máx. de frequência : {metrics['max_freq_deviation_hz']:.4f} Hz")
    print(f"  IAE (erro de frequência)  : {metrics['iae_freq_rad']:.6f} rad")
    print(f"  ISE (erro de frequência)  : {metrics['ise_freq_rad2s']:.6f} rad²·s")
    ts = metrics['settling_time_s']
    ts_str = f"{ts*1000:.1f} ms" if ts is not None else "não acomodou"
    print(f"  Settling time (2 %%)       : {ts_str}")
    print("─" * 45)
