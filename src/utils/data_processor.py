"""Data processing utilities."""

from typing import Dict, Optional

import pandas as pd

from .logger import logger


def load_data() -> pd.DataFrame:
    """Load data from CSV."""
    df = pd.read_csv("data/test_EFDDH-Jira-Data-All.csv")
    return df.rename(columns={"Issue_Key": "Issue Key", "Story_Points": "Story Points"})


def process_sprint_data(data: pd.DataFrame) -> Dict:
    """Process sprint data."""
    return {"data": data}


class DataProcessor:
    """Process Jira data."""

    def __init__(self) -> None:
        """Initialize processor."""
        self.data: Optional[pd.DataFrame] = None
        logger.info("DataProcessor initialized")

    def standardize_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names.

        Args:
            data: DataFrame to standardize

        Returns:
            DataFrame with standardized column names
        """
        try:
            # Create a copy to avoid modifying the original
            df = data.copy()

            # Standardize common column variations
            column_mapping = {
                "Issue_Key": "Issue Key",
                "Story_Points": "Story Points",
                "Created_Date": "Created",
            }

            # Apply mapping for known variations
            df = df.rename(columns=column_mapping)

            # Validate after standardization
            if not self.validate_columns(df):
                raise ValueError("Required columns missing after standardization")

            return df

        except Exception as e:
            logger.error(f"Error standardizing columns: {str(e)}")
            raise

    def validate_columns(self, data: pd.DataFrame) -> bool:
        """Validate required columns exist in DataFrame.

        Args:
            data: DataFrame to validate

        Returns:
            bool: True if all required columns exist
        """
        required_columns = {
            "Issue Key": ["issue key", "issue_key", "key"],
            "Story Points": ["story points", "story_points", "points"],
            "Status": ["status"],
            "Sprint": ["sprint"],
            "Created": ["created", "created_date"],
        }

        for required, alternatives in required_columns.items():
            if not any(col.lower() in alternatives for col in data.columns):
                logger.error(f"Required column missing: {required}")
                return False

        return True

    def process_csv(self, file_path: str) -> pd.DataFrame:
        """Process CSV file."""
        try:
            df = pd.read_csv(file_path)
            df = self.standardize_columns(df)
            if not self.validate_columns(df):
                raise ValueError("Missing required columns")
            self.data = df
            return self.data
        except Exception as e:
            logger.error(f"Error processing CSV: {str(e)}")
            raise
