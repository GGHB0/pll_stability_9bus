"""
Gera as figuras didaticas da construcao da RETENCAO de v_d em assets/charts/.

Motivacao (2026-08-26): o termo "retencao" aparece no Cap. 5 do TCC com valores
fechados (9,2%, 8,2%, 11,3%, 47,1%, 58,4%) sem que o texto mostre de onde sai a
razao. Estas figuras exibem a construcao sobre os dados reais, em vez de definir
a metrica so em prosa.

Receita (identica a de src/pipeline e a registrada em
.claude/kb/tcc-word/revisao_fragmento_cap5_metricas.md, secao "Definicoes
fechadas"):

    retencao = media(v_d) em [t_fault + 2 ciclos, t_clear]
             / media(v_d) em [t_fault - 50 ms, t_fault)

Os 2 ciclos descartados (33,3 ms a 60 Hz) removem o transitorio de comutacao da
aplicacao da falta, que domina o trecho inicial e nao representa o afundamento.

Saidas (SVG + PNG, mesma convencao de gen_fault_waveforms.py):
  retencao_construcao.svg  -- painel unico, caso nominal (bus7/3phase)
  retencao_comparacao.svg  -- painel duplo nominal x sintonia inadequada,
                              usado na Secao 5.4: mostra que as bases pre-falta
                              diferem (0,989 x 0,823 pu) mas as razoes quase
                              coincidem, que e o que autoriza atribuir a
                              diferenca de comportamento a sintonia e nao a
                              severidade da perturbacao.

No painel duplo o eixo X e o tempo RELATIVO ao inicio da falta, porque t_fault
difere entre os cenarios (0,3 s no nominal, 0,6 s na sintonia inadequada); o
eixo Y e compartilhado, pois e justamente a diferenca das bases pre-falta que a
figura precisa deixar visivel (mesmo motivo de YLIM_GROUPS em
gen_fault_waveforms.py).

Requer matplotlib (nao listado em requirements.txt, ver gen_fault_waveforms.py).
"""
import io
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "output" / "results"
OUT_DIR = ROOT / "assets" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# paleta do projeto (src/config/settings.py, LIGHT_COLORS)
AZUL, VERMELHO, VERDE, LARANJA = "#2563eb", "#dc2626", "#16a34a", "#ea580c"
NAVY = "#0B132B"
GRID_COLOR = "#e2e8f0"
CINZA_DESCARTE = "#cbd5e1"

CICLO_S = 1 / 60          # 60 Hz
JANELA_PRE_S = 0.05       # 50 ms antes da falta
N_CICLOS_DESCARTE = 2

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

# formatador pt-BR: separador decimal virgula
virg2 = FuncFormatter(lambda v, _p: f"{v:.2f}".replace(".", ","))


def br(x, casas=3):
    """Numero em notacao pt-BR (virgula decimal)."""
    return f"{x:.{casas}f}".replace(".", ",")


def carregar(folder):
    """Le o cenario e devolve o traco de v_d com as duas medias da receita."""
    base = RESULTS_DIR / folder
    fi = json.loads((base / "fault_info.json").read_text())
    df = pd.read_csv(base / "sim_data.csv")
    t_fault, t_clear = fi["t_fault"], fi["t_clear"]

    t, vd = df.t_s, df.vd_rede_pu
    pre = vd[(t >= t_fault - JANELA_PRE_S) & (t < t_fault)]
    dur = vd[(t >= t_fault + N_CICLOS_DESCARTE * CICLO_S) & (t <= t_clear)]

    v_pre, v_dur = float(pre.mean()), float(dur.mean())
    return dict(t=t, vd=vd, t_fault=t_fault, t_clear=t_clear,
                v_pre=v_pre, v_dur=v_dur, retencao=v_dur / v_pre * 100.0)


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)


