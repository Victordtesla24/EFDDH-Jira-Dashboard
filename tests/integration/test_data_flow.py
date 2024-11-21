"""Integration tests for data flow."""

import pandas as pd
import plotly.graph_objects as go

from src.metrics.metrics_calculator import MetricsCalculator
from src.utils.types import DataFrame
from src.visualizations.program_charts import Visualizer


def test_data_to_metrics_flow(sample_data: DataFrame) -> None:
    """Test data flow from raw data to metrics."""
    calculator = MetricsCalculator(sample_data)
    metrics = calculator.get_basic_metrics()

    assert isinstance(metrics, dict)
    assert metrics["total_stories"] == len(sample_data)
    assert "completed_stories" in metrics
    assert "completion_rate" in metrics

    velocity = calculator.get_sprint_velocity()
    assert isinstance(velocity, pd.Series)
    assert not velocity.empty


def test_data_to_visualization_flow(sample_data: DataFrame) -> None:
    """Test data flow from raw data to visualization."""
    visualizer = Visualizer(sample_data)
    velocity_chart = visualizer.create_velocity_chart()
    assert isinstance(velocity_chart, go.Figure)
