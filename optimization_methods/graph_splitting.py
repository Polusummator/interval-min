from mp_exp import Interval, set_precision
from mp_exp.interval_arithmetics import intersect, is_in
from sortedcontainers import SortedList
from helpers import get_scale
from decimal import Decimal

from dataclasses import dataclass
from interval_differentiation.sympy_diffentiation import SympyGradientEvaluator
from interval_extensions import NaturalExtension


@dataclass(frozen=True)
class _Cell:
    lower_bound: Decimal
    domain: dict


class GraphSplitting:
    def __init__(self, func: str, func_args: dict[str, Interval], interval_extension, precision: Decimal) -> None:
        self.func = func
        self.func_args = func_args
        self.interval_extension = interval_extension
        self.answer_precision = precision
        self.calculation_scale = get_scale(precision)

        self.gradient_calculator = SympyGradientEvaluator(func, func_args)
        self.natural_extension = NaturalExtension(func, list(func_args))

        self.cells = SortedList(key=lambda x: x.lower_bound)
        self.bounds = interval_extension.evaluate(func_args)
        self.upper_bound = self.bounds.b

        self.muted_variable = list(func_args)[0]
        box = {}
        for variable in func_args.items():
            if variable[0] != self.muted_variable:
                box[variable[0]] = variable[1]
        box[0] = self.bounds
        self.cells.add(_Cell(self.bounds.a, box))

        self.newton_answer = []
        self.has_answer = False

    def calculate(self):
        while self.upper_bound - (current_cell := self.cells[0]).lower_bound >= self.answer_precision:
            max_wid_variable = self._get_max_wid_variable(current_cell.domain)
            new_domains = self._split_domain(current_cell.domain, max_wid_variable)
            self.cells.pop(0)
            for domain in new_domains:
                status = self._check_zeros(domain)
                if status:
                    if domain[0].a <= self.upper_bound:
                        self.cells.add(_Cell(domain[0].a, domain))
                    if status == 2:
                        self.upper_bound = min(self.upper_bound, domain[0].b)
        return self.cells[0].lower_bound

    def _split_domain(self, domain, variable: str) -> list[dict]:
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
        if interval.a.is_infinite() or interval.b.is_infinite():
            return
        if get_scale(interval.wid) <= self.calculation_scale:
            set_precision(self.calculation_scale + 5)
            self.calculation_scale += 1

    def _get_max_wid_variable(self, domain):
        max_wid_variable = ""
        max_wid = 0
        for variable in domain.items():
            if variable[1].wid >= max_wid:
                max_wid = variable[1].wid
                max_wid_variable = variable[0]
        return max_wid_variable

    def _check_zeros(self, domain):
        self.has_answer = False
        self.newton_answer = []
        current_interval = self.func_args[self.muted_variable]
        real_domain = domain.copy()
        bounds = real_domain.pop(0)
        work_list = [current_interval]
        skip_choosing_interval = False

        while work_list or skip_choosing_interval:
            if self.has_answer:
                break
            if not skip_choosing_interval:
                current_interval = work_list.pop()
            skip_choosing_interval = False
            current_domain = real_domain | {self.muted_variable: current_interval}
            df_value = self.gradient_calculator.evaluate(current_domain)[self.muted_variable]
            if not is_in(0, df_value):
                newton_interval = current_interval
                need_procedure = False
                while True:
                    newton_intervals = self._newton_step(domain.copy(), newton_interval)
                    if not newton_intervals:
                        newton_interval = None
                        break
                    assert(len(newton_intervals) == 1)
                    newton_interval = newton_intervals[0]  # phi'(X) != 0 => one interval
                    phi_value = self._calculate_phi(real_domain, newton_interval.mid_interval, bounds)
                    if is_in(0, phi_value):
                        need_procedure = True
                        break
                if not newton_interval:
                    continue
                if need_procedure:
                    procedure_interval = self._procedure_df_without_zero(newton_interval, domain)
                    if procedure_interval:
                        self.newton_answer.append(procedure_interval)
                continue
            expansion_point = None
            phi_value = self._calculate_phi(real_domain, current_interval.mid_interval, bounds)
            if not is_in(0, phi_value):
                phi_value = self._calculate_phi(real_domain, current_interval, bounds)
                if phi_value.wid <= self.answer_precision:
                    self.newton_answer.append(current_interval)
                    return 2
            else:
                status = self._procedure_decision(current_interval, real_domain, bounds)
                if status is None:
                    self.newton_answer.append(current_interval)
                    continue
                elif type(status) == int:
                    self._set_precision(current_interval)
                    left_half = Interval(current_interval.a, current_interval.mid)
                    right_half = Interval(current_interval.mid, current_interval.b)
                    work_list.append(left_half)
                    work_list.append(right_half)
                    continue
                expansion_point = status
            if not expansion_point:
                expansion_point = current_interval.mid_interval
            newton_intervals = self._newton_step(domain.copy(), current_interval, expansion_point)
            if not newton_intervals:
                continue
            if len(newton_intervals) > 1:
                work_list.append(newton_intervals[0])
                work_list.append(newton_intervals[1])
                continue
            skip_choosing_interval = True
            newton_interval = newton_intervals[0]
            if newton_interval.wid * 2 <= current_interval.wid:
                current_interval = newton_interval
                continue
            current_interval = newton_interval
            self._set_precision(current_interval)
            left_half = Interval(current_interval.a, current_interval.mid)
            right_half = Interval(current_interval.mid, current_interval.b)
            work_list.append(left_half)
            current_interval = right_half
        if self.has_answer:
            return 2
        if not self.newton_answer:
            return 0
        return 1

    def _newton_step(self, domain, muted_interval, expansion_point=None):
        if expansion_point is None:
            expansion_point = muted_interval.mid_interval
        bounds = domain.pop(0)
        expansion_dict = {self.muted_variable: expansion_point}
        muted_dict = {self.muted_variable: muted_interval}
        df_value = self.gradient_calculator.evaluate(domain | muted_dict)[self.muted_variable]
        f_value = self.interval_extension.evaluate(expansion_dict | domain) - bounds
        fraction = f_value / df_value
        intervals = []
        if fraction:
            if type(fraction) == Interval:
                newton_interval = expansion_point - fraction
                result = intersect(muted_interval, newton_interval)
                if muted_interval.a.is_finite() and muted_interval.b.is_finite() and result and is_in(newton_interval, muted_interval):
                    self.has_answer = True
                if result:
                    intervals.append(result)
            else:
                for interval in fraction:
                    newton_interval = expansion_point - interval
                    result = intersect(muted_interval, newton_interval)
                    if result:
                        intervals.append(result)
        return intervals

    def _calculate_phi(self, domain, muted_interval, bounds):
        muted_dict = {self.muted_variable: muted_interval}
        return self.interval_extension.evaluate(domain | muted_dict) - bounds

    def _procedure_df_without_zero(self, muted_interval, domain):
        real_domain = domain.copy()
        bounds = real_domain.pop(0)
        steps = 0
        flag_a = False
        flag_b = False
        interval = muted_interval
        first_zero = None
        while steps < 4:
            if not flag_a:
                phi_value = self._calculate_phi(real_domain, Interval.to_interval(interval.a), bounds)
                if is_in(0, phi_value):
                    flag_a = True
                    if first_zero is None:
                        first_zero = Interval.to_interval(interval.a)
                else:
                    newton_intervals = self._newton_step(domain.copy(), interval, Interval.to_interval(interval.a))
                    if not newton_intervals:
                        interval = None
                        break
                    assert(len(newton_intervals) == 1)
                    interval = newton_intervals[0]
            if not flag_b:
                phi_value = self._calculate_phi(real_domain, Interval.to_interval(interval.b), bounds)
                if is_in(0, phi_value):
                    flag_b = True
                    if first_zero is None:
                        first_zero = Interval.to_interval(interval.b)
                else:
                    expansion_point = interval.mid_interval
                    if first_zero and is_in(first_zero, interval):
                        expansion_point = Interval.to_interval(interval.b)
                    phi_value = self._calculate_phi(real_domain, expansion_point, bounds)
                    if is_in(0, phi_value) and first_zero is None:
                        first_zero = expansion_point
                    newton_intervals = self._newton_step(domain.copy(), interval, expansion_point)
                    if not newton_intervals:
                        interval = None
                        break
                    assert(len(newton_intervals) == 1)
                    interval = newton_intervals[0]
            if flag_a and flag_b:
                break
            phi_value = self._calculate_phi(real_domain, interval.mid_interval, bounds)
            if is_in(0, phi_value) and not first_zero:
                first_zero = interval.mid_interval
            newton_intervals = self._newton_step(domain.copy(), interval)
            if not newton_intervals:
                interval = None
                break
            assert(len(newton_intervals) == 1)
            interval = newton_intervals[0]
            steps += 1
        return interval

    def _procedure_decision(self, muted_interval, domain, bounds):  # None - accepted, Interval - point for Newton method, 1 - split
        a = muted_interval.a
        ai = Interval.to_interval(a)
        phi_value_a = self._calculate_phi(domain, ai, bounds)
        if not is_in(0, phi_value_a):
            return ai
        b = muted_interval.b
        bi = Interval.to_interval(b)
        phi_value_b = self._calculate_phi(domain, bi, bounds)
        if not is_in(0, phi_value_b):
            return bi
        x1 = (Decimal(3) * a + b) / Decimal(4)
        x2 = (a + Decimal(3) * b) / Decimal(4)
        phi_value_x1 = self._calculate_phi(domain, Interval.to_interval(x1), bounds)
        phi_value_x2 = self._calculate_phi(domain, Interval.to_interval(x2), bounds)
        if not is_in(0, phi_value_x1) or not is_in(0, phi_value_x2):
            return 1
        return None
