# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from __future__ import division
import math

from model import Model
from independent_variable import IndependentVariable as IV
from witschey.base import memo_sqrt

class Fonseca(Model):
    def __init__(self, ivs=3):
        ivs = tuple(IV(min=-4, max=4) for _ in xrange(ivs - 1))

        def f1(xs):
            e = sum((x - (1 / memo_sqrt(i+1))) ** 2 for i, x in enumerate(xs))
            return 1 - math.exp(-e)

        self.f1 = f1

        def f2(xs):
            e = sum((x + (1 / memo_sqrt(i+1))) ** 2 for i, x in enumerate(xs))
            return 1 - math.exp(-e)

        self.f2 = f2

        super(Fonseca, self).__init__(independents=ivs, dependents=(f1, f2))
