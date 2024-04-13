from decimal import Decimal
from .forward_differentiation import DerivativePair, pair_exp, pair_log
from .function_evaluator import FunctionEvaluator
from mp_exp import Interval, exp, log
from .slopes_evaluator import SlopesEvaluator


class SlopeTuple:
    def __init__(self, value1, value2=None, slope=Interval(0, 0)):
        if not value2:
            value2 = value1
        self.value1 = Interval.to_interval(value1)
        self.value2 = Interval.to_interval(value2)
        self.slope = Interval.to_interval(slope)

    @classmethod
    def to_slope(cls, other):
        if type(other) is DerivativePair:
            return SlopeTuple(other.value, other.value, other.derivative)
        if type(other) is Decimal or type(other) is Interval:
            return SlopeTuple(other)
        elif type(other) is int or type(other) is float:
            v = Decimal(other)
            return SlopeTuple(v)
        else:
            return other

    def __neg__(self):
        value1 = -self.value1
        value2 = -self.value2
        slope = -self.slope
        return SlopeTuple(value1, value2, slope)

    def __add__(self, other):
        other = SlopeTuple.to_slope(other)
        value1 = self.value1 + other.value1
        value2 = self.value2 + other.value2
        slope = self.slope + other.slope
        return SlopeTuple(value1, value2, slope)

    def __sub__(self, other):
        other = SlopeTuple.to_slope(other)
        value1 = self.value1 - other.value1
        value2 = self.value2 - other.value2
        slope = self.slope - other.slope
        return SlopeTuple(value1, value2, slope)

    def __mul__(self, other):
        other = SlopeTuple.to_slope(other)
        value1 = self.value1 * other.value1
        value2 = self.value2 * other.value2
        slope = self.slope * other.value2 + self.value1 * other.slope
        return SlopeTuple(value1, value2, slope)

    def __truediv__(self, other):
        other = SlopeTuple.to_slope(other)
        value1 = self.value1 / other.value1
        value2 = self.value2 / other.value2
        slope = (self.slope - other.slope * value2) / other.value1
        return SlopeTuple(value1, value2, slope)

    def __pow__(self, power):
        derivative = DerivativePair(self.value1, 1) ** power
        value1 = self.value1 ** power
        value2 = self.value2 ** power
        slope = derivative.derivative * self.slope
        return SlopeTuple(value1, value2, slope)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)


def slope_log(slope_tuple: SlopeTuple):
    derivative = pair_log(DerivativePair(slope_tuple.value1, 1))
    value1 = log(slope_tuple.value1)
    value2 = log(slope_tuple.value2)
    slope = derivative.derivative * slope_tuple.slope

    return SlopeTuple(value1, value2, slope)


def slope_exp(slope_tuple: SlopeTuple):
    derivative = pair_exp(DerivativePair(slope_tuple.value1, 1))
    value1 = exp(slope_tuple.value1)
    value2 = exp(slope_tuple.value2)
    slope = derivative.derivative * slope_tuple.slope

    return SlopeTuple(value1, value2, slope)


def slope_factorial(pair: SlopeTuple):
    raise RuntimeError("Cannot differentiate factorial")


slope_tuple_operations = {'exp': slope_exp, 'log': slope_log, 'factorial': slope_factorial}


class ForwardSlopeEvaluator(SlopesEvaluator):
    def __init__(self, expr: str, variable_names):
        self.gradient_evaluator = FunctionEvaluator(expr, variable_names, slope_tuple_operations)

    def evaluate(self, variables: dict, point: dict):
        slopes = dict()
        slope_tuple = {variable: SlopeTuple(interval, point[variable]) for variable, interval in variables.items()}
        for variable, interval in variables.items():
            slope_tuple[variable].slope = Interval.to_interval(1)
            slopes[variable] = self.gradient_evaluator.evaluate(slope_tuple).slope
            slope_tuple[variable].slope = Interval.to_interval(0)
        return slopes
