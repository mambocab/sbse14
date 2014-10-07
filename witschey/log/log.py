from __future__ import division, print_function
import random, functools
from witschey.base import memo
import witschey.base

class Log(object):
    """Keep a random sample of stuff seen so far. Based on Dr. Menzies'
    implementation."""

    def __init__(self, inits=None, label=None, max_size=256):
        self._cache            = []
        self._n                = 0
        self._report           = None
        self.label             = label or ''
        self.max_size          = max_size
        self._valid_statistics = False
        if inits:
            map(self.__iadd__, inits)

    def random_index(self):
        return base.random_index(self._cache)

    def __iadd__(self, x):
        if x is None:
            return x

        if isinstance(x, Log):
            map(self.__iadd__, x._cache)

        self._n += 1
        changed = False

        # if cache has room, add item
        if self.max_size is None or len(self._cache) < self.max_size:
            changed = True
            self._cache.append(x)
        # cache is full: maybe replace an old item
        else: 
            # items less likely to be replaced later in the run:
            # leads to uniform sample of entire run
            if random.random() <= self.max_size / self._n:
                changed = True
                self._cache[self.random_index()] = x

        if changed:
            self._invalidate_statistics()
            self._change(x)

        return self

    def __add__(self, x):
        inits = self._cache + x._cache
        return NumberLog(inits=inits, label='generated via __add__', max_size=None)

    def any(self):
        return random.choice(self._cache)

    def report(self):
        if self._report is None:
            self._report = self.generate_report()
        return self._report

    def setup(self):
        raise NotImplementedError()

    def contents(self):
        # slow, but most generic copy implementation
        return copy.deepcopy(self._cache)

    def _invalidate_statistics(self):
        '''
        default implementation. if _valid_statistics is something other than
        a boolean, reimplement!
        '''
        self._valid_statistics = False

    def ish(self, *args, **kwargs):
        raise NotImplementedError()

    def _change(self, x):
        '''
        override to add incremental updating functionality
        '''
        pass

    def _prepare_data(self):
        s = '_prepare_data() not implemented for ' + self.__class__.__name__
        raise NotImplementedError(s)

    @staticmethod
    def log_for(t):
        if t == int or t == float or isinstance(t, (int, float)):
            return NumberLog()
        else:
            return SymbolLog()


def statistic(f):
    '''
    decorator for log functions that return statistics about contents.
    if _valid_statistics is False, generate valid stats before calling
    the wrapped function.
    '''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]
        if not self._valid_statistics:
            self._prepare_data()
        return f(*args, **kwargs)

    return wrapper
