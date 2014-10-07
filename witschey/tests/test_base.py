import collections

from witschey import base
from unittest import TestCase

import types

class TestPairs(TestCase):
    def test_type(self):
        assert isinstance(base.pairs([1,2]), collections.Iterable)

    def test_empty(self):
        assert list(base.pairs([])) == []

    def test_tuple(self):
        assert list(base.pairs((1, 2, 3))) == [(1, 2), (2, 3)]

    def test_one_element(self):
        assert list(base.pairs([1])) == []

    def test_many_elements(self):
        ps = list(base.pairs([x for x in xrange(15)]))
        assert len(ps) == 14, len(ps)
        for p in ps:
            assert p[0] == p[1] - 1

class TestMemo(TestCase):
    def test_basic(self):
        v = 1
        m = base.memo(a=v)
        assert m.a == v

    def test_nested(self):
        v = 1
        m = base.memo(a=base.memo(a=v))
        assert m.a.a == v

    def test_multiple(self):
        v1 = 't'
        v2 = 3
        m = base.memo(a=v1, b= v2)
        assert m.a == v1
        assert m.b == v2
