import logging
from pathlib import Path

def setup_logger(name="ragbot") -> logging.Logger:
  logger = logging.getLogger(name)
  logger.setLevel(logging.DEBUG)

  # Formatter
  formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")

  if not logger.hasHandlers():
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

  return logger

logger = setup_logger()
