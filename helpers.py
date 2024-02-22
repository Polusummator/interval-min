from decimal import Decimal


def get_scale(decimal: Decimal) -> int:
    """
    Returns number of digits in the number

    """
    decimal_tuple = decimal.as_tuple()
    return max(len(decimal_tuple.digits), -decimal_tuple.exponent + 1)
