from mp_exp import Interval
from decimal import Decimal
from interval_extensions import NaturalExtension
from scipy.stats import truncnorm
from math import exp
from random import random

DEVIATION = 1
INIT_TEMPERATURE = Decimal(100)
STEP = Decimal("0.1")
PROBABILITY_CONSTANT = 1
ITERATIONS = 10


class SimulatedAnnealing:
    def __init__(self, func: str, func_args: dict[str, Interval], interval_extension, precision: Decimal) -> None:
        self.func = func
        self.func_args = func_args
        self.temperature = INIT_TEMPERATURE
        self.natural_extension = NaturalExtension(func, list(func_args))

    def calculate(self):
        current_point = dict()
        for variable in self.func_args.items():
            current_point[variable[0]] = variable[1].mid_interval
        answer = self._get_function_value(current_point)

        while self.temperature > 0:
            for i in range(ITERATIONS):
                new_point = self._get_neighbour(current_point)
                function_value = self._get_function_value(new_point)
                if function_value < answer:
                    answer = function_value
                choice = random()
                if choice <= self._get_probability(current_point, new_point):
                    current_point = new_point
            self.temperature -= STEP
        return answer

    def _get_probability(self, old_point, new_point):
        delta = self._get_function_value(new_point) - self._get_function_value(old_point)
        if delta <= 0:
            return 1
        else:
            return exp(-delta / (PROBABILITY_CONSTANT * self.temperature))

    def _get_neighbour(self, point: dict[str, Interval]) -> dict[str, Interval]:
        neighbour = {}
        for variable in point.items():
            mean = variable[1].a
            variable_interval = self.func_args[variable[0]]
            lower_bound = float(variable_interval.a)
            upper_bound = float(variable_interval.b)
            neighbour[variable[0]] = Interval.to_interval(
                Decimal.from_float(truncnorm(
                    (lower_bound - float(mean)) / DEVIATION,
                    (upper_bound - float(mean)) / DEVIATION,
                    loc=float(mean),
                    scale=DEVIATION).rvs()))
        return neighbour

    def _get_function_value(self, point: dict[str, Interval]) -> Decimal:
        return self.natural_extension.evaluate(point).a
