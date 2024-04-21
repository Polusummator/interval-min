from mp_exp import Interval, set_precision
from sortedcontainers import SortedList
from helpers import get_scale
from decimal import Decimal

from dataclasses import dataclass
from interval_differentiation.sympy_diffentiation import SympyGradientEvaluator
from interval_inclusions import NaturalInclusion


@dataclass(frozen=True)
class _Cell:
    lower_bound: Decimal
    domain: dict[str, Interval]


class MooreSkelboe:
    def __init__(self, func: str, func_args: dict[str, Interval], interval_extension, precision: Decimal) -> None:
        self.func = func
        self.func_args = func_args
        self.interval_extension = interval_extension
        self.answer_precision = precision
        self.calculation_scale = get_scale(precision)

        self.gradient_calculator = SympyGradientEvaluator(func, func_args)
        self.natural_extension = NaturalInclusion(func, list(func_args))
        self.extremum_bound = self._calculate_mid_value(func_args)

        self.cells = SortedList(key=lambda x: x.lower_bound)
        self.cells.add(_Cell(interval_extension.evaluate(func_args).a, func_args))

    def calculate(self):
        while self.interval_extension.evaluate((current_cell := self.cells[0]).domain).wid >= self.answer_precision:
            max_speed_variable = self._get_max_speed_variable(current_cell.domain)
            new_domains = self._split_domain(current_cell.domain, max_speed_variable)
            self.cells.pop(0)
            check_needed = False
            for domain in new_domains:
                midpoint_value = self._calculate_mid_value(domain)
                if midpoint_value < self.extremum_bound:
                    self.extremum_bound = midpoint_value
                    check_needed = True
                self.cells.add(_Cell(self.interval_extension.evaluate(domain).a, domain))
            if check_needed:
                self._check_list()
        return self.cells[0].lower_bound

    def _split_domain(self, domain: dict[str, Interval], variable: str) -> list[dict]:
        split_interval = domain[variable]
        self._set_precision(split_interval)
        new_interval_left = Interval(split_interval.a, split_interval.mid)
        new_interval_right = Interval(split_interval.mid, split_interval.b)

        left_half = domain.copy()
        right_half = domain.copy()
        left_half[variable] = new_interval_left
        right_half[variable] = new_interval_right

        return [left_half, right_half]

    def _set_precision(self, interval: Interval):
        if get_scale(interval.wid) <= self.calculation_scale:
            set_precision(self.calculation_scale + 5)
            self.calculation_scale += 1

    def _get_max_speed_variable(self, domain: dict[str, Interval]) -> str:
        max_speed_variable = ""
        max_speed_value = 0
        for variable in domain.items():
            derivative = self.gradient_calculator.evaluate(domain)[variable[0]]
            derivative_magnitude = max(abs(derivative.a), abs(derivative.b))
            if not max_speed_variable or variable[1].wid * derivative_magnitude > max_speed_value:
                max_speed_value = variable[1].wid * derivative_magnitude
                max_speed_variable = variable[0]
        return max_speed_variable

    def _calculate_mid_value(self, domain: dict[str, Interval]):
        mid_point = dict()
        for variable in domain.items():
            mid_point[variable[0]] = variable[1].mid_interval
        mid_value = self.natural_extension.evaluate(mid_point)
        return mid_value.a  # mid_value.a == mid_value.b

    def _check_list(self):
        index = self.cells.bisect_right(_Cell(self.extremum_bound, {}))
        del self.cells[index:]
