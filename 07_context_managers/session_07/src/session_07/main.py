import time
from contextlib import contextmanager

# The timer
@contextmanager
def timer():
    start = time.time()
    try:
        yield
    finally:
        print(f"\nExecution time: Printing {times_to_execute} took {time.time() - start:.2f} seconds!")

# The exception handler
@contextmanager
def exception_handler():
    try:
        yield
    except Exception as e:
        print(f"Error: {e}")
        pass # Keeps running code as if nothing happened at all
        
# DNT The main, defaulted, feature
class FileOpener:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        print(f"Opening file {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Closing file {self.filename}")
        if self.file:
            self.file.close()
        # Do not suppress exceptions
        return False
# DNT

# Usage example:
if __name__ == "__main__":
    with timer():  # Measure execution time
        with exception_handler():  # Handle exceptions
            with FileOpener("example.txt", "r") as f: # Forces an exception by making it a read-only file through the fileopener mode
                times_to_execute = 100_000 # Write x number lines
                for fileOpener in range(times_to_execute): f.write("The quick brown fox jumps over the lazy dog\n")

