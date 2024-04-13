import sympy

from mp_exp import Interval
from .natural_extension import NaturalExtension


class SympyGradientEvaluator:
    def __init__(self, variables: dict, expr: str):
        self.gradient = dict()
        for variable in variables:
            derivative = sympy.diff(expr, variable)
            self.gradient[variable] = NaturalExtension(variables, derivative)

    def evaluate(self, variables: dict, *args) -> dict[str, Interval]:
        return {variable: Interval.to_interval(self.gradient[variable].evaluate(variables)) for variable in variables}
