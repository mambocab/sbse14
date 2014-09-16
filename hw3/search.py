from __future__ import print_function, division

from witschey.searchers import SimulatedAnnealer
from witschey.model import Kursawe, Fonseca

r = 20
for klass in (Fonseca, Kursawe):
# for klass in [Schaffer, Fonseca, Kursawe, ZDT1]:
    print("\n", klass.__name__, sep='')
    for searcher in (SimulatedAnnealer):
    # for searcher in [sa, mws]:
        n = 0.0
        for _ in range(r):
            n += searcher(klass())
        print(searcher.__name__ + ':',  n/r)
