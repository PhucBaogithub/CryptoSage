"""Logging configuration for the trading system."""

import sys
from pathlib import Path

from loguru import logger


def setup_logger(
    name: str,
    log_level: str = "INFO",
    log_file: str = "logs/trading.log",
    rotation: str = "500 MB",
    retention: str = "10 days",
):
    """Setup logger with file and console handlers.

    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        rotation: Log rotation policy
        retention: Log retention policy

    Returns:
        Logger instance
    """
    # Remove default handler
    logger.remove()

    # Create log directory if it doesn't exist
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Console handler
    logger.add(
        sys.stdout,
        format="<level>{time:YYYY-MM-DD HH:mm:ss}</level> | <level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # File handler
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation=rotation,
        retention=retention,
    )

    logger.info(f"Logger initialized: {name}")
    return logger


def get_logger(name: str):
    """Get logger instance.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)

