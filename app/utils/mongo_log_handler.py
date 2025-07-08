import logging
from datetime import datetime
import pytz
from app.configs.config import timezone
from app.db.mongo import db 

class MongoLogHandler(logging.Handler):
    def __init__(self, collection_name="logs"):
        super().__init__()
        self.collection = db[collection_name]
        self.timezone = pytz.timezone(timezone)

    def emit(self, record):
        try:
            log_entry = {
                "message": self.format(record),
                "level": record.levelname,
                "timestamp": datetime.now(self.timezone),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }
            self.collection.insert_one(log_entry)
        except Exception as e:
            print(f"MongoLogHandler Error: {e}")
