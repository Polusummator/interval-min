import sympy

from mp_exp import Interval
from interval_extensions.natural_extension import NaturalExtension
from .slope_evaluator import SlopeEvaluator


class SympyGradientEvaluator(SlopeEvaluator):
    def __init__(self, expr: str, variable_names):
        self.gradient = dict()
        for variable_name in variable_names:
            derivative = sympy.diff(expr, variable_name)
            self.gradient[variable_name] = NaturalExtension(derivative, variable_names)

    def evaluate(self, variables: dict, point=None) -> dict[str, Interval]:
        return {variable: Interval.to_interval(self.gradient[variable].evaluate(variables)) for variable in variables}
