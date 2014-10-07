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

    def mutate(self, child, pMut):
        #nothing happens! Hooray! TODO
        return child

    def crossover(self, parent1, parent2, crossovers=1):
        if crossovers < 1:
            raise ValueError('cannot have fewer than 1 crossover')
        if len(parent1) != len(parent2):
            raise ValueError('parents must be same length to breed')

        if crossovers == 1:
            xpt = random.choice(range(1, len(parent1 - 1)))
            return itertools.chain(parent1[:xpt], parent2[xpt:])

        x_pts = sorted(random.sample(range(1, len(parent1) - 1), crossovers))
        x_pts = itertools.chain((0,), x_pts, (None,))

        ugh_mom_dad = itertools.cycle((parent1, parent2))
        segments = []

        for pts, parent in itertools.izip(base.pairs(x_pts), ugh_mom_dad):
            segments.append(itertools.islice(parent, pts[0], pts[1]))

        return tuple(itertools.chain(*segments))
    
    def select_parents(self, population): #all possible parents
        xs = itertools.combinations(population, 2)
        ys = itertools.combinations(reversed(population), 2)
        return list(set(a).union(set(b)))

    def run(self, text_report=True):
        p_mutation = 1 / len(self.model.xs)
        rand_vect = self.model.random_input_vector
        XVarBest = rand_vect()
        population = [rand_vect() for _ in xrange(self.spec.population_size)]
        eList = []
        stop = False

        k = 1
        for gens in myOpt.ga_gen_list:
            eBest = 1
            while k < gens:
                parents = self.select_parents(population)
                children = []
                for parent1, parent2 in parents:
                    child1, child2 = self.crossover(parent1, parent2, myOpt.  ga_crossover  )
                    children.append(self.mutate(child1, p_mutation))
                    children.append(self.mutate(child2, p_mutation))
                eBest = min([c.energy for c in children])
                population = children
                k += 1
            eList.append(eBest)
            #some "is significantly better" termination logic here

        return min(eList), True
