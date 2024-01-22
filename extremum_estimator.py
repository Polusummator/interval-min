import sympy
from decimal import Decimal

from mp_exp import set_precision
from mp_exp.interval_arithmetics import *

from natural_extension import NaturalExtension
from optimization_methods import ExtremumType
from optimization_methods import MooreSkelboe

METHODS = {"moore_skelboe": MooreSkelboe}
EXTENSIONS = {"natural": NaturalExtension}
EXTREMUM_TYPES = {"max": ExtremumType.MAX, "min": ExtremumType.MIN}


def get_extremum_estimation(func: str, func_args: dict, extremum_type: str = "min",
                            precision: Decimal = Decimal("0.000001"), extension: str = "natural",
                            method: str = "moore_skelboe"):
    """Estimates interval for a given function with a given precision

    Parameters
    ----------
    func : str
        function to be evaluated
    func_args : dict
        A dictionary containing variable strings and corresponding intervals
    extremum_type : str
        Should be one of 'min', 'max'
    precision : int:
        The least needed precision
    extension : str
        An interval extension to use for estimation. Should be one of 'natural
    method : str
        A method to use for estimation. Should be one of 'moore_skelboe'

    Returns
    -------
    point where maximum/minimum is reached
    """

    set_precision(-precision.as_tuple().exponent + 1)
    #     TODO: Set a number of Taylor's series terms based on precision

    interval_extension = _parse_extension_type(extension)(_parse_function(func))
    extremum_type = _parse_extremum_type(extremum_type)
    method_obj = _parse_method(method)(func_args, interval_extension, precision, extremum_type)
    return method_obj.calculate()


def _parse_extremum_type(extremum_type: str) -> ExtremumType:
    if extremum_type in EXTREMUM_TYPES:
        return EXTREMUM_TYPES[extremum_type]
    raise SyntaxError("Unexpected argument given as an extremum type")


def _parse_extension_type(extension: str):
    if extension in EXTENSIONS:
        return EXTENSIONS[extension]
    raise SyntaxError("Unexpected argument given as an extension type")


def _parse_method(method: str):
    if method in METHODS:
        return METHODS[method]
    raise SyntaxError("Unexpected argument given as a method")


def _parse_function(func: str):
    expr = sympy.parse_expr(func, evaluate=False)
    return expr


if __name__ == '__main__':
    f = "x**2 + 1"
    res = get_extremum_estimation(f, {sympy.Symbol("x"): Interval(Decimal(-2), Decimal(100))}, "min")
    print(res)
