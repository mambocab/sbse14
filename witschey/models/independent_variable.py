from __future__ import division, print_function
# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

import random


class IndependentVariable(object):
    """
    An independent variable for a model.

    >>> iv = IndependentVariable(0, 10)
    >>> iv.lo, iv.hi
    (0, 10)

    Call an independent variable object to generating random variables within
    its range:

    >>> random.seed(1); iv(), iv(), iv()
    (1.3436424411240122, 8.474337369372327, 7.6377461897661405)

    Provices a `clip` method to return a variable clipped within the bounds
    of the variable:

    >>> iv.clip(10.5), iv.clip(-100), iv.clip(4.2)
    (10, 0, 4.2)
    """

    def __init__(self, lo, hi, type=float):
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
        """
        Clip the input number within the bounds of the independent variable.
        """
        return max(self.lo, min(self.hi, x))

    @property
    def lo(self):
        """
        Return the lower bound on values for this independent variable.
        Write-only.
        """
        return self._lo

    @property
    def hi(self):
        """
        Return the upper bound on values for this independent variable.
        Write-only.
        """
        return self._hi
