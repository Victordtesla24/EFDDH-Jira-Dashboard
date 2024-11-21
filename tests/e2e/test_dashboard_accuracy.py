"""End-to-end tests for dashboard accuracy."""

import pandas as pd
import plotly.graph_objects as go
import pytest

from src.utils.types import DataFrame
from src.visualizations.program_charts import Visualizer


def test_dashboard_data_accuracy(test_data_path: str) -> None:
    """Test that dashboard loads and processes data correctly."""
    data = pd.read_csv(test_data_path)
    assert isinstance(data, pd.DataFrame)
    required_columns = ["Issue Key", "Summary", "Status", "Story Points"]
    for col in required_columns:
        assert col in data.columns


def test_visualization_precision(sample_data: DataFrame) -> None:
    """Test visualization data precision."""
    visualizer = Visualizer(sample_data)

    try:
        velocity_chart = visualizer.create_velocity_chart()
        assert isinstance(velocity_chart, go.Figure)
        assert len(velocity_chart.data) > 0

        chart_data = velocity_chart.data[0]
        assert len(chart_data.x) == len(chart_data.y)
        assert all(isinstance(y, (int, float)) for y in chart_data.y)

    except Exception as e:
        pytest.fail(f"Unexpected error in visualization test: {str(e)}")
