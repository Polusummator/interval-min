from decimal import Decimal
from extremum_estimator import get_extremum_estimation
import unittest
import mp_exp.interval_arithmetics as ia


class TestExtr(unittest.TestCase):
    def test_base(self):
        f = "x**2 + 1"
        base = "0."
        for i in range(200):
            epsilon = Decimal(base + '1')
            res = get_extremum_estimation(
                f, {"x": ia.Interval(Decimal("-10"), Decimal("100"))}, "min", epsilon
            )
            self.assertTrue(abs(Decimal(res) - Decimal("1")) < epsilon)
            base += '0'

    def test_border(self):
        f = "x"
        base = "0."
        for i in range(100):
            epsilon = Decimal(base + '1')
            res = get_extremum_estimation(
                f, {"x": ia.Interval(Decimal("-10000"), Decimal("100"))}, "min", epsilon
            )
            self.assertTrue(abs(Decimal(res) - Decimal("-10000")) < epsilon)
            base += '0'
        f = "x**3"
        base = "0."
        for i in range(10):
            epsilon = Decimal(base + '1')
            res = get_extremum_estimation(
                f, {"x": ia.Interval(Decimal("100"), Decimal("200"))}, "min", epsilon
            )
            self.assertTrue(abs(Decimal(res) - Decimal("1000000")) < epsilon)
            base += '0'

    def test_exp(self):
        f = "exp(x)"
        base = "0."
        for i in range(10):
            epsilon = Decimal(base + '1')
            res = get_extremum_estimation(
                f, {"x": ia.Interval(Decimal('1'), Decimal('10'))}, "min", epsilon
            )
            self.assertTrue(abs(Decimal(res) - Decimal("2.7182818284590452353602874713526624")) < epsilon)
            base += '0'

    def test_TL_moment(self):
        f = "x**2 + x + 1"
        base = "0."
        for i in range(10):
            epsilon = Decimal(base + '1')
            res = get_extremum_estimation(
                f, {"x": ia.Interval(Decimal("-100"), Decimal("100"))}, "min", epsilon
            )
            self.assertTrue(abs(Decimal(res) - Decimal("0.75")) < epsilon)
            base += '0'

    def test_dot(self):
        f = "1"
        base = "0."
        for i in range(10):
            epsilon = Decimal(base + '1')
            res = get_extremum_estimation(
                f, {"x": ia.Interval(Decimal("-10"), Decimal("100"))}, "min", epsilon
            )
            self.assertTrue(abs(Decimal(res) - Decimal("1")) < epsilon)
            base += '0'


def suite():
    s = unittest.TestSuite()
    s.addTest(TestExtr('test_base'))
    s.addTest(TestExtr('test_border'))
    s.addTest(TestExtr('test_exp'))
    s.addTest(TestExtr('test_TL_moment'))
    s.addTest(TestExtr('test_dot'))
    return s


def run_tests():
    runner = unittest.TextTestRunner(verbosity=4)
    runner.run(suite())


if __name__ == '__main__':
    unittest.main()
