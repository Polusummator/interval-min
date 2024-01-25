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
            current_cell = cells[0]
            for item in current_cell.items():
                if wid(item[1]) > widmax:
                    widmax = wid(item[1])
                    widmax_variable = item[0]
            widmax_interval = current_cell[widmax_variable]
            new_cell_left = current_cell.copy()
            new_cell_right = current_cell.copy()
            middle = mid(widmax_interval)
            new_interval_left = Interval(widmax_interval.a, middle)
            new_interval_right = Interval(middle, widmax_interval.b)
            new_cell_left[widmax_variable] = new_interval_left
            new_cell_right[widmax_variable] = new_interval_right
            cells.pop(0)
            cells.add(new_cell_left)
            cells.add(new_cell_right)
        return cells[0]
