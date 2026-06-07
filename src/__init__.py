"""
src — Pacote de análise PLL-IEEE9Bus.

Módulos:
    config    → constantes (T_FAULT, TOL_RAD, paletas)
    loader    → SimData  (carrega CSV, calcula métricas)
    chart     → ChartBuilder (constrói subplots Plotly)
    renderer  → HTMLRenderer (gera relatório HTML)
"""

from .loader   import SimData
from .chart    import ChartBuilder
from .renderer import HTMLRenderer

__all__ = ["SimData", "ChartBuilder", "HTMLRenderer"]
