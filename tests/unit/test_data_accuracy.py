"""Test data accuracy."""

import pandas as pd

from src.utils.data_processor import load_data, process_sprint_data


def test_load_data():
    """Test data loading."""
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
