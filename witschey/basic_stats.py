from __future__ import division, print_function

import sortedcontainers, math

def basic_stats_sorted(xs):
    return xs if isinstance(xs, sortedcontainers.SortedList) else sorted(xs)

def median(xs):
    # implementation from http://stackoverflow.com/a/10482734/3408454
    xs = basic_stats_sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2] + xs[n // 2 - 1]) / 2

def mean(xs):
    print(xs)
    return sum(xs) / len(xs)

def iqr(xs):
    n = len(xs)
    return xs[int(n * .75)] - xs[int(n * .25)]

def standard_deviation(xs, mean=None):
    if mean is None: mean = mean(xs)
    return math.sqrt((sum(x - mean) for x in xs) ** 2)

def norm(x, lo, hi):
    return (x - lo) / (hi - lo)

def xtile(xs, lo=0, hi=0.001,
        width=50,
        chops=[0.1, 0.3, 0.5, 0.7, 0.9],
        marks=["-", " ", " ", "-", " "],
        bar="|", star="*",
        show=" {: >6.2f}"):
    """The function _xtile_ takes a list of (possibly)
    unsorted numbers and presents them as a horizontal
    xtile chart (in ascii format). The default is a 
    contracted _quintile_ that shows the 
    10,30,50,70,90 breaks in the data (but this can be 
    changed- see the optional flags of the function).
    """

    xs = basic_stats_sorted(xs)

    lo = min(lo, xs[0])
    hi = max(hi, xs[-1])
    if hi == lo:
        hi += .001 # ugh

    out     = [' '] * width

    pos = lambda p: xs[int(len(xs) * p)]
    place  = lambda x: min(width-1, int(len(out) * norm(x, lo, hi)))

    what   = [pos(p)   for p in chops]
    where  = [place(n) for n in  what]

    for one, two in base.pairs(where):
        for i in range(one, two): 
            out[i] = marks[0]
        marks = marks[1:]

    out[int(width / 2)]  = bar
    out[place(pos(0.5))] = star

    return ''.join(out) +  "," +  ','.join([show.format(x) for x in what])

