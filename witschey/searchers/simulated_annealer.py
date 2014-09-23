from __future__ import division

import random
import math

from searcher import Searcher
from witschey.base import memo

class SimulatedAnnealer(Searcher):
    def __init__(self, model, *args, **kw):
        super(SimulatedAnnealer, self).__init__(model=model, *args, **kw)

    def run(self, text_report=True):
        rv = memo(report='')
        def report_append(s):
            if text_report:
                rv.report += s

        init = self.model.random_input_vector()
        solution = init
        state = solution
        rv.best = self.model(solution)


        def p(old, new, temp):
            """
            sets the threshold we compare to to decide whether to jump

            returns e^-((new-old)/temp)
            """
            numerator = new - old

            if not 0 <= numerator <= 1:
                numerator = old - new
            try:
                exponent = numerator / temp
            except ZeroDivisionError:
                return 0
            rv = math.exp(-exponent)
            if rv > 1:
                raise ValueError('p returning greater than one',
                    rv, old, new, temp)
            return rv

        report_append('{: .2}'.format(rv.best) + ' ')

        for k in range(self.spec.iterations):
            neighbor_candidate = self.model.random_input_vector()
            neighbor = tuple(neighbor_candidate[i]
                if random.random() < self.spec.p_mutation else v
                for i, v in enumerate(state))

            rv.best = self.model(solution)
            neighbor_energy = self.model(neighbor)
            current_energy  = self.model(state)


            if neighbor_energy < rv.best:
                solution = neighbor
                rv.best = neighbor_energy
                report_append('!')

            if neighbor_energy < current_energy:
                state = neighbor
                report_append('+')
            else:
                good_idea = p(
                    self.model.normalize(current_energy),
                    self.model.normalize(neighbor_energy),
                    k / self.spec.iterations)
                if good_idea < random.random():
                    state = neighbor
                    report_append('?')

            report_append('.')
            if k % 50 == 0 and k != 0:
                report_append('\n' + '{: .2}'.format(energy_min) + ' ')

        return rv

