from decimal import Decimal

import sympy

from helpers import get_scale
from interval_extensions import NaturalExtension, CentredForm, BicentredForm, SympyGradientEvaluator, \
    ForwardSlopeEvaluator
from mp_exp import set_precision, Interval
from optimization_methods import MooreSkelboe

METHODS = {"moore_skelboe": MooreSkelboe}
EXTENSIONS = {"natural": NaturalExtension,
              "centred_form": CentredForm,
              "bicentred_form": BicentredForm}
DIFFS = {"sympy_forward_mode": SympyGradientEvaluator,
         "slopes_forward_mode": ForwardSlopeEvaluator}


def get_extremum_estimation(func: str, func_args: dict[str, Interval], extremum_type: str = "min",
                            precision: Decimal = Decimal("0.000001"), extension: str = "natural",
                            method: str = "moore_skelboe",
                            diff: str = "sympy_forward_mode") -> Decimal:
    """Estimate interval for a given function with a given precision

    Parameters
    ----------
    func : str
        function to be evaluated
    func_args : dict[str, Interval]
        A dictionary containing variable strings and corresponding intervals
    extremum_type : str
        Should be one of 'min', 'max'
    precision : int
        The least needed precision
    extension : str
        An interval extension to use for estimation. Should be one of 'natural
    method : str
        A method to use for estimation. Should be one of 'moore_skelboe'
    diff : str
        A differentiation method to use in centred/bicentred form. Should be one of 'sympy_forward_mode'

    Returns
    -------
    point where maximum/minimum is reached
    """

    calculation_scale = get_scale(precision)
    set_precision(calculation_scale + 5)
    #     TODO: Set a number of Taylor's series terms based on precision

    parsed_function = _parse_function(func)
    interval_extension = _parse_extension_type(extension)(func_args, parsed_function, DIFFS[diff])
    extremum_type = _parse_extremum_type(extremum_type)
    method_obj = _parse_method(method)(func_args, interval_extension, precision, extremum_type)

    if not parsed_function.free_symbols:
        return Decimal(str(parsed_function.evalf(calculation_scale)))

    variable_interval = method_obj.calculate()
    return interval_extension.evaluate(variable_interval).a


def _parse_extremum_type(extremum_type: str) -> str:
    if extremum_type == "min" or extremum_type == "max":
        return extremum_type
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
