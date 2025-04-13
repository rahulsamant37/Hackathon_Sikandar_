"""
Logging configuration for the application.
"""

import logging
import sys
from typing import List

from app.core.config import settings

# Define log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Define log levels
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

def setup_logging():
    """
    Set up logging configuration.
    """
    # Get log level from settings
    log_level = LOG_LEVELS.get(settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log"),
        ],
    )
    
    # Set log levels for specific loggers
    loggers = [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "supabase",
        "langchain",
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
    
    # Create application logger
    logger = logging.getLogger("app")
    logger.setLevel(log_level)
    
    return logger

# Create application logger
logger = setup_logging()
