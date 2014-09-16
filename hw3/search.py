from __future__ import print_function, division

from witschey.searchers import SimulatedAnnealer, MaxWalkSat
from witschey.models import Schaffer, Kursawe, Fonseca, ZDT1
from witschey.log import NumberLog

import random
from datetime import datetime
from time import clock

def run(r=20, seed=10):
    print(datetime.now())
    for klass in (Schaffer, Fonseca, Kursawe, ZDT1):
        xtiles = []
        print("\n", klass.__name__, sep='')
        print('-' * 50)
        for searcher in (SimulatedAnnealer, MaxWalkSat):
            random.seed(seed)
            n = NumberLog(max_size=None)
            times = NumberLog(max_size=None)
            print(searcher.__name__)
            for _ in range(r):
                start_time = clock()
                s = searcher(klass())
                out = s.run(text_report=False)
                times += clock() - start_time
                n += out.best
            print(s.spec.to_str(sep=': '))

            print('Best: {: .4f}'.format(n.mean()))
            print('total time: {:.3f}s'.format(times.total()),
                'mean time: {:.3f}s'.format(times.mean()), sep='\t')
            print(n.xtile(width=30), sep='\n')
            print('\n')
        print('=' * 50 + '\n', '=' * 50, sep='')

if __name__ == '__main__':
    run()
