from __future__ import division
import sys
import random
import math
from itertools import chain

from log import NumberLog
import texttable
from basic_stats import xtile, median
from witschey import base, basic_stats
from witschey.base import memo_sqrt

# flake8: noqa

def a12(lst1,lst2):
    "how often is x in lst1 more than y in lst2?"
    def loop(t,t1,t2): 
        while t1.j < t1.n and t2.j < t2.n:
            h1 = t1.l[t1.j]
            h2 = t2.l[t2.j]
            h3 = t2.l[t2.j+1] if t2.j+1 < t2.n else None 
            if h1>  h2:
                t1.j  += 1; t1.gt += t2.n - t2.j
            elif h1 == h2:
                if h3 and h1 > h3 :
                    t1.gt += t2.n - t2.j  - 1
                t1.j  += 1; t1.eq += 1; t2.eq += 1
            else:
                t2,t1  = t1,t2
        return t.gt*1.0, t.eq*1.0
    #--------------------------
    lst1 = sorted(lst1, reverse=True)
    lst2 = sorted(lst2, reverse=True)
    n1   = len(lst1)
    n2   = len(lst2)
    t1   = base.memo(l=lst1,j=0,eq=0,gt=0,n=n1)
    t2   = base.memo(l=lst2,j=0,eq=0,gt=0,n=n2)
    gt,eq= loop(t1, t1, t2)
    return gt/(n1*n2) + eq/2/(n1*n2)


def testStatistic(y, z): 
    """Checks if two means are different, tempered
     by the sample size of 'y' and 'z'"""
    delta = z.mean() - y.mean()
    sd_y = y.standard_deviation()
    sd_z = z.standard_deviation()

    if sd_y + sd_z:
        delta /= memo_sqrt(sd_y / len(y) + sd_z / len(z))

    return delta


def bootstrap(y0, z0, conf=0.01, b=1000):
    """
    The bootstrap hypothesis test from p220 to 223 of Efron's book 'An
    introduction to the boostrap.

    Simple way to describe: "If you randomly generate 1000 similar datasets,
    is a likely to be significantly different to b?"
    """
    y, z   = NumberLog(y0), NumberLog(z0)
    x      = NumberLog(inits=(y, z))
    tobs   = testStatistic(y,z)
    yhat   = tuple(y1 - y.mean() + x.mean() for y1 in y.contents())
    zhat   = tuple(z1 - z.mean() + x.mean() for z1 in z.contents())
    bigger = 0
    for i in range(b):
        # sample with replacement for yhat and zhat
        swr_yhat = (random.choice(yhat) for _ in yhat)
        swr_zhat = (random.choice(zhat) for _ in zhat)
        mean_difference = testStatistic(
            NumberLog(swr_yhat, max_size=None),
            NumberLog(swr_zhat, max_size=None))
        if mean_difference > tobs:
            bigger += 1
    return bigger / b < conf


def different(l1,l2):
    """
    Quick test to see if 2 things are different. A12 is a reasonable first
    approximation, and fast, and if it gets past A12, run the slower, more
    authoritative, bootstrap.
    """
    return a12(l2,l1) and bootstrap(l1,l2)


def scottknott(data, max_rank_size=3, epsilon=0.01):
    """
    Recursively split data, maximizing delta of the expected value of the
    mean before and after the splits. Reject splits with under max_rank_size
    items.
    """
    flat_data = [x for log in data for x in log.contents()]
    data_mean = basic_stats.mean(flat_data)

    def recurse(parts, rank=0):
        "Split, then recurse on each part."

        cut = minMu(parts, data_mean, len(flat_data), max_rank_size, epsilon)
        if cut:
            # if cut, rank "right" higher than "left"
            rank = recurse(parts[:cut], rank) + 1
            rank = recurse(parts[cut:], rank)
        else: 
            # if no cut, then all get same rank
            for part in parts:
                part.rank = rank
        return rank


    recurse(sorted(data, key=lambda x: x.median()))
    return data

def minMu(parts, data_mean, data_size, max_rank_size, epsilon):
    """Find a cut in the parts that maximizes the expected value of the
    difference in the mean before and after the cut. Reject splits that are
    insignificantly different or that generate very small subsets.
    """
    cut = None
    max_delta = 0
    mrs = max_rank_size
    for i, left, right in leftRight(parts, epsilon):
        if len(parts[:i]) >= mrs and len(parts[i:]) >= mrs:
            delta = len(left) / data_size * (data_mean - left.mean()) ** 2
            delta += len(right) / data_size * (data_mean - right.mean()) ** 2

            if abs(delta) > max_delta and different(parts[i-1], parts[i]):
                max_delta, cut = abs(delta), i
    return cut


def leftRight(parts,epsilon=0.01):
    """For each item in 'parts', yield the splitting index, everything to the
    beginning (including the item) and everything to the end.
    """
    for i in range(1, len(parts)):
        if parts[i].median() - parts[i - 1].median() > epsilon:
            left = NumberLog((p for p in parts[:i]), max_size=None)
            right = NumberLog((p for p in parts[i:]), max_size=None)
            yield i, left, right


def rdiv_report(data):
    """
    Generate a tabular report on the data. Assumes data is in lists, where the
    first element of each list is its name.
    """
    # wrap each line in a NumberLog
    data = map(lambda xs: NumberLog(label=xs[0], inits=xs[1:], max_size=None),
               data)

    # sort by rank & median within each rank
    # sorting is stable, so sort by median first, then rank
    ranked = sorted((x for x in scottknott(data, max_rank_size=1)),
                     key=lambda y: y.median())
    ranked = tuple(sorted(ranked, key=lambda y: y.rank))

    # get high and low values for entire dataset
    lo = min(log.lo for log in data)
    hi = max(log.hi for log in data)

    # generate column names
    rows = [['rank', 'name', 'med', 'iqr', '',
            '10%', '30%', '50%', '70%', '90%']]

    # generate rows
    for x in ranked:
        # each row starts with 'rank label, median, iqr'
        next_row = [x.rank + 1]
        next_row.append(x.label + ',')
        next_row.append('{0:0.2},'.format(x.median()))
        next_row.append('{0:0.2}'.format(x.iqr()))

        # get xtile: '( -* | -- ) ##, ##, ##, ##, ##'
        xtile_out = xtile(x.contents(), lo=lo, hi=hi, width=30, as_list=True)
        # xtile is displayed as the whisker plot, then comma-separated values
        row_xtile = [xtile_out[0]]
        # don't use `join`, we want each to be its own list element
        row_xtile.extend(map(lambda x: x + ',', xtile_out[1:-1]))
        row_xtile.append(xtile_out[-1])

        next_row.extend(row_xtile)
        rows.append(next_row)

    table = texttable.Texttable(200)
    table.set_precision(2)
    table.set_cols_dtype(['t', 't', 't', 't', 't', 't', 't', 't', 't', 't'])
    table.set_cols_align(['r', 'l', 'l', 'r', 'c', 'r', 'r', 'r', 'r', 'r'])
    table.set_deco(texttable.Texttable.HEADER)
    table.add_rows(rows)
    return table.draw()
