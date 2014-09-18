from __future__ import division, print_function, unicode_literals

import json, random, functools, sys, math

def pretty_input(t):
    float_format = lambda x: '{: .2f}'.format(x)
    str_tuple = tuple(float_format(x).encode(sys.stdout.encoding) for x in t)
    return ', '.join(s for s in str_tuple)

def pairs(xs):
    for p in zip(xs[:-1], xs[1:]):
        yield p

class memo():
    '''adapted from https://github.com/timm/sbse14/wiki/basepy'''
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # from http://stackoverflow.com/a/15538391/3408454
    def to_JSON(self, indent=None):
        'adapted from from http://stackoverflow.com/a/15538391/3408454'

        d = lambda o: o.__dict__
        return json.dumps(self, default=d, sort_keys=True, indent=indent)

    def to_str(self, depth=0, indent=4, sep='\u2192', d=None):
        return self._to_str(
            depth=depth,
            indent=indent,
            sep=sep,
            d = self.__dict__ if d is None else d)

    def _to_str(self, depth, indent, d, sep):
        after = []
        reps = []
        rv = ''
        for k in sorted([s for s in d.keys() if s[0] != '_']):
            val = d[k]
            if isinstance(val, (memo, dict)):
                after.append(k)
            else:
                if callable(val):
                    val = val.__name__ + '()'
                reps.append('{}{}{}'.format(k, sep, val))
        rv += ' ' * depth * indent
        rv += ', '.join(reps)
        rv += '\n'

        for k in after:
            rv += ' ' * depth * indent
            rv += '{ '
            rv += '{}:\n'.format(k)
            k = d[k]
            k = k if isinstance(k, dict) else k.__dict__
            rv += self._to_str(depth=depth+1, indent=indent, d=k)
            rv += ' ' * depth * indent
            rv += '}'
            rv += '\n'

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
    if isinstance(x, list):
        return random.randint(0, len(x) - 1)
    if isinstance(x, dict):
        return random.choice(x.keys)
    raise ValueError('{} is not a list or dict'.format(x))
