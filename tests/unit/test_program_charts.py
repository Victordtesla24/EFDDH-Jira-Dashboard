"""Test program charts functionality."""

from typing import Any, Dict

import pandas as pd
import pytest

from src.visualizations.program_charts import Visualizer


def test_create_status_chart(sample_data: pd.DataFrame) -> None:
    """Test status chart creation."""
    visualizer = Visualizer(sample_data)
    chart = visualizer.create_status_chart()
    assert chart is not None


def test_sprint_metrics_chart(sample_data: pd.DataFrame) -> None:
    """Test sprint metrics chart creation."""
    visualizer = Visualizer(sample_data)
    chart = visualizer.create_velocity_chart()
    assert chart is not None
