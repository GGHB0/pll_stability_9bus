"""pipeline — CSV (MATLAB export) → dados carregados → figuras Plotly."""

from .loader import SimData
from .chart import ChartBuilder
from .spectrum import SpectrumBuilder

__all__ = ["SimData", "ChartBuilder", "SpectrumBuilder"]
