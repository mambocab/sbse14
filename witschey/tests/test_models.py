from witschey import models
from unittest import TestCase

class TestSchaffer(TestCase):
    def setUp(self):
        self.model = models.Schaffer()

    def test_inputs_length(self):
        i = 10
        model = models.Schaffer(ivs=i)
        x = len(model.xs)
        assert x == i, 'len(model.xs) == {}'.format(x)

    def test_default_inputs_length(self):
        x = len(self.model.xs)
        assert x == 1, 'len(model.xs) == {}'.format(x)

    def test_f1(self):
        assert self.model.f1((0,)) == 0
        assert self.model.f1([2]) == 4
        assert self.model.f1((-2, 2)) == 8

    def test_f2(self):
        assert self.model.f2((0,)) == 4
        assert self.model.f2([2]) == 0
        assert self.model.f2((0, 0)) == 8
