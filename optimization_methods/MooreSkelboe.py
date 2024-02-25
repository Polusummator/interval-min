from mp_exp import Interval, set_precision
from sortedcontainers import SortedList
from helpers import get_scale

from decimal import Decimal


class MooreSkelboe:
    def __init__(self, func_args: dict[str, Interval], interval_extension, precision: Decimal,
                 extremum_type: str) -> None:
        self.func_args = func_args
        self.interval_extension = interval_extension
        self.answer_precision = precision
        self.calculation_scale = get_scale(precision)
        self.extremum_type = extremum_type

    def calculate(self):
        cells = self._get_sorted_list()
        cells.add(self.func_args)
        while self.interval_extension.evaluate(current_cell := cells[0]).wid >= self.answer_precision:
            max_wid_variable = self._get_max_wid_variable(current_cell)
            new_cells = self._split_domain(current_cell, max_wid_variable)
            cells.pop(0)
            for cell in new_cells:
                cells.add(cell)
        return cells[0]

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
        if self.extremum_type == "min":
            return SortedList(key=lambda x: self.interval_extension.evaluate(x).a)
        return SortedList(key=lambda x: -self.interval_extension.evaluate(x).b)

    def _get_max_wid_variable(self, domain: dict[str, Interval]) -> str:
        max_wid_variable = 0  # sympy.Symbol actually
        max_wid = 0
        for item in domain.items():
            if item[1].wid > max_wid:
                max_wid = item[1].wid
                max_wid_variable = item[0]
        return max_wid_variable
