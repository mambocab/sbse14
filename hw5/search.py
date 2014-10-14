from __future__ import print_function, division

import itertools, random
from collections import namedtuple, defaultdict

from witschey.models import Model
from witschey.searchers import Searcher, SearcherConfig
from witschey.searchers import SEARCHER_SHORTNAMES as SSNAMES

from witschey.rdiv import rdivDemo

import timeit

def run(n=30, text_report=True):
    ss, ms = Searcher.__subclasses__(), Model.__subclasses__()
    random.seed(1)
    for model_cls in ms:
        outs = []
        print("#### {}".format(model_cls.__name__))
        bests = defaultdict(list)
        last_logs = defaultdict(list)
        for searcher_cls in ss:
            for _ in xrange(n):
                Output = namedtuple('Output', ('name', 'best'))
                name = ('{}'.format(SSNAMES[searcher_cls]))
                searcher = searcher_cls(model_cls)
                out = searcher.run(text_report=text_report)
                out.searcher = searcher_cls
                outs.append(out)
                last_index = max(out.era_logs_best_energy.keys())
                last_logs[name].append(out.era_logs_best_energy[last_index])
                bests[name].append(out.best)

        # rdiv_in = list([name] + log.contents()
        #     for name, log_list in last_logs.iteritems()
        #     for log in log_list)
        rdiv_in = list([name] + bests[name] for name in bests.keys())
        print(rdivDemo(rdiv_in))

if __name__ == '__main__':
    run(n=5, text_report=False)
