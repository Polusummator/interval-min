from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_UP
from mp_exp import Interval, set_precision


def exp(x: Interval) -> Interval:
    precision = getcontext().prec
    lower_bound = _precise_calc(x.a, lambda a: a.exp(), precision, ROUND_DOWN) if x.a != 0 else 1
    upper_bound = _precise_calc(x.b, lambda a: a.exp(), precision, ROUND_UP) if x.b != 0 else 1

    return Interval(lower_bound, upper_bound)


def log(x: Interval) -> Interval:
    if x.a <= 0:
        raise ValueError("Log cannot be applied to an interval containing values less or equal to zero")

    precision = getcontext().prec
    lower_bound = _precise_calc(x.a, lambda a: a.ln(), precision, ROUND_DOWN) if x.a != 1 else 0
    upper_bound = _precise_calc(x.b, lambda a: a.ln(), precision, ROUND_UP) if x.b != 1 else 0

    return Interval(lower_bound, upper_bound)


def _precise_calc(x: Decimal, func, precision: int, rounding) -> Decimal:
    precision_value = Decimal("0." + "0" * (precision - 1) + "1")
    extra = 3
    while True:
        set_precision(precision + extra)
        estimation = func(x)
        if -estimation.as_tuple().exponent >= precision and estimation % precision_value != 0:
            estimation.quantize(Decimal(precision_value), rounding=rounding)
            set_precision(int(precision))
            return estimation
        extra += 3
