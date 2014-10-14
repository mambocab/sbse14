from __future__ import division, print_function

import random
from witschey import base

from witschey.searcher import compute_model_io

class DifferentialEvolution(Searcher):

    def __init__(self, model, *args, **kw):
        super(DifferentialEvolution, self).__init__(model=model, *args, **kw)

    def run(self, text_report=True):
        n_candiates = self.spec.n_candiates
        self.frontier = [self.random_search_io() for _ in xrange(n_candiates)]

        for _ in xrange(self.spec.generations):
            pass

    def _sample_frontier_exclude(self, ex, n=3):
        flen = len(self.frontier)
        if flen < n:
            e = 'cannot sample {} values from frontier of length {}'.format(
                n, flen)
            raise ValueError(e)
        # if frontier has only n+1 elements, avoid thrashing
        if flen == n + 1:
            return tuple(i for i in set(self.frontier) - {ex})

        rv = {ex}
        while ex in rv:
            rv = random.sample(self.frontier, n)
        return tuple(rv)

    def _extrapolate_xs(self, current):
        a, b, c = tuple(self._sample_frontier_exclude(current, n=3))
        rv_list = [x for x in current.xs]

        # randomly pick at least one x-position to change
        change_indices = [i for i in xrange(len(rv_list))
            if random.random() < self.spec.cr] or [base.random_index(rv_list)]

        # extrapolate a new value for each of the chosen indices
        for i in change_indices:
            extrapolated = a.xs[i] + self.spec.f * (b.xs[i] - c.xs[i])
            x.clip(extrapolated)
            rv_list[i] = extrapolated

        return tuple(rv_list)
