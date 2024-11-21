"""Centralized logging configuration."""

import logging

from streamlit.logger import get_logger


def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        name: Name of the logger instance

    Returns:
        Configured logger instance
    """
    logger = get_logger(name)

    # Clear existing handlers
    logger.handlers.clear()

    # Add stream handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Initialize default logger
logger = setup_logger(__name__)
