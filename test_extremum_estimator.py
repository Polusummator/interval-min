from decimal import Decimal
from mp_exp.interval_arithmetics import *

from extremum_estimator import get_extremum_estimation

if __name__ == '__main__':
    f2 = "(log(x))"
    f = "x**2 + 1"
    res = get_extremum_estimation(f2, {"x": Interval(Decimal(-2), Decimal(100))}, "min")
    print(res)
