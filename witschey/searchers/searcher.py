from __future__ import division, unicode_literals

from witschey.base import memo, The

from datetime import datetime

class Searcher(object):

    def __new__(cls, *args, **kwargs):
        # construct our object
        future_self = super(Searcher, cls).__new__(cls, *args, **kwargs)

        name = cls.__name__
        # initialize a dict with searcher's name
        # and the initialization time
        d = dict(searcher=name, initialized=datetime.now())

        # if there are global options for this class or its bases in The
        for k in [name] + [k.__name__ for k in cls.__bases__]:
            if hasattr(The, k):
                # add them to the dict
                d.update(getattr(The, k).__dict__)

        # then, add the kwargs to the constructor call to the dict.
        # NB: this happens after adding options from The, so 
        #     call-specific options override the globals
        d.update(kwargs)

        # set our spec with the contents of the dict
        future_self.spec = memo(**d)

        return future_self

    def __init__(self, model, *args, **kw):
        self.model = model
