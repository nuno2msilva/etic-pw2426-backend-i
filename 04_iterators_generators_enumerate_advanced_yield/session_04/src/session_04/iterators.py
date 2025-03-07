class EvenIterator:
    def __init__(self, numbers):
        self.numbers = numbers
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        # Use enumerate-like behaviour to track index and value
        while self.index < len(self.numbers):
            num = self.numbers[self.index]
            self.index += 1
            if num % 2 == 0:
                return num
        raise StopIteration

# Using enumerate to show index-value pairs
items = ['apple', 'banana', 'cherry']
for index, item in enumerate(items):
    print(f"Index {index}: {item}")

def fibonacci(n):
    """Yield the Fibonacci sequence up to n terms.
    
    'yield' pauses the function saving its state, and produces a value
    on each iteration. This is memory efficient for large sequences.
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Tutorial snippet: Generate and print first 10 Fibonacci numbers
for num in fibonacci(10):
    print("Fibonacci number:", num)    