from __future__ import division

import random
import numpy as np
from collections import defaultdict

from searcher import Searcher
from witschey.base import memo, tuple_replace
from witschey.log import NumberLog


class MaxWalkSat(Searcher):

    def __init__(self, model, *args, **kw):
        super(MaxWalkSat, self).__init__(model=model, *args, **kw)

    def local_search_inputs(self, bottom, top, n=10):
        chunk_length = (top - bottom) / n

        for a in np.arange(bottom, top, chunk_length):
            yield random.uniform(a, a + chunk_length)

    def run(self, text_report=True):
        rv = memo(report='')

        log_objectives = self.spec.log_eras_by_objective
        log_objectives = log_objectives or self.spec.terminate_early
        self.lives = 4

        if log_objectives:
            rv.era_logs_by_objective = {f.__name__: defaultdict(NumberLog)
                                        for f in self.model.ys}
        if self.spec.log_eras_best_energy:
            rv.era_logs_best_energy = defaultdict(NumberLog)

        def report(s):
            if text_report:
                rv.report += s

        self.terminate = False

        def end_era(evals, era_length, log_value):
            report('\n{: .2}'.format(log_value) + ' ')

            self.lives -= 1
            eras = evals // era_length

            for logs in rv.era_logs_by_objective.values():
                if eras not in logs:
                    break
                if len(logs.keys()) < 2:
                    break

                prev_log = logs[logs.keys().index(eras) - 1]
                if logs[eras].better(prev_log):
                    self.lives += 1

            if self.lives <= 0:
                self.terminate = True

        def log_era(evals, era_length, dependents_outputs):
            era = evals // era_length
            for f, v in dependents_outputs:
                if log_objectives:
                    rv.era_logs_by_objective[f.__name__][era] += v
                if self.spec.log_eras_best_energy:
                    rv.era_logs_best_energy[era] += rv.best

        init = self.model.random_input_vector()
        solution = init
        state = solution
        current_energy = self.model.energy(self.model(state))
        rv.best = current_energy
        evals = 0

        report('{: .2}'.format(rv.best) + ' ')

        while evals < self.spec.iterations:
            if self.terminate:
                break

            for j in range(20):
                if evals > self.spec.iterations or self.terminate:
                    break

                dimension = random.randint(0, len(state) - 1)
                if self.spec.p_mutation > random.random():
                    state = tuple_replace(state, dimension,
                                          self.model.xs[dimension]())

                    current_energy = self.model.energy(self.model(state))

                    if current_energy < rv.best:
                        solution = state
                        rv.best = current_energy
                        report('+')
                    else:
                        report('.')

                    evals += 1

                    if evals % self.spec.era_length == 0:
                        end_era(evals, self.spec.era_length, rv.best)

                else:
                    local = self.model.xs[dimension]
                    for j in self.local_search_inputs(local.lo, local.hi):
                        if self.terminate:
                            break

                        state = tuple_replace(state, dimension,
                                              self.model.xs[dimension]())

                        current_energy = self.model(state)

                        if current_energy < rv.best:
                            solution = state
                            rv.best = current_energy
                            report('|')
                        else:
                            report('.')

                        evals += 1
                        if evals % self.spec.era_length == 0:
                            end_era(evals, self.spec.era_length, rv.best)
                if log_objectives or self.spec.log_eras_energy:
                    log_era(evals, self.spec.era_length,
                            zip(self.model.ys, self.model(solution)))

        rv.evaluations = evals
        return rv
