from __future__ import print_function

from base import memo, memoize
import math
import random

@memoize
def memo_sqrt(x):
    return math.sqrt(x)

# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

class IndependentVariable(object):
    def __init__(self, min=None, max=None, type=float):
        self.min = min
        self.max = max
        self.type = type

    def __call__(self):
        if self.type == float:
            f = random.uniform
        elif self.type == int:
            f = random.randint

        return f(self.min, self.max)

IV = IndependentVariable

class Model(object):
    def __init__(self, independents=None, dependents=None,
        energy_min=None, energy_max=None, enforce_energy_constraints=False):
        if independents is None or dependents is None:
            raise ValueError

        self.xs = independents
        self.ys = dependents
        self.energy_max = energy_max
        self.energy_min = energy_min
        self.enforce_energy_constraints = enforce_energy_constraints

    def normalize(self, x):
        n = x - self.energy_min
        d = self.energy_max - self.energy_min
        try:
            return n / d
        except ZeroDivisionError:
            return 0.5

    def random_input_vector(self):
        return tuple(x() for x in self.xs)

    def __call__(self, v, vector=False, norm=False):
        energy_vector = tuple(y(v) for y in self.ys)
        energy_total = sum(energy_vector)

        if self.enforce_energy_constraints:
            energy_errmsg ='current energy {} not in range [{}, {}]'.format(
                energy_total, self.energy_min, self.energy_max)

        if self.energy_min is None or self.energy_min > energy_total:
            if self.enforce_energy_constraints:
                raise ValueError(energy_errmsg)
            self.energy_min = energy_total

        if self.energy_max is None or energy_total > self.energy_max:
            if self.enforce_energy_constraints:
                raise ValueError(energy_errmsg)
            self.energy_max = energy_total

        if vector:
            return energy_vector
        if norm:
            return self.normalize(energy_total)

        return energy_total


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

class Kursawe(Model):
    def __init__(self, ivs=3, a=0.8, b=3):
        ivs = tuple(IV(min=-5, max=5) for _ in xrange(ivs - 1))
        self.a = a
        self.b = b

        def f1(xs):
            rv = 0
            for i in xrange(len(xs) - 1):
                exponent = (-0.2) * math.sqrt(xs[i] ** 2 + xs[i+1] ** 2)
                rv += -10 * math.exp(exponent)
            return rv

        self.f1 = f1

        def f2(xs):
            f = lambda x: (math.fabs(x)**self.a) + (5 * math.sin(x)**self.b)
            return sum(f(x) for x in xs)

        self.f2 = f2

        super(Kursawe, self).__init__(independents=ivs, dependents=(f1, f2))

class Schaffer(Model):
    def __init__(self, ivs=1):
        ivs = tuple(IV(min=-10^5, max=10^5) for _ in xrange(ivs))
        self.f1 = lambda xs: sum(x ** 2 for x in xs)
        self.f2 = lambda xs: sum((x - 2) ** 2 for x in xs)

        super(Schaffer, self).__init__(
            independents=ivs,dependents=(self.f1, self.f2))

class ZDT1(Model):
    def __init__(self, ivs=30):

        f1 = lambda xs: xs[0]
        self.f1 = f1

        g = lambda xs: 1 + 9 * sum(xs[1:]) / (len(xs) - 1)

        def f2(xs):
            gxs = g(xs)
            return gxs * (1 - math.sqrt(xs[0] / gxs))
        self.f2 = f2

        ivs = tuple(IV(min=0, max=1) for _ in xrange(30))
        super(ZDT1, self).__init__(independents=ivs, dependents=(f1, f2))
