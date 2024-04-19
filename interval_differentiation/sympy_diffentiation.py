import sympy

from interval_inclusions.natural_inclusion import NaturalInclusion
from mp_exp import Interval
from .slope_evaluator import SlopeEvaluator


class SympyGradientEvaluator(SlopeEvaluator):
    """
    Evaluates interval derivatives using sympy.diff function.

    Differentiation is performed during __init__.
    """

    def __init__(self, expr: str, variable_names):
        self.gradient = dict()
        for variable_name in variable_names:
            derivative = sympy.diff(expr, variable_name)
            self.gradient[variable_name] = NaturalInclusion(derivative, variable_names)

    def evaluate(self, variables: dict, point=None) -> dict[str, Interval]:
        return {variable: Interval.to_interval(self.gradient[variable].evaluate(variables)) for variable in variables}
