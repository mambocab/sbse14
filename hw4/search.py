from __future__ import division, print_function

from datetime import datetime
import random, time

from witschey.models import Schaffer, Fonseca, Kursawe
from witschey.models import ZDT1, ZDT3, Viennet3
from witschey.searchers import SimulatedAnnealer, MaxWalkSat
from witschey.log import NumberLog

def run(r=20, seed=10, text_report=False):
    print(datetime.now())
    for klass in (Schaffer,):
    # for klass in (Schaffer, Fonseca, Kursawe, ZDT1, ZDT3, Viennet3):
        xtiles = []
        print("\n", klass.__name__, sep='')
        print('-' * 50)
        # for searcher in (SimulatedAnnealer,):
        for searcher in (SimulatedAnnealer, MaxWalkSat):
            random.seed(seed)
            n = NumberLog(max_size=None)
            times = NumberLog(max_size=None)
            print(searcher.__name__)
            for _ in range(r):
                start_time = time.clock()
                s = searcher(klass())
                out = s.run(text_report=text_report)
                times += time.clock() - start_time
                n += out.best
            print(s.spec.to_str(sep=': '))
            if text_report:
                print(out.report)

            if hasattr(out, 'era_logs'):
                for fname, logs in sorted(out.era_logs.iteritems()):
                    print('<', fname)
                    for era, log in logs.iteritems():
                        print(era, log.xtile(width=20), sep='\t')

            print('Best: {: .4f}'.format(n.mean()))
            print('total time: {:.3f}s'.format(times.total()),
                'mean time: {:.3f}s'.format(times.mean()), sep='\t')

            print(n.xtile(width=30), sep='\n')
            print('\n')
        print('=' * 50 + '\n', '=' * 50, sep='')

if __name__ == '__main__':
    run(r=1, seed=1, text_report=True)
