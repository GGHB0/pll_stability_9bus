"""
src — Pacote de análise PLL-IEEE9Bus.

Subpacotes:
    config    → constantes (T_FAULT, TOL_RAD, thresholds, paletas)
    pipeline  → SimData (carrega CSV, calcula métricas) + ChartBuilder (Plotly)
    report    → HTMLRenderer (gera relatório HTML)
"""

from .pipeline.loader   import SimData
from .pipeline.chart    import ChartBuilder
from .pipeline.spectrum import SpectrumBuilder
from .report.renderer   import HTMLRenderer

__all__ = ["SimData", "ChartBuilder", "SpectrumBuilder", "HTMLRenderer"]
