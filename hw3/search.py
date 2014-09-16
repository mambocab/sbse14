from __future__ import print_function, division

from witschey.searchers import SimulatedAnnealer, MaxWalkSat
from witschey.models import Schaffer, Kursawe, Fonseca, ZDT1

def run(r=20):
    for klass in (Schaffer, Fonseca, Kursawe, ZDT1):
        print("\n", klass.__name__, sep='')
        for searcher in (SimulatedAnnealer, MaxWalkSat):
            n = 0.0
            for _ in range(r):
                n += searcher(klass()).run(text_report=False).best
            print(searcher.__name__ + ':', '{: .4f}'.format(n/r))

if __name__ == '__main__':
    run()
