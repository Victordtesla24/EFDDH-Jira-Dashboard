"""Test data validation utilities."""

import pandas as pd

REQUIRED_COLUMNS = [
    "Issue Key",
    "Story Points",
    "Status",
    "Sprint",
    "Created",
    "Priority",
    "Issue Type",
    "Epic Name",
]


def validate_test_data(df: pd.DataFrame) -> bool:
    """Validate test data has required columns and structure."""
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        print(f"Missing columns: {missing_cols}")
        print(f"Available columns: {df.columns.tolist()}")
        return False
    return True
