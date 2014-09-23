from __future__ import division

import random
import numpy as np

from searcher import Searcher
from witschey.base import memo, tuple_replace

class MaxWalkSat(Searcher):

    def __init__(self, model, *args, **kw):
        super(MaxWalkSat, self).__init__(model=model, *args, **kw)

    def local_search_inputs(self, bottom, top, n=10):
        chunk_length = (top - bottom) / n

        for a in np.arange(bottom, top, chunk_length):
            yield random.uniform(a, a + chunk_length)


    def run(self, text_report=True):
        rv = memo(report='')
        def report(s):
            if text_report:
                rv.report += s

        init = self.model.random_input_vector()
        solution = init
        state = solution
        current_energy = self.model(state)
        solution_energy = current_energy
        evals = 0

        report('{: .2}'.format(solution_energy) + ' ')

        while evals < self.spec.iterations:

            for j in range(20):
                if evals > self.spec.iterations:
                    break

                dimension = random.randint(0, len(state) - 1)
                if self.spec.p_mutation > random.random():
                    state = tuple_replace(state,
                        dimension, self.model.xs[dimension]())

                    current_energy = self.model(state)

                    if current_energy < solution_energy:
                        solution = state
                        solution_energy = current_energy
                        report('+')
                    else:
                        report('.')

                    evals += 1
                    if evals % 50 == 0:
                        report('\n{: .2}'.format(solution_energy) + ' ')

                else:
                    for j in self.local_search_inputs(
                        self.model.xs[dimension].min,
                        self.model.xs[dimension].max
                        ):
                        state = tuple_replace(state,
                            dimension, self.model.xs[dimension]())

                        current_energy = self.model(state)

                        if current_energy < solution_energy:
                            solution = state
                            solution_energy = current_energy
                            report('|')
                        else:
                            report('.')

                        evals += 1
                        if evals % 50 == 0:
                            report('\n{: .2}'.format(solution_energy) + ' ')

        rv.best = solution_energy
        return rv
