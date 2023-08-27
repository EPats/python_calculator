import re
import json

TOKEN_PATTERN = re.compile(r'(\b\w+[\.]?\w*\b|[+\-*/^()])')
OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'sqrt': 3}

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


def tokenise_input(expression):
    return TOKEN_PATTERN.findall(expression)


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Helper function to evaluate an expression tree
def evaluate_tree(node):
    if node is None:
        return 0

    # If leaf node, return its value
    if node.left is None and node.right is None:
        return float(node.value)

    left_value = evaluate_tree(node.left)
    right_value = evaluate_tree(node.right)

    # Perform the operation based on the operator in the node's value
    if node.value == '+':
        return left_value + right_value
    if node.value == '-':
        return left_value - right_value
    if node.value == '*':
        return left_value * right_value
    if node.value == '/':
        if right_value == 0:
            return "Division by zero."
        return left_value / right_value
    if node.value == '^':
        return left_value ** right_value
    if node.value == 'sqrt':
        if left_value < 0:
            return "Square root of negative number."
        return left_value ** 0.5


# Function to create an expression tree from a tokenized expression (infix notation)
def build_expression_tree(tokens):
    stack = []
    output = []

    for token in tokens:
        if token in OPERATOR_PRECEDENCE:
            while (stack and stack[-1] in OPERATOR_PRECEDENCE and
                   OPERATOR_PRECEDENCE[token] <= OPERATOR_PRECEDENCE[stack[-1]]):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:  # Operand
            output.append(token)

    while stack:
        output.append(stack.pop())

        # Build the expression tree from the output (postfix notation)
    for token in output:
        if token not in OPERATOR_PRECEDENCE:
            stack.append(Node(token))
        else:
            node = Node(token)
            if token == 'sqrt':  # Unary operator
                node.left = stack.pop()
            else:  # Binary operator
                node.right = stack.pop()
                node.left = stack.pop()
            stack.append(node)

    return stack[0] if stack else None


def parse_and_eval(expression):
    tokens = tokenise_input(expression)
    root = build_expression_tree(tokens)
    return evaluate_tree(root)


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
# Test the expression tree building and evaluation
test_expressions = [
    '5+3',
    '(3+4)*5',
    '3+4*5',
    '4/2',
    '8/9',
    '9/0',
    '(2+5)/(3-3)',
    '100/(3+2)',
    '3*(4+5)',
    'sqrt(25)',
    'sqrt(24)',
    '3^2',
    '3.2 * 2.5'
]
test_expressions_results = {expr: parse_and_eval(expr) for expr in test_expressions}
print(json.dumps(test_expressions_results, indent=4))