from __future__ import print_function, division, unicode_literals

from random import random as rand
import random
import math
import sys

try:
    model_name = sys.argv[1]
except IndexError:
    raise ValueError('needs at least 1 argument', sys.argv)

class Model(object):
    def __init__(self, function, input_min, input_max, energy_min, energy_max):
        self.function = function
        self.input_max = input_max
        self.input_min = input_min
        self.energy_max = energy_max
        self.energy_min = energy_min

    def normalize(self, x):
        n = x - self.energy_min
        d = self.energy_max - self.energy_min
        try:
            rv = n / d
        except ZeroDivisionError:
            raise ValueError("model's max and min energy are the same!")
        return rv

    def __call__(self, *vals):
        energy_raw = sum(self.function(v) for v in vals)
        return self.normalize(energy_raw)

def p(old, new, temp):
    """
    sets the threshold we compare to to decide whether to jump

    returns e^-((new-old)/temp)
    """
    numerator = new - old

    if not 0 <= numerator <= 1:
        numerator = old - new
    try:
        exponent = numerator / temp
    except ZeroDivisionError:
        return 0
    rv = math.exp(-exponent)
    if rv >= 1:
        raise ValueError('p returning greater than one', rv, old, new, temp)
    return rv

schaffer = lambda x: (x ** 2) + ((x - 2) ** 2)

model_table = {
    'schaffer': Model(schaffer, -100, 100, 0, 20400),
    'fonseca': None,
    'kursawe': None
}

try:
    model = model_table[model_name.lower()]
except KeyError as e:
    exit('{e} is an invalid model name. valid model names are {ms}'.format(
        e=e, ms=model_table.keys())
    )
    exit(1)


new_input = lambda: random.uniform(model.input_min, model.input_max)

init = new_input()
solution = init
state = solution

print(str(init) + ' ', end='')
kmax = 50 * 20
for k in range(kmax):
    neighbor = new_input()

    solution_energy = model(solution)
    neighbor_energy = model(neighbor)
    current_energy  = model(state)

    if neighbor_energy < solution_energy:
        solution = neighbor
        energy_min = solution_energy
        print('!', end='')

    if neighbor_energy < current_energy:
        state = neighbor
        print('+', end='')
    elif p(current_energy, neighbor_energy, k/kmax) < rand():
        state = neighbor
        print('?', end='')

    print('.', end='')
    if k % 50 == 0 and k != 0:
        print('\n' + str(solution) + ' ', end='')

print()
