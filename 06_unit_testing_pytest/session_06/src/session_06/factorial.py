def factorial(x):
    if x < 0: raise ValueError("Cannot assert factorial of negative number!")
    if x <= 1: return 1 
    return x * factorial(x - 1)