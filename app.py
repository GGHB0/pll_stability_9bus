"""
app.py — Ponto de entrada do analisador PLL-IEEE9Bus.

Uso:
    .venv/Scripts/python.exe app.py
    .venv/Scripts/python.exe app.py --csv output/sim_data.csv
    .venv/Scripts/python.exe app.py --out output/relatorio.html
"""

import sys
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src import SimData, ChartBuilder, HTMLRenderer
from src.config import CSV_PATH, HTML_OUT


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Gera relatório HTML com métricas e gráficos do SRF-PLL."
    )
    p.add_argument(
        "--csv",
        type=Path,
        default=CSV_PATH,
        metavar="PATH",
        help=f"Caminho do CSV de entrada (padrão: {CSV_PATH})",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=HTML_OUT,
        metavar="PATH",
        help=f"Caminho do HTML de saída (padrão: {HTML_OUT})",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # 1. Carregar dados e calcular métricas
    print(f"📂  Lendo: {args.csv}")
    data = SimData(args.csv)
    print(f"    {data}")

    m = data.metrics
    print("\n📊  Métricas pós-falta:")
    if m["IAE"] is not None:
        print(f"    IAE = {m['IAE']:.4f} rad·s")
        print(f"    ISE = {m['ISE']:.4f} rad²·s")
        print(f"    ts  = {m['ts']:.4f} s")
    else:
        print("    (ângulos não disponíveis — IAE/ISE/ts omitidos)")
    print(f"    ΔP  = {m['dP']:.4f} pu")
    print(f"    ΔQ  = {m['dQ']:.4f} pu")

    # 2. Construir figura Plotly
    print("\n📈  Construindo gráficos...")
    builder = ChartBuilder(data)
    fig, trace_map = builder.build()
    print(f"    {len(fig.data)} traços, {len(trace_map)} com tema dinâmico")

    # 3. Renderizar HTML
    print("\n🖊   Gerando HTML...")
    renderer = HTMLRenderer(data, fig, trace_map)
    out = renderer.render(args.out)
    print(f"    ✅  Salvo em: {out}")


if __name__ == "__main__":
    main()
