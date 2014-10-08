from __future__ import division, print_function

import itertools, random

from witschey import base
from searcher import Searcher, SearchIO

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
        if crossovers < 1:
            raise ValueError('cannot have fewer than 1 crossover')
        if len(parent1) != len(parent2):
            raise ValueError('parents must be same length to breed')

        x_pts = sorted(random.sample(xrange(1, len(parent1) - 1), crossovers))
        x_pts = itertools.chain((0,), x_pts, (None,))

        ugh_mom_dad = itertools.cycle((parent1, parent2))

        segments = [itertools.islice(parent, p[0], p[1])
            for parent, p in itertools.izip(ugh_mom_dad, base.pairs(x_pts))]

        return tuple(itertools.chain(*segments))
    
    def select_parents(self, population, output_size): #all possible parents
        xs = itertools.combinations(population, 2)
        ys = itertools.combinations(reversed(population), 2)
        return random.sample(set(a).union(set(b)), output_size)

    def run(self, text_report=True):
        rand_vect = lambda: self.model.random_input_vector()
        max_pop = self.spec.population_size
        init_xs = (rand_vect() for _ in xrange(max_pop))
        import pdb; pdb.set_trace()
        init_xs_ys = itertools.izip(init_xs, map(self.model, init_xs))
        population = map(lambda x, y: SearchIO(y, y, self.model.energy(y)),
            init_xs_ys)

        stop = False

        best = min(population, key=lambda x: x.energy)

        for gens in xrange(self.spec.iterations):
            children = []
            for parent1, parent2 in self.select_parents(population, max_pop):
                child = self.crossover(parent1, parent2)
                children.append(self.mutate(child2, p_mutation))
            best_in_pop = min(c.energy for c in children)
            if best_in_pop.energy < best.energy:
                best = best_in_pop

            population = children
            #some "is significantly better" termination logic here

        return best.energy
