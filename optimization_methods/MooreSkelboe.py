from mp_exp import Interval, set_precision
from sortedcontainers import SortedList
from helpers import get_scale
from decimal import Decimal

from interval_differentiation.sympy_diffentiation import SympyGradientEvaluator
from interval_extensions import NaturalExtension


class MooreSkelboe:
    def __init__(self, func: str, func_args: dict[str, Interval], interval_extension, precision: Decimal) -> None:
        self.func = func
        self.func_args = func_args
        self.interval_extension = interval_extension
        self.answer_precision = precision
        self.calculation_scale = get_scale(precision)

        self.gradient_calculator = SympyGradientEvaluator(func, func_args)
        self.natural_extension = NaturalExtension(func, list(func_args))
        self.extremum_bound = self._calculate_mid_value(func_args)

        self.cells = self._get_sorted_list()
        self.cells.add(func_args)

    def calculate(self):
        while self.interval_extension.evaluate(current_cell := self.cells[0]).wid >= self.answer_precision:
            max_speed_variable = self._get_max_speed_variable(current_cell)
            new_cells = self._split_domain(current_cell, max_speed_variable)
            self.cells.pop(0)
            check_needed = False
            for cell in new_cells:
                midpoint_value = self._calculate_mid_value(cell)
                if midpoint_value < self.extremum_bound:
                    self.extremum_bound = midpoint_value
                    check_needed = True
                self.cells.add(cell)
            if check_needed:
                self._check_list()
        return self.cells[0]

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

    def _get_sorted_list(self):
        return SortedList(key=lambda x: self.interval_extension.evaluate(x).a)

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
        checked_cells = self._get_sorted_list()
        for cell in self.cells:
            cell_evaluation = self.interval_extension.evaluate(cell)
            if cell_evaluation.a <= self.extremum_bound:
                checked_cells.add(cell)
        self.cells = checked_cells

