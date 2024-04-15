import sympy


class FunctionEvaluator:
    def __init__(self, expr: str, variable_names, operations: dict):
        self.function = sympy.lambdify(list(variable_names), expr, modules=operations)

    def evaluate(self, variables: dict):
        return self.function(*list(variables.values()))
