from __future__ import print_function, division, unicode_literals

from random import random as rand
import sys
import random
import math
import numpy as np

def pretty_input(t, model=None):
    float_format = lambda x: '{: .2f}'.format(x)
    str_tuple = tuple(float_format(x).encode(sys.stdout.encoding) for x in t)
    rv = ', '.join(s for s in str_tuple)
    if model:
        return rv + ': ' + '{: .3f}'.format(model(t))
    return rv

def fonseca(t, n=3):
    assert len(t) == n
    e1, e2 = 0, 0
    for i, x in enumerate(t):
        f = math.sqrt(i + 1)
        e1 += (x - (1 / f)) ** 2
        e2 += (x + (1 / f)) ** 2

    f1 = 1 - math.exp(-e1)
    f2 = 1 - math.exp(-e2)
    return f1 + f2

class Model(object):
    def __init__(self, function,
        input_len, input_min, input_max,
        energy_min, energy_max,
        iterations=1000):
        self.function = function
        self.input_max = input_max
        self.input_min = input_min
        self.energy_max = energy_max
        self.energy_min = energy_min
        self.input_len = input_len
        self.iterations = iterations

    def normalize(self, x):
        n = x - self.energy_min
        d = self.energy_max - self.energy_min
        try:
            rv = n / d
        except ZeroDivisionError:
            raise ValueError("model's max and min energy are the same!")
        return rv

    def random_input(self):
        return random.uniform(self.input_min, self.input_max)

    def random_input_vector(self):
        return tuple(self.random_input() for i in range(self.input_len))

    def __call__(self, *vals):
        energy_raw = sum(self.function(v) for v in vals)

        if not self.energy_min <= energy_raw <= self.energy_max:
            raise ValueError(
                'current energy {c} not in range [{min}, {max}]'.format(
                    c=energy_raw, min=self.energy_min, max=self.energy_max
                )
            )

        return self.normalize(energy_raw)

class State(object):

    def __init__(self):
        self._solution = None
        self._current = None

    @property
    def solution(self):
        return self._solution
    @solution.setter
    def solution(self, value):
        if value != self.solution:
            # print(pretty_input(value, model))
            self._solution = value
    
    @property
    def current(self):
        return self._current
    @current.setter
    def current(self, value):
        self._current = value


def local_search_inputs(bottom, top, n=10):
    chunk_length = (top - bottom) / n

    for a in np.arange(bottom, top, chunk_length):
        yield random.uniform(a, a + chunk_length)

model = Model(fonseca, 3, -4, 4, 0, 20)

state = State()

state.current = model.random_input_vector()
state.solution = state.current

def main():
    for i in range(model.iterations):

        solution_energy = model(state.solution)
        current_energy  = model(state.current)

        dimension = random.randint(0, len(state.current) - 1)
        for j in range(20):
            if .5 < rand():
                slist = list(state.current)
                slist[dimension] = model.random_input()
                state.current = tuple(slist)
                pre = state.solution
                state.solution = min(state.current, state.solution, key=model)
                if state.solution != pre:
                    print(pretty_input(state.solution),
                        'improved by random permutation', sep=': ')
            else:
                for i in local_search_inputs(model.input_min, model.input_max):
                    slist = list(state.current)
                    slist[dimension] = i
                    state.current = tuple(slist)
                    pre = state.solution
                    state.solution = min(state.current, state.solution, key=model)
                    if state.solution != pre:
                        print(pretty_input(state.solution),
                            'improved by exploration', sep=': ')


if __name__ == '__main__':
    main()



















