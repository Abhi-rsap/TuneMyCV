import logging
from app.utils.mongo_log_handler import MongoLogHandler

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

    mongo_handler = MongoLogHandler()
    mongo_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(mongo_handler)
