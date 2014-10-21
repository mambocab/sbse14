from __future__ import print_function, division

import itertools, random
from collections import namedtuple, defaultdict

from witschey.models import Model, Schwefel
from witschey.searchers import Searcher

from witschey.rdiv import rdiv_report

import timeit

def run(n=30, text_report=True):
    ms = Model.__subclasses__()
    ms.remove(Schwefel)
    ms.extend(Schwefel.initalizer_with(d=d) for d in (10, 20, 40))
    ss = Searcher.__subclasses__()
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
                if not hasattr(out, 'searcher'):
                    out.searcher = searcher_cls
                outs.append(out)
                bests[name].append(out.best)

        rdiv_in = list([name] + best for name, best in bests.iteritems())
        print(rdivDemo(rdiv_in), end='\n\n')

if __name__ == '__main__':
    run(n = 2, text_report=False)
