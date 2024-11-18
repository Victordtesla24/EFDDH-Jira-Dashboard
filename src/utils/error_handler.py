import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Generator, Iterator

from utils.logger import logger


class ErrorHandler:
    """Class for handling errors and monitoring application health."""

    def __init__(self) -> None:
        self.recovery_attempts: int = 0
        self.backoff_times: List[datetime] = []

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

    @staticmethod
    def handle_error(error_msg: str):
        """Handle errors by logging them and taking appropriate action"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Configure logging
        logging.basicConfig(
            filename="logs/app.log",
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
            force=True,  # Ensure configuration is applied
        )

        # Create detailed error message
        detailed_msg = f"""
        Error Details:
        Timestamp: {timestamp}
        Message: {error_msg}
        """

        # Log the error
        logging.error(detailed_msg)

        # Print to console for immediate visibility
        print(f"[{timestamp}] ERROR: {error_msg}")

        return False

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
