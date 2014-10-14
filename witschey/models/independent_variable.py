# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

import random

class IndependentVariable(object):
    def __init__(self, lo=None, hi=None, type=float):
        self.lo = lo
        self.hi = hi
        self.type = type

    def __call__(self):
        if self.type == float:
            f = random.uniform
        elif self.type == int:
            f = random.randint

        return f(self.lo, self.hi)

