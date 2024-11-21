"""Test metrics calculator."""

import pandas as pd
import pytest

from src.metrics.metrics_calculator import MetricsCalculator


def test_basic_metrics(test_data):
    """Test basic metrics calculation."""
    calculator = MetricsCalculator(test_data)
    metrics = calculator.get_basic_metrics()

    assert isinstance(metrics, dict)
    assert metrics["total_stories"] == len(test_data)
    assert metrics["completed_stories"] >= 0
    assert metrics["total_points"] >= 0
    assert 0 <= metrics["completion_rate"] <= 1


def test_sprint_velocity(test_data):
    """Test sprint velocity calculation."""
    calculator = MetricsCalculator(test_data)
    velocity = calculator.get_sprint_velocity()

    assert isinstance(velocity, pd.Series)
    assert not velocity.empty
    assert all(v >= 0 for v in velocity)
