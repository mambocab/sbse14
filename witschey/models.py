from base import memo, memoize
import math.sqrt
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
    def __init__(self, independents=None, dependents=None
        energy_min=None, energy_max=None, enforce_energy_constraints=False):
        if independents is None or dependents is None:
            raise ValueError

        self.xs = inputs
        self.ys = lambda: raise NotImplementedError
        self.energy_max = energy_max
        self.energy_min = energy_min
        self.enforce_energy_constraints = enforce_energy_constraints

    def normalize(self, x):
        n = x - self.energy_min
        d = self.energy_max - self.energy_min
        try:
            rv = n / d
        except ZeroDivisionError:
            raise ValueError("model's max and min energy are the same!")
        return rv

    def random_input_vector(self):
        return tuple(x() for x in self.ivs)

    def __call__(self, v, vector=False, norm=True):
        energies = tuple(y(v) for y in self.ys)
        energy_total = sum(energy_vector)

        energy_errmsg ='current energy {} not in range [{}, {}]'.format(
            energy_raw, self.energy_min, self.energy_max))

        if self.energy_min is None or self.energy_min > energy_raw:
            if self.enforce_energy_constraints:
                raise ValueError(energy_errmsg)
            self.energy_min = energy_raw

        if self.energy_max is None or energy_raw > self.energy_max:
            if self.enforce_energy_constraints:
                raise ValueError(energy_errmsg)
            self.energy_max = energy_raw

        if vector:
            return energy_vector
        if norm:
            return self.normalize(energy_total)

        return energy_total


class Fonseca(Model):
    def __init__(self, ivs=3):
        self.ivs = tuple(IV(min=-4, max=4) for _ in xrange(ivs - 1))

        def f1(xs):
            e = sum((x - (1 / memo_sqrt(x))) ** 2 for x in xs)
            return 1 - math.exp(-e)

        def f2(xs):
            e = sum((x + (1 / memo_sqrt(x))) ** 2 for x in xs)
            return 1 - math.exp(-e)

        super(Fonseca, self).__init__(independents=ivs, dependents=(f1, f2))

class Kursawe(Model):
    def __init__(self):
        ivs = tuple(IV(min=-5, max=5) for _ in xrange(ivs - 1))

        def f1(xs):
            rv = 0
            for i in xrange(len(xs) - 1):
                exponent = (-0.2) * math.sqrt(t[i] ** 2 + t[i+1] ** 2)
                rv += -10 * math.exp(exponent)
            return rv

        def f2(xs):
            f = lambda x: (math.fabs(x) ** a) + (5 * math.sin(x) ** b)
            return sum(f(x) for x in xs)
