import logging
import os
import sys
from datetime import datetime


class LogConfig:
    """Configuration class for logging settings."""

    LOG_DIR = "logs"
    LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
    LOG_LEVEL = logging.INFO


def configure_logging():
    """Configure logging with file and console handlers."""
    # Ensure logs directory exists
    if not os.path.exists(LogConfig.LOG_DIR):
        os.makedirs(LogConfig.LOG_DIR)

    # Configure logging
    logging.basicConfig(
        level=LogConfig.LOG_LEVEL,
        format=LogConfig.LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(
                os.path.join(
                    LogConfig.LOG_DIR, f'app_{datetime.now().strftime("%Y%m%d")}.log'
                )
            ),
        ],
    )


__all__ = [
    "configure_logging",
    "LogConfig",
]
