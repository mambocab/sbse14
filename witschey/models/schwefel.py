from __future__ import print_function, division

import math, random

from model import Model
from independent_variable import IndependentVariable as IV

def randint_matrix(x, lo=-100, hi=100):
    "returns x by x matrix of random integers in [lo, hi]"
    return [[random.randint(lo, hi) for i in xrange(x)]
        for j in xrange(x)]

class Schwefel(Model):
    """Schwefel's problem 2.13, as described in "Problem Definitions and
    Evaluation Criteria for the CEC 2005 Special Session on Real-Parameter
    Optimization", p. 15. Quotes in comments are from this description unless
    otherwise"""


    def __init__(self, d=10):
        f_bias = -460 # magic number from model specification

        # input space is d values from -pi to pi
        independents = tuple((IV(min=-math.pi, max=math.pi)
            for _ in xrange(d)))

        # "a_ij, b_ij are integer random numbers in the range [-100, 100]"
        a, b = randint_matrix(d), randint_matrix(d)
        # "alpha... [is a vector] of random numbers in [-pi, pi]"
        alpha = [random.uniform(-math.pi, math.pi) for _ in xrange(d)]

        # 1D matrix of d sums
        A = [sum(a[i][j] * math.sin(alpha[j]) + b[i][j] * math.cos(alpha[j])
                for j in xrange(d))
            for i in xrange(d)]

        def B_sum(i):
            # generate a function for B_i = sum(a_ij sin(x) + b_ij cos(x))
            a_sin = lambda j, x: a[i][j] * math.sin(x)
            b_cos = lambda j, x: b[i][j] * math.cos(x)
            f = lambda x: sum(a_sin(j, x) + b_cos(j, x) for j in xrange(d))
            return f

        # generate 1D matrix of functions B_i
        B = [B_sum(i) for i in xrange(d)]

        # and finally, here's the function to minimize
        def f12(xs):
            if len(xs) != d:
                e = 'len of input vector to {0} must be {0}.d = {1}'.format(
                    self.__name__, d)
                raise ValueError(e)

            return sum((A[i] - B[i](x))**2 + f_bias for i, x in enumerate(xs))

        super(Schwefel, self).__init__(
            independents=independents, dependents=(f12,))
