import re
import json

NUMBER_PATTERN = re.compile(r'[0-9]*?.\.{0,1}[0-9e]+')


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return "Division by zero is not allowed."
    return x / y


def power(x, y):
    return x ** y


def root(x):
    if x < 0:
        return "Square root of negative number is not allowed."
    return power(x, 0.5)


def parse_input(ip):
    numbers = NUMBER_PATTERN.match(ip)


test_operations = {
    'add': add(5, 3),
    'subtract': subtract(5, 3),
    'multiply': multiply(5, 3),
    'divide': divide(5, 3),
    'divide_by_zero': divide(5, 0),
    'power': power(5, 3),
    'sqrt': root(25),
    'sqrt_negative': root(-25),
}

print(json.dumps(test_operations, indent=4))
