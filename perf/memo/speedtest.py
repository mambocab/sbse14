class memo():
    '''adapted from https://github.com/timm/sbse14/wiki/basepy'''
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
 
def init_memo():
    m = memo(stats=memo(mean=3.5, median=3),
         author=memo(name='Jim Witschey', twitter='mambocab', github='mambocab'))

g = memo(stats=memo(mean=3.5, median=3),
         author=memo(name='Jim Witschey', twitter='mambocab', github='mambocab'),
         when='now')

def append_memo():
    global g
    g.age = 25
    g.age = 26

def access_memo():
    global g
    _ = g.author.name
    _ = g.when

def init_dict():
    d = { 'stats': { 'mean': 3.5, 'median': 3 },
        'author': { 'name': 'Jim Witschey',
                    'twitter': 'mambocab',
                    'github': 'mambocab' } }

d = {   'stats': { 'mean': 3.5, 'median': 3 },
        'author': { 'name': 'Jim Witschey',
                    'twitter': 'mambocab',
                    'github': 'mambocab' },
        'when': 'now'}

def append_dict():
    global d
    d['age'] = 25
    d['age'] = 26

def access_dict():
    global d
    _ = d['author']['name']
    _ = d['when']


