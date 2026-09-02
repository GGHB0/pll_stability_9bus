"""
Gera a versao DIDATICA do oscilograma de potencia em assets/charts/.

Motivacao (2026-09-01): o grafico de P/Q da falta trifasica na Barra 7 com
sintonia inadequada (bus7_3phase_bad_pll_potencia_pq, Figura 5.13 do fragmento)
mostra o fenomeno mas nao carrega nenhum conceito -- o paragrafo ao lado tinha
que enumerar nove valores em prosa para dizer o que estava acontecendo (ver
.claude/kb/tcc-word/revisao_fragmento_cap5_analise.md).

Em vez de trocar por um plano de estado (gen_plano_pq.py), esta figura ANOTA a
propria serie temporal que ja existe -- pedido do usuario: "vale fazer algo em
cima dos graficos que ja existe em serie temporal". Mesma familia didatica de
gen_retencao_didatica.py (Figura 5.11).

O que a anotacao acrescenta ao tracado bruto:

  1. AREA PREENCHIDA DOS DOIS LADOS do zero: verde onde a potencia e positiva
     (o inversor ENTREGA a rede), vermelho onde e negativa (ABSORVE). Preencher
     so o lado negativo deixava o "entrega" implicito; com os dois lados o
     leitor ve a alternancia de sentido a cada ciclo do escorregamento.
  2. PATAMAR PRE-FALTA em linha tracejada, que e o valor ao qual a potencia
     deveria ter retornado apos a eliminacao.
  3. MEDIA POS-FALTA em linha tracejada, que e o valor que ela de fato assumiu.
     A distancia entre as duas tracejadas E o resultado da secao.
  4. FRACAO DO TEMPO em cada sentido, em caixa (entrega x absorve). Razao
     adimensional, nao depende do comprimento da janela -- ao contrario dos
     valores de pico.

Janela das estatisticas: [t_clear, fim da simulacao], a mesma regiao que aparece
sombreada, para que numero e desenho nao divirjam.

Saidas (SVG + PNG, mesma convencao de gen_fault_waveforms.py):
  potencia_didatica.svg -- dois paineis empilhados (P em cima, Q embaixo)

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
AZUL, VERMELHO, VERDE, LARANJA = "#2563eb", "#dc2626", "#16a34a", "#ea580c"
NAVY = "#0B132B"
GRID_COLOR = "#e2e8f0"

CENARIO = "bus7/3phase_bad_pll"
JANELA_PRE_S = 0.05        # media pre-falta, mesma receita da figura da retencao
T_INI_PLOT = 0.55          # mesmo recorte do oscilograma atual
ALVO_PONTOS = 6000

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

virg1 = FuncFormatter(lambda v, _p: f"{v:.1f}".replace(".", ","))   # eixo Y (pu)
virg2 = FuncFormatter(lambda v, _p: f"{v:.2f}".replace(".", ","))   # eixo X (s)

# O transitorio de comutacao da ELIMINACAO leva P a -2,4 pu por ~1 ms e domina a
# escala vertical, escondendo a oscilacao que a figura precisa mostrar. A escala
# de P e calculada ignorando esses primeiros milissegundos (o traco continua
# desenhado, so sai do recorte). Mesmo racional do descarte de 2 ciclos na
# figura da retencao.
LAG_ESCALA_S = 0.020


def br(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",")


def carregar():
    base = RESULTS_DIR / CENARIO
    fi = json.loads((base / "fault_info.json").read_text())
    df = pd.read_csv(base / "sim_data.csv")
    t_fault, t_clear = fi["t_fault"], fi["t_clear"]
    t = df.t_s

    pre = (t >= t_fault - JANELA_PRE_S) & (t < t_fault)
    pos = t >= t_clear
    janela = t >= T_INI_PLOT
    passo = max(1, int(janela.sum()) // ALVO_PONTOS)

    out = dict(t_fault=t_fault, t_clear=t_clear, t_fim=float(t.max()),
               t=t[janela].iloc[::passo].to_numpy())
    escala = (t >= T_INI_PLOT) & ((t < t_fault) | (t >= t_clear + LAG_ESCALA_S))
    for nome, col, in (("P", "P_ufv_pu"), ("Q", "Q_ufv_pu")):
        s = df[col]
        out[nome] = s[janela].iloc[::passo].to_numpy()
        out[f"{nome}_pre"] = float(s[pre].mean())
        out[f"{nome}_pos"] = float(s[pos].mean())
        out[f"{nome}_frac"] = float((s[pos] < 0).mean()) * 100.0
        out[f"{nome}_frac_pos"] = float((s[pos] >= 0).mean()) * 100.0
        lo, hi = float(s[escala].min()), float(s[escala].max())
        # folga assimetrica: o topo abriga os rotulos de evento ("falta
        # aplicada"/"falta eliminada") e o patamar pre-falta, que em P fica
        # justamente no valor mais alto do tracado.
        out[f"{nome}_ylim"] = (lo - 0.12 * (hi - lo), hi + 0.34 * (hi - lo))
    return out


def painel(ax, d, nome, cor, rotulo, caixa):
    y = d[nome]
    t = d["t"]

    # janela da falta, mesma marcacao do oscilograma original
    ax.axvspan(d["t_fault"], d["t_clear"], color=VERMELHO, alpha=0.06, zorder=0)
    ax.axvline(d["t_fault"], color=VERMELHO, lw=1.2, ls="--", alpha=0.8, zorder=2)
    ax.axvline(d["t_clear"], color=VERDE, lw=1.2, ls="--", alpha=0.8, zorder=2)

    # 1. a area que carrega o conceito: o SINAL da potencia diz o sentido do
    # fluxo. Preencher os dois lados, e nao so o negativo, e o que deixa o
    # leitor ver a alternancia entre entregar e absorver a cada ciclo.
    ax.fill_between(t, y, 0, where=(y >= 0), interpolate=True,
                    color=VERDE, alpha=0.16, zorder=3, linewidth=0)
    ax.fill_between(t, y, 0, where=(y < 0), interpolate=True,
                    color=VERMELHO, alpha=0.30, zorder=3, linewidth=0)
    ax.axhline(0.0, color="#334155", lw=1.3, zorder=4)

    ax.plot(t, y, color=cor, lw=0.9, zorder=5)

    # 2 e 3. patamar pre-falta x media pos-falta
    cx = dict(fontsize=9.5, fontweight="bold", zorder=9,
              bbox=dict(boxstyle="round,pad=0.28", facecolor="white",
                        edgecolor="none", alpha=0.85))
    ax.hlines(d[f"{nome}_pre"], T_INI_PLOT, d["t_fault"], color=VERDE,
              lw=1.8, ls=(0, (5, 2)), zorder=6)
    ax.text(T_INI_PLOT + 0.004, d[f"{nome}_pre"],
            f"antes: {br(d[f'{nome}_pre'])} pu",
            va="bottom", ha="left", color=VERDE, **cx)
    ax.hlines(d[f"{nome}_pos"], d["t_clear"], d["t_fim"], color=VERMELHO,
              lw=1.8, ls=(0, (5, 2)), zorder=6)
    ax.text(d["t_clear"] + 0.004, d[f"{nome}_pos"],
            f"média pós-falta: {br(d[f'{nome}_pos'])} pu",
            va="bottom", ha="left", color=VERMELHO, **cx)

    # 4. quanto do tempo em cada sentido de fluxo
    ax.text(0.985, 0.965, caixa, transform=ax.transAxes, va="top", ha="right",
            fontsize=9.5, fontweight="bold", color=NAVY, zorder=9, linespacing=1.45,
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor="#cbd5e1", alpha=0.94))

    ax.set_ylabel(rotulo)
    ax.set_xlim(T_INI_PLOT, d["t_fim"])
    ax.set_ylim(*d[f"{nome}_ylim"])
    ax.yaxis.set_major_formatter(virg1)
    ax.xaxis.set_major_formatter(virg2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=1)
    ax.set_axisbelow(True)


def main():
    d = carregar()
    # figsize escolhido pela LEGIBILIDADE NO DOCX, nao pelo visual isolado: a
    # fonte efetiva na pagina e font_pt * 6,5/largura_figsize. O padrao do Cap. 5
    # e escala ~0,79 (~7,9 pt efetivos); 8,3 in inserido a 6,5 in da isso. Ver o
    # comentario equivalente em gen_retencao_didatica.py. Aumentar a fonte em vez
    # de encolher o figsize nao resolve.
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.3, 5.4), sharex=True)

    painel(ax1, d, "P", AZUL, "Potência ativa P (pu)",
           f"após a eliminação da falta:\n"
           f"entrega {br(d['P_frac_pos'], 1)}% do tempo · absorve {br(d['P_frac'], 1)}%")
    painel(ax2, d, "Q", LARANJA, "Potência reativa Q (pu)",
           f"após a eliminação da falta:\n"
           f"entrega {br(d['Q_frac_pos'], 1)}% do tempo · absorve {br(d['Q_frac'], 1)}%")

    ax1.annotate("falta aplicada", xy=(d["t_fault"], 1.0), xycoords=("data", "axes fraction"),
                 xytext=(4, -12), textcoords="offset points", fontsize=9,
                 color=VERMELHO, fontweight="bold")
    ax1.annotate("falta eliminada", xy=(d["t_clear"], 1.0), xycoords=("data", "axes fraction"),
                 xytext=(4, -12), textcoords="offset points", fontsize=9,
                 color=VERDE, fontweight="bold")
    ax2.set_xlabel("Tempo (s)")

    handles = [
        Patch(facecolor=VERDE, alpha=0.16,
              label="Potência > 0: o inversor ENTREGA energia à rede"),
        Patch(facecolor=VERMELHO, alpha=0.30,
              label="Potência < 0: o inversor ABSORVE energia da rede"),
        Line2D([], [], color=VERDE, lw=1.8, ls=(0, (5, 2)),
               label="Patamar pré-falta"),
        Line2D([], [], color=VERMELHO, lw=1.8, ls=(0, (5, 2)),
               label="Média após a eliminação da falta"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, -0.075), fontsize=9)

    fig.suptitle("Potência injetada pelo inversor: falta trifásica na Barra 7 "
                 "com sintonia inadequada", fontsize=11.5, fontweight="bold",
                 y=0.995)
    fig.tight_layout(rect=(0, 0.085, 1, 0.98))

    for ext in ("svg", "png"):
        p = OUT_DIR / f"potencia_didatica.{ext}"
        fig.savefig(p, format=ext, dpi=200, bbox_inches="tight", facecolor="white")
        print("gerado:", p.relative_to(ROOT))
    plt.close(fig)

    print(f"  P: antes {br(d['P_pre'])} pu -> media pos {br(d['P_pos'])} pu, "
          f"negativa em {br(d['P_frac'], 1)}% do tempo")
    print(f"  Q: antes {br(d['Q_pre'])} pu -> media pos {br(d['Q_pos'])} pu, "
          f"negativa em {br(d['Q_frac'], 1)}% do tempo")


if __name__ == "__main__":
    main()
