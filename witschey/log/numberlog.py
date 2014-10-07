from __future__ import division

import sys

from log import Log, statistic
from witschey import base

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

