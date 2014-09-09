import json

class memo():
    '''adapted from https://github.com/timm/sbse14/wiki/basepy'''
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    # from http://stackoverflow.com/a/15538391/3408454
    def to_JSON(self, indent=None):
        'adapted from from http://stackoverflow.com/a/15538391/3408454'

        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=indent) 
