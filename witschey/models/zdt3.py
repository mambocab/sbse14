# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from __future__ import division

import math

from model import Model
from independent_variable import IndependentVariable as IV
from witschey.base import memo_sqrt


class ZDT3(Model):

    def __init__(self, ivs=30):

        self.g = lambda xs: 1 + 9 * sum(xs[1:]) / (len(xs) - 1)
        g = self.g

        self.f1 = lambda xs: xs[0]
        f1 = self.f1

        def f2(xs):
            gxs = g(xs)
            a = 1 - memo_sqrt(xs[0] / gxs) - (xs[0] / gxs)
            a *= math.sin(10 * math.pi * xs[0])
            return gxs * a

        ivs = (IV(min=0, max=1) for _ in xrange(30))

        super(ZDT3, self).__init__(independents=ivs, dependents=(f1, f2, g))

