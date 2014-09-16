from __future__ import division, unicode_literals

from base import memo, pretty_input, tuple_replace
import random
import math
import numpy as np

class Searcher(object):
    def __init__(self, iterations, model):
        self.iterations = iterations
        self.model = model

class SimulatedAnnealer(Searcher):
    def __init__(self, model, iterations=1000, p_mutation=1/3, *args, **kwargs):
        super(SimulatedAnnealer, self).__init__(
            iterations=iterations,
            model=model,
            *args, **kwargs
            )

        self.p_mutation = p_mutation

    def run(self, text_report=True):
        rv = memo(report='')
        def report_append(s):
            if text_report:
                rv.report += s

        init = self.model.random_input_vector()
        solution = init
        state = solution
        solution_energy = self.model(solution)
        energy_min = solution_energy


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
                raise ValueError('p returning greater than one', rv, old, new, temp)
            return rv

        for k in range(self.iterations):
            neighbor_candidate = self.model.random_input_vector()
            neighbor = tuple(neighbor_candidate[i]
                if random.random() < self.p_mutation else v
                for i, v in enumerate(state))

            solution_energy = self.model(solution)
            neighbor_energy = self.model(neighbor)
            current_energy  = self.model(state)

            if neighbor_energy < solution_energy:
                solution = neighbor
                energy_min = solution_energy
                report_append('!')

            if neighbor_energy < current_energy:
                state = neighbor
                report_append('+')
            else:
                good_idea = p(
                    self.model.normalize(current_energy),
                    self.model.normalize(neighbor_energy),
                    k / self.iterations)
                if good_idea < random.random():
                    state = neighbor
                    report_append('?')

            report_append('.')
            if k % 50 == 0 and k != 0:
                report_append('\n' + pretty_input(solution) + ': ' 
                                    + '{: .2}'.format(energy_min) + ' ')

        rv.best = solution_energy
        return rv

class MaxWalkSat(Searcher):

    def __init__(self, model, iterations=1000, p_mutation=1/3,
        *args, **kwargs):
        super(MaxWalkSat, self).__init__(
            iterations=iterations,
            model=model,
            *args, **kwargs
            )
        self.p_mutation = p_mutation

    def local_search_inputs(self, bottom, top, n=10):
        chunk_length = (top - bottom) / n

        for a in np.arange(bottom, top, chunk_length):
            yield random.uniform(a, a + chunk_length)


    def run(self, text_report=True):
        rv = memo(report='')
        def report_append(s):
            if text_report:
                rv.report += s

        init = self.model.random_input_vector()
        solution = init
        state = solution
        current_energy = self.model(state)
        solution_energy = current_energy
        energy_min = solution_energy
        evals = 0

        while evals < self.iterations:

            for j in range(20):
                if solution_energy < 0.06:
                    report_append('%\n')
                if evals > self.iterations:
                    break

                dimension = random.randint(0, len(state) - 1)
                if self.p_mutation > random.random():
                    state = tuple_replace(state,
                        dimension, self.model.xs[dimension]())

                    current_energy = self.model(state)

                    if current_energy < solution_energy:
                        solution = state
                        solution_energy = current_energy
                        report_append('+')
                    else:
                        report_append('.')

                    evals += 1
                    if evals % 50 == 0:
                        report_append('\n{}'.format(solution_energy))

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
                            report_append('|')
                        else:
                            report_append('.')

                        evals += 1
                        if evals % 50 == 0:
                            report_append('\n{}'.format(state))

            rv.best = solution_energy
            return rv
