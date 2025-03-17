from contextlib import contextmanager


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
        # print(f"Closing file {self.filename}")
        if self.file:
            self.file.close()
        # Do not suppress exceptions
        return False

# Usage example:
if __name__ == "__main__":
    with FileOpener("example.txt", "w") as f:
        f.write("Hello, Context Managers!")

@contextmanager
def open_file(filename, mode):
    # print(f"Opening file {filename}")
    f = open(filename, mode)
    try:
        yield f
    finally:
        print(f"Closing file {filename}")
        f.close()

# Usage example:
if __name__ == "__main__":
    with open_file("example.txt", "a") as f:
        f.write("\nAppending with context manager using @contextmanager.")