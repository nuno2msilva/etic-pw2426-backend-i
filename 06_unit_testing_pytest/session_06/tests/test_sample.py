import pytest
from session_06 import sum, multiply, factorial

# Sum tests
def test_sum_two_with_three():
    assert sum(2, 3) == 5

def test_sum_negative_one_with_one():
    assert sum(-1, 1) == 0

# Multipy tests
def test_multiply_two_with_five():
    assert multiply(2,5) == 10

def test_multiply_negative_two_with_five():
    assert multiply(-2,5) == -10

# Factorial tests
def test_error_for_factorial_of_negative_one():
    with pytest.raises(ValueError,match="Cannot assert factorial of negative number!"): assert factorial(-1)

def test_factorial_of_seven():
    assert factorial(7) == 5040