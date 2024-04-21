from mp_exp import Interval, set_precision
from sortedcontainers import SortedList
from helpers import get_scale
from decimal import Decimal
from dataclasses import dataclass

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

        self.cells = SortedList(key=lambda x: x.lower_bound)
        self.cells.add(_Cell(interval_extension.evaluate(func_args).a, func_args))

    def calculate(self):
        while self.interval_extension.evaluate((current_cell := self.cells[0]).domain).wid >= self.answer_precision:
            max_wid_variable = self._get_max_wid_variable(current_cell.domain)
            new_domains = self._split_domain(current_cell.domain, max_wid_variable)
            self.cells.pop(0)
            for domain in new_domains:
                self.cells.add(_Cell(self.interval_extension.evaluate(domain).a, domain))
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

    def _get_max_wid_variable(self, domain):
        max_wid_variable = ""
        max_wid = 0
        for variable in domain.items():
            if variable[1].wid > max_wid:
                max_wid = variable[1].wid
                max_wid_variable = variable[0]
        return max_wid_variable
