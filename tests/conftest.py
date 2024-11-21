"""Test configuration and fixtures."""

import pandas as pd
import pytest


@pytest.fixture
def test_data():
    """Provide test data."""
    return pd.DataFrame(
        {
            "Issue Key": ["TEST-1", "TEST-2"],
            "Story Points": [3, 5],
            "Status": ["Done", "In Progress"],
            "Sprint": ["Sprint 1", "Sprint 1"],
            "Created": ["2024-01-01", "2024-01-02"],
            "Summary": ["Test 1", "Test 2"],
        }
    )


@pytest.fixture
def test_data_path(tmp_path):
    """Create test data file."""
    data = pd.DataFrame(
        {
            "Issue Key": ["TEST-1", "TEST-2"],
            "Story Points": [3, 5],
            "Status": ["Done", "In Progress"],
            "Sprint": ["Sprint 1", "Sprint 1"],
            "Created": ["2024-01-01", "2024-01-02"],
            "Summary": ["Test 1", "Test 2"],
        }
    )
    file_path = tmp_path / "test_data.csv"
    data.to_csv(file_path, index=False)
    return file_path
