import sympy
from functools import reduce

from mp_exp import log, exp


def add(a, b):
    return a + b


def mul(a, b):
    return a * b


def pow(a, b):
    return a ** b


class NaturalExtension:
    def __init__(self, expr):
        self._expr = expr

    def evaluate(self, variables):
        return self._rec(self._expr, variables)

    def _rec(self, expr, variables) -> list:
        if isinstance(expr, sympy.Integer):
            return [expr]
        if isinstance(expr, sympy.Symbol):
            return variables[expr]
        arguments = [self._rec(argument, variables) for argument in expr.args]
        if isinstance(expr, sympy.Add):
            return reduce(add, arguments)
        if isinstance(expr, sympy.Mul):
            return reduce(mul, arguments)
        if isinstance(expr, sympy.Pow):
            return pow(*arguments)
        if isinstance(expr, sympy.log):
            return log(arguments[0])
        if isinstance(expr, sympy.exp):
            return exp(arguments[0])
