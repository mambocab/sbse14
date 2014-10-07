from __future__ import division

#Structure from SA Lecture
import sys, re, random, math, itertools

from searcher import Searcher

# adapted from Chris Theisen's code
#     his code provided the shell that I worked in and styled to my liking
#Structure from:
#http://www.cleveralgorithms.com/nature-inspired/evolution/genetic_algorithm.html
class GeneticAlgorithm(Searcher):

    def __init__(self, model *args, **kw):
        super(GA, self).__init__(model=model, *args, **kw)

    def mutate(self, child, pMut):
        #nothing happens! Hooray! TODO
        return child

    def crossover(self, parent1, parent2, crossover):
        #BECAUSE REASONS OK TODO
        return parent1, parent2
    
    def select_parents(self, pop): #all possible parents
        a = itertools.combinations(pop, 2)
        b = itertools.combinations(reversed(pop), 2)
        return set(a).union(set(b))

    def run(self, text_report=True):
        p_mutation = 1 / len(self.model.xs)
        riv = self.model.random_input_vector
        XVarBest = riv()
        eList = []
        population = [riv() for _ in self.spec.population_size]
        stop = False

        k = 1
        for gens in myOpt.ga_gen_list:
            eBest = 1
            while k < gens:
                parents = self.select_parents(population)
                children = []
                for parent1, parent2 in parents:
                    child1, child2 = self.Crossover(parent1, parent2, myOpt.  ga_crossover  )
                    children.append(self.Mutate(child1, pMutate))
                    children.append(self.Mutate(child2, pMutate))
                eBest = min([c.energy for c in children])
                population = children
                k += 1
            eList.append(eBest)
            #some "is significantly better" termination logic here
        
        return min(eList), True

  def printOptions(self):
    print "GA Options:"
    print "popSize:", myOpt.ga_pop_size, "Crossover:", myOpt.ga_crossover 
    print "Gens:", myOpt.ga_gen_list
