"""Logging module"""
import logging
from typing import Dict


logging_levels: Dict[int, int] = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


def set_logging(verbosity: int) -> None:
    """
    Set the logging level to display to user based on requested verbosity level
    Args:
        verbosity: requested verbosity level

    Returns:
        Void
    """
    min_v = min(logging_levels.keys())
    max_v = max(logging_levels.keys())
    verbosity = min_v if verbosity < min_v else verbosity
    verbosity = max_v if verbosity > max_v else verbosity
    logging.basicConfig(level=logging_levels[verbosity])
