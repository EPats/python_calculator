import re
import json
import math
import sympy as sym


TOKEN_PATTERN = re.compile(r'([a-zA-Z]+|\d*\.\d+|\d+|[+\-*/^()])')
NUMBER_PATTERN = re.compile(r'\d+(\.\d+)?')
OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
FUNCTIONS = ['sqrt', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan']
OPERATOR_PRECEDENCE.update({fn: 4 for fn in FUNCTIONS})
DIVIDE_ZERO_ERROR_STRING = 'Division by zero is not allowed.'
NEGATIVE_ROOT_ERROR_STRING = 'Sqrt of negative number not allowed.'


symbolic_output = True


def tokenise_input(expression):
    raw_tokens = TOKEN_PATTERN.findall(expression)
    processed_tokens = []

    for i, token in (token_iter := enumerate(raw_tokens)):
        if token == '-' and i + 1 < len(raw_tokens) and (i == 0 or raw_tokens[i - 1] in '+-*/^('):
            if NUMBER_PATTERN.match(raw_tokens[i + 1]):
                processed_tokens.append(f'-{raw_tokens[i + 1]}')
                next(token_iter, None)
            else:
                processed_tokens.append('-1')
                processed_tokens.append('*')
        elif token in ['(', 'sqrt'] and i > 0 and (NUMBER_PATTERN.match(raw_tokens[i - 1]) or raw_tokens[i - 1] == ')'):
            processed_tokens.append('*')
            processed_tokens.append(token)
        else:
            processed_tokens.append(token)

    return processed_tokens


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


# Helper function to evaluate an expression tree
def evaluate_tree_calc(node):
    if node is None:
        return 0

    # If leaf node, return its value
    if node.left is None and node.right is None:
        return float(node.value)

    left_value = evaluate_tree_calc(node.left)
    right_value = evaluate_tree_calc(node.right)

    # Perform the operation based on the operator in the node's value
    match node.value:
        case '+':
            return left_value + right_value
        case '-':
            return left_value - right_value
        case '*':
            return left_value * right_value
        case '/':
            if right_value == 0:
                return DIVIDE_ZERO_ERROR_STRING
            return left_value / right_value
        case '^':
            return left_value ** right_value
        case 'sqrt':
            if left_value < 0:
                return NEGATIVE_ROOT_ERROR_STRING
            return left_value ** 0.5
        case 'sin':
            return math.sin(left_value)
        case 'cos':
            return math.cos(left_value)
        case 'tan':
            return math.tan(left_value)
        case 'asin':
            return math.asin(left_value)
        case 'acos':
            return math.acos(left_value)
        case 'atan':
            return math.atan(left_value)


def evaluate_tree(node):
    if node is None:
        return 0

    # If leaf node, return its value
    if node.left is None and node.right is None:
        return float(node.value)

    left_value = evaluate_tree(node.left)
    right_value = evaluate_tree(node.right)

    # Perform the operation based on the operator in the node's value
    match node.value:
        case '+':
            return left_value + right_value
        case '-':
            return left_value - right_value
        case '*':
            return left_value * right_value
        case '/':
            if right_value == 0:
                return DIVIDE_ZERO_ERROR_STRING
            return left_value / right_value
        case '^':
            return left_value ** right_value
        case 'sqrt':
            if left_value < 0:
                return NEGATIVE_ROOT_ERROR_STRING
            return left_value ** 0.5
        case 'sin':
            return sym.sin(left_value)
        case 'cos':
            return sym.cos(left_value)
        case 'tan':
            return sym.tan(left_value)
        case 'asin':
            return sym.asin(left_value)
        case 'acos':
            return sym.acos(left_value)
        case 'atan':
            return sym.atan(left_value)

# Function to create an expression tree from a tokenized expression (infix notation)
def build_expression_tree(tokens):
    if 'sin' in tokens:
        print("hi")
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
            match token:
                case 'pi':
                    output.append(sym.pi)
                case 'e':
                    output.append(sym.e)
                case other:
                    output.append(token)

    while stack:
        output.append(stack.pop())

        # Build the expression tree from the output (postfix notation)
    for token in output:
        if token not in OPERATOR_PRECEDENCE:
            stack.append(Node(token))
        else:
            node = Node(token)
            if token in FUNCTIONS:  # Unary operator
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


# Test the expression tree building and evaluation
test_expressions = [
    ('-5+3', -2),
    ('5+3', 8),
    ('(3+4)*5', 35),
    ('3+4*5', 23),
    ('4/2', 2),
    ('8/9', 8 / 9),
    ('9/0', DIVIDE_ZERO_ERROR_STRING),
    ('(2+5)/(3-3)', DIVIDE_ZERO_ERROR_STRING),
    ('100/(3+2)', 20),
    ('3*(4+5)', 27),
    ('sqrt(25)', 5),
    ('sqrt(24)', 24 ** 0.5),
    ('-sqrt(25)', -5),
    ('3^2', 9),
    ('3.2 * 2.5', 8),
    ('3+-2', 1),
    ('(2*-4)', -8),
    ('sqrt(-25)', NEGATIVE_ROOT_ERROR_STRING),
    ('5 + -3', 2),
    ('(-3+2)*(2+4)', -6),
    ('(-3)^2', 9),
    ('5', 5),
    ('-2', -2),
    ('(3+2)(4*2)', 40),
    ('4(2+3)', 20),
    ('(2+3)-(1+2)', 2),
    ('7sqrt(25)', 35),
    ('sin(0)', 0),
    ('cos(0)', 1),
    ('tan(0)', 0),
    ('pi', sym.pi),
    ('cos(pi)', -1),
    ('cos(pi/2)', 0)
]
test_expressions_results = [{'expression': expr, 'tokens': tokenise_input(expr),
                             'passed': parse_and_eval(expr) == answer, 'expected': answer,
                             'received': parse_and_eval(expr)} for expr, answer in test_expressions]
serialisable_test_expressions = [{'expression': key['expression'], 'tokens': key['tokens'], 'passed': key['passed'],
                                  'expected': sym.N(key['expected']) if isinstance(key['expected'], sym.Basic) else key['expected'],
                                  'received': sym.N(key['received']) if isinstance(key['received'], sym.Basic) else key['received']}
                                  for key in test_expressions_results]
print(json.dumps(serialisable_test_expressions, indent=4))
print('\n\n')
all_correct = all([expr['passed'] for expr in test_expressions_results])
if all_correct:
    print('All tests passed')
else:
    print(
        f'{len(test_expressions_results) - sum([1 if expr["passed"] else 0 for expr in test_expressions_results])}'
        f' tests failed')
    print(json.dumps({i: test for i, test in enumerate(serialisable_test_expressions) if not test['passed']}, indent=4))

print(math.cos(math.pi/2))
print(sym.sqrt(8))