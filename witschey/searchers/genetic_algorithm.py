from __future__ import division, print_function

import itertools
import random
from collections import defaultdict

from witschey import base
from witschey.base import memo
from searcher import Searcher
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

    def select_parents(self, population, output_size):
        """generates all possible parent pairs from population, clipped to
        output_size
        """
        fore = itertools.combinations(population, 2)
        back = itertools.combinations(reversed(population), 2)
        all_parents = set(fore).union(set(back))
        if len(all_parents) < output_size:
            return all_parents
        return random.sample(all_parents, output_size)

    def run(self, text_report=True):
        rand_vect = lambda: self.model.random_input_vector()
        pop_size = self.spec.population_size
        init_xs = tuple(rand_vect() for _ in xrange(pop_size))
        energy = lambda x: x.energy

        report = base.StringBuilder() if text_report else base.NullObject()
        energy_by_generation = defaultdict(
            NumberLog if self.spec.log_eras_best_energy else base.NullObject)

        population = tuple(self.model.compute_model_io(xs) for xs in init_xs)

        best = min(population, key=energy)

        evals = 0
        for gen in xrange(self.spec.iterations or 1000):
            children = []
            for parent1, parent2 in self.select_parents(population, pop_size):
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

            energy_by_generation[gen] += best.energy

            population = children
            evals += len(population)

            if evals > self.spec.iterations:
                break
            # TODO: some "is significantly better" termination logic here

        rv = memo(best=best.energy, evals=evals)
        if report:
            rv.report = report.as_str()
        if energy_by_generation:
            rv.era_logs_best_energy = energy_by_generation

        return rv
