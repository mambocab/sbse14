from __future__ import print_function, division

import itertools

from witschey.models import Model
from witschey.searchers import Searcher, SearcherConfig

from witschey.searchers import *
from witschey.models import *

import timeit

def run():
    ss, ms = Searcher.__subclasses__(), (Fonseca,)
    # ss, ms = Searcher.__subclasses__(), Model.__subclasses__()
    for searcher, model in itertools.product(ss, ms):
        print('{}({})'.format(searcher.__name__, model.__name__))
        searcher = searcher(model)
        out = searcher.run()
        print('{}:\n{}'.format(model.__name__, out.to_str()))
        print('#' * 40)
        print()

if __name__ == '__main__':
    run()
    sc = SearcherConfig()
    print(sc)
