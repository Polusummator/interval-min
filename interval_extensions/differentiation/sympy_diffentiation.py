import sympy

from interval_extensions import get_natural_extension
from mp_exp import Interval


class SympyGradientEvaluator:
    def __init__(self, variables: dict, expr: str):
        self.gradient = dict()
        for variable in variables:
            derivative = sympy.diff(expr, variable)
            self.gradient[variable] = get_natural_extension(variables, derivative)

    def evaluate(self, variables: dict, *args) -> dict:
        return {variable: Interval.to_interval(self.gradient[variable].evaluate(variables)) for variable in variables}
