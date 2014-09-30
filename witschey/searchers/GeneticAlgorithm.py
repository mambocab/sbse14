from __future__ import division

#Structure from SA Lecture
import sys, re, random, math
import copy

from options import *
from utils import *
from analyzer import *

myOpt = Options()

# adapted from Chris Theisen's code
#     his code provided the shell that I worked in and styled to my liking
#Structure from:
#http://www.cleveralgorithms.com/nature-inspired/evolution/genetic_algorithm.html
class GA:

    def mutate(self, child, pMut):
        #nothing happens! Hooray! TODO
        return child

  def Crossover(self, parent1, parent2, crossover):
    #BECAUSE REASONS OK TODO
    return parent1, parent2
    
  def SelectParents(self, pop): #all possible parents
    temp = []
    for x in pop:
      for y in pop:
        if x != y:
          temp.append(x, y)
    return temp
          
  def GetBestSolution(self, pop):
    eMin = 1
    for x in pop:
      temp = x.Energy
      if temp < 1:
        eMin = temp
    return eMin

  def run(self, klass):
    ga = klass
    pMutate = 1/len(ga.XVar)
    XVarBest = ga.XVar
    #print 'start energy: ', eBest           
    k = 1
    eList = []
    population = []
    analyze = Analyzer()
    stop = False
    
    for i in range(myOpt.ga_pop_size):
      population.append(copy.deepcopy(ga).Chaos()) #add a randomly generated model to list
  
    for gens in myOpt.ga_gen_list:
      eBest = 1
      while k < gens:
        parents = self.SelectParents(population) #all possible pairings of parents
        children = []
        for parent1, parent2 in parents:
          child1, child2 = self.Crossover(parent1, parent2, myOpt.ga_crossover)
          children.append(self.Mutate(child1, pMutate))
          children.append(self.Mutate(child2, pMutate))
        eBest = self.GetBestSolution(children)
        population = children
        k += 1
      eList.append(eBest)
      #some "is significantly better" termination logic here
    
    return min(eList), True

  def printOptions(self):
    print "GA Options:"
    print "popSize:", myOpt.ga_pop_size, "Crossover:", myOpt.ga_crossover 
    print "Gens:", myOpt.ga_gen_list
