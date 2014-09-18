from __future__ import division, unicode_literals

from witschey.base import memo

class Searcher(object):
    def __init__(self, model, *args, **kw):
        self.iterations = kw['iterations']
        self.model = model
        kw.setdefault('seed', 123)
        self.spec = memo(**kw)

