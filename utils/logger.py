import os
import logging

def get_logger(name) -> logging.Logger:
    """
    Create and return a configured logger.

    - Log level is set via the LOG_LEVEL environment variable (defaults to INFO).
    - Logs are output to the console with timestamps and levels.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        level_name = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, level_name, logging.INFO)
        logger.setLevel(level)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.propagate = False

    return logger
