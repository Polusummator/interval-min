from .function_evaluator import FunctionEvaluator
from .interval_extension import IntervalExtension
from mp_exp import exp, log, factorial


interval_operations = {'exp': exp, 'log': log, 'factorial': factorial}


class NaturalExtension(IntervalExtension):
    def __init__(self, variables, expr: str, gradient_evaluator = None):
        self.extension = FunctionEvaluator(variables, expr, interval_operations)

    def evaluate(self, variables):
        return self.extension.evaluate(variables)
