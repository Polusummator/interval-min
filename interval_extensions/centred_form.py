from interval_extensions import get_natural_extension
from .differentiation import get_gradient_evaluator


class CentredForm:
    def __init__(self, variables: dict, expr: str):
        self.extension = get_natural_extension(variables, expr)
        self.gradient_evaluator = get_gradient_evaluator(variables, expr)

    def evaluate(self, variables: dict):
        dot = dict()
        for variable, interval in variables.items():
            dot[variable] = interval.mid_interval

        result = self.extension.evaluate(dot)
        gradient = self.gradient_evaluator.evaluate(variables)
        for variable, interval in variables.items():
            result += gradient[variable] * (variables[variable] - dot[variable])
        return result


def get_centred_form(variables: dict, expr: str):
    return CentredForm(variables, expr)
