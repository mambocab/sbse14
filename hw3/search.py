from __future__ import print_function, division

from witschey.searchers import SimulatedAnnealer, MaxWalkSat
from witschey.models import Schaffer, Kursawe, Fonseca, ZDT1
from witschey.log import NumberLog

import random
from datetime import datetime
from time import clock



def run(r=20, seed=10):
    print(datetime.now())
    outputs = []
    for klass in (Schaffer, Fonseca, Kursawe, ZDT1):
        print("\n", klass.__name__, sep='')
        for searcher in (SimulatedAnnealer, MaxWalkSat):
            random.seed(seed)
            n = NumberLog(max_size=None)
            for _ in range(r):
                print(klass.__name__, searcher.__name__, sep=': ')
                start_time = clock()
                out = searcher(klass()).run()
                print('time: {:.4f}s'.format(clock() - start_time))
                print(out.report, end='\n\n')
                n += out.best
            print(searcher.__name__ + ':', '{: .4f}'.format(n.mean()))

if __name__ == '__main__':
    run()
