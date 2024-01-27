from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_UP
import mp_exp.interval_arithmetics as ia


def factorial(n):
    """
    Computes interval extension for a factorial function

    Parameters
    ----------
    n : Interval

    Returns:
    --------
    The interval that enclose the range of the factorial function
    """
    a = ia.c_one
    ia._set_rounding_mode_floor()
    for i in range(2, int(n.a) + 1):
        a = a * Decimal(i)
    b = ia.c_one
    ia._set_rounding_mode_ceil()
    for i in range(2, int(n.b) + 1):
        b = b * Decimal(i)
    return ia.Interval(a, b)


def exp(x: ia.Interval) -> ia.Interval:
    precision = getcontext().prec
    lower_bound = _precise_exp(x.a, precision, ROUND_DOWN)
    upper_bound = _precise_exp(x.b, precision, ROUND_UP)

    return ia.Interval(lower_bound, upper_bound)


def _precise_exp(x: Decimal, precision: Decimal, rounding) -> Decimal:
    precision_value = Decimal("0." + "0" * (precision - 1) + "1")
    extra = 3
    while True:
        ia.set_precision(precision + extra)
        estimation = x.exp()
        if -estimation.as_tuple().exponent >= precision and estimation % precision_value != 0:
            estimation.quantize(Decimal(precision_value), rounding=rounding)
            ia.set_precision(int(precision))
            return estimation
        extra += 3
