import sympy


class IntervalExtension:
    def __init__(self, variables: dict, expr: str):
        self.function = sympy.lambdify(list(variables.keys()), expr)

    def evaluate(self, variables: dict):
        return self.function(*list(variables.values()))
