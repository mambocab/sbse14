from __future__ import division, print_function

# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from abc import ABCMeta
from collections import namedtuple


ModelIO = namedtuple('ModelIO', ('xs', 'ys', 'energy'))


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

    def __call__(self, xs, io=False):
        ys = tuple(y(xs) for y in self.ys)
        energy = sum(ys)

        if self.enforce_energy_constraints:
            energy_errmsg = 'current energy {} not in range [{}, {}]'.format(
                energy, self.energy_min, self.energy_max)

        if self.energy_min is None or self.energy_min > energy:
            if self.enforce_energy_constraints:
                raise ValueError(energy_errmsg)
            self.energy_min = energy

        if self.energy_max is None or energy > self.energy_max:
            if self.enforce_energy_constraints:
                raise ValueError(energy_errmsg)
            self.energy_max = energy

        if io:
            return ModelIO(xs, ys, energy)

        return ys

    def energy(self, ys, norm=False):
        rv = sum(ys)
        return self.normalize(rv) if norm else rv

    def compute_model_io(self, xs):
        ys = self(xs)
        return ModelIO(xs, ys, self.energy(ys))

    def random_model_io(self):
        return self.compute_model_io(self.random_input_vector())


class ModelInputException(Exception):
    pass
