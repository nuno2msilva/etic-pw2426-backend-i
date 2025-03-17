import time
import logging
import sys
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format=" %(asctime)s - LEVEL: [%(levelname)s] - FILE: %(filename)s @ LINE %(lineno)d - FUNCTION: %(funcName)s - MESSAGE: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def audit(func):
    def wrapper(*args, **kwargs):
        
        start_time = time.time()
        logger.info(f"START @ {datetime.now()}")

        result = func(*args, **kwargs)
        
        finish_time = time.time()
        logger.info(f"FINISH @ {datetime.now()}")

        processing_time = finish_time - start_time
        logger.info(f"TOTAL TIME {processing_time:.4f} SECONDS")
        
        return result
    return wrapper

def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@audit
@log_calls
def add(a, b):
    return a + b

print("Result of add:", add(3, 4))