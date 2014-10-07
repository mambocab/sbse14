from __future__ import division

from witschey import models
from unittest import TestCase

class TestSchaffer(TestCase):
    def setUp(self):
        self.model = models.Schaffer()

    def test_different_dependents(self):
        names = [y.__name__ for y in self.model.ys]
        assert len(names) == len(self.model.ys)

    def test_inputs_length(self):
        i = 10
        model = models.Schaffer(ivs=i)
        x = len(model.xs)
        assert x == i, 'len(model.xs) == {}'.format(x)

    def test_default_inputs_length(self):
        x = len(self.model.xs)
        assert x == 1, 'len(model.xs) == {}'.format(x)

    def test_f1(self):
        f1 = next(y for y in self.model.ys if y.__name__ == 'f1')
        assert f1((0,)) == 0
        assert f1([2]) == 4
        assert f1((-2, 2)) == 8

    def test_f2(self):
        f2 = next(y for y in self.model.ys if y.__name__ == 'f2')
        assert f2((0,)) == 4
        assert f2([2]) == 0
        assert f2((0, 0)) == 8
