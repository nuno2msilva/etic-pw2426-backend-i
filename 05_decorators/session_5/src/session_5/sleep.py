import time
import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(filename)s@%(lineno)d - %(funcName)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

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