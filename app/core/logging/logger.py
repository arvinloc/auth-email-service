import logging
import sys
from decouple import config

LOG_LEVEL = config("LOG_LEVEL", default="INFO")

# сетап логгера


def setup_logging() -> None:
    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

# функция для подключения логгера


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
