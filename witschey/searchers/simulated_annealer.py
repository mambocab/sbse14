from __future__ import division, print_function

import random, math
from collections import defaultdict
from copy import deepcopy

from searcher import Searcher, SearchIO, compute_model_io
from witschey.base import memo
from witschey.log import NumberLog

def p(old, new, temp, cooling_factor):
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
    return rv * cooling_factor


class SimulatedAnnealer(Searcher):
    def __init__(self, model, *args, **kw):
        super(SimulatedAnnealer, self).__init__(model=model, *args, **kw)

    def run(self, text_report=True):
        rv = memo(report='')
        log_eras_by_objective =\
            self.spec.log_eras_by_objective or self.spec.terminate_early
        if log_eras_by_objective:
            rv.era_logs_by_objective = {
                f.__name__: defaultdict(NumberLog)
                for f in self.model.ys
            }
        if self.spec.log_eras_best_energy:
            rv.era_logs_best_energy = defaultdict(NumberLog)
        def report_append(s):
            if text_report:
                rv.report += s

        init_xs = self.model.random_input_vector()
        init_ys = self.model(init_xs)
        best = SearchIO(init_xs, init_ys, self.model.energy(init_ys))
        current = deepcopy(best)

        report_append('{: .2}'.format(best.energy) + ' ')
        self.lives = 4

        for k in range(self.spec.iterations):
            if self.lives <= 0 and self.spec.terminate_early: break

            neighbor_candidate_xs = self.model.random_input_vector()
            neighbor_xs = tuple(current.xs[i]
                if random.random() < self.spec.p_mutation else v
                for i, v in enumerate(neighbor_candidate_xs))

            neighbor = compute_model_io(self.model, neighbor_candidate_xs)

            if neighbor.energy < best.energy:
                best, current = neighbor, neighbor
                report_append('!')

            if neighbor.energy < current.energy:
                current = neighbor
                report_append('+')
            else:
                good_idea = p(
                    self.model.normalize(current.energy),
                    self.model.normalize(neighbor.energy),
                    k / self.spec.iterations, self.spec.cooling_factor)
                # if random.random() < good_idea:
                if good_idea < random.random():
                    current = neighbor
                    report_append('?')

            report_append('.')

            era = k // self.spec.era_length
            for f, v in zip(self.model.ys, best.ys):
                if log_eras_by_objective:
                    rv.era_logs_by_objective[f.__name__][era] += v
                if self.spec.log_eras_best_energy:
                    rv.era_logs_best_energy[era] += best.energy

            if k % self.spec.era_length == 0 and k != 0:
                report_append('\n' + '{: .2}'.format(best.energy) + ' ')

                self.lives -= 1

                if not self.spec.terminate_early: break
                for logs in rv.era_logs_by_objective.values():
                    if era not in logs: break
                    if len(logs.keys()) < 2: break

                    prev_log = logs[logs.keys().index(era) - 1]
                    if logs[era].better(prev_log): self.lives += 1

        rv.best = best.energy
        return rv

