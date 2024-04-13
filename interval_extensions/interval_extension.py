import abc

from mp_exp import Interval


class IntervalExtension(abc.ABC):

    @abc.abstractmethod
    def __init__(self, variables, expr: str, gradient_evaluator):
        """Initialize an interval extension of expr"""

    @abc.abstractmethod
    def evaluate(self, variables: dict[str, Interval]) -> Interval:
        """Get an interval extension of the expression over given variables"""
