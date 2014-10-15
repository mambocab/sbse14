from __future__ import print_function, division

import itertools, random
from collections import namedtuple, defaultdict

from witschey.models import Model, Schwefel, Viennet3, Schaffer
from witschey.searchers import Searcher, SearcherConfig, DifferentialEvolution
from witschey.searchers import SEARCHER_SHORTNAMES as SSNAMES

from witschey.rdiv import rdivDemo

import timeit

def run(n=30, text_report=True):
    ss, ms = Searcher.__subclasses__(), Model.__subclasses__()
    # ss, ms = Searcher.__subclasses__(), (Schaffer,)
    # ss, ms = (DifferentialEvolution,), Model.__subclasses__()
    # ss, ms = (DifferentialEvolution,), (Viennet3,)
    random.seed(1)
    outs = []
    last_logs = defaultdict(list)
    for model_cls in ms:
        print("#### {}".format(model_cls.__name__))
        bests = defaultdict(list)
        for searcher_cls in ss:
            for _ in xrange(n):
                Output = namedtuple('Output', ('name', 'best'))
                name = ('{}'.format(searcher_cls.shortname))
                searcher = searcher_cls(model_cls)
                out = searcher.run(text_report=text_report)
                out.searcher = searcher_cls
                outs.append(out)
                bests[name].append(out.best)

        rdiv_in = list([name] + best for name, best in bests.iteritems())
        print(rdivDemo(rdiv_in))

if __name__ == '__main__':
    run(n = 2, text_report=False)
