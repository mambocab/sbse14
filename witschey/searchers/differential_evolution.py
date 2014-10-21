from __future__ import division, print_function

import random

from witschey import base
from witschey.base import memo
from witschey.searchers.searcher import Searcher
from witschey.log import NumberLog


class DifferentialEvolution(Searcher):

    def __init__(self, model, *args, **kw):
        super(DifferentialEvolution, self).__init__(model=model, *args, **kw)

    def run(self, text_report=True):
        n_candiates = self.spec.n_candiates
        self._frontier = [self.model.random_model_io()
                          for _ in xrange(n_candiates)]

        for _ in xrange(self.spec.generations):
            self._update_frontier()

        energy = lambda x: x.energy

        best_era = NumberLog(inits=(x.energy for x in self._frontier))
        rv = memo(best=min(self._frontier, key=energy).energy,
                  best_era=best_era,
                  spec=self.spec)
        return rv

    def _update_frontier(self):
        '''for each member of the frontier, generate a new individual, have
        them compete, then keep the best of the two.'''
        bested, better = [], []
        for x in self._frontier:
            new = self.model(self._extrapolate_xs(x), io=True)
            if new.energy < x.energy:
                bested.append(x)
                better.append(new)

        keep = lambda x: id(x) not in map(id, bested)

        self._frontier = filter(keep, self._frontier) + list(better)

    def _sample_frontier_exclude(self, ex, n=3):
        '''Samples n (default 3) items from the current frontier.
        Returns a shallow copy of the frontier if n is as large or larger
        than the frontier.
        '''
        try:
            # pigeonhole principle: sample n+1 things; at least n aren't ex
            samp = random.sample(self._frontier, n+1)
        except ValueError:
            # if n is too big, just return the frontier
            return self._frontier[:]

        # remove ex if it's there; otherwise remove a random thing
        try:
            samp.remove(ex)
        except ValueError:
            samp.remove(random.choice(samp))

        return samp

    def _extrapolate_xs(self, current):
        '''generate a new individual based on individuals in the frontier'''
        a, b, c = self._sample_frontier_exclude(current, n=3)
        rv_list = [x for x in current.xs]

        # randomly pick at least one x-position to change
        change_indices = [i for i in xrange(len(rv_list))
                          if random.random() < self.spec.p_crossover]
        if not change_indices:
            change_indices = [base.random_index(rv_list)]

        # extrapolate a new value for each of the chosen indices
        for i in change_indices:
            extrapolated = a.xs[i] + self.spec.f * (b.xs[i] - c.xs[i])
            rv_list[i] = self.model.xs[i].clip(extrapolated)

        return tuple(rv_list)
