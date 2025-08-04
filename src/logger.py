import logging


def setup_logging(
    name: str = "src",
    level: int = logging.INFO,
    log_format: str = "%(asctime)s - %(levelname)s - %(message)s",
    log_file: str | None = "logs.txt",
) -> logging.Logger:
    """
    Basic logging configuration with console output and optional file logging.

    Args:
        name: Logger name (default "src")
        level: Logging level (default INFO)
        log_format: Format string for log messages
        log_file: Optional path to log file (default "logs.text")

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Console handler (always added)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
