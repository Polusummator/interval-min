import unittest
from dataclasses import dataclass
from decimal import Decimal
from itertools import product
import timeout_decorator
import pandas as pd
from parameterized import parameterized
import re
from extremum_estimator import get_extremum_estimation, EXTENSIONS, METHODS, DIFFS
from mp_exp import Interval

TIMEOUT = 5


@dataclass(init=True)
class TestData:
    name: str
    func: str
    intervals: dict[str, Interval]
    precision: Decimal
    extremum_type: str
    answer: Decimal


TEST_TABLE = pd.read_csv('test_extremum_estimator.csv', dtype=str).fillna("")
# TEST_TABLE = TEST_TABLE[TEST_TABLE["Test name"] == "test_01"]


def custom_name_func(testcase_func, param_num, param):
    args = param.args
    return parameterized.to_safe_name("_".join([args[0].name, args[1], args[2], args[3]]))


def construct_test(row):
    intervals = dict()
    parsed_input = re.findall(r'([a-zA-Z]+).*?\[([-+]?\d*\.?\d+).*?([-+]?\d*\.?\d+)\]', row["Intervals"])
    for variable_name, a, b in parsed_input:
        intervals[variable_name] = Interval(Decimal(a), Decimal(b))
    return TestData(name=row["Test name"], func=row["Function"],
                    extremum_type=row["Extr"], answer=Decimal(row["Correct"]),
                    intervals=intervals, precision=Decimal(row["Precision"]))


class TestExtr(unittest.TestCase):

    @parameterized.expand(product([construct_test(row) for index, row in TEST_TABLE.iterrows()],
                                  EXTENSIONS, METHODS, DIFFS), name_func=custom_name_func)
    @timeout_decorator.timeout(TIMEOUT)
    def test(self, test, extension, method, diff):
        result = get_extremum_estimation(test.func, test.intervals,
                                         test.extremum_type, test.precision,
                                         extension, method, diff)
        difference = abs(test.answer - result)
        message = (f"expected: {test.answer}, actual: {result}.\n"
                   f"difference > precision: {difference} > {test.precision}")
        self.assertTrue(difference < test.precision, msg=message)


def suite():
    s = unittest.TestSuite()
    s.addTest(TestExtr('test'))
    return s


def run_tests():
    runner = unittest.TextTestRunner(verbosity=4)
    runner.run(suite())


if __name__ == '__main__':
    unittest.main()
