from __future__ import division, unicode_literals

from witschey.base import memo, The

from datetime import datetime

print(The.to_str())

class Searcher(object):

    def __new__(cls, *args, **kwargs):
        # construct our object
        future_self = super(Searcher, cls).__new__(cls, *args, **kwargs)

        name = cls.__name__
        # give our object a spec, initialized with searcher's name
        # and the initialization time
        future_self.spec = memo(searcher=name, initialized=datetime.now())

        # if there are global options for this class in The
        if hasattr(The, name):
            # add them to the spec
            o.spec(getattr(The, name))

        # then, add the kwargs to the constructor call to spec.
        # NB: this happens after adding options from The, so 
        #     call-specific options override the globals
        o.spec(**kwargs)

        return o

    def __init__(self, model, *args, **kw):
        self.model = model

