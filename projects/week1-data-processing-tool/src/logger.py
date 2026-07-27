import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str) -> logging.Logger:
    """
    Creates (or reuses) a logger with a given name.
    Every part of your project that needs to log something
    should call get_logger(__name__) to get one of these.
    """
    logger = logging.getLogger(name)

    # If this logger already has handlers attached, don't add more.
    # (Prevents duplicate log lines if get_logger() is called twice for the same name.)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    # Make sure a "logs" folder exists to write into
    os.makedirs("logs", exist_ok=True)

    # RotatingFileHandler: writes to a file, and automatically starts a
    # new file once the old one hits 5MB, keeping 3 old backups max.
    # This stops your log file from growing forever.
    handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=5_000_000,
        backupCount=3
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Also print to the console at the same time, so you still see
    # things live while developing, not just in the file.
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger
