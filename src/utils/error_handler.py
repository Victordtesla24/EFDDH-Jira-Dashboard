from typing import Any, Optional

import pandas as pd

from src.utils.logger import logger


class ErrorHandler:
    """Handle application errors."""

    def __init__(self):
        self.logger = logger

    def handle_error(self, error: Exception, context: Optional[str] = None) -> None:
        """Handle and log errors."""
        error_msg = f"{context}: {str(error)}" if context else str(error)
        self.logger.error(error_msg)

    @staticmethod
    def check_connection() -> bool:
        """Check connection status."""
        return True

    @staticmethod
    def validate_input(data: Any) -> bool:
        """Validate input data."""
        return bool(data)

    @staticmethod
    def log_error(error: Exception) -> None:
        """Log error details."""
        logger.error(str(error))

    @staticmethod
    def check_data_quality(df: pd.DataFrame) -> bool:
        """Check data quality and completeness."""
        try:
            if len(df) < 1:
                logger.error("Empty dataset")
                return False

            # Check for invalid story points
            points_col = (
                "Story Points" if "Story Points" in df.columns else "Story_Points"
            )
            invalid_points = df[(df[points_col].notna()) & (df[points_col] < 0)].shape[
                0
            ]
            if invalid_points > 0:
                logger.warning(f"Found {invalid_points} rows with invalid story points")

            # Check for future created dates
            future_dates = df[df["Created"] > pd.Timestamp.now()].shape[0]
            if future_dates > 0:
                logger.warning(f"Found {future_dates} rows with future created dates")

            # Check for invalid date ranges
            due_col = "Due Date" if "Due Date" in df.columns else "Due_Date"
            if due_col in df.columns:
                invalid_dates = df[
                    (df[due_col].notna())
                    & (df["Created"].notna())
                    & (df[due_col] < df["Created"])
                ].shape[0]
                if invalid_dates > 0:
                    logger.warning(
                        f"Found {invalid_dates} rows with due date before created date"
                    )

            return True

        except Exception as e:
            logger.error(f"Error in data quality check: {str(e)}")
            return False
