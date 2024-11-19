"""Root package initialization."""

# Import core utilities first
from .utils import ErrorHandler, logger, DataProcessor

# Then import visualizations that depend on utils
from .visualizations import create_program_overview, create_program_charts

__all__ = [
    "ErrorHandler",
    "logger",
    "DataProcessor",
    "create_program_overview",
    "create_program_charts"
]
