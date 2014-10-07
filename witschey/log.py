from __future__ import division, print_function
import sys, random, math, datetime, time, re
from base import memo
import base
import functools

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


"""
### Num

A _Num_ is a _Log_ for numbers. 

+ Tracks _lo_ and _hi_ values. 
+ Reports median and the IQR the (75-25)th range.
+ Generates numbers from the log by a three-way interpolation (see _ish()_).


"""
class NumberLog(Log):

    def __init__(self, *args, **kwargs):
        super(NumberLog, self).__init__(*args, **kwargs)
        assert self._n == 0

        # set to values that will be immediately overridden
        self.lo, self.hi = sys.maxint, -sys.maxint

    def _change(self, x):
        # update lo,hi
        self.lo = min(self.lo, x)
        self.hi = max(self.hi, x)

    def _prepare_data(self):
        if not self._valid_statistics:
            self._cache.sort()
        self._valid_statistics = True

    def contents(self):
        return list(self._cache)

    def norm(self,x):
        "normalize the argument with respect to maximum and minimum"
        if self.hi == self.lo:
            raise ValueError('hi and lo of {} are equal'.format(self.__name__))
        return (x - self.lo) / (self.hi - self.lo)

    def generate_report(self):
        return memo(median=self.median(), iqr=self.iqr(),
            lo=self.lo, hi=self.hi)

    def ish(self,f=0.1):
        """return a num likely to be similar to/representative of
        nums in the distribution"""
        return self.any() + f*(self.any() - self.any())

    @statistic
    def median(self):
        # implementation from http://stackoverflow.com/a/10482734/3408454
        n = len(self._cache)

        if n % 2:
            return self._cache[n // 2]

        return (self._cache[n // 2] + self._cache[n // 2 - 1]) / 2

    def mean(self):
        n = len(self._cache)
        return sum(self._cache) / n

    @statistic
    def iqr(self):
        n = len(self._cache)
        return self._cache[int(n*.75)] - self._cache[int(n*.5)]

    def total(self):
        return sum(self._cache)

    def better(self, log2):
        if not self._cache or not log2._cache: return False
        if self.median() < log2.median(): return True
        if self.iqr() < log2.iqr(): return True
        return False

    @statistic
    def xtile(self, lo=0, hi=0.001,
            width=50,
            chops=[0.1, 0.3, 0.5, 0.7, 0.9],
            marks=["-", " ", " ", "-", " "],
            bar="|", star="*",
            show=" {: >6.2f}"):
        """The function _xtile_ takes a list of (possibly)
        unsorted numbers and presents them as a horizontal
        xtile chart (in ascii format). The default is a 
        contracted _quintile_ that shows the 
        10,30,50,70,90 breaks in the data (but this can be 
        changed- see the optional flags of the function).
        """

        lo = min(lo, self._cache[0])
        hi = max(hi, self._cache[-1])
        if hi == lo:
            hi = hi + .001 # ugh


        pos = lambda p: self._cache[int(len(self._cache) * p)]
        place = lambda x: min(width-1, int(width * float((x - lo))/(hi - lo)))
        pretty = lambda xs: ','.join([show.format(x) for x in xs])

        what    = [pos(p)   for p in chops]
        where   = [place(n) for n in  what]

        out     = [' '] * width

        for one,two in base.pairs(where):
            for i in range(one, two): 
                out[i] = marks[0]
            marks = marks[1:]

        out[int(width / 2)]  = bar
        out[place(pos(0.5))] = star

        return ''.join(out) +  "," +  pretty(what)

class SymbolLog(Log):
    """a Log for symbols"""

    @property
    def valid_statistics(self):
        return self._counts is None

    def _invalidate_statistics(self):
        # `_counts is None` => invalidation of calculated statistics
        # _mode would be a bad idea: what's the 'null' equivalent,
        # when None is a valid index into _counts?
        self._counts = None

    def _prepare_data(self):
        counts = {}
        mode = None
        mode_count = 0

        for x in self._cache:
            c = counts[x] = counts.get(x, 0) + 1
            if c > mode_count:
                mode = x

        self._counts, self._mode = counts, mode
        return self._counts, self._mode

    @statistic
    def counts(self):
        return self._counts

    @statistic
    def mode(self):
        return self._mode

    @statistic
    def distribution(self):
        return {k: v / len(self._cache) for k, v in self.counts().items()}

    def generate_report(self):
        return memo(
            distribution = self.distribution(),
            entropy      = self.entropy(),
            mode         = self.mode())

    @statistic
    def ish(self):
        tmp = 0
        threshold = random.random()
        for k, v in self.distribution().items():
            tmp += v
            if tmp >= threshold:
                return k
        # this shouldn't happen, but just in case...
        return random.choice(self._cache)

    @statistic
    def entropy(self,e=0):
        n = len(self._cache)
        for k, v in self.counts().items():
            p = v / n
            # TODO: understand this equation better
            e -= p * math.log(p, 2) if p else 0
        return e
