"""
Gera a figura do PLANO P-Q pos-falta em assets/charts/.

Motivacao (2026-09-01): o paragrafo do Cap. 5 que comenta as potencias da falta
trifasica na Barra 7 com sintonia inadequada era uma enumeracao de valores todos
legiveis no proprio oscilograma (ver .claude/kb/tcc-word/
revisao_fragmento_cap5_analise.md). Esta figura mostra no plano P-Q o que a serie
temporal nao mostra: o ponto de operacao deixa de ser um ponto e vira uma orbita
que cruza para o semiplano de potencia ativa negativa, ou seja, o inversor passa
a absorver energia do sistema.

Mesma logica didatica de gen_retencao_didatica.py (Figura 5.11): construir o
conceito sobre o dado real em vez de defini-lo so em prosa.

Metrica destacada: FRACAO DO TEMPO COM P < 0 na janela pos-falta assentada.
E adimensional, nao depende do comprimento da janela (e uma razao) e separa os
dois cenarios por quase duas ordens de grandeza (1,1% x 64,6%), ao contrario dos
valores de pico, que dependem do recorte.

Janela: [t_clear + 50 ms, fim da simulacao]. Os 50 ms descartados removem o
transitorio de comutacao da ELIMINACAO da falta, que no caso nominal leva P a
-3,4 pu por alguns milissegundos e falsearia a comparacao. Mesmo racional do
descarte de 2 ciclos na figura da retencao.

Saidas (SVG + PNG, mesma convencao de gen_fault_waveforms.py):
  plano_pq_comparacao.svg -- painel duplo nominal x sintonia inadequada

Eixos COMPARTILHADOS entre os paineis (uniao dos extremos): a diferenca de
extensao da orbita e justamente o que a figura precisa deixar visivel.

Requer matplotlib (nao listado em requirements.txt, ver gen_fault_waveforms.py).
"""
import io
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "output" / "results"
OUT_DIR = ROOT / "assets" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# paleta do projeto (src/config/settings.py, LIGHT_COLORS)
AZUL, VERMELHO, VERDE = "#2563eb", "#dc2626", "#16a34a"
NAVY = "#0B132B"
GRID_COLOR = "#e2e8f0"

LAG_POS_S = 0.050          # descarte apos t_clear (transitorio de eliminacao)
JANELA_PRE_S = 0.05        # media pre-falta, mesma da figura da retencao
ALVO_PONTOS = 5000         # decimacao da trajetoria

CENARIOS = [
    ("bus7/3phase", "Sintonia nominal"),
    ("bus7/3phase_bad_pll", "Sintonia inadequada"),
]

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Segoe UI", "Arial"],
    "font.size": 10,
    "axes.edgecolor": "#94a3b8",
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": "#334155",
    "ytick.color": "#334155",
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "svg.fonttype": "path",  # ver gen_fault_waveforms.py -- evita glifo esticado
})

virg1 = FuncFormatter(lambda v, _p: f"{v:.1f}".replace(".", ","))


def br(x, casas=1):
    return f"{x:.{casas}f}".replace(".", ",")


