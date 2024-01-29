from decimal import Decimal
from extremum_estimator import get_extremum_estimation
import unittest
import csv
import mp_exp.interval_arithmetics as ia


class TestExtr(unittest.TestCase):
    def test(self):
        print("\n\n\n")
        with open('test_extremum_estimator.csv', 'r', encoding='utf-8') as csv_file:
            caption = ""
            for num, row in enumerate(csv.reader(csv_file, delimiter=',')):
                flag = True
                if not num:
                    caption = row
                    continue
                else:
                    f = ""
                    ans = ""
                    d = dict()
                    extr = ""
                    for nm, data in enumerate(row):
                        if caption[nm] == "Function":
                            f = data
                        elif caption[nm] == "Extr":
                            extr = data
                        elif caption[nm] == "Intervals":
                            s = data.split(" ")
                            for x in s:
                                ds = x.split(":")
                                dx = ds[1].split(",")
                                a = Decimal(dx[0][1:])
                                b = Decimal(dx[1][:-1])
                                d = {ds[0]: ia.Interval(a, b)}
                        elif caption[nm] == "Correct":
                            ans = Decimal(data)
                        print(f'{caption[nm]}: {data}')
                    base = "0."
                    for i in range(5):
                        epsilon = Decimal(base + '1')
                        try:
                            res = get_extremum_estimation(f, d, extr, epsilon)
                            self.assertTrue(abs(Decimal(res) - ans) < epsilon)
                        except:
                            flag = False
                            break
                        base += '0'
                    if flag:
                        print(f"TEST PASSED\n")
                    else:
                        print(f"TEST FAILED\n")




def suite():
    s = unittest.TestSuite()
    s.addTest(TestExtr('test'))
    return s


def run_tests():
    runner = unittest.TextTestRunner(verbosity=4)
    runner.run(suite())


if __name__ == '__main__':
    unittest.main()
