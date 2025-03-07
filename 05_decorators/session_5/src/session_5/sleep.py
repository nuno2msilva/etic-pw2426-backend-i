import time
import logging
import sys
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

def audit(func):
    def wrapper():
        logger.info(f"start at {datetime.now()}")
        result=func()
        logger.info(f"finish at {datetime.now()}")
        return result
    return wrapper

@ audit
def wait():
    time.sleep(1)

if __name__ == "__main__":
    wait()