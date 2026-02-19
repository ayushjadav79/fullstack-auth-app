import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Define path
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logger():
    logger = logging.getLogger("api_logger")
    logger.setLevel(logging.INFO)

    # "when='midnight'" creates a new file every day
    # "backupCount=7" keeps logs for the last 7 days
    handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, "backend.log"),
        when="midnight",
        interval=1,
        backupCount=7
    )

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
    
    return logger

logger = setup_logger()