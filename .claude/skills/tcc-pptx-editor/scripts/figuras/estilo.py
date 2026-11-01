"""Estilo das figuras dedicadas do deck da defesa (ver casos/figura_dedicada.md).

A figura nasce no tamanho da caixa da imagem no slide (polegadas), então o
tamanho de fonte aqui é o tamanho na tela: piso de 12 pt, acima dos 11 pt do
design.md. Cores do design.md (azul = nominal, laranja = inadequada).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[5]
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
OUT = ROOT / "assets" / "charts" / "defesa"

AZUL, LARANJA = "#2563EB", "#EA580C"
MARINHO, TEXTO, CINZA = "#1E3A8A", "#0F172A", "#64748B"
VERMELHO, VERDE, ROXO = "#DC2626", "#16A34A", "#7C3AED"
GRADE = "#E2E8F0"
PT = 12          # ticks, legenda
PT_ROTULO = 13   # rótulo de eixo, título de painel, anotação


def aplica():
    """Chamar depois de importar os geradores do TCC, que mexem no rcParams."""
    plt.rcParams.update({
        "font.family": "Calibri", "font.size": PT,
        "axes.labelsize": PT_ROTULO, "axes.titlesize": PT_ROTULO, "axes.titleweight": "bold",
        "xtick.labelsize": PT, "ytick.labelsize": PT, "legend.fontsize": PT,
        "text.color": TEXTO, "axes.labelcolor": TEXTO, "axes.edgecolor": CINZA,
        "xtick.color": TEXTO, "ytick.color": TEXTO,
        "lines.linewidth": 1.6, "axes.linewidth": 0.8,
        "mathtext.fontset": "custom", "mathtext.rm": "Calibri", "mathtext.it": "Calibri:italic",
        "svg.fonttype": "none", "axes.unicode_minus": True,
    })


def figura(caixa, nrows=1, ncols=1, **kw):
    """Figura do tamanho exato da caixa (largura, altura) em polegadas."""
    return plt.subplots(nrows, ncols, figsize=caixa, layout="constrained", **kw)


def eixos(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=GRADE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


LEGENDA = dict(frameon=False, handlelength=1.6, columnspacing=1.2)


def salva(fig, nome):
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in ("svg", "png"):
        fig.savefig(OUT / f"{nome}.{ext}", dpi=300, facecolor="white")
    plt.close(fig)
    print(f"{nome}: {fig.get_figwidth():.2f} x {fig.get_figheight():.2f} in -> {OUT / nome}.png")
