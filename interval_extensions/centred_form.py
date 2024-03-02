from interval_extensions import get_natural_extension
from interval_extensions.helpers import calculate_centred_form


class CentredForm:
    def __init__(self, variables: dict, expr: str, gradient_evaluator):
        self.extension = get_natural_extension(variables, expr)
        self.gradient_evaluator = gradient_evaluator(variables, expr)

    def evaluate(self, variables: dict):
        centre = dict()
        for variable, interval in variables.items():
            centre[variable] = interval.mid_interval

        gradient = self.gradient_evaluator.evaluate(variables)
        return calculate_centred_form(variables, centre, gradient, self.extension)
