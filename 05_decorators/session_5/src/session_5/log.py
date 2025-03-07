import logging
import sys
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

def audit(func: callable):
    def wrapper():
        logger.info(f"start at {datetime.now()}")
        yield func
        logger.info(f"finish at {datetime.now()}")
    return wrapper