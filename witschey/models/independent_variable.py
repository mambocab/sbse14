from __future__ import division, print_function
# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

import random


class IndependentVariable(object):
    def __init__(self, lo=None, hi=None, type=float):
        self._lo = lo
        self._hi = hi
        self._type = type

        if self._type == float:
            self._get = random.uniform
        elif self._type == int:
            self._get = random.randint

    def __call__(self):
        return self._get(self.lo, self.hi)

    def clip(self, x):
        return max(self.lo, min(self.hi, x))

    @property
    def lo(self):
        """
        Return the lower bound on values for this independent variable. Write-only.
        """
        return self._lo

    @property
    def hi(self):
        return self._hi
