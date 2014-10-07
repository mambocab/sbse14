from __future__ import division

import random

from witschey import searchers
from unittest import TestCase
from witschey import models

class TestGeneticAlgorithm(TestCase):
    def setUp(self):
        self.model = searchers.GeneticAlgorithm(models.Schaffer)

    def test_crossover_lengths(self):
        parent1 = tuple(i * 10 for i in range(10))
        parent2 = tuple((i * 10) + 1 for i in range(10))

        xo = self.model.crossover(parent1, parent2, 3)

        assert len(parent1) == len(xo)
        assert len(xo) == len(parent2)

    def test_crossover_values(self):
        random.seed(0)
        parent1 = tuple(i * 10 for i in range(10))
        parent2 = tuple((i * 10) + 1 for i in range(10))

        xo = self.model.crossover(parent1, parent2, 3)

        for i, x in enumerate(xo):
            print(x, parent1[1], parent2[i])
            assert x == parent1[i] or x == parent2[i]
