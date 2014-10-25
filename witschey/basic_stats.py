from __future__ import division, print_function

import itertools
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


def standard_deviation(xs, mean_val=None):
    if mean_val is None:
        mean_val = mean(xs)
    return base.memo_sqrt(sum((x - mean_val) ** 2 for x in xs))


def norm(x, a, b):
    lo, hi = min(a, b), max(a, b)
    return (x - lo) / (hi - lo)


def value_at_proportion(p, xs):
    return xs[int(round(len(xs) - 1) * p)]


def percentile(x, xs, is_sorted=False):
    if not is_sorted:
        xs = sorted(xs)
    before = len(tuple(itertools.ifilter(lambda y: y < x, xs)))
    return before / len(xs)


def xtile(xs, lo=None, hi=None, width=50,
          marks=(' ', '-', ' ', ' ', '-', ' '),
          bar='|', star='*', show=' {:6.2f}',
          as_list=False):
    '''Take an iterable of numbers and present them as a horizontal xtile
    ascii chart. The chart is a contracted quintile showing the 10th, 30th,
    50th, 70th, and 90th percentiles.
    '''
    xs = sorted(xs)

    lo = min(xs) if lo is None else min(lo, *xs)
    hi = max(xs) if hi is None else max(hi, *xs)
    if hi == lo:
        hi += .001  # ugh
    chops_marks = zip((.1, .3, .5, .7, .9, 1), marks)
    cursor = 0

    out = [None] * width

    for i in range(width):

        xs_at_cursor = value_at_proportion(i / (width - 1), xs)

        rank = percentile(xs_at_cursor, xs, is_sorted=True)

        while rank > chops_marks[cursor][0]:
            cursor += 1
        out[i] = chops_marks[cursor][1]

    out[width // 2] = bar

    ind = int(norm(value_at_proportion(.5, xs), lo, hi) * width)
    out[ind] = star

    if as_list:
        rv = ['(' + ''.join(out) + ")"]
        rv.extend((show.format(value_at_proportion(x, xs))
                  for x in (.1, .3, .5, .7, .9)))
        return rv

    return ''.join(out) + "," + ','.join(
        [show.format(value_at_proportion(x, xs))
         for x in (.1, .3, .5, .7, .9)])