def desenhar(ax, d, relativo, y_bot, y_top, rotulos_longos):
    """Desenha um painel da construcao da retencao.

    relativo=True desloca o eixo X para o inicio da falta (necessario no painel
    duplo, onde t_fault difere entre os cenarios).
    """
    origem = d["t_fault"] if relativo else 0.0
    t = d["t"] - origem
    t_ini = d["t_fault"] - origem
    t_fim = d["t_clear"] - origem
    t_corte = t_ini + N_CICLOS_DESCARTE * CICLO_S
    t_pre = t_ini - JANELA_PRE_S

    x0, x1 = t_ini - 0.09, t_fim + 0.025
    w = (t >= x0) & (t <= x1)
    ax.plot(t[w], d["vd"][w], color=AZUL, lw=1.1, zorder=4)

    # faixas das duas janelas de media + trecho descartado
    ax.axvspan(t_pre, t_ini, color=VERDE, alpha=0.13, zorder=0)
    ax.axvspan(t_ini, t_corte, facecolor=CINZA_DESCARTE, alpha=0.35,
               edgecolor="none", zorder=0)
    ax.axvspan(t_corte, t_fim, color=LARANJA, alpha=0.16, zorder=0)

    # as duas medias que formam a razao
    ax.hlines(d["v_pre"], t_pre, t_ini, color=VERDE, lw=2.0, ls="--", zorder=6)
    ax.hlines(d["v_dur"], t_corte, t_fim, color=LARANJA, lw=2.0, ls="--", zorder=6)

    ax.axvline(t_ini, color=VERMELHO, ls=":", lw=1.2, zorder=3)
    ax.axvline(t_fim, color=VERDE, ls=":", lw=1.2, zorder=3)

    # barra com a duracao real da falta (a janela de medicao comeca depois dela)
    y_bar = y_top - 0.14
    ax.annotate("", xy=(t_ini, y_bar), xytext=(t_fim, y_bar),
                arrowprops=dict(arrowstyle="<->", color=VERMELHO, lw=1.2))
    ax.text((t_ini + t_fim) / 2, y_bar + 0.035, "falta aplicada (0,1 s)",
            ha="center", fontsize=8, color=VERMELHO, fontweight="bold")

    rot_pre = (f"média pré-falta = {br(d['v_pre'])} pu" if rotulos_longos
               else f"{br(d['v_pre'])} pu")
    rot_dur = (f"média durante a falta = {br(d['v_dur'])} pu" if rotulos_longos
               else f"{br(d['v_dur'])} pu")

    ax.annotate(rot_pre, xy=(t_ini - 0.030, d["v_pre"]),
                xytext=(x0 + 0.002, d["v_pre"] - 0.28),
                color=VERDE, fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=VERDE, lw=1.0))
    ax.annotate(rot_dur, xy=(t_ini + 0.052, d["v_dur"]),
                xytext=(t_ini - 0.028, d["v_dur"] + 0.27),
                color=LARANJA, fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.0))

    # a conta fechada, dentro da propria figura
    ax.text(t_fim - 0.003, 0.62,
            f"retenção = {br(d['v_dur'])} / {br(d['v_pre'])}\n"
            f"= {br(d['retencao'], 1)} %",
            fontsize=9.5, fontweight="bold", color=NAVY, va="center",
            ha="right", linespacing=1.4, zorder=7,
            bbox=dict(boxstyle="round,pad=0.42", facecolor="#f8fafc",
                      edgecolor="#94a3b8", lw=0.8))

    ax.set_xlim(x0, x1)
    ax.set_ylim(y_bot, y_top)
    ax.set_xticks([t_ini - 0.05, t_ini, t_ini + 0.05, t_ini + 0.10])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.xaxis.set_major_formatter(virg2)
    ax.yaxis.set_major_formatter(virg2)
    style_axes(ax)


def legenda_faixas(fig, y):
    handles = [
        Line2D([], [], color=AZUL, lw=1.4, label="$v_d$ da rede"),
        Patch(facecolor=VERDE, alpha=0.13, label="janela pré-falta (50 ms)"),
        Patch(facecolor=CINZA_DESCARTE, alpha=0.5, label="2 ciclos descartados"),
        Patch(facecolor=LARANJA, alpha=0.16, label="janela de medição"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, y))


def save(fig, name):
    svg_path = OUT_DIR / f"{name}.svg"
    png_path = OUT_DIR / f"{name}.png"
    fig.savefig(svg_path, format="svg", facecolor="white")
    fig.savefig(png_path, format="png", dpi=220, facecolor="white")
    plt.close(fig)
    print("OK", svg_path.name, "+", png_path.name)


def fig_construcao():
    """Painel unico, caso nominal: define a metrica sobre dado real."""
    d = carregar("bus7/3phase")
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    desenhar(ax, d, relativo=False, y_bot=-0.14, y_top=1.46,
             rotulos_longos=True)
    ax.set_xlabel("Tempo (s)")
    ax.set_ylabel("Tensão de eixo direto (pu)")
    ax.set_title("Construção da retenção da componente de eixo direto")
    legenda_faixas(fig, -0.005)
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    save(fig, "retencao_construcao")
    return d


def fig_comparacao():
    """Painel duplo da Secao 5.4: bases pre-falta diferentes, razoes proximas."""
    paineis = [
        ("bus7/3phase", "(a) Sintonia nominal"),
        ("bus7/3phase_bad_pll", "(b) Sintonia inadequada"),
    ]
    # figsize escolhido pela LEGIBILIDADE NO DOCX, nao pelo visual isolado: a
    # figura entra na pagina com 6,5 in de largura, entao a fonte efetiva vale
    # font_pt * 6,5/largura_figsize. As demais figuras do Cap. 5 usam
    # figsize 7,0 in a 5,5 in na pagina (escala 0,79, ~7,9 pt efetivos); 8,3 in
    # a 6,5 in da a mesma escala. Aumentar a fonte em vez de encolher o figsize
    # desalinha esta figura das outras -- ver skill svg-diagrams.
    fig, axes = plt.subplots(1, 2, figsize=(8.3, 3.6), sharey=True)
    dados = []
    for ax, (folder, titulo) in zip(axes, paineis):
        d = carregar(folder)
        dados.append((folder, d))
        desenhar(ax, d, relativo=True, y_bot=-0.14, y_top=1.46,
                 rotulos_longos=False)
        ax.set_title(titulo, fontsize=10.5)
        ax.set_xlabel("Tempo relativo ao início da falta (s)")
    axes[0].set_ylabel("Tensão de eixo direto (pu)")
    legenda_faixas(fig, -0.005)
    fig.tight_layout(rect=(0, 0.065, 1, 1))
    save(fig, "retencao_comparacao")
    return dados


def main():
    d_nom = fig_construcao()
    dados = fig_comparacao()

    print()
    print("Valores medidos (conferir contra o KB de metricas):")
    for folder, d in dados:
        print(f"  {folder:24s} pre={br(d['v_pre'], 4)}  "
              f"falta={br(d['v_dur'], 4)}  retencao={br(d['retencao'], 2)} %")

    # o painel unico usa o mesmo cenario nominal do painel duplo
    assert abs(d_nom["retencao"] - dados[0][1]["retencao"]) < 1e-9


if __name__ == "__main__":
    main()
