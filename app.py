"""
app.py - Ponto de entrada do analisador PLL-IEEE9Bus.

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
        description="Gera relatorio HTML com metricas e graficos do SRF-PLL."
    )
    p.add_argument("--csv", type=Path, default=default_csv, metavar="PATH",
                   help=f"CSV de entrada (padrao: mais recente em output/results/ ou {CSV_PATH})")
    p.add_argument("--out", type=Path, default=None, metavar="PATH",
                   help="HTML de saida (padrao: pll_metrics.html na mesma pasta do CSV)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    out_path: Path = args.out if args.out is not None else args.csv.parent / "pll_metrics.html"

    # 1. Carregar dados
    print(f"Lendo: {args.csv}")
    data = SimData(args.csv)
    print(f"    {data}")

    m = data.metrics
    print("\nMetricas pos-falta:")
    if m["IAE"] is not None:
        print(f"    IAE = {m['IAE']:.4f} rad*s")
        print(f"    ISE = {m['ISE']:.4f} rad2*s")
        print(f"    ts  = {m['ts']:.4f} s")
    else:
        print("    (angulos nao disponiveis - IAE/ISE/ts omitidos)")
    print(f"    dP  = {m['dP_ufv']:.4f} pu")
    print(f"    dQ  = {m['dQ_ufv']:.4f} pu")

    # 2. Construir figuras Plotly
    print("\nConstruindo graficos...")
    builder = ChartBuilder(data)
    fig_inv, fig_sys, tm_inv, tm_sys = builder.build_sections()
    n_total = len(fig_inv.data) + (len(fig_sys.data) if fig_sys else 0)
    print(f"    {n_total} tracas ({len(tm_inv)} inv, {len(tm_sys)} sys)")

    # 3. Renderizar HTML
    print("\nGerando HTML...")
    renderer = HTMLRenderer(data, fig_inv, fig_sys, tm_inv, tm_sys)
    out = renderer.render(out_path)
    print(f"    Salvo em: {out}")


if __name__ == "__main__":
    main()