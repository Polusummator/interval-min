import decimal
import time
from dataclasses import dataclass
from decimal import Decimal
import timeout_decorator
import numpy as np
from random import randint, sample
import matplotlib.pyplot as plt
from extremum_estimator import get_extremum_estimation, EXTENSIONS, DIFFS
from mp_exp import Interval

TIMEOUT = 10
amount = 20
values = []
koefs = [str(i) for i in range(-100, 101)]
degs = [i for i in range(0, 16)]
max_time = [-1] * (len(EXTENSIONS) * len(DIFFS))
min_time = [10000] * (len(EXTENSIONS) * len(DIFFS))
middle = [[amount, 0] for _ in range(len(EXTENSIONS) * len(DIFFS))]
average = []
failures = []


@dataclass(init=True)
class TestData:
    name: str
    func: str
    intervals: dict[str, Interval]
    precision: Decimal
    answer: Decimal


@timeout_decorator.timeout(TIMEOUT)
def limited_extremum_estimation_execution(tst, e, m, d):
    return get_extremum_estimation(tst.func, tst.intervals, tst.precision, e, m, d)


def generate(argzz):
    f = ""
    for arg in range(argzz):
        m = randint(0, 15)
        m += 1
        koefk = sample(koefs, m)
        degk = sample(degs, m)
        degk = sorted(degk)
        degk.reverse()
        degk = [str(i) for i in degk]
        if arg == 0:
            c_arg = 'x'
        elif arg == 1:
            c_arg = 'y'
            if len(f) != 0:
                f += ' + '
        else:
            c_arg = 'z'
            if len(f) != 0:
                f += ' + '
        if koefk[0] != '0':
            f += "(" + koefk[0] + f") * {c_arg}**(" + degk[0] + ")"
        else:
            f += '0'
        for i in range(1, m):
            if koefk[i] == '0':
                continue
            if degk[i] == '1':
                if int(koefk[i]) > 0:
                    f += " + " + koefk[i] + f" * {c_arg}"
                else:
                    f += " - " + str(-int(koefk[i])) + f" * {c_arg}"
                continue
            if degk[i] == '0':
                if int(koefk[i]) > 0:
                    f += " + " + koefk[i]
                else:
                    f += " - " + str(-int(koefk[i]))
                continue
            if int(koefk[i]) > 0:
                f += " + " + koefk[i] + f" * {c_arg}**(" + degk[i] + ")"
            else:
                f += " - " + str(-int(koefk[i])) + f" * {c_arg}**(" + degk[i] + ")"
    return f


def do_it():
    method = "moore_skelboe"
    index = 0
    for _ in range(amount):
        i = dict()
        args = randint(1, 3)
        if args == 1:
            i['x'] = Interval(-10, 10)
        elif args == 2:
            i['x'] = Interval(-10, 10)
            i['y'] = Interval(-10, 10)
        else:
            i['x'] = Interval(-10, 10)
            i['y'] = Interval(-10, 10)
            i['z'] = Interval(-10, 10)
        f = generate(args)
        test = TestData(name='base', func=f,
                        answer=decimal.Decimal(0), intervals=i,
                        precision=decimal.Decimal('0.01'))
        x = []
        for extension in EXTENSIONS.keys():
            for diff in DIFFS.keys():
                try:
                    t = time.time()
                    result = limited_extremum_estimation_execution(test, extension, method, diff)
                    real_time = time.time() - t
                    x.append(real_time)
                except:
                    x.append(None)
                index += 1
        values.append(x)


def collect_statistics():
    for x in values:
        for i in range(0, len(EXTENSIONS) * len(DIFFS)):
            if x[i] is None:
                middle[i][0] -= 1
                continue
            max_time[i] = max(max_time[i], x[i])
            min_time[i] = min(min_time[i], x[i])
            middle[i][1] += x[i]
    for x in middle:
        average.append(x[1] / x[0])
        failures.append(amount - x[0])


def building_plots():
    objects = [x[0] + '_' + y[0:2] for x in EXTENSIONS for y in DIFFS]  # * 2
    y_pos = np.arange(len(objects))

    plt.subplot(221)
    plt.bar(y_pos, average, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('time')
    plt.title('Average execution time')

    plt.subplot(222)
    plt.bar(y_pos, failures, align='center', alpha=0.5, color='red')
    plt.xticks(y_pos, objects)
    plt.ylabel('amount')
    plt.title('Amount of failed tests')

    plt.subplot(223)
    plt.bar(y_pos, max_time, align='center', alpha=0.5, color='orange')
    plt.xticks(y_pos, objects)
    plt.ylabel('time')
    plt.title('Max execution time')

    plt.subplot(224)
    plt.bar(y_pos, min_time, align='center', alpha=0.5, color='green')
    plt.xticks(y_pos, objects)
    plt.ylabel('time')
    plt.title('Min execution time')

    plt.show()


if __name__ == '__main__':
    do_it()
    collect_statistics()
    building_plots()
