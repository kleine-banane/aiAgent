import ast
import operator

operations = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow}

def calculate(expression):
    node = ast.parse(expression, mode='eval').body
    return evaluate(node)

def evaluate(node):
    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        op = operations[type(node.op)]
        left = evaluate(node.left)
        right = evaluate(node.right)
        return op(left, right)
    else:
        raise TypeError(node)

if __name__ == "__main__":
    expression = "3 + 7 * 2"
    result = calculate(expression)
    print(result)