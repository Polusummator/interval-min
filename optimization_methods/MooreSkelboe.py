from mp_exp.interval_arithmetics import *
from sortedcontainers import SortedList


class MooreSkelboe:
    def __init__(self, func_args: dict[str, Interval], interval_extension, precision: dec.Decimal,
                 extremum_type: str) -> None:
        self.func_args = func_args
        self.interval_extension = interval_extension
        self.precision = precision
        self.extremum_type = extremum_type

    def calculate(self):
        if self.extremum_type == "min":
            cells = SortedList(key=lambda x: self.interval_extension.evaluate(x).a)
        else:
            cells = SortedList(key=lambda x: -self.interval_extension.evaluate(x).b)
        cells.add(self.func_args)
        while wid(self.interval_extension.evaluate(cells[0])) >= self.precision:
            maxwid_variable = 0  # sympy.Symbol actually
            maxwid = 0
            for item in cells[0].items():
                if wid(item[1]) > maxwid:
                    maxwid = wid(item[1])
                    maxwid_variable = item[0]

            new_cells = self._split_domain(cells[0], maxwid_variable)
            cells.pop(0)
            for cell in new_cells:
                cells.add(cell)
        return cells[0]

    def _split_domain(self, domain: dict[str, Interval], variable: str) -> list[dict]:
        split_interval = domain[variable]
        new_interval_left = Interval(split_interval.a, mid(split_interval))
        new_interval_right = Interval(mid(split_interval), split_interval.b)

        left_half = domain.copy()  # todo: copy?
        right_half = domain.copy()  # todo: copy?
        left_half[variable] = new_interval_left
        right_half[variable] = new_interval_right

        return [left_half, right_half]
