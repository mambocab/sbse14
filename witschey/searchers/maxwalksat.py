from __future__ import division

import random
import numpy as np

from searcher import Searcher, SearchReport
from witschey import base
from witschey.base import tuple_replace, StringBuilder, NullObject
from witschey.log import NumberLog


class MaxWalkSat(Searcher):

    def __init__(self, model, *args, **kw):
        super(MaxWalkSat, self).__init__(model=model, *args, **kw)

    def _local_search_xs(self, bottom, top, n=10):
        '''divide the space from bottom to top into n partitions, then
        randomly sample within each partition'''
        chunk_length = (top - bottom) / n

        for a in np.arange(bottom, top, chunk_length):
            yield random.uniform(a, a + chunk_length)

    def _update(self, improvement_char, dimension=None, value=None):
        '''calculate the next value from the model and update state as
        necessary'''
        # check for invalid input
        if value is not None and dimension is None:
            err = 'cannot call _update with specified value but no dimension'
            raise ValueError(err)

        if dimension is None:
            dimension = base.random_index(self._current.xs)
        if value is None:
            # get random value if no value input
            value = self.model.xs[dimension]()

        # generate and evaluate input vector
        new_xs = tuple_replace(self._current.xs, dimension, value)
        self._current = self.model(new_xs, io=True)
        self._evals += 1
        self._current_era += self._current.energy

        # compare to previous best and update as necessary
        if self._current.energy < self._best.energy:
            self._best = self._current
            self._report += improvement_char
        else:
            self._report += '.'

    def run(self, text_report=True):
        '''run MaxWalkSat on self.model'''

        # current ModelIO to evaluate and mutate
        self._current = self.model.random_model_io()
        self._best = self._current
        # initialize and update log variables to track values by era
        self._current_era = NumberLog()
        self._current_era += self._current.energy
        best_era = None
        # bookkeeping variables
        self._evals = 0
        lives = 4
        self._report = StringBuilder() if text_report else NullObject()
        terminate = False

        while self._evals < self.spec.iterations and not terminate:
            # get the generator for a random independent variable

            if self.spec.p_mutation > random.random():
                # if not searching a dimension, mutate randomly
                self._update('+')
            else:
                # if doing a local search, choose a dimension
                dimension = base.random_index(self._current.xs)
                search_iv = self.model.xs[dimension]
                # make sure local search ends at era end
                max_search = self.spec.era_length - (self._evals
                                                     % self.spec.era_length)
                n = min(10, max_search)
                # then try points all along the dimension
                lo, hi = search_iv.lo, search_iv.hi
                for j in self._local_search_xs(lo, hi, n):
                    self._update('|', dimension=dimension, value=j)

            # end-of-era bookkeeping
            if self._evals % self.spec.era_length == 0:
                self._report += ('\n{: .2}'.format(self._best.energy), ' ')

                # _prev_era won't exist in era 0, so account for that case
                try:
                    improved = self._current_era.better(self._prev_era)
                except AttributeError:
                    improved = False
                self._prev_era = self._current_era

                # track best_era
                if improved or best_era is None:
                    best_era = self._current_era
                else:
                    lives -= 1

                if lives <= 0:
                    terminate = True
                else:
                    self._current_era = NumberLog()

        return SearchReport(best=self._best.energy,
                            best_era=best_era,
                            evaluations=self._evals,
                            searcher=self.__class__)
