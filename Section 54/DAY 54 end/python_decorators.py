import time

def add(n1, n2):
    """Add two numbers."""
    return n1 + n2

def subtract(n1, n2):
    """Subtract the second number from the first number."""
    return n1 - n2

def multiply(n1, n2):
    """Multiply two numbers."""
    return n1 * n2

def divide(n1, n2):
    """Divide the first number by the second number, with error handling for division by zero."""
    if n2 == 0:
        raise ValueError("Cannot divide by zero.")
    return n1 / n2

def calculate(calc_function, n1, n2):
    """Perform a calculation using the provided function and two numbers."""
    return calc_function(n1, n2)

# Testing the calculation functions
result = calculate(add, 2, 3)
print(f"Result of addition: {result}")

# Function nesting example
def outer_function():
    """Demonstrates nested functions."""
    print("I'm outer")

    def nested_function():
        print("I'm inner")

    nested_function()

outer_function()

# Function returning example
def outer_function_with_return():
    """Returns a nested function."""
    print("I'm outer")

    def nested_function():
        print("I'm inner")

    return nested_function

# Obtain and call the inner function
inner_function = outer_function_with_return()
inner_function()

# Simple Python Decorator Function
def delay_decorator(function):
    """Decorator to add a delay before executing the decorated function."""
    def wrapper_function(*args, **kwargs):
        time.sleep(2)
        # Do something before
        function(*args, **kwargs)
        # Do something after
    return wrapper_function

@delay_decorator
def say_hello():
    """Print a hello message."""
    print("Hello")

@delay_decorator
def say_bye():
    """Print a goodbye message."""
    print("Bye")

def say_greeting():
    """Print a greeting message."""
    print("How are you?")

# Applying the decorator manually
decorated_say_greeting = delay_decorator(say_greeting)
decorated_say_greeting()