import abc


class SlopeEvaluator(abc.ABC):
    """Evaluates interval slopes or derivatives of a functions"""

    @abc.abstractmethod
    def __init__(self, expr: str, variable_names):
        """Initialize the slope evaluator for a given expression"""

    def evaluate(self, variables: dict, point: dict):
        """Get an interval slope over a given variables with respect to the given point"""
