# all adapted from Dr. Tim Menzies' model code:
# https://github.com/timm/sbse14/blob/master/models.py

from model import Model
from independent_variable import IndependentVariable as IV

class Schaffer(Model):
    def __init__(self, ivs=1):
        ivs = tuple(IV(min=-10^5, max=10^5) for _ in xrange(ivs))
        self.f1 = lambda xs: sum(x ** 2 for x in xs)
        self.f2 = lambda xs: sum((x - 2) ** 2 for x in xs)

        super(Schaffer, self).__init__(
            independents=ivs,dependents=(self.f1, self.f2))

