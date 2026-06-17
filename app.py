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


def _latest_results_csv() -> Path:
    """Retorna o sim_data.csv mais recente em output/results/, ou CSV_PATH como fallback."""
    results_dir = CSV_PATH.parent / "results"
    if results_dir.exists():
        candidates = list(results_dir.glob("*/sim_data.csv"))
        if candidates:
            return max(candidates, key=lambda p: p.stat().st_mtime)
    return CSV_PATH


def parse_args() -> argparse.Namespace:
    default_csv = _latest_results_csv()
    p = argparse.ArgumentParser(
        description="Gera relatório HTML com métricas e gráficos do SRF-PLL."
    )
    p.add_argument(
        "--csv",
        type=Path,
        default=default_csv,
        metavar="PATH",
        help=f"Caminho do CSV de entrada (padrão: mais recente em output/results/ ou {CSV_PATH})",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=None,
        metavar="PATH",
        help="Caminho do HTML de saída (padrão: pll_metrics.html na mesma pasta do CSV)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    # HTML de saída: mesma pasta do CSV se não especificado
    out_path: Path = args.out if args.out is not None else args.csv.parent / "pll_metrics.html"

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
    print(f"    ΔP  = {m['dP_ufv']:.4f} pu")
    print(f"    ΔQ  = {m['dQ_ufv']:.4f} pu")

    # 2. Construir figura Plotly
    print("\n📈  Construindo gráficos...")
    builder = ChartBuilder(data)
    fig, trace_map = builder.build()
    print(f"    {len(fig.data)} traços, {len(trace_map)} com tema dinâmico")

    # 3. Renderizar HTML
    print("\n🖊   Gerando HTML...")
    renderer = HTMLRenderer(data, fig, trace_map)
    out = renderer.render(out_path)
    print(f"    ✅  Salvo em: {out}")


if __name__ == "__main__":
    main()
