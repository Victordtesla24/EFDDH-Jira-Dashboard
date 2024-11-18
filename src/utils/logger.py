import logging
import os
from datetime import datetime
from typing import Optional, Union

import pandas as pd


class CustomLogger(logging.Logger):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        
    def data_validation(self, msg: str, data: Optional[pd.DataFrame] = None) -> None:
        """Custom method for data validation logging."""
        if data is not None and isinstance(data, pd.DataFrame):
            msg = f"{msg}\nData Shape: {data.shape}\nColumns: {data.columns.tolist()}"
        self.info(msg)


def setup_logger() -> logging.Logger:
    """
    Configure and return a logger instance for the application.

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Configure logging with more detailed format
    log_filename = f'logs/dashboard_{datetime.now().strftime("%Y%m%d")}.log'

    # Create file handler
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Get logger
    logger = CustomLogger(__name__)
    logger.setLevel(logging.INFO)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Add data validation logging
    logger.data_validation = logger.data_validation

    return logger


# Create logger instance
logger = setup_logger()

# Export logger
__all__ = ["logger"]
