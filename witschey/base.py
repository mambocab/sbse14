from __future__ import division, print_function, unicode_literals

import json, random, functools, sys, math, itertools

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

class memo(object):
    '''adapted from https://github.com/timm/sbse14/wiki/basepy'''

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def to_str(self, depth=0, indent=4, sep=': ', d=None):
        return self._to_str(
            depth=depth,
            indent=indent,
            sep=sep,
            d = self.__dict__ if d is None else d)

    def _to_str(self, depth, indent, sep, d):
        after = []
        reps = []
        rv = ''
        for k in sorted([s for s in d.keys() if s[0] != '_']):
            val = d[k]
            if isinstance(val, memo) or type(val) == dict:
                after.append(k)
            else:
                if callable(val):
                    val = val.__name__ + '()'
                reps.append('{}{}{}'.format(k, sep, val))
        rv += ' ' * depth * indent
        rv += ', '.join(reps)
        rv += '\n'

        for k in after:
            rv += ''.join([' ' * depth * indent,
                '{' + ' {}:\n'.format(k)])
            k = d[k]
            k = k if type(k) == dict else k.__dict__
            rv += ''.join([self._to_str(depth=depth+1, indent=indent, sep=sep, d=k),
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
    if isinstance(x, (list, tuple)):
        return random.randint(0, len(x) - 1)
    if isinstance(x, dict):
        return random.choice(x.keys)
    raise ValueError('{} is not a list, tuple or dict'.format(x))

The = memo(
    Searcher=memo(era_length=50, terminate_early=True,
        log_eras_energy=False, log_eras_by_objective=False,
        iterations=1000, p_mutation=1/3),
    SimulatedAnnealer=memo(cooling_factor=.8),
    MaxWalkSat=memo(),
    GeneticAlgorithm=memo(population_size=50, p_mutation=.6))
