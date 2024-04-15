from decimal import Decimal
from interval_extensions.function_evaluator import FunctionEvaluator
from mp_exp import Interval, exp, log
from .slope_evaluator import SlopeEvaluator


class DerivativePair:
    """
    A class that represents a value and a derivative of a function.

    This class is ment to be used with SymPy
    """

    def __init__(self, value, derivative=Interval(0, 0)):
        self.value = Interval.to_interval(value)
        self.derivative = Interval.to_interval(derivative)

    @classmethod
    def to_pair(cls, other):
        if type(other) is Decimal or type(other) is Interval:
            return DerivativePair(other)
        elif type(other) is int or type(other) is float:
            v = Decimal(other)
            return DerivativePair(v)
        else:
            return other

    def __neg__(self):
        value = -self.value
        derivative = -self.derivative
        return DerivativePair(value, derivative)

    def __add__(self, other):
        other = DerivativePair.to_pair(other)
        value = self.value + other.value
        derivative = self.derivative + other.derivative
        return DerivativePair(value, derivative)

    def __sub__(self, other):
        other = DerivativePair.to_pair(other)
        value = self.value - other.value
        derivative = self.derivative - other.derivative
        return DerivativePair(value, derivative)

    def __mul__(self, other):
        other = DerivativePair.to_pair(other)
        value = self.value * other.value
        derivative = self.derivative * other.value + self.value * other.derivative
        return DerivativePair(value, derivative)

    def __truediv__(self, other):
        other = DerivativePair.to_pair(other)
        value = self.value / other.value
        derivative = (self.derivative * other.value - self.value * other.derivative) / (other.value ** 2)
        return DerivativePair(value, derivative)

    def __pow__(self, power):
        value = self.value ** power
        derivative = self.value ** (power - 1) * self.derivative * (power)
        return DerivativePair(value, derivative)

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rtruediv__(self, other):
        return self.__truediv__(other)


def pair_log(pair: DerivativePair):
    value = log(pair.value)
    derivative = pair.derivative / pair.value
    return DerivativePair(value, derivative)


def pair_exp(pair: DerivativePair):
    value = exp(pair.value)
    derivative = pair.derivative * exp(pair.value)
    return DerivativePair(value, derivative)


def pair_factorial(pair: DerivativePair):
    raise RuntimeError("Cannot differentiate factorial")


derivative_pair_operations = {'exp': pair_exp, 'log': pair_log, 'factorial': pair_factorial}


class ForwardGradientEvaluator(SlopeEvaluator):
    def __init__(self, expr: str, variable_names):
        self.gradient_evaluator = FunctionEvaluator(expr, variable_names, derivative_pair_operations)

    def evaluate(self, variables: dict, point=None):
        gradient = dict()
        derivative_pairs = {variable: DerivativePair(interval) for variable, interval in variables.items()}
        for variable, interval in variables.items():
            derivative_pairs[variable].derivative = Interval.to_interval(1)
            gradient[variable] = self.gradient_evaluator.evaluate(derivative_pairs).derivative
            derivative_pairs[variable].derivative = Interval.to_interval(0)
        return gradient
