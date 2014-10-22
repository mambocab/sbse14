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


class GeneticAlgorithm(Searcher):

    def __init__(self, model, *args, **kw):
        super(GeneticAlgorithm, self).__init__(model=model, *args, **kw)

    def mutate(self, child):
        i = base.random_index(child)
        return base.tuple_replace(child, i, self.model.xs[i]())

    def crossover(self, parent1, parent2, xovers=1):
        if len(parent1) != len(parent2):
            raise ValueError('parents must be same length to breed')
        if len(parent1) == 1:
            return random.choice((parent1, parent2))

        if xovers < 1:
            raise ValueError('cannot have fewer than 1 crossover')
        xovers = min(len(parent1) - 2, xovers)
        xovers = sorted(random.sample(xrange(1, len(parent1) - 1), xovers))
        x_pts = itertools.chain((0,), xovers, (None,))

        cycle_parents = itertools.cycle((parent1, parent2))
        parent_point_zip = itertools.izip(cycle_parents, base.pairs(x_pts))

        segments = [itertools.islice(parent, p[0], p[1])
                    for parent, p in parent_point_zip]

        return tuple(itertools.chain(*segments))

    def _select_parents(self):
        """generates all possible parent pairs from population, clipped to
        max population size
        """
        size = self.spec.population_size
        all_parents = filter(lambda t: t[0] != t[1],
                             itertools.product(self._population,
                                               self._population))

        if len(all_parents) < size:
            return all_parents

        elite_parents = sorted(all_parents,
                               key=lambda x: x[0].energy * x[1].energy)[:size]
        assert len(elite_parents) == len(self._population) != 0
        return elite_parents

    def run(self, text_report=True):
        init_xs = tuple(self.model.random_input_vector()
                        for _ in xrange(self.spec.population_size))
        energy = lambda x: x.energy
        best_era = None

        report = base.StringBuilder() if text_report else base.NullObject()

        self._population = tuple(self.model.compute_model_io(xs)
                                 for xs in init_xs)

        best = min(self._population, key=energy)

        evals, lives = 0, 4

        for gen in xrange(self.spec.iterations):
            if evals > self.spec.iterations or lives <= 0:
                break

            children = []
            for parent1, parent2 in self._select_parents():
                xs = self.crossover(parent1.xs, parent2.xs, 2)
                if random.random() < self.spec.p_mutation:
                    self.mutate(xs)
                child = self.model(xs, io=True)
                children.append(child)

            best_in_pop = min(children, key=energy)

            prev_best_energy = best.energy
            best = min(best, best_in_pop, key=energy)

            report += str(best.energy)
            report += ('+' if x.energy < prev_best_energy else '.'
                       for x in children)
            report += '\n'

            self._population = children
            evals += len(self._population)

            energies = NumberLog(inits=(c.energy for c in children))
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
                            evaluations=evals,
                            searcher=self.__class__,
                            spec=self.spec)
