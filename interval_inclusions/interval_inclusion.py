import abc

from mp_exp import Interval


class IntervalInclusion(abc.ABC):

    @abc.abstractmethod
    def __init__(self, expr: str, variable_names, gradient_evaluator):
        """Initialize an interval inclosure of expr"""

    @abc.abstractmethod
    def evaluate(self, variables: dict[str, Interval]) -> Interval:
        """Get an interval inclosure of the expression over given variables"""
