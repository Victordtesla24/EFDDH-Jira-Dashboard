import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Generator, Iterator

from src.utils.logger import logger
import pandas as pd

class ErrorHandler:
    """Class for handling errors and monitoring application health."""

    def __init__(self) -> None:
        self.recovery_attempts: int = 0
        self.backoff_times: List[datetime] = []
        self.logger = logger

    @contextmanager
    def handle_operation(self, operation_name: str) -> Generator[None, None, None]:
        """
        Context manager for handling operations.

        Args:
            operation_name: Name of the operation being handled

        Returns:
            ErrorHandler instance
        """
        try:
            yield
        except Exception as e:
            self.handle_error(f"Error in {operation_name}: {str(e)}")
            raise

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get current health status of error handling.

        Returns:
            Dict containing health metrics
        """
        return {
            "recent_errors": [],
            "circuit_breakers": {},
            "recovery_attempts": self.recovery_attempts,
            "backoff_times": self.backoff_times,
        }

    def reset_error_tracking(self):
        self.recovery_attempts = 0
        self.backoff_times = []

    def _recover_data_corruption(self, component, error):
        pass

    def handle_error(self, error, context=""):
        """Handle errors and log them appropriately"""
        error_message = f"{context}: {str(error)}" if context else str(error)
        self.logger.error(error_message)
        return error_message

    @classmethod
    def monitor_visualization(cls, viz_method):
        """Decorator for monitoring visualization methods"""

        def wrapper(*args, **kwargs):
            try:
                result = viz_method(*args, **kwargs)
                if result is None:
                    error_msg = f"Visualization {viz_method.__name__} returned None"
                    cls.handle_error(error_msg)
                    logger.error(error_msg)
                return result
            except Exception as e:
                error_msg = f"Error in {viz_method.__name__}: {str(e)}"
                cls.handle_error(error_msg)
                logger.error(error_msg)
                return None

        return wrapper

    @classmethod
    def check_data_requirements(cls, df, required_columns):
        """Check if DataFrame has required columns"""
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            error_msg = f"Missing required columns: {missing_columns}"
            cls.handle_error(error_msg)
            logger.error(error_msg)
            return False
        return True

    @staticmethod
    def check_data_quality(df: pd.DataFrame) -> bool:
        """Check data quality and completeness."""
        try:
            # Check for minimum required rows
            if len(df) < 1:
                logger.error("Empty dataset")
                return False
            
            # Check for invalid story points
            invalid_points = df[
                (df['Story Points'].notna()) & 
                (df['Story Points'] < 0)
            ].shape[0]
            if invalid_points > 0:
                logger.warning(f"Found {invalid_points} rows with invalid story points")
            
            # Check for future created dates
            future_dates = df[
                df['Created'] > pd.Timestamp.now()
            ].shape[0]
            if future_dates > 0:
                logger.warning(f"Found {future_dates} rows with future created dates")
            
            # Check for invalid date ranges
            invalid_dates = df[
                (df['Due Date'].notna()) & 
                (df['Created'].notna()) & 
                (df['Due Date'] < df['Created'])
            ].shape[0]
            if invalid_dates > 0:
                logger.warning(f"Found {invalid_dates} rows with due date before created date")
            
            return True
        
        except Exception as e:
            logger.error(f"Error in data quality check: {str(e)}")
            return False
