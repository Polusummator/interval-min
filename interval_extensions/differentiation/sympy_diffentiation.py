import sympy

from interval_extensions import get_natural_extension


class SympyGradientEvaluator:
    def __init__(self, variables: dict, expr: str):
        self.gradient = dict()
        for variable in variables:
            derivative = sympy.diff(expr, variable)
            self.gradient[variable] = get_natural_extension(variables, derivative)

    def evaluate(self, variables: dict) -> dict:
        return {variable: self.gradient[variable].evaluate(variables) for variable in variables}


def get_gradient_evaluator(variables: dict, expr: str):
    return SympyGradientEvaluator(variables, expr)
