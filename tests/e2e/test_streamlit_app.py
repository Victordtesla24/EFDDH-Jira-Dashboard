"""End-to-end tests for the Streamlit application."""

import pandas as pd
import pytest
from pandas import DataFrame
from streamlit.testing.v1 import AppTest

from src.metrics.metrics_calculator import MetricsCalculator
from src.visualizations.program_charts import Visualizer


def test_streamlit_app(sample_data: DataFrame) -> None:
    """Test the main Streamlit application."""
    # Initialize app
    at = AppTest.from_file("Home.py")

    # Set up session state with sample data and required objects
    at.session_state.data = sample_data
    at.session_state.calculator = MetricsCalculator(sample_data)
    at.session_state.visualizer = Visualizer(sample_data)

    # Run the app
    at.run()

    # Check for metrics
    metrics_found = False
    for element in at.main:
        if "metric" in str(element.type).lower():
            metrics_found = True
            break

    assert metrics_found, "No metrics found in app"

    # Verify error message not present
    error_found = False
    for element in at.main:
        if "error" in str(element.type).lower():
            error_found = True
            break

    assert not error_found, "Unexpected error message found"


def test_invalid_column_handling() -> None:
    """Test handling of invalid/missing columns."""
    # Initialize app
    at = AppTest.from_file("Home.py")

    # Create invalid data
    invalid_data = pd.DataFrame(
        {"Wrong_Column": ["TEST-1"], "Points": [5], "Current": ["Done"]}
    )

    # Set session state with invalid data
    at.session_state.data = invalid_data

    # Run the app
    at.run()

    # Check for error message
    error_found = False
    for element in at.main:
        if "error" in str(element.type).lower():
            error_found = True
            break

    assert error_found, "Expected error message not found"


@pytest.fixture
def sample_data() -> DataFrame:
    """Create sample data for testing."""
    return pd.DataFrame(
        {
            "Issue Key": ["EFDDH-1", "EFDDH-2", "EFDDH-3"],
            "Story Points": [5, 8, 3],
            "Status": ["Done", "In Progress", "To Do"],
            "Sprint": ["Sprint 1", "Sprint 1", "Sprint 2"],
            "Created": ["2024-01-01", "2024-01-02", "2024-01-03"],
        }
    )
