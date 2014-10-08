from __future__ import print_function, division

from witschey.models import Model
from witschey.searchers import Searcher, SearcherConfig

def run():
    for m in Model.__subclasses__():
        print(m.__name__)

if __name__ == '__main__':
    run()
    sc = SearcherConfig()
    print(sc)
