from __future__ import division

import math
import random

from log import Log, statistic
from witschey.base import memo


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
        return memo(distribution=self.distribution(),
                    entropy=self.entropy(),
                    mode=self.mode())

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
    def entropy(self, e=0):
        n = len(self._cache)
        for k, v in self.counts().items():
            p = v / n
            # TODO: understand this equation better
            e -= p * math.log(p, 2) if p else 0
        return e
