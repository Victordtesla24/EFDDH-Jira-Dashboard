"""Centralized logging configuration."""
import logging
import os
from datetime import datetime
from typing import Optional

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    
    # Only add handlers if they don't exist
    if not logger.handlers:
        # Configure logging format and handlers
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # File handler
        log_file = f'logs/dashboard_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.setLevel(logging.DEBUG)
    
    return logger

# Create default logger instance
logger = setup_logger("jira_dashboard")
