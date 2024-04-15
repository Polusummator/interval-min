from .natural_extension import NaturalExtension
from .helpers import calculate_centred_form, get_centre
from .interval_extension import IntervalExtension
from mp_exp import Interval


class CentredForm(IntervalExtension):
    def __init__(self, expr: str, variable_names, gradient_evaluator):
        self.extension = NaturalExtension(expr, variable_names)
        self.gradient_evaluator = gradient_evaluator(expr, variable_names)

    def evaluate(self, variables: dict[str, Interval]) -> Interval:
        centre = get_centre(variables)
        gradient = self.gradient_evaluator.evaluate(variables, centre)
        return calculate_centred_form(variables, centre, gradient, self.extension)
