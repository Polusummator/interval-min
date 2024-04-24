from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_UP

import mp_exp as ia
from mp_exp import Interval, set_precision


def exp(x: Interval) -> Interval:
    precision = getcontext().prec
    is_edge_case, lower_bound = _exp_edge_cases_check(x.a)
    if not is_edge_case:
        lower_bound = _precise_calc(x.a, lambda a: a.exp(), precision, ROUND_DOWN)

    is_edge_case, upper_bound = _exp_edge_cases_check(x.b)
    if not is_edge_case:
        upper_bound = _precise_calc(x.b, lambda a: a.exp(), precision, ROUND_UP)

    return Interval(lower_bound, upper_bound)


def _exp_edge_cases_check(x: Decimal) -> tuple[bool, Decimal]:
    """Returns if edge case is present for exp function and result value"""

    if x == ia.c_zero:
        return True, ia.c_one
    if x == ia.c_minf:
        return True, ia.c_zero
    if x == ia.c_inf:
        return True, ia.c_inf
    return False, ia.c_zero


def log(x: Interval) -> Interval:
    precision = getcontext().prec
    is_edge_case, lower_bound = _log_edge_cases_check(x.a)
    if not is_edge_case:
        lower_bound = _precise_calc(x.a, lambda a: a.ln(), precision, ROUND_DOWN)

    is_edge_case, upper_bound = _log_edge_cases_check(x.b)
    if not is_edge_case:
        upper_bound = _precise_calc(x.b, lambda a: a.ln(), precision, ROUND_UP)

    return Interval(lower_bound, upper_bound)


def _log_edge_cases_check(x: Decimal) -> tuple[bool, Decimal]:
    """Returns if edge case is present for log function and result value"""

    if x < ia.c_zero:
        raise ValueError("Log cannot be applied to an interval containing values less than zero")
    if x == ia.c_zero:
        return True, ia.c_minf
    if x == ia.c_one:
        return True, ia.c_zero
    if x == ia.c_inf:
        return True, ia.c_inf
    return False, ia.c_zero


def _precise_calc(x: Decimal, func, precision: int, rounding) -> Decimal:
    precision_value = Decimal("0." + "0" * (precision - 1) + "1")
    extra = 3

    # correctly rounded result: repeatedly increase precision by 3
    # until we get an unambiguously roundable result
    while True:
        set_precision(precision + extra)
        estimation = func(x)
        if -estimation.as_tuple().exponent >= precision and estimation % precision_value != 0:
            estimation = _round(estimation, rounding, precision_value)
            set_precision(int(precision))
            return estimation
        extra += 3


def _round(x: Decimal, rounding, precision_value: Decimal) -> Decimal:
    if x < ia.c_zero:
        rounding = ROUND_UP if rounding == ROUND_DOWN else ROUND_DOWN
    return x.quantize(precision_value, rounding=rounding)
