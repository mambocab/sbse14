from __future__ import division, print_function

import itertools
import random
from collections import Iterable

from witschey import base
from searcher import Searcher, SearchReport
from witschey.log import NumberLog

# adapted from Chris Theisen's code
#     his code provided the shell that I worked in and styled to my liking
# Structure from:
# www.cleveralgorithms.com/nature-inspired/evolution/genetic_algorithm.html


def _random_crossover_points(n, length):
    # get n random valid crossover points for a sequence of len length
    r = list(xrange(1, length - 1))
    if len(r) <= length:
        return r
    xovers = sorted(random.sample(xrange(1, length - 1), n))
    return xovers


def _crossover_at(seq1, seq2, xovers):
    # takes two sequences and a single crossover point or a list of points
    if not isinstance(xovers, Iterable):
        xovers = [xovers]
    cycle_seq = itertools.cycle((seq1, seq2))

    # iter. of start and stop points for sections
    xovers = itertools.chain((None,), xovers, (None,))
    parent_point_zip = itertools.izip(cycle_seq, base.pairs(xovers))

    segments = tuple(itertools.islice(parent, start_stop[0], start_stop[1])
                     for parent, start_stop in parent_point_zip)

    return tuple(itertools.chain(*segments))


def _crossover_at_no_islice(seq1, seq2, xovers):
    # takes two sequences and a single crossover point or a list of points
    if not isinstance(xovers, Iterable):
        xovers = [xovers]
    cycle_seq = itertools.cycle((seq1, seq2))

    # iter. of start and stop points for sections
    xovers = itertools.chain((None,), xovers, (None,))
    parent_point_zip = itertools.izip(cycle_seq, base.pairs(xovers))

    segments = tuple(parent[start_stop[0]:start_stop[1]]
                     for parent, start_stop in parent_point_zip)

    return tuple(itertools.chain(*segments))


class GeneticAlgorithm(Searcher):

    def __init__(self, model, *args, **kw):
        super(GeneticAlgorithm, self).__init__(model=model, *args, **kw)

    def _mutate(self, child):
        i = base.random_index(child)
        return base.tuple_replace(child, i, self.model.xs[i]())

    def _crossover(self, parent1, parent2, xovers=None):
        if len(parent1) != len(parent2):
            raise ValueError('parents must be same length to breed')
        if len(parent1) == 1:
            return random.choice((parent1, parent2))
        if xovers is None:
            xovers = self.spec.crossovers

        x_pts = _random_crossover_points(xovers, len(parent1))

        return _crossover_at(parent1, parent2, x_pts)

    def _select_parents(self):
        """
        Return the best n pairs of parents in the population, where quality
        is measured by minimizing the product of their energies
        """

        size = self.spec.population_size
        all_parents = filter(lambda t: t[0] != t[1],
                             itertools.product(self._population,
                                               self._population))

        return sorted(all_parents,
                      key=lambda x: x[0].energy * x[1].energy)[:size]

    def _breed_next_generation(self):
        children = []
        for parent1, parent2 in self._select_parents():
            xs = self._crossover(parent1.xs, parent2.xs)
            if random.random() < self.spec.p_mutation:
                self._mutations += 1
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

        self._evals, lives, self._mutations = 0, 4, 0

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
