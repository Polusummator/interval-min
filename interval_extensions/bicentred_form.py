from decimal import Decimal
from .helpers import calculate_centred_form, get_centre
from .interval_extension import IntervalExtension
from mp_exp import intersect, Interval
from .natural_extension import NaturalExtension


def cut(value, cut_interval):
    if value < cut_interval.a:
        return cut_interval.a
    if value > cut_interval.b:
        return cut_interval.b
    return value


class BicentredForm(IntervalExtension):
    def __init__(self, expr: str, variable_names, gradient_evaluator):
        self.extension = NaturalExtension(expr, variable_names)
        self.gradient_evaluator = gradient_evaluator(expr, variable_names)

    def evaluate(self, variables: dict):
        p_gradient = self.gradient_evaluator.evaluate(variables, get_centre(variables))
        p = self._get_p(p_gradient)

        centre = self._get_centre(variables, p, 1)
        gradient = self.gradient_evaluator.evaluate(variables, centre)
        lower_form = calculate_centred_form(variables, centre, gradient, self.extension)

        centre = self._get_centre(variables, p, -1)
        gradient = self.gradient_evaluator.evaluate(variables, centre)
        upper_form = calculate_centred_form(variables, centre, gradient, self.extension)

        return intersect(lower_form, upper_form)

    def _get_p(self, gradient):
        p = dict()
        for variable, interval in gradient.items():
            mid = interval.mid
            rad = interval.rad
            if rad == 0:
                p[variable] = 1  # if rad is 0, this value is not used
            else:
                p[variable] = cut(mid / rad, Interval(Decimal(-1), Decimal(1)))
        return p

    def _get_centre(self, variables: dict, p: dict, sign):
        centre = dict()
        for variable, interval in variables.items():
            centre[variable] = Interval.to_interval(interval.mid + p[variable] * interval.rad * sign)
        return centre
