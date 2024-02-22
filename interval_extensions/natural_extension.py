from function_evaluator import FunctionEvaluator
from mp_exp import exp, log, factorial


interval_operations = {'exp': exp, 'log': log, 'factorial': factorial}


def get_natural_extension(variables: dict, expr: str):
    return FunctionEvaluator(variables, expr, interval_operations)