def carregar(folder):
    """Le o cenario e devolve a trajetoria P-Q pos-falta e o ponto pre-falta."""
    base = RESULTS_DIR / folder
    fi = json.loads((base / "fault_info.json").read_text())
    df = pd.read_csv(base / "sim_data.csv")
    t_clear, t_fault = fi["t_clear"], fi["t_fault"]
    t = df.t_s

    pre = (t >= t_fault - JANELA_PRE_S) & (t < t_fault)
    pos = t >= t_clear + LAG_POS_S

    P, Q = df.P_ufv_pu[pos], df.Q_ufv_pu[pos]
    passo = max(1, len(P) // ALVO_PONTOS)
    return dict(
        P=P.iloc[::passo].to_numpy(), Q=Q.iloc[::passo].to_numpy(),
        P_pre=float(df.P_ufv_pu[pre].mean()), Q_pre=float(df.Q_ufv_pu[pre].mean()),
        P_med=float(P.mean()), Q_med=float(Q.mean()),
        frac_absorve=float((P < 0).mean()) * 100.0,
        t_ini=t_clear + LAG_POS_S, t_fim=float(t.max()),
    )


def desenhar(ax, d, titulo, xlim, ylim):
    # semiplano de potencia ativa negativa -- o inversor absorve da rede
    ax.axvspan(xlim[0], 0.0, color=VERMELHO, alpha=0.07, zorder=0)
    ax.axvline(0.0, color=VERMELHO, lw=1.2, zorder=2)
    ax.axhline(0.0, color="#94a3b8", lw=0.9, zorder=2)

    ax.plot(d["P"], d["Q"], color=AZUL, lw=0.7, alpha=0.7, zorder=4)

    # onde operava antes x onde passou a operar (media da janela pos-falta)
    ax.plot(d["P_pre"], d["Q_pre"], "o", ms=9, color=VERDE,
            markeredgecolor="white", markeredgewidth=1.4, zorder=7)
    ax.plot(d["P_med"], d["Q_med"], "X", ms=12, color=VERMELHO,
            markeredgecolor="white", markeredgewidth=1.4, zorder=7)
    ax.annotate("antes", xy=(d["P_pre"], d["Q_pre"]),
                xytext=(0, 22), textcoords="offset points",
                ha="center", fontsize=9, color=VERDE, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=VERDE, lw=1.0))
    ax.annotate("depois", xy=(d["P_med"], d["Q_med"]),
                xytext=(0, -26), textcoords="offset points",
                ha="center", fontsize=9, color=VERMELHO, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color=VERMELHO, lw=1.0))

    ax.text(0.035, 0.965,
            f"absorve ativa em\n{br(d['frac_absorve'])}% do tempo",
            transform=ax.transAxes, va="top", ha="left", fontsize=10,
            fontweight="bold", color=NAVY,
            bbox=dict(boxstyle="round,pad=0.42", facecolor="white",
                      edgecolor="#cbd5e1", alpha=0.94))

    ax.set_title(titulo)
    ax.set_xlabel("Potência ativa P (pu)")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.xaxis.set_major_formatter(virg1)
    ax.yaxis.set_major_formatter(virg1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=1)
    ax.set_axisbelow(True)


def main():
    dados = [(carregar(f), lbl) for f, lbl in CENARIOS]

    # eixos compartilhados: uniao dos extremos dos dois cenarios
    todos_P = [v for d, _ in dados for v in (d["P"].min(), d["P"].max(), d["P_pre"])]
    todos_Q = [v for d, _ in dados for v in (d["Q"].min(), d["Q"].max(), d["Q_pre"])]
    mx, my = 0.22, 0.30
    xlim = (min(todos_P) - mx, max(todos_P) + mx)
    ylim = (min(todos_Q) - my, max(todos_Q) + my)

    # figsize pela LEGIBILIDADE NO DOCX: fonte efetiva = font_pt * 6,5/largura.
    # 8,3 in inserido a 6,5 in da a escala ~0,79 padrao do Cap. 5 (ver o mesmo
    # comentario em gen_retencao_didatica.py). Encolher o figsize, nunca subir a fonte.
    fig, axes = plt.subplots(1, 2, figsize=(8.3, 3.9), sharey=True)
    for ax, (d, lbl) in zip(axes, dados):
        desenhar(ax, d, lbl, xlim, ylim)
    axes[0].set_ylabel("Potência reativa Q (pu)")

    handles = [
        Line2D([], [], color=AZUL, lw=1.4, label="Trajetória P-Q após a eliminação da falta"),
        Line2D([], [], marker="o", ls="", ms=8, color=VERDE,
               markeredgecolor="white", label="Ponto de operação pré-falta"),
        Line2D([], [], marker="X", ls="", ms=10, color=VERMELHO,
               markeredgecolor="white", label="Ponto de operação médio pós-falta"),
        Patch(facecolor=VERMELHO, alpha=0.16, label="P < 0: inversor absorve energia da rede"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, -0.055), fontsize=9)

    d0 = dados[0][0]
    fig.suptitle(
        "Plano P-Q no intervalo pós-falta: falta trifásica na Barra 7\n"
        f"(a partir de {LAG_POS_S*1000:.0f} ms após a eliminação, até o fim da simulação)",
        fontsize=11.5, fontweight="bold", y=1.005)
    fig.tight_layout(rect=(0, 0.10, 1, 0.99))

    for ext in ("svg", "png"):
        p = OUT_DIR / f"plano_pq_comparacao.{ext}"
        fig.savefig(p, format=ext, dpi=200, bbox_inches="tight",
                    facecolor="white")
        print("gerado:", p.relative_to(ROOT))
    plt.close(fig)

    for d, lbl in dados:
        print(f"  {lbl:20s} P medio={br(d['P_med'], 3)} pu   "
              f"P<0 em {br(d['frac_absorve'])}% da janela "
              f"[{br(d['t_ini'], 2)} s, {br(d['t_fim'], 2)} s]")


if __name__ == "__main__":
    main()
