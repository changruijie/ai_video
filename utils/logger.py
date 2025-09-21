from loguru import logger
import sys, os

LOG_DIR = os.path.join("data", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(os.path.join(LOG_DIR, "app.log"), rotation="10 MB", retention="7 days")

__all__ = ["logger"]
