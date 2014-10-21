from __future__ import division, print_function

import random
import math

from searcher import Searcher
from witschey.base import memo, NullObject, StringBuilder
from witschey.log import NumberLog


class SimulatedAnnealer(Searcher):
    def __init__(self, model, *args, **kw):
        super(SimulatedAnnealer, self).__init__(model=model, *args, **kw)

    def _get_neighbor(self, model_io):
        n_gen = (model_io.xs[i]
                 if random.random() < self.spec.p_mutation else v
                 for i, v in enumerate(self.model.random_input_vector()))
        return self.model(tuple(n_gen), io=True)

    def run(self, text_report=True):
        report = StringBuilder() if text_report else NullObject()
        current = self.model.random_model_io()
        best = current  # assumes current is immutable
        self.lives = 4
        current_era_energies = NumberLog(max_size=None)
        best_era = None

        for k in range(self.spec.iterations):
            if self.lives <= 0 and self.spec.terminate_early:
                break
            prev_era_energies = current_era_energies

            neighbor = self._get_neighbor(current)
            current_era_energies += neighbor.energy

            if neighbor.energy < best.energy:
                best, current = neighbor, neighbor
                report += '!'

            if neighbor.energy < current.energy:
                current = neighbor
                report += '+'
            else:
                cnorm = self.model.normalize(current.energy)
                nnorm = self.model.normalize(neighbor.energy)
                temp = k / self.spec.iterations
                if self._good_idea(cnorm, nnorm, temp) < random.random():
                    current = neighbor
                    report += '?'

            report += '.'

            if k % self.spec.era_length == 0 and k != 0:
                report += ('\n', '{: .2}'.format(best.energy), ' ')
                if not best_era:
                    best_era = current_era_energies

                try:
                    improved = current_era_energies.better(prev_era_energies)
                except ValueError:
                    improved = False
                if improved:
                    best_era = current_era_energies
                else:
                    self.lives -= 1
                current_era_energies = NumberLog()

        rv = memo(report=report.as_str(), best=best.energy,
                  best_era=best_era)
        return rv

    def _good_idea(self, old, new, temp):
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
        return rv * self.spec.cooling_factor
