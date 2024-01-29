from dataclasses import dataclass
import operator
import sympy

import mp_exp
from tree import BinaryNode, ConstNode, VariableNode, UnaryNode


def _get_tree(expr, elementary_func):
    """Convert sympy tree to Node tree

    Parameters
    ----------
    expr
        sympy expression
    elementary_func
        dataclass that provides elementary operations
    """

    func = None
    arguments = [_get_tree(argument, elementary_func) for argument in expr.args]
    match expr:
        case sympy.Symbol():
            return VariableNode(str(expr))
        case sympy.Integer():
            return ConstNode(elementary_func.convert_to_interval, int(expr))
        case sympy.Float():
            return ConstNode(elementary_func.convert_to_interval, float(expr))
        case sympy.log():
            return UnaryNode(elementary_func.log, arguments[0])
        case sympy.exp():
            return UnaryNode(elementary_func.exp, arguments[0])
        case sympy.factorial():
            return UnaryNode(elementary_func.factorial, arguments[0])
        case sympy.Add():
            func = operator.add
        case sympy.Mul():
            func = operator.mul
        case sympy.Pow():
            func = operator.pow
    return BinaryNode(func, arguments)


@dataclass
class IntervalElementaryFunc:
    log = mp_exp.log
    exp = mp_exp.exp
    factorial = mp_exp.factorial
    convert_to_interval = mp_exp.convert_to_interval


def get_interval_tree(expr):
    return _get_tree(expr, IntervalElementaryFunc)
