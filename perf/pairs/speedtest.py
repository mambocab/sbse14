from __future__ import print_function

import itertools

def pairs_2(xs):
    for p in itertools.izip(xs[:-1], xs[1:]): 
        yield p

def pairs_0(lst):
    last = object()
    dummy = last
    for x in lst:
        if last is not dummy:
            yield last,x
        last = x

def pairs_1(xs):
    for ii in range(1,len(xs)):
        yield xs[ii-1], xs[ii]

d = {2: pairs_2, 0: pairs_0, 1: pairs_1}

def test(i, n, w):
    r = range(2 ** n)
    if w is list:
        r = list(r)
    big_list = list(d[i](r))

