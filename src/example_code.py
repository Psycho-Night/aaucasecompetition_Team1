def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def buggy_function(x):
    return x / 0 


def another_function( a ,b ):
    return a+b


def faulty_logic(a, b):
    if a > b:
        return b - a  
    return a - b