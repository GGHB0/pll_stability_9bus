"""
indicadores.py — Indicadores do Cap. 5 do TCC, com as receitas fechadas.

Fonte única das definições usadas no texto e nas Tabelas 5.1-5.3: o dashboard
(loader.SimData) e o script das tabelas (scripts/medir_tabelas_cap5.py) chamam
estas funções, para que o número mostrado ao vivo seja o mesmo do TCC.
Receitas e valores conferidos em
.claude/kb/tcc-word/revisao-fragmento/revisao_fragmento_cap5_metricas.md.

    erro_fase_deg   → atan2(v_q, v_d) da tensão da rede no PCC, em graus
    pico_e_retorno  → pico após o 1º ciclo de falta e retorno à faixa de 2°
    indicadores_falta → retenção de v_d, 120 Hz, rampa ONS × i_q,ref, P média,
                        % do tempo com erro > 90°, sentido do fluxo pós-falta
    indicadores_partida → acomodação de v_d (5%) e do erro (2°) na energização
"""
from __future__ import annotations

import numpy as np

from .spectrum import _amplitude_spectrum

CICLO_S = 1 / 60      # 1 ciclo da fundamental
TOL_DEG = 2.0         # faixa de retorno do erro de fase (§5.1-5.4)
JANELA_PRE_S = 0.05   # média pré-falta da retenção de v_d
TAU_V = 0.005         # filtro de |V| na entrada do bloco ONS_2_11
FAIXA_VD = 0.05       # acomodação de v_d na partida: ±5% do valor final
JANELA_FINAL_S = 0.05  # valor final de v_d = média dos últimos 50 ms


def erro_fase_deg(vd_rede: np.ndarray, vq_rede: np.ndarray) -> np.ndarray:
    """Erro de fase do SRF-PLL: ângulo do vetor de tensão da rede no
    referencial estimado (zero quando o PLL está travado)."""
    return np.degrees(np.arctan2(vq_rede, vd_rede))


def pico_e_retorno(t: np.ndarray, e_deg: np.ndarray,
                   t_fault: float, t_clear: float) -> tuple[float, float | None]:
    """(pico em °, retorno em ms). O pico descarta o 1º ciclo (salto de fase
    da aplicação da falta). O retorno é o último instante com |e| > 2°,
    contado de t_clear; None se o erro não volta à faixa na janela simulada
    (margem de 2 ms no fim), 0 se nunca sai dela."""
    pico = float(np.abs(e_deg[(t >= t_fault + CICLO_S) & (t <= t_clear)]).max())
    pos = t >= t_clear
    fora = t[pos][np.abs(e_deg[pos]) > TOL_DEG]
    if len(fora) == 0:
        return pico, 0.0
    if fora[-1] >= t[-1] - 2e-3:
        return pico, None
    return pico, float((fora[-1] - t_clear) * 1000)


def rampa_ons(v):
    """Corrente reativa adicional da rampa ONS (pu): nula em 0,85 pu, 1 pu em 0,5 pu."""
    return np.clip((0.85 - v) / 0.35, 0, 1) * (v < 0.85)


def _filtra(t: np.ndarray, x: np.ndarray, tau: float) -> np.ndarray:
    dt = np.diff(t, prepend=t[0])
    y = np.empty_like(x)
    y[0] = x[0]
    for k in range(1, len(x)):
        al = dt[k] / (tau + dt[k])
        y[k] = y[k - 1] + al * (x[k] - y[k - 1])
    return y


def indicadores_falta(t: np.ndarray, s: dict, t_fault: float, t_clear: float) -> dict:
    """Indicadores de uma falta eliminada. `s` mapeia as colunas do sim_data.csv
    (já com P/Q corrigidos por pq.corrige_pq) para arrays: vd_rede_pu,
    vq_rede_pu, vd_ufv_pu, vq_ufv_pu, iq_ufv_ref_pu, iq_ufv_pu, P_ufv_pu, Q_ufv_pu."""
    vd = s["vd_rede_pu"]
    e = erro_fase_deg(vd, s["vq_rede_pu"])
    pico, ts = pico_e_retorno(t, e, t_fault, t_clear)
    pre = (t >= t_fault - JANELA_PRE_S) & (t < t_fault)
    w2 = (t >= t_fault + 2 * CICLO_S) & (t <= t_clear)
    w1 = (t >= t_fault + CICLO_S) & (t <= t_clear)
    wf = (t >= t_fault) & (t <= t_clear)
    pos = t >= t_clear
    f, a, _ = _amplitude_spectrum(t[w2], vd[w2], window="hann")
    V = np.hypot(s["vd_ufv_pu"], s["vq_ufv_pu"])
    Vf = _filtra(t, V, TAU_V)
    iq_ref = s["iq_ufv_ref_pu"]
    P, Q = s["P_ufv_pu"], s["Q_ufv_pu"]
    return dict(
        ret=float(vd[w2].mean() / vd[pre].mean() * 100),
        vdmed=float(vd[w1].mean()), vdmin=float(vd[w1].min()), vdmax=float(vd[w1].max()),
        a120=float(a[np.argmin(np.abs(f - 120))]),
        pico=pico, ts=ts,
        frac90=float((np.abs(e[wf]) > 90).mean() * 100),
        Vmed=float(V[w1].mean()),
        iq_rampa_Vmed=float(rampa_ons(V[w1].mean())),
        iq_rampa_inst=float(rampa_ons(Vf[w1]).mean()),
        iqref=float(-iq_ref[w1].mean()), iqref_pico=float(np.abs(iq_ref[w1]).max()),
        iq=float(-s["iq_ufv_pu"][w1].mean()),
        P=float(P[w1].mean()), Q=float(Q[w1].mean()),
        frac_P_absorve=float((P[pos] < 0).mean() * 100),
        frac_Q_injeta=float((Q[pos] >= 0).mean() * 100),
    )


def indicadores_partida(t: np.ndarray, vd_rede: np.ndarray, vq_rede: np.ndarray) -> dict:
    """Acomodação na energização (§5.1), em ms desde t = 0: v_d na faixa de
    ±5% do valor final e erro de fase na faixa de 2°."""
    e = erro_fase_deg(vd_rede, vq_rede)
    fin = vd_rede[t >= t[-1] - JANELA_FINAL_S].mean()
    fora_vd = t[np.abs(vd_rede - fin) > FAIXA_VD * abs(fin)]
    fora_e = t[np.abs(e) > TOL_DEG]
    return dict(
        t_vd5=float(fora_vd[-1] * 1000) if len(fora_vd) else 0.0,
        t_err2=float(fora_e[-1] * 1000) if len(fora_e) else 0.0,
    )
