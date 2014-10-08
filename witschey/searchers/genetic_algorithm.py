from __future__ import division, print_function

import itertools, random

from witschey import base
from searcher import Searcher

# adapted from Chris Theisen's code
#     his code provided the shell that I worked in and styled to my liking
#Structure from:
#http://www.cleveralgorithms.com/nature-inspired/evolution/genetic_algorithm.html

class GeneticAlgorithm(Searcher):

    def __init__(self, model, *args, **kw):
        super(GeneticAlgorithm, self).__init__(model=model, *args, **kw)

    def mutate(self, child):
        #nothing happens! Hooray! TODO
        return child

    def crossover(self, parent1, parent2, crossovers=1):
        if crossovers < 1:
            raise ValueError('cannot have fewer than 1 crossover')
        if len(parent1) != len(parent2):
            raise ValueError('parents must be same length to breed')

        x_pts = sorted(random.sample(range(1, len(parent1) - 1), crossovers))
        x_pts = itertools.chain((0,), x_pts, (None,))

        ugh_mom_dad = itertools.cycle((parent1, parent2))

        segments = [itertools.islice(parent, p[0], p[1])
            for parent, p in itertools.izip(ugh_mom_dad, base.pairs(x_pts))]

        return tuple(itertools.chain(*segments))
    
    def select_parents(self, population): #all possible parents
        xs = itertools.combinations(population, 2)
        ys = itertools.combinations(reversed(population), 2)
        return random.sample(set(a).union(set(b)), self.spec.population_size)

    def run(self, text_report=True):
        p_mutation = 1 / len(self.model.xs)
        rand_vect = self.model.random_input_vector
        population = [rand_vect() for _ in xrange(self.spec.population_size)]
        eList = []
        stop = False

        state = {
            'best':    {'xs': None, 'ys': None, 'energy': None},
            'current': {'xs': None, 'ys': None, 'energy': None}
            }

        k = 1
        for gens in myOpt.ga_gen_list:
            eBest = 1
            while k < gens:
                parent_pairs = self.select_parents(population)
                children = []
                for parent1, parent2 in parent_pairs:
                    child = self.crossover(parent1, parent2)
                    children.append(self.mutate(child1, p_mutation))
                    children.append(self.mutate(child2, p_mutation))
                eBest = min([c.energy for c in children])
                population = children
                k += 1
            eList.append(eBest)
            #some "is significantly better" termination logic here

        return min(eList), True
