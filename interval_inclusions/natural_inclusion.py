from mp_exp import exp, log, factorial
from .function_evaluator import FunctionEvaluator
from .interval_inclusion import IntervalInclusion

interval_operations = {'exp': exp, 'log': log, 'factorial': factorial}


class NaturalInclusion(IntervalInclusion):
    def __init__(self, expr: str, variable_names, gradient_evaluator=None):
        """
        Parameters
        ----------
        expr : str
            The expression to be evaluated.
        variable_names : list
            A list of variable names.
        gradient_evaluator:
            Is not used in natural inclosure.
        """

        self.inclosure = FunctionEvaluator(expr, variable_names, interval_operations)

    def evaluate(self, variables):
        return self.inclosure.evaluate(variables)
