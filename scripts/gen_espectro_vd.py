"""
Gera o grafico do espectro de frequencias da componente de eixo direto da
tensao durante a falta (Cap. 5 do TCC, Secao 5.3) em assets/charts/ -- pedido
do Oscar no comentario 275 do V10 ("acredito que aqui podem colocar a grafica
do espectro de frequencia").

Mesma receita da coluna "Componente de 120 Hz" das Tabelas 5.1 e 5.3 (ver
.claude/kb/tcc-word/revisao-fragmento/revisao_fragmento_cap5_metricas.md):
FFT com janela de Hann de vd_rede_pu em [t_fault + 2 ciclos, t_clear], por
src.pipeline.spectrum._amplitude_spectrum (janela truncada a numero inteiro
de ciclos, media removida). A janela de ~67 ms nao fecha 4 ciclos inteiros
(o 1o instante cai uma amostra depois de t_fault + 2 ciclos), entao a FFT
usa 3: df = 20 Hz, 120 Hz cai exatamente num bin, e os bins abaixo de 60 Hz
carregam a variacao lenta de v_d ao longo da falta, nao harmonica.

Figura (SVG + PNG): espectro_vd_falta -- trifasicas x assimetricas, sintonia nominal.
"""
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from gen_fault_waveforms import (  # noqa: E402  (estilo e paleta comuns ao Cap. 5)
    AZUL, LARANJA, NAVY, VERDE, VERMELHO, LEGEND_KW, ROOT, save, style_axes,
)
from src.pipeline.spectrum import _amplitude_spectrum  # noqa: E402

CICLO_S = 1 / 60
F_MAX = 480
ROXO, CINZA = "#7c3aed", "#64748b"

# (pasta, rotulo, cor, estilo)
CASOS = [
    ("bus7/2phase", "Bifásica na Barra 7", VERMELHO, "-"),
    ("bus7/1phase", "Monofásica na Barra 7", LARANJA, "-"),
    ("bus6/2phase", "Bifásica na Barra 6", AZUL, "-"),
    ("bus6/1phase", "Monofásica na Barra 6", ROXO, "-"),
    ("bus7/3phase", "Trifásica na Barra 7", NAVY, "--"),
    ("bus6/3phase", "Trifásica na Barra 6", CINZA, "--"),
]


def espectro(folder):
    base = ROOT / "output" / "results" / folder
    fi = json.loads((base / "fault_info.json").read_text())
    d = pd.read_csv(base / "sim_data.csv", usecols=["t_s", "vd_rede_pu"])
    t, vd = d.t_s.to_numpy(), d.vd_rede_pu.to_numpy()
    m = (t >= fi["t_fault"] + 2 * CICLO_S) & (t <= fi["t_clear"])
    f, a, _ = _amplitude_spectrum(t[m], vd[m], fmax=F_MAX, window="hann")
    return f, a


def num(x, casas):
    return f"{x:.{casas}f}".replace(".", ",")


def fig_espectro():
    fig, ax = plt.subplots(figsize=(7.0, 3.8), dpi=150)
    fig.subplots_adjust(top=0.80, bottom=0.14, left=0.11, right=0.97)
    ax.axvspan(112.5, 127.5, color=VERMELHO, alpha=0.07, zorder=0, lw=0)
    sim_max = 0.0
    for folder, rot, cor, ls in CASOS:
        f, a = espectro(folder)
        ax.plot(f, a, color=cor, ls=ls, lw=1.2, marker="o", ms=2.5, label=rot)
        if ls == "--":
            sim_max = max(sim_max, float(a[np.argmin(np.abs(f - 120))]))
    style_axes(ax)
    ax.set_xlim(0, F_MAX)
    ax.set_ylim(0, None)
    ax.set_xticks(np.arange(0, F_MAX + 1, 60))
    ax.set_xlabel("Frequência (Hz)")
    ax.set_ylabel(r"Amplitude em $v_d$ (pu)")
    ax.text(124, ax.get_ylim()[1] * 0.97, "120 Hz", fontsize=9, color=VERMELHO, va="top", ha="left")
    ax.text(F_MAX - 5, ax.get_ylim()[1] * 0.10,
            f"trifásicas em 120 Hz: no máximo {num(sim_max, 4)} pu",
            fontsize=8.5, color=CINZA, ha="right", va="bottom")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=3, fontsize=8.5, **LEGEND_KW)
    save(fig, "espectro_vd_falta")


if __name__ == "__main__":
    fig_espectro()
