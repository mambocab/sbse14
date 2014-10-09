from __future__ import division, print_function

import itertools, random, collections

from witschey import base
from witschey.base import memo
from searcher import Searcher, SearchIO, compute_model_io

# adapted from Chris Theisen's code
#     his code provided the shell that I worked in and styled to my liking
#Structure from:
#http://www.cleveralgorithms.com/nature-inspired/evolution/genetic_algorithm.html

class GeneticAlgorithm(Searcher):

    def __init__(self, model, *args, **kw):
        super(GeneticAlgorithm, self).__init__(model=model, *args, **kw)

    def mutate(self, child):
        i = base.random_index(child)
        return base.tuple_replace(child, i, self.model.xs[i]())

    def crossover(self, parent1, parent2, crossovers=1):
        if len(parent1) != len(parent2):
            raise ValueError('parents must be same length to breed')
        if len(parent1) == 1:
            return random.choice((parent1, parent2))

        if crossovers < 1:
            raise ValueError('cannot have fewer than 1 crossover')
        crossovers = min(len(parent1) - 2, crossovers)
        # print(crossovers)
        x_pts = itertools.chain((0,),
            sorted(random.sample(xrange(1, len(parent1) - 1), crossovers)),
            (None,))

        ugh_mom_dad = itertools.cycle((parent1, parent2))

        segments = [itertools.islice(parent, p[0], p[1])
            for parent, p in itertools.izip(ugh_mom_dad, base.pairs(x_pts))]

        return tuple(itertools.chain(*segments))
    
    def select_parents(self, population, output_size): #all possible parents
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

        population = tuple(compute_model_io(self.model, xs) for xs in init_xs)

        stop = False

        best = min(population, key=energy)

        evals = 0
        for gens in xrange(self.spec.iterations or 1000):
            children = []
            for parent1, parent2 in self.select_parents(population, pop_size):
                xs = self.crossover(parent1.xs, parent2.xs, 2)
                ys = self.model(xs)
                if random.random() < self.spec.p_mutation:
                    self.mutate(xs)
                child = SearchIO(xs, ys, self.model.energy(ys))
                children.append(child)
            best_in_pop = min(children, key=energy)

            best = min(best, best_in_pop, key=energy)

            population = children
            evals += len(population)
            if evals > self.spec.iterations: break
            #some "is significantly better" termination logic here

        return best.energy
