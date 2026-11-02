"""Figuras do Sec. 1.1 do TCC (R6a, Prof. Rafael): participacao das renovaveis na
geracao mundial (IEA, 2026) e capacidade eolica + solar + MMGD no SIN (ONS, 2025).

Mesmos dados dos graficos do slide 2 do deck da defesa
(assets/charts/defesa/participacao_renovaveis_iea.png e crescimento_renovaveis_sin.png),
redesenhados para a pagina do TCC: fundo branco, sem titulo dentro da imagem
(a legenda do Word faz esse papel), virgula decimal.

    .venv\\Scripts\\python.exe scripts\\gen_matriz_renovaveis.py
"""
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# paleta do projeto (src/config/settings.py, LIGHT_COLORS)
AZUL = "#2563eb"
CINZA = "#94a3b8"
NAVY = "#0B132B"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Segoe UI", "Arial"],
    "font.size": 10,
    "axes.edgecolor": "#94a3b8",
    "axes.labelcolor": NAVY,
    "text.color": NAVY,
    "xtick.color": "#334155",
    "ytick.color": "#334155",
    "svg.fonttype": "path",  # ver gen_fault_waveforms.py -- evita glifo esticado
})

# Sec. 1.1 do TCC (IEA, 2026)
PARTICIPACAO = [
    ("Solar + eólica no mundo,\nhá uma década", 5, "~5%"),
    ("Solar + eólica no mundo,\n2025", 17, "17%"),
    ("Solar + eólica na\nUnião Europeia, 2025", 30, "30%"),
    ("Renováveis no mundo,\n2025", 34, "34%"),
]

# Apresentacao do ONS ao Senado Federal, 15/10/2025 (slide 2 do deck)
CAPACIDADE_SIN = [("2020", 25.5), ("2021", 35.3), ("2022", 48.5),
                  ("2023", 66.6), ("2024", 84.7), ("2025", 96.8)]


def virgula(x):
    return f"{x:.1f}".replace(".", ",")


def salva(fig, nome):
    for ext, kw in (("svg", {}), ("png", {"dpi": 220})):
        fig.savefig(OUT_DIR / f"{nome}.{ext}", format=ext, facecolor="white",
                    bbox_inches="tight", **kw)
    plt.close(fig)
    print("ok", OUT_DIR / f"{nome}.png")


def participacao():
    fig, ax = plt.subplots(figsize=(6.3, 2.9))
    rot = [r for r, _, _ in PARTICIPACAO][::-1]
    val = [v for _, v, _ in PARTICIPACAO][::-1]
    txt = [t for _, _, t in PARTICIPACAO][::-1]
    cores = [CINZA, AZUL, CINZA, CINZA][::-1]
    ax.barh(rot, val, color=cores, height=0.62, zorder=3)
    for y, (v, t) in enumerate(zip(val, txt)):
        ax.text(v + 0.8, y, t, va="center", fontweight="bold", fontsize=10)
    ax.set_xlim(0, 40)
    ax.set_xlabel("Participação na geração elétrica (%)")
    ax.xaxis.grid(True, color="#e2e8f0", linewidth=0.8, zorder=0)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    salva(fig, "matriz_participacao_renovaveis")


def capacidade_sin():
    fig, ax = plt.subplots(figsize=(6.3, 3.0))
    anos = [a for a, _ in CAPACIDADE_SIN]
    gw = [g for _, g in CAPACIDADE_SIN]
    cores = [CINZA] * (len(gw) - 1) + [AZUL]
    ax.bar(anos, gw, color=cores, width=0.6, zorder=3)
    for x, g in enumerate(gw):
        ax.text(x, g + 1.5, f"{virgula(g)} GW", ha="center", fontweight="bold", fontsize=9.5)
    ax.annotate("", xy=(5, 108), xytext=(0, 108),
                arrowprops=dict(arrowstyle="->", color="#475569", lw=1.1))
    ax.text(2.5, 111, "+279%", ha="center", color=AZUL, fontweight="bold", fontsize=10.5)
    ax.set_ylim(0, 122)
    ax.set_ylabel("Capacidade instalada (GW)")
    ax.yaxis.grid(True, color="#e2e8f0", linewidth=0.8, zorder=0)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    salva(fig, "matriz_capacidade_sin")


if __name__ == "__main__":
    participacao()
    capacidade_sin()
