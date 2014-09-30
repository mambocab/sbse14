from __future__ import division, print_function

from datetime import datetime
from collections import defaultdict
import random, time

from witschey.models import Schaffer, Fonseca, Kursawe
from witschey.models import ZDT1, ZDT3, Viennet3
from witschey.searchers import SimulatedAnnealer, MaxWalkSat
from witschey.log import NumberLog
from witschey.base import memo

def run(r=20, seed=10, text_report=False, searcher_args={},
    models=None):
    if text_report: print(datetime.now())
    outs = []
    for model in models or (Schaffer, Fonseca, Kursawe, ZDT1, ZDT3, Viennet3):
        xtiles = []
        if text_report:
            print("\n", model.__name__, sep='')
            print('-' * 50)
        for searcher in (SimulatedAnnealer, MaxWalkSat):
            if seed is not None:
                random.seed(seed)
            n = NumberLog(max_size=None)
            times = NumberLog(max_size=None)

            if text_report: print(searcher.__name__)

            for _ in range(r):
                start_time = time.clock()
                s = searcher(model(), **searcher_args)
                out = s.run(text_report=text_report)
                out.spec = s.spec
                outs.append(out)
                times += time.clock() - start_time
                n += out.best
            if text_report:
                print(s.spec.to_str(sep=': '))
                print(out.report, end='\n\n')

            if hasattr(out, 'era_logs') and text_report:
                for fname, logs in sorted(out.era_logs.iteritems()):
                    if not logs: break
                    print('<', fname)
                    lo = min(logs.values(), key=lambda a: a.lo).lo
                    hi = max(logs.values(), key=lambda a: a.hi).lo
                    for era in range(max(logs.keys())):
                        width = 20
                        if era in logs:
                            rep = logs[era].xtile(width=width, lo=lo, hi=hi)
                        else: rep = 'x' * width
                        print(era, rep, sep='\t')
                    print()

            if text_report:
                print('Best: {: .4f}'.format(n.mean()))
                print('total time: {:.3f}s'.format(times.total()),
                    'mean time: {:.3f}s'.format(times.mean()), sep='\t')

                print(n.xtile(width=30), sep='\n')
                print('\n')
        if text_report: print('=' * 50 + '\n', '=' * 50, sep='')
    return outs

def aggregate_report(outs):
    logs_by_searcher = defaultdict(list)
    for o in outs:
        last_best = {}
        for fname, log in o.era_logs.iteritems():
            last_best[fname] = log[max(log.keys())]
        logs_by_searcher[o.spec.searcher].append(last_best)

    mws = logs_by_searcher['MaxWalkSat']
    sa = logs_by_searcher['SimulatedAnnealer']

    mws_logs_by_function = defaultdict(list)
    sa_logs_by_function = defaultdict(list)
    for x, d in ((mws, mws_logs_by_function), (sa, sa_logs_by_function)):
        for log in x:
            d[fname].append(log[fname])

    

    print(mws_logs_by_function)

if __name__ == '__main__':
    # print('############# Part 3 #############')
    # run(r=1, seed=1, text_report=True,
    #     searcher_args={'terminate_early': False})

    # print('############# Part 5 #############')
    # run(r=30, seed=1, text_report=True)

    print('############# Part 6 #############')

    random.seed(1)
    outs = run(r=30, seed=None, text_report=False, models=(ZDT1,))

    aggregate_report(outs)


