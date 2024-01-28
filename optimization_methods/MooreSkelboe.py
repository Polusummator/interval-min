from mp_exp.interval_arithmetics import *
from sortedcontainers import SortedList


class MooreSkelboe:
    def __init__(self, func_args: dict[str, Interval], interval_extension, precision: dec.Decimal,
                 extremum_type: str) -> None:
        self.func_args = func_args
        self.interval_extension = interval_extension
        self.answer_precision = precision
        self.calculation_precision = precision
        self.extremum_type = extremum_type

    def calculate(self):
        cells = self._get_sorted_list()
        cells.add(self.func_args)
        while wid(self.interval_extension.evaluate(current_cell := cells[0])) >= self.answer_precision:
            max_wid_variable = self._get_max_wid_variable(current_cell)
            new_cells = self._split_domain(current_cell, max_wid_variable)
            cells.pop(0)
            for cell in new_cells:
                cells.add(cell)
        return cells[0]

    def _split_domain(self, domain: dict[str, Interval], variable: str) -> list[dict]:
        split_interval = domain[variable]
        self._set_precision(split_interval)
        new_interval_left = Interval(split_interval.a, mid(split_interval))
        new_interval_right = Interval(mid(split_interval), split_interval.b)

        left_half = domain.copy()
        right_half = domain.copy()
        left_half[variable] = new_interval_left
        right_half[variable] = new_interval_right

        return [left_half, right_half]

    def _set_precision(self, interval: Interval):
        if wid(interval) <= self.calculation_precision * 2:
            set_precision(-self.calculation_precision.as_tuple().exponent + 5)
            self.calculation_precision /= 10

    def _get_sorted_list(self):
        if self.extremum_type == "min":
            return SortedList(key=lambda x: self.interval_extension.evaluate(x).a)
        return SortedList(key=lambda x: -self.interval_extension.evaluate(x).b)

    def _get_max_wid_variable(self, domain: dict[str, Interval]) -> str:
        max_wid_variable = 0  # sympy.Symbol actually
        max_wid = 0
        for item in domain.items():
            if wid(item[1]) > max_wid:
                max_wid = wid(item[1])
                max_wid_variable = item[0]
        return max_wid_variable
