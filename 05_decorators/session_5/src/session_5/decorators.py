def log_calls(func):
    """A decorator that logs function call details."""
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    return a + b

print("Result of add:", add(3, 4))