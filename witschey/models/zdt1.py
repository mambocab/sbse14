# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from __future__ import division
import math

from model import Model
from independent_variable import IndependentVariable as IV

class ZDT1(Model):
    def __init__(self, ivs=30):

        f1 = lambda xs: xs[0]
        self.f1 = f1

        g = lambda xs: 1 + 9 * sum(xs[1:]) / (len(xs) - 1)
        self.g = g

        def f2(xs):
            gxs = g(xs)
            return gxs * (1 - math.sqrt(xs[0] / gxs))
        self.f2 = f2

        ivs = tuple(IV(min=0, max=1) for _ in xrange(30))
        super(ZDT1, self).__init__(independents=ivs, dependents=(f1, f2, g))
