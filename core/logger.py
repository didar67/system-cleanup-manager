import logging
from logging import Logger
import os

def get_logger(log_file: str, log_level: str = 'INFO') -> Logger:
    """
    Creates and returns a logger with both file and console handlers.

    :param log_file: Path to the log file.
    :param log_level: Logging level as string (e.g., 'INFO', 'DEBUG').
    :return: Configured logger object.
    """

    # Convert level string to logging level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    # Create a logger instance
    logger = logging.getLogger("system_cleaner")
    logger.setLevel(numeric_level)
    
    # Avoid adding handlers multiple times (important when reused)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create log directory if not exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # File Handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(numeric_level)
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_format = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    return logger
