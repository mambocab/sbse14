# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from __future__ import division
import math

from model import Model
from independent_variable import IndependentVariable as IV

class DTLZ7(Model):
    def __init__(self, ivs=20):

        # h/t http://stackoverflow.com/a/13184536/3408454
        # dynamically generate these suckers

        generated_fs = []
        for x in xrange(1, ivs):
            f = lambda xs: xs[x]
            f.__name__ = 'f{}'.format(x)
            generated_fs.append(f)

        def g(xs):
            return 1 + (9 / abs(xs[-1])) * sum(xs)

        def h(xs, fs=generated_fs, g=g):
            s = 0
            for f in fs:
                fxs = f(xs)
                a = fxs / (1 + g(xs))
                b = 1 + math.sin(3 * math.pi * fxs)
                s += a * b

            return ivs - s

        def final_f(xs):
            return (1 + g(xs)) * h(xs)
        final_f.__name__ = 'f{}'.format(ivs)

        fs = tuple(generated_fs + [final_f])

        ivs = tuple(IV(min=0, max=1) for _ in xrange(30))
        super(DTLZ7, self).__init__(independents=ivs, dependents=fs)
