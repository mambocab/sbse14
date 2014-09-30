"""## Log Stuff

Adapted from [Dr. Tim Menzies' logging code](https://github.com/timm/sbse14/blob/master/log.py).

Logs are places to store records of past events. There are two types of logs:

+ _Num_ : for numbers
+ _Sym_ : for everything else. 

Those logs can be queried to find e.g. the highest
and lowest value of the number seen so far. Alternatively,
they can be queried to return values at the same probability
as the current log contents.

### Max Log Size

To avoid logs consuming all memory, logs store at
most _The.cache.keep_ entries (e.g. 128):

+ If more
than that number of entries arrive, then some old
entry (selected at random) will be deleted.
+ The nature of this cache means that some rare
events might be missed. To check for that, running
the code multiple times and, each time, double the
cache size. Stop when doubling the cache size stops
changing the output.

Just as an example of that process, here we are logging 1,000,000 numbers in a log with a cache of size 16.
Note that the resulting cache is much smaller than 1,000,000 items. Also, the contents of the cache
come from the entire range one to one million (so our log is not biased to just the first few samples:

 % python -i log.py
 >>> The.cache.keep = 16
 >>> log = Num()  
 >>> for x in xrange(1000000): log += x 
 >>> sorted(log._cache)
 [77748, 114712, 122521, 224268, 
 289880, 313675, 502464, 625036, 
 661881, 663207, 680085, 684674, 
 867075, 875594, 922141, 945896]
 >>> 

 ### Caching Slow Reports

 Some of the things we want to report from these logs take a little while to calculate (e.g. finding the median
    requires a sort of a numeric cache):

+ Such reports should be run and cached so they can be accessed many time without the need
for tedious recalculation. 
+ These reports become outdated if new log information arrives so the following
code deletes these reports if ever new data arrives.
+ The protocol for access those reports is to call _log.has().x_ where "x" is a field
generated by the report.  Log subclasses generate reports using the special _report()_ method
(see examples, below).

Just as an example of reporting, after the above run (where we logged 1,000,000 numbers), the following reports are available:

>>> log.has().lo
0 
>>> log.has().hi
945896
>>> print log.has().median # 50th percentile
662544.0
>>> print log.has().iqr # (75-25)th percentile
205194

Note that our median is not as expected (it should be around half a million). Why? Well, clearly a cache of size 16 is
too small to track a million numbers. So how many numbers do we need? Well, that depends on the distribution being explored
but here's how the median is effected by cache size for uniform distributions:

>>> for size in [16,32,64,128,256]:
...     The.cache.keep=size
...     log = Num()
...     for x in xrange(1000000): log += x
...     print size, ":" log.has().median
... 
16 : 637374.5
32 : 480145.5
64 : 520585.5
128 : 490742.0
256 : 470870.5


Note that we get pretty close to half a million with cache sizes at 32 or above. And the lesson: sometimes, a limited
sample can offer a useful approximation to a seemingly complex process.

## Standard Header
"""
from __future__ import division, print_function
import sys, random, math, datetime, time, re
from base import memo
import base
import functools

class Log(object):
    "Keep a random sample of stuff seen so far."

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

        lo = min(lo,self._cache[0])
        hi = max(hi,self._cache[-1])

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

"""

WARNING: the call to _sorted_ in _report()_ makes this code
a candidate for a massive CPU suck (it is always sorting newly arrived data).
So distinguish between _adding_ things to a log in the _last_ era and 
using that information in the _next_ era (so the log from the last era
    is staple in the current).

### Sym

A _Sym_ is a _Log_ for non-numerics.

+ Tracks frequency counts for symbols, and the most common symbol (the _mode_);
+ Reports the entropy of the space (a measure of diversity: lower values mean fewer rarer symbols);
+ Generated symbols from the log by returning symbols at the same probability of the frequency counts (see _ish()_).

"""
class SymbolLog(Log):

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
