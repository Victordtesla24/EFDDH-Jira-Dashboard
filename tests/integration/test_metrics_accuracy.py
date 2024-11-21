"""Integration tests for metrics accuracy."""

import pandas as pd
import pytest

from src.metrics.metrics_calculator import MetricsCalculator


def test_metrics_accuracy(test_data):
    """Test accuracy of metrics calculations."""
    calculator = MetricsCalculator(test_data)
    metrics = calculator.get_basic_metrics()

    # Verify completion rate
    completed = test_data[test_data["Status"] == "Done"]
    expected_rate = len(completed) / len(test_data)
    assert metrics["completion_rate"] == pytest.approx(expected_rate)

    # Verify story points
    total_points = test_data["Story Points"].fillna(0).sum()
    assert metrics["total_points"] == pytest.approx(total_points)
