from __future__ import division, unicode_literals

from witschey.base import memo, The


print(The.to_str())

class Searcher(object):

    def __new__(cls, *args, **kwargs):
        o = super(Searcher, cls).__new__(cls, *args, **kwargs)
        o.spec = memo(**kwargs)

        if hasattr(The, cls.__name__):
            o.spec(getattr(The, cls.__name__))

        return o

    def __init__(self, model, *args, **kw):
        self.model = model

