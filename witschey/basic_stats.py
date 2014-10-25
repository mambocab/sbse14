from __future__ import division, print_function

import math

import base


def median(xs, is_sorted=False):
    """
    Return the median of the integer-indexed object passed in. To save sorting
    time, the client can pass in is_sorted=True to skip the sorting step.
    """
    # implementation from http://stackoverflow.com/a/10482734/3408454
    if not is_sorted:
        xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2] + xs[n // 2 - 1]) / 2


def mean(xs):
    "Returns the mean of the iterable argument."
    return sum(xs) / len(xs)


def iqr(xs):
    n = len(xs)
    return xs[int(n * .75)] - xs[int(n * .25)]


def standard_deviation(xs, mean=None):
    if mean is None:
        mean = mean(xs)
    return math.sqrt((sum(x - mean) for x in xs) ** 2)


def norm(x, lo, hi):
    return (x - lo) / (hi - lo)


def xtile(xs, lo=0, hi=0.001, width=50,
          chops=[0.1, 0.3, 0.5, 0.7, 0.9], marks=["-", " ", " ", "-", " "],
          bar="|", star="*", show=" {: >6.2f}",
          as_list=False):
    """Take an iterable of numbers and present them as a horizontal xtile
    ascii chart. The default is a contracted quintile showing the 10th, 30th,
    50th, 70th, and 90th percentiles. These breaks can be customized with the
    chops parameter.
    """

    xs = sorted(xs)

    lo, hi = min(lo, xs[0]), max(hi, xs[-1])
    if hi == lo:
        hi += .001  # ugh

    out = [' '] * width

    pos = lambda p: xs[int(len(xs) * p)]
    place = lambda x: min(width-1, int(len(out) * norm(x, lo, hi)))

    what = [pos(p) for p in chops]
    where = [place(n) for n in what]

    for one, two in base.pairs(where):
        for i in range(one, two):
            out[i] = marks[0]
        marks = marks[1:]

    out[int(width / 2)] = bar
    out[place(pos(0.5))] = star

    if as_list:
        rv = ['(' + ''.join(out) + ")"]
        rv.extend(show % x for x in what)
        return rv

    return ''.join(out) + "," + ','.join([show.format(x) for x in what])
