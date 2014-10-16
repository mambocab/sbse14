import collections

from witschey import base
from unittest import TestCase

import types
from nose.tools import assert_equal, assert_true
import mock
import math

class TestPairs(TestCase):

    def test_type(self):
        assert_true(isinstance(base.pairs([1,2]), collections.Iterable))

    def test_empty(self):
        assert_equal(list(base.pairs([])), [])

    def test_tuple(self):
        assert_equal(list(base.pairs((1, 2, 3))), [(1, 2), (2, 3)])

    def test_one_element(self):
        assert_equal(list(base.pairs([1])), [])

    def test_many_elements(self):
        ps = list(base.pairs([x for x in xrange(15)]))
        assert_equal(len(ps), 14)
        for p in ps:
            assert_equal(p[0], p[1] - 1)


class TestMemo(TestCase):

    def test_basic(self):
        v = 1
        m = base.memo(a=v)
        assert_equal(m.a, v)

    def test_nested(self):
        v = 1
        m = base.memo(a=base.memo(a=v))
        assert_equal(m.a.a, v)

    def test_multiple(self):
        v1 = 't'
        v2 = 3
        m = base.memo(a=v1, b= v2)
        assert_equal(m.a, v1)
        assert_equal(m.b, v2)

    def test_string(self):
        m = base.memo(a=base.memo(a=1, b=2), b=2)
        s = '{\n    b: 2\n    a: {\n        a: 1, b: 2\n    }\n}'
        assert_equal(m.to_str(), s)

