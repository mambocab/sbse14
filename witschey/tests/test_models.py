from __future__ import division, print_function

from unittest import TestCase
from nose.tools import assert_equal, assert_in, assert_true

from witschey import models

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

class TestDTLZ7(TestCase):

    def correct_names(self, m):
        z = zip((f.__name__ for f in m.ys),
            ('f{}'.format(x) for x in range(1, len(m.ys) + 1)))
        for act, corr in z:
            assert_equal(act, corr)

    def generated_fs_correct(self, x):
        m = models.DTLZ7(x)
        assert_equal(len(m.ys), x)
        self.correct_names(m)

    def test_default_fs(self):
        m = models.DTLZ7()
        assert_equal(len(m.ys), 20)

        self.correct_names(m)

    def test_generated_fs(self):
        self.generated_fs_correct(30)
        self.generated_fs_correct(100)
