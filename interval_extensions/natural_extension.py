from .function_evaluator import FunctionEvaluator
from .interval_extension import IntervalExtension
from mp_exp import exp, log, factorial


interval_operations = {'exp': exp, 'log': log, 'factorial': factorial}


class NaturalExtension(IntervalExtension):
    def __init__(self, expr: str, variable_names, gradient_evaluator = None):
        self.extension = FunctionEvaluator(expr, variable_names, interval_operations)

    def evaluate(self, variables):
        return self.extension.evaluate(variables)
