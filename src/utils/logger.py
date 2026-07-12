import logging   #Its job is to record messages while the program is running.
from logging.handlers import RotatingFileHandler #Prevents log files from growing forever by rotating them automatically
from pathlib import Path  #Lets us build file paths that work on Windows, Linux, and macOS.

from src.config.settings import PROJECT_ROOT

LOG_DIR = PROJECT_ROOT / "logs"  # / Join folders together
LOG_FILE = LOG_DIR / "app.log"

DEFAULT_LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name: str) -> logging.Logger:
    """
    Create and configure a logger for a specific module.

    The logger writes messages to:
    1. The terminal.
    2. A rotating log file located at logs/app.log.

    Args:
        name: The name of the module requesting the logger.
              Usually, __name__ should be passed.

    Returns:
        A configured logging.Logger instance.
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)  #make direction 
    #Make sure the logs folder exists. If it doesn't, create it. If it does exist, don't consider it an error and continue running the program.

    logger = logging.getLogger(name)
    logger.setLevel(DEFAULT_LOG_LEVEL)

    # Prevent the same log message from being handled more than once.
    logger.propagate = False

    # Avoid adding duplicate handlers when get_logger is called repeatedly.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(DEFAULT_LOG_LEVEL)
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(DEFAULT_LOG_LEVEL)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger