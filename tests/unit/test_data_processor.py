"""Test data processor functionality."""

import pandas as pd
import pytest

from src.utils.data_processor import DataProcessor, process_sprint_data


def test_process_sprint_data():
    """Test sprint data processing."""
    data = pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]})
    result = process_sprint_data(data)
    assert isinstance(result, dict)
    assert "data" in result
    assert isinstance(result["data"], pd.DataFrame)
