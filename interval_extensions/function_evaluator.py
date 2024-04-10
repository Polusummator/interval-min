import sympy


class FunctionEvaluator:
    def __init__(self, variables: dict, expr: str, operations: dict):
        self.function = sympy.lambdify(list(variables.keys()), expr, modules=operations)

    def evaluate(self, variables: dict):
        return self.function(*list(variables.values()))
