import abc

from mp_exp import Interval


class IntervalInclusion(abc.ABC):

    @abc.abstractmethod
    def __init__(self, expr: str, variable_names, gradient_evaluator):
        """Initialize an interval extension of expr"""

    @abc.abstractmethod
    def evaluate(self, variables: dict[str, Interval]) -> Interval:
        """Get an interval extension of the expression over given variables"""
