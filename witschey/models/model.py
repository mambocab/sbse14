from __future__ import division, print_function

# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from abc import ABCMeta


class Model(object):
    # allows us to get all subclasses with __subclasses__()
    __metaclass__ = ABCMeta

    def __init__(self, independents=None, dependents=None,
                 energy_min=None, energy_max=None,
                 enforce_energy_constraints=False):
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

    def __call__(self, v, norm=False):
        energy_vector = tuple(y(v) for y in self.ys)
        energy_total = sum(energy_vector)

        if self.enforce_energy_constraints:
            energy_errmsg = 'current energy {} not in range [{}, {}]'.format(
                energy_total, self.energy_min, self.energy_max)

        if self.energy_min is None or self.energy_min > energy_total:
            if self.enforce_energy_constraints:
                raise ValueError(energy_errmsg)
            self.energy_min = energy_total

        if self.energy_max is None or energy_total > self.energy_max:
            if self.enforce_energy_constraints:
                raise ValueError(energy_errmsg)
            self.energy_max = energy_total

        return energy_vector

    def energy(self, energy_vector):
        return sum(energy_vector)
