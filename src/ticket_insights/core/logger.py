import os
import logging

def get_logger(name) -> logging.Logger:
    """
    Create and return a configured logger.

    Args:
        name: Name of the logger.

    Returns:
        logging.Logger: Configured logger instance with console handler,
        formatted output, and level set from LOG_LEVEL environment variable.
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
