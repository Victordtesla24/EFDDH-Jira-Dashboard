"""Visualization modules for the application."""

from .program_charts import Visualizer


def create_program_charts():
    """Create program charts visualization."""
    return Visualizer()


def create_program_overview():
    """Create program overview visualization."""
    return Visualizer()


__all__ = ["create_program_charts", "create_program_overview"]
