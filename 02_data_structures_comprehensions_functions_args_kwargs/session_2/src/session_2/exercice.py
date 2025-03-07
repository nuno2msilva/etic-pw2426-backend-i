# Exercise
# 
# Write a function that accepts any number of numeric arguments (using *args) and returns their sum. 
# Then, write another function using **kwargs to filter a dictionary for values above a specified threshold.
# 
# Challenge
# 
# Develop a mini user registration system that:
# Uses comprehensions to manage users.
# Accepts dynamic user details via *args and **kwargs.


def sum_it_up(*args):
    total = sum(args)
    return total

print(f"The total is: {sum_it_up(1,2,3)}")

