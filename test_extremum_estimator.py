import unittest
from dataclasses import dataclass
from decimal import Decimal
from itertools import product
import pandas as pd
from parameterized import parameterized
from extremum_estimator import get_extremum_estimation, EXTENSIONS, METHODS
from mp_exp import Interval


@dataclass(init=True)
class TestData:
    name: str
    func: str
    intervals: dict[str, Interval]
    precision: Decimal
    extremum_type: str
    answer: Decimal


TEST_TABLE = pd.read_csv('test_extremum_estimator.csv', dtype=str)


def custom_name_func(testcase_func, param_num, param):
    args = param.args
    return parameterized.to_safe_name("_".join([args[0].name, args[1], args[2]]))


def construct_test(row):
    intervals = dict()
    for var_int_string in row["Intervals"].split(" "):
        variable_name, interval_string = var_int_string.split(":")
        a, b = interval_string.split(",")
        a = Decimal(a[1:])
        b = Decimal(b[:-1])
        intervals[variable_name] = Interval(a, b)
    return TestData(name=row["Test name"], func=row["Function"],
                    extremum_type=row["Extr"], answer=Decimal(row["Correct"]),
                    intervals=intervals, precision=Decimal(row["Precision"]))


class TestExtr(unittest.TestCase):

    @parameterized.expand(product([construct_test(row) for index, row in TEST_TABLE.iterrows()],
                                  EXTENSIONS,
                                  METHODS), name_func=custom_name_func)
    def test(self, test, extension, method):
        result = get_extremum_estimation(test.func, test.intervals,
                                         test.extremum_type, test.precision,
                                         extension, method)
        print(f" Result value: {result}")
        self.assertTrue(abs(test.answer - result) < test.precision)


def suite():
    s = unittest.TestSuite()
    s.addTest(TestExtr('test'))
    return s


def run_tests():
    runner = unittest.TextTestRunner(verbosity=4)
    runner.run(suite())


if __name__ == '__main__':
    unittest.main()
