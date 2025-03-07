def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

def printFibonacci(n):
    for num in fibonacci(n):
        print("Fibonacci number:", num)

printFibonacci(10)