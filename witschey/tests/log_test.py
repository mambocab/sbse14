from witschey.log import SymbolLog, NumberLog
from unittest import TestCase

import random, itertools

def init_list(d):
    return [].extend(itertools.repeat(k, v) for k, v in d.items())

class TestNumberLog(TestCase):
    def setUp(self):
        self.max_size = 64
        self.log = NumberLog(max_size=self.max_size)
        random.seed(7)

    def test_validation(self):
        self.log += 48.8
        self.log += 14.24

        # make sure sortedness actually changes
        assert sorted(self.log._cache) != self.log._cache
        assert not self.log._valid_statistics

        self.log._prepare_data()

        assert self.log._valid_statistics
        assert sorted(self.log._cache) == self.log._cache

    def test_invalidation(self):
        self.log += 48.8
        self.log += 14.24
        self.log._prepare_data()

        # make sure validness actually changes
        assert self.log._valid_statistics

        self.log += 56.4

        assert not self.log._valid_statistics

    def test_n(self):
        n = 2000
        for _ in xrange(n):
            self.log += 2
        assert self.log._n == n

    def test_max_size(self):
        for x in xrange(2000):
            self.log += 2
        assert len(self.log._cache) == self.max_size

"""

#### Sym, Example

As an example of generating numbers from a distribution, consider the following code.
The logged population has plus, grapes and pears in the ration 2:1:1.
From that population, we can generate another distribution that is nearly the same:

>>> symDemo()
(0.5, 'plums'), (0.265625, 'grapes'), (0.234375, 'pears')]
{'plums': 64, 'grapes': 34, 'pears': 30}

"""
# TODO: testify this
def sym_entropy_demo(n1=10, n2=1000):

    random.seed(7)
    init_fruit = ['plums'] * (n1*2) + ['grapes'] * n1 + ['pears'] * n1
    log = SymbolLog(init_fruit)
    print(json.dumps(log.distribution(), indent=2, sort_keys=True))

    found = Sym([log.ish() for _ in xrange(n2)])
    print(json.dumps(found.distribution(), indent=2, sort_keys=True))
    print(found.counts())

    print('entropy:', found.entropy())
    for x in xrange(15):
        desired = random.randint(1, 5)
        while found._cache.count(x) < desired:
            found += x
    print(json.dumps(found.distribution(), indent=2, sort_keys=True))
    print('entropy:', found.entropy())

# TODO: testify this
def report_demo(n1=10, n2=1000):
    init_fruit = ['plums'] * (n1*2) + ['grapes'] * n1 + ['pears'] * n1
    log = SymbolLog(init_fruit)
    print(log.report().to_str())


if __name__ == "__main__":

    report_demo()
    print()
    print('=' * 50)
    print()

    sym_entropy_demo()

