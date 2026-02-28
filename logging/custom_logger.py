"""
custom_logger.py
-----------------
Provides a reusable logger for the entire project.
"""

import logging
import sys


def get_logger(name: str, level=logging.DEBUG) -> logging.Logger:
    """Return a configured logger with console output."""

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
