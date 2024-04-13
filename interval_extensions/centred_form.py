from .natural_extension import NaturalExtension
from .helpers import calculate_centred_form
from .interval_extension import IntervalExtension
from mp_exp import Interval


class CentredForm(IntervalExtension):
    def __init__(self, variables: dict, expr: str, gradient_evaluator):
        self.extension = NaturalExtension(variables, expr)
        self.gradient_evaluator = gradient_evaluator(variables, expr)

    def evaluate(self, variables: dict[str, Interval]) -> Interval:
        centre = dict()
        for variable, interval in variables.items():
            centre[variable] = interval.mid_interval

        gradient = self.gradient_evaluator.evaluate(variables, centre)
        return calculate_centred_form(variables, centre, gradient, self.extension)
