"""pipeline — CSV (MATLAB export) → dados carregados → figuras Plotly."""

from .loader import SimData
from .chart import ChartBuilder

__all__ = ["SimData", "ChartBuilder"]
