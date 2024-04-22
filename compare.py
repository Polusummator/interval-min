import decimal
import time
import unittest
from dataclasses import dataclass
from decimal import Decimal
from itertools import product
import timeout_decorator
import pandas as pd
import numpy as np
from parameterized import parameterized
import re
from random import *
import matplotlib.pyplot as plt
from extremum_estimator import get_extremum_estimation, EXTENSIONS, METHODS, DIFFS
from mp_exp import Interval

TIMEOUT = 5
a = []


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


koefs = [str(i) for i in range(-100, 101)]
degs = [i for i in range(0, 16)]


def generate():
    f = ""
    m = randint(0, 15)
    m += 1
    koefk = sample(koefs, m)
    degk = sample(degs, m)
    degk = sorted(degk)
    degk.reverse()
    degk = [str(i) for i in degk]
    # print(koefk, degk)
    f += koefk[0] + " * x**(" + degk[0] + ")"
    for i in range(1, m):
        if koefk[i] == '0':
            continue
        if degk[i] == '1':
            if int(koefk[i]) > 0:
                f += " + " + koefk[i] + " * x"
            else:
                f += " - " + str(-int(koefk[i])) + " * x"
            continue
        if degk[i] == '0':
            if int(koefk[i]) > 0:
                f += " + " + koefk[i]
            else:
                f += " - " + str(-int(koefk[i]))
            continue
        if int(koefk[i]) > 0:
            f += " + " + koefk[i] + " * x**(" + degk[i] + ")"
        else:
            f += " - " + str(-int(koefk[i])) + " * x**(" + degk[i] + ")"
    return f


values = []


def do_it():
    method = "moore_skelboe"
    index = 0

    for _ in range(20):
        i = dict()
        i['x'] = Interval(-10, 10)
        f = generate()
        test = TestData(name='base', func=f,
                        answer=decimal.Decimal(0), intervals=i,
                        precision=decimal.Decimal('0.01'))
        x = []
        print(f)
        for extension in EXTENSIONS.keys():
            for diff in DIFFS.keys():
                try:
                    t = time.time()
                    result = limited_extremum_estimation_execution(test, extension, method, diff)
                    real_time = time.time() - t
                    x.append(real_time)
                    print(f"method: {method}\nextension: {extension}\ndiff: {diff}\nstatus: passed\ntest name: {index}\ntime: {real_time}")
                    print()
                except:
                    x.append(None)
                    print(f"method: {method}\nextension: {extension}\ndiff: {diff}\nstatus: failed\ntest name: {index}\ntime: infinity")
                    print()
                index += 1
        values.append(x)


do_it()
max_time = [-1, -1, -1, -1, -1, -1]
min_time = [10000, 10000, 10000, 10000, 10000, 10000]
middle = [[20, 0], [20, 0], [20, 0], [20, 0], [20, 0], [20, 0]]
for x in values:
    print(x)
    for i in range(0, 6):
        if x[i] is None:
            middle[i][0] -= 1
            continue
        max_time[i] = max(max_time[i], x[i])
        min_time[i] = min(min_time[i], x[i])
        middle[i][1] += x[i]
print(middle)
average = []
failures = []

for x in middle:
    print(x[1] / x[0])
    average.append(x[1] / x[0])
    failures.append(20 - x[0])

objects = ('natural\nsympy_forward_mode', 'natural\nslopes_forward_mode', 'centred_form\nsympy_forward_mode', 'centred_form\nslopes_forward_mode', 'bicentred_form\nsympy_forward_mode', 'bicentred_form\nslopes_forward_mode')
y_pos = np.arange(len(objects))

plt.subplot(221)
plt.bar(y_pos, average, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('time')
plt.xticks(rotation=315)
plt.title('Average execution time')

plt.subplot(222)
plt.bar(y_pos, failures, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('amount')
plt.xticks(rotation=315)
plt.title('Amount of failed tests')

plt.subplot(223)
plt.bar(y_pos, max_time, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('time')
plt.xticks(rotation=315)
plt.title('Max execution time')

plt.subplot(224)
plt.bar(y_pos, min_time, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('time')
plt.xticks(rotation=315)
plt.title('Min execution time')

plt.show()
