"""
app.py — Gerador de relatório PLL-IEEE9Bus com múltiplos cenários.

Varre output/results/**/sim_data.csv e gera um HTML com seletor de cenário.
Uso: .venv/Scripts/python.exe app.py [--out PATH]
"""
import sys
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from src import SimData, ChartBuilder, SpectrumBuilder, HTMLRenderer

RESULTS_DIR = Path("output/results")
DEFAULT_OUT = Path("output/pll_metrics.html")

FAULT_LABELS: dict[str, str] = {
    "3phase":        "Trifásica",
    "1phase":        "Monofásica",
    "1phase_ground": "Monofásica-terra",
    "2phase":        "Bifásica",
    "2phase_ground": "Bifásica-terra",
}


def _is_bad_pll(key: str) -> bool:
    return key.split("/")[-1].endswith("_bad_pll")


def _scenario_label(key: str) -> str:
    clean = key.replace("_bad_pll", "")
    if clean == "regime":
        return "Regime permanente"
    parts = clean.split("/")
    if len(parts) == 2:
        loc, fault = parts
        fl = FAULT_LABELS.get(fault, fault)
        if loc.startswith("bus"):
            return f"Barra {loc[3:]} — {fl}"
        if loc.startswith("line"):
            return f"Linha {loc[4:].replace('_', '-')} — {fl}"
    return clean


def _sort_key(key: str) -> tuple:
    bad   = 1 if _is_bad_pll(key) else 0
    clean = key.replace("_bad_pll", "")
    if clean == "regime":
        return (0, 0, 0, "", bad)
    parts = clean.split("/")
    loc   = parts[0]
    fault = parts[1] if len(parts) > 1 else ""
    if loc.startswith("bus"):
        try:
            n = int(loc[3:])
        except ValueError:
            n = 0
        return (1, n, 0, fault, bad)
    if loc.startswith("line"):
        nums = loc[4:].split("_")
        a = int(nums[0]) if nums else 0
        b = int(nums[1]) if len(nums) > 1 else 0
        return (2, a, b, fault, bad)
    return (3, 0, 0, key, bad)


def scan_scenarios(results_dir: Path) -> dict[str, Path]:
    """Retorna {key: csv_path} de todos os sim_data.csv abaixo de results_dir."""
    raw = {
        csv.parent.relative_to(results_dir).as_posix(): csv
        for csv in results_dir.glob("**/sim_data.csv")
    }
    return dict(sorted(raw.items(), key=lambda kv: _sort_key(kv[0])))


def main() -> None:
    p = argparse.ArgumentParser(description="Gera relatorio HTML PLL-IEEE9Bus.")
    p.add_argument("--out", type=Path, default=DEFAULT_OUT, metavar="PATH",
                   help=f"HTML de saida (padrao: {DEFAULT_OUT})")
    args = p.parse_args()

    scenarios_csv = scan_scenarios(RESULTS_DIR)
    if not scenarios_csv:
        print(f"Nenhum sim_data.csv encontrado em {RESULTS_DIR}")
        return

    print(f"Cenarios encontrados: {len(scenarios_csv)}")
    scenarios: dict[str, dict] = {}
    for key, csv_path in scenarios_csv.items():
        print(f"  [{key}] carregando...", end=" ", flush=True)
        data    = SimData(csv_path)
        builder = ChartBuilder(data)
        fig_inv, fig_sys, tm_inv, tm_sys = builder.build_sections()
        fig_spec, tm_spec = SpectrumBuilder(data).build()
        n = (len(fig_inv.data) + (len(fig_sys.data) if fig_sys else 0)
             + (len(fig_spec.data) if fig_spec else 0))
        scenarios[key] = {
            "data":     data,
            "label":    _scenario_label(key),
            "bad_pll":  _is_bad_pll(key),
            "fig_inv":  fig_inv,
            "fig_sys":  fig_sys,
            "fig_spec": fig_spec,
            "tm_inv":   tm_inv,
            "tm_sys":   tm_sys,
            "tm_spec":  tm_spec,
        }
        print(f"{n} tracas")

    print("\nGerando HTML...")
    out = HTMLRenderer(scenarios).render(args.out)
    print(f"Salvo em: {out}")


if __name__ == "__main__":
    main()
