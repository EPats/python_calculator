import re
import json

TOKEN_PATTERN = re.compile(r'(-?\b\w+[\.]?\w*\b|[+\-*/^()])')
OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, 'sqrt': 3}
DIVIDE_ZERO_ERROR_STRING = 'Division by zero is not allowed.'
NEGATIVE_ROOT_ERROR_STRING = 'Sqrt of negative number not allowed.'

def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return DIVIDE_ZERO_ERROR_STRING
    return x / y


def power(x, y):
    return x ** y


def root(x):
    if x < 0:
        return NEGATIVE_ROOT_ERROR_STRING
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
            return DIVIDE_ZERO_ERROR_STRING
        return left_value / right_value
    if node.value == '^':
        return left_value ** right_value
    if node.value == 'sqrt':
        if left_value < 0:
            return NEGATIVE_ROOT_ERROR_STRING
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
    ('5+3', 8),
    ('(3+4)*5', 35),
    ('3+4*5', 23),
    ('4/2', 2),
    ('8/9', 8/9),
    ('9/0', DIVIDE_ZERO_ERROR_STRING),
    ('(2+5)/(3-3)', DIVIDE_ZERO_ERROR_STRING),
    ('100/(3+2)', 20),
    ('3*(4+5)', 27),
    ('sqrt(25)', 5),
    ('sqrt(24)', root(24)),
    ('3^2', 9),
    ('3.2 * 2.5', 8),
    ('3+-2', 1),
    ('(2*-4)', -8),
    ('sqrt(-25)', NEGATIVE_ROOT_ERROR_STRING),
    ('5 + -3', 2),
    ('(-3+2)*(2+4)', -6),
    ('(-3)^2', 9),
    ('5', 5),
    ('-2', -2)
]
test_expressions_results = [{'expression': expr, 'passed': parse_and_eval(expr) == answer, 'expected': answer,
                             'received': parse_and_eval(expr)} for expr, answer in test_expressions]
print(json.dumps(test_expressions_results, indent=4))
print('\n\n')
all_correct = all([expr['passed'] for expr in test_expressions_results])
if all_correct:
    print('All tests passed')
else:
    print(f'{len(test_expressions_results) - sum([1 if expr["passed"] else 0 for expr in test_expressions_results])} tests failed')
    print(json.dumps([test for test in test_expressions_results if not test['passed']], indent=4))