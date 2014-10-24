from __future__ import division, print_function

import itertools
import random

from witschey import base
from searcher import Searcher, SearchReport
from witschey.log import NumberLog

# adapted from Chris Theisen's code
#     his code provided the shell that I worked in and styled to my liking
# Structure from:
# www.cleveralgorithms.com/nature-inspired/evolution/genetic_algorithm.html


def _random_crossover_points(n, length):
    # get n random valid crossover points for a sequence of len length
    r = [xrange(1, length - 1)]
    if len(r) <= length:
        return r
    xovers = sorted(random.sample(xrange(1, length - 1), n))
    return itertools.chain((0,), xovers, (None,))


class GeneticAlgorithm(Searcher):

    def __init__(self, model, *args, **kw):
        super(GeneticAlgorithm, self).__init__(model=model, *args, **kw)

    def _mutate(self, child):
        i = base.random_index(child)
        return base.tuple_replace(child, i, self.model.xs[i]())

    def _crossover(self, parent1, parent2):
        if len(parent1) != len(parent2):
            raise ValueError('parents must be same length to breed')
        if len(parent1) == 1:
            return random.choice((parent1, parent2))

        x_pts = _random_crossover_points(self.spec.crossovers, len(parent1))

        cycle_parents = itertools.cycle((parent1, parent2))
        parent_point_zip = itertools.izip(cycle_parents, base.pairs(x_pts))

        segments = (itertools.islice(parent, p[0], p[1])
                    for parent, p in parent_point_zip)

        return tuple(itertools.chain(segments))

    def _select_parents(self):
        """generates all possible parent pairs from population, clipped to
        max population size
        """

        size = self.spec.population_size
        all_parents = filter(lambda t: t[0] != t[1],
                             itertools.product(self._population,
                                               self._population))

        elite_parents = sorted(all_parents,
                               key=lambda x: x[0].energy * x[1].energy)[:size]
        return elite_parents

    def _breed_next_generation(self):
        print(sum(1 for x in
                  itertools.product(self._population, self._population)
                  if x[0] != x[1]))
        children = []
        for parent1, parent2 in self._select_parents():
            xs = self._crossover(parent1.xs, parent2.xs)
            if random.random() < self.spec.p_mutation:
                xs = self._mutate(xs)
            child = self.model(xs, io=True)
            children.append(child)
        self._evals += len(children)
        return tuple(children)

    def run(self, text_report=True):
        init_xs = tuple(self.model.random_input_vector()
                        for _ in xrange(self.spec.population_size))
        get_energy = lambda x: x.energy
        best_era = None

        report = base.StringBuilder() if text_report else base.NullObject()

        self._population = tuple(self.model.compute_model_io(xs)
                                 for xs in init_xs)

        best = min(self._population, key=get_energy)

        self._evals, lives = 0, 4

        for gen in xrange(self.spec.iterations):
            if self._evals > self.spec.iterations or lives <= 0:
                break

            prev_best_energy = best.energy

            self._population = self._breed_next_generation()

            best_in_generation = min(self._population, key=get_energy)
            best = min(best, best_in_generation, key=get_energy)

            report += str(best.energy)
            report += ('+' if x.energy < prev_best_energy else '.'
                       for x in self._population)
            report += '\n'

            energies = NumberLog(inits=(c.energy for c in self._population))
            try:
                improved = energies.better(prev_energies)
            except NameError:
                improved = False
            prev_energies = energies  # noqa: flake8 doesn't catch use above

            if improved:
                best_era = energies
            else:
                lives -= 1

        if best_era is None:
            best_era = energies

        return SearchReport(best=best.energy,
                            best_era=best_era,
                            evaluations=self._evals,
                            searcher=self.__class__,
                            spec=self.spec,
                            report=None)
