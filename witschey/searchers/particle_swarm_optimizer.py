from __future__ import division, print_function

import random

from searcher import Searcher


def _random_scaled_velocity(a, b, scale=.1):
    magnitude = max(a, b) - min(a, b)
    return random.uniform(-magnitude, magnitude) * scale


class ParticleSwarmOptimizer(Searcher):
    """
    A searcher that models a "flock" of individuals roaming the search space.
    Individuals make decisions about where to go next based both on their
    own experience and on the experience of the whole group. For more
    information, see https://github.com/timm/sbse14/wiki/pso#details and
    http://en.wikipedia.org/wiki/Particle_swarm_optimization
    """
    pass


class Particle(object):
    """
    A particle in the "flock".
    """

    def __init__(self, model):
        self._model = model
        self._loc = model.random_model_io()
        self._best = self._io

        self._velocites = tuple(_random_scaled_velocity(iv.lo, iv.hi)
                                for iv in model.xs)

    def update(self, local_best):
        pass
