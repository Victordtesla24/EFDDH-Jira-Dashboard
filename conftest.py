"""Pytest configuration and fixtures."""

import logging
import os
import sys
from unittest.mock import Mock

import pandas as pd
import pytest

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(project_root))


@pytest.fixture
def sample_data():
    """Provide sample data for testing."""
    return pd.DataFrame(
        {
            "Issue_Key": ["PROJ-1", "PROJ-2", "PROJ-3", "PROJ-4"],
            "Story_Points": [5, 3, 8, 4],
            "Status": ["Done", "In Progress", "Done", "To Do"],
            "Sprint": ["Sprint 1", "Sprint 1", "Sprint 2", "Sprint 2"],
            "Created": pd.date_range(start="2024-01-01", periods=4),
        }
    )


@pytest.fixture
def test_data_path(tmp_path):
    """Create a temporary test data file."""
    data = pd.DataFrame(
        {
            "Issue_Key": ["TEST-1", "TEST-2"],
            "Story_Points": [3, 5],
            "Status": ["Done", "In Progress"],
            "Sprint": ["Sprint 1", "Sprint 1"],
            "Created": ["01/01/2024", "02/01/2024"],
        }
    )

    file_path = tmp_path / "test_data.csv"
    data.to_csv(file_path, index=False)
    return file_path


@pytest.fixture
def mock_logger():
    """Provide mock logger for testing."""
    return Mock(spec=logging.Logger)


@pytest.fixture(autouse=True)
def setup_streamlit():
    """Setup streamlit environment for testing."""
    import streamlit as st

    if "data" not in st.session_state:
        st.session_state.data = None
