from __future__ import division, print_function, unicode_literals

import random
import functools
import sys
import math
import itertools
import collections


def pretty_input(t):
    float_format = lambda x: '{: .2f}'.format(x)
    str_tuple = tuple(float_format(x).encode(sys.stdout.encoding) for x in t)
    return ', '.join(s for s in str_tuple)


def pairs(xs):
    # from https://docs.python.org/2/library/itertools.html
    a, b = itertools.tee(xs)
    next(b, None)
    for p in itertools.izip(a, b):
        yield p


class memo(object):  # noqa -- TODO: rethink this name
    '''adapted from https://github.com/timm/sbse14/wiki/basepy'''

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_str(self, depth=0, indent=4, infix=': ', sep=', ', d=None):
        return '{\n' + self._to_str(
            depth=depth + 1,
            indent=indent,
            infix=infix,
            sep=sep,
            d=self.__dict__ if d is None else d) + '}'

    def _to_str(self, depth, indent, infix, sep, d):
        after, before = [], []
        rv = ' ' * depth * indent
        for k in sorted([s for s in d.keys() if s[0] != '_']):
            val = d[k]
            if isinstance(val, memo) or type(val) == dict:
                after.append(k)
            else:
                before.append('{}{}{}'.format(k, infix, repr(val)))
        rv += sep.join(before)
        if after:
            rv += ','
        rv += '\n'

        for k in after:
            rv += ''.join([' ' * depth * indent, k, infix, '{\n'])
            k = d[k]
            k = k if type(k) == dict else k.__dict__
            rv += ''.join([self._to_str(depth=depth+1, indent=indent,
                           infix=infix, sep=sep, d=k),
                           ' ' * depth * indent,
                           '}\n'])

        return rv


def memoize(f):
    'memoizer for single-arg functions'
    d = {}

    @functools.wraps(f)
    def wrapper(x):
        try:
            return d[x]
        except KeyError:
            d[x] = f(x)
            return d[x]

    return wrapper


@memoize
def memo_sqrt(x):
    return math.sqrt(x)


def tuple_replace(t, replace_at, value):
    return tuple(value if i == replace_at else v for i, v in enumerate(t))


def random_index(x):
    if isinstance(x, dict):
        return random.choice(x.keys)
    if isinstance(x, collections.Iterable):
        return random.randint(0, len(x) - 1)
    raise ValueError('{} is not a list, tuple or dict'.format(x))


class StringBuilder(object):
    def __init__(self, *args):
        self._s = ''.join(args)
        self._next = []

    def append(self, arg):
        'recurse through iterables in args, adding all strings to _next '
        'raises TypeError if it finds a non-Iterable non-string'
        if isinstance(arg, basestring):
            self._next.append(arg)
        elif isinstance(arg, collections.Iterable):
            map(self.append, arg)
        else:
            raise TypeError('{} not a string or iterable'.format(arg))

    def __iadd__(self, arg):
        self.append(arg)
        return self

    def as_str(self):
        'build and cache _s if necessary, then return it.'
        if self._next:
            self._s += ''.join(self._next)
            self._next = []
        return self._s

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.as_str())


class NullObject(object):
    __slots__ = ()

    def __init__(self, *args, **kw):
        return None

    def __getattribute__(self, *name, **kw):
        return self

    def __setattr__(self, *args, **kw):
        return self

    def __iadd__(self, *args, **kw):
        return self

    def __call__(self, *args, **kw):
        return self

    def __bool__(self, *args, **kw):
        return False

    __nonzero__ = __bool__

The = memo(
    Searcher=memo(era_length=50, terminate_early=True,
                  log_eras_best_energy=True, log_eras_by_objective=False,
                  iterations=1000, p_mutation=1/3, epsilon=.01),
    SimulatedAnnealer=memo(cooling_factor=.8),
    MaxWalkSat=memo(),
    GeneticAlgorithm=memo(population_size=50, p_mutation=.6),
    DifferentialEvolution=memo(generations=100, n_candiates=100,
                               f=.75, p_crossover=.3))
