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
            widmax_variable = 0  # sympy.Symbol actually
            widmax = 0
            for item in cells[0].items():
                if wid(item[1]) > widmax:
                    widmax = wid(item[1])
                    widmax_variable = item[0]
            widmax_interval = cells[0][widmax_variable]
            new_cell_left = cells[0].copy()  # todo: copy?
            new_cell_right = cells[0].copy()  # todo: copy?
            new_interval_left = Interval(widmax_interval.a, mid(widmax_interval))
            new_interval_right = Interval(mid(widmax_interval), widmax_interval.b)
            new_cell_left[widmax_variable] = new_interval_left
            new_cell_right[widmax_variable] = new_interval_right
            cells.pop(0)
            cells.add(new_cell_left)
            cells.add(new_cell_right)
        return cells[0]
