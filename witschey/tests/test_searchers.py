from __future__ import division

import random
from nose.tools import assert_equals, assert_is_instance, assert_is_none
from nose.tools import assert_greater_equal, assert_less_equal

from witschey import searchers
from unittest import TestCase
from witschey import models


class TestGeneticAlgorithm(TestCase):
    def setUp(self):  # noqa
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


class TestSearcherConfig(TestCase):

    def test_empty_config(self):
        sc = searchers.SearcherConfig()
        assert_is_none(sc._model)
        assert_is_none(sc._searcher)
        assert_equals(sc._kw_dict, {})

    def test_empty_config_repr(self):
        sc = searchers.SearcherConfig()
        sc_str_ref = 'SearcherConfig(searcher=None, model=None)'

        assert_equals(repr(sc), sc_str_ref)
        assert_equals(str(sc),  sc_str_ref)

    def test_update_model_and_searcher(self):
        sc = searchers.SearcherConfig()
        sc.update(model=models.Schaffer, searcher=searchers.SimulatedAnnealer)
        assert sc.model == models.Schaffer
        assert sc.searcher == searchers.SimulatedAnnealer

    def test_update_kw_dict(self):
        for s in (searchers.SimulatedAnnealer, None):
            for m in (models.Schaffer, None):
                sc = searchers.SearcherConfig(searcher=s, model=m)
                sc.update(p_mutation=1/3)
                assert sc.as_dict()['p_mutation'] == 1/3
                assert len(sc.as_dict()) == 3
                assert sc.searcher == s
                assert sc.model == m

    def test_get_searcher_no_args(self):
        s, m = searchers.SimulatedAnnealer, models.Schaffer
        sc = searchers.SearcherConfig(model=m, searcher=s)

        searcher = sc.get_searcher()
        assert_is_instance(searcher.model, m)
        assert_is_instance(searcher, s)


class TestMaxWalkSat(TestCase):

    def setUp(self):  # noqa
        self.mws = searchers.MaxWalkSat(models.Schaffer)

    def test_init(self):
        s = searchers.MaxWalkSat(models.Schaffer, iterations=222)
        assert_equals(s.spec.iterations, 222)

    def test_local_inputs_length(self):
        n = 15
        assert_equals(n, len(list(self.mws.local_search_inputs(3, 6, n))))

    def test_local_inputs_contents(self):
        xs = self.mws.local_search_inputs(0, 20, 20)
        random.seed(1)
        # this is stochastic, so run it 100 times & hope any errors are caught
        for _ in xrange(100):
            for i, x in enumerate(xs):
                assert_greater_equal(i + 1, x)
                assert_less_equal(i, x)

    def test_doesnt_fall_over(self):
        """this test doesn't help much, except to make sure there aren't any
        dumb type errors"""
        self.mws = searchers.MaxWalkSat(models.Schaffer, iterations=300)
