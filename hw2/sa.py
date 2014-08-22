from __future__ import print_function, division

import random
import math


f1 = lambda x: x ** 2
f2 = lambda x: (x - 2) ** 2

correct_energy_max = None
correct_energy_min = None


def energy(x):
    global correct_energy_min
    global correct_energy_max
    energy_max = 20000400004
    energy_min = 2

    energy_raw = f1(x) + f2(x)
    try:
        assert energy_min <= energy_raw, 'energy_min must be less than or equal to %d' % energy_raw
    except:
        correct_energy_min = energy_raw
    try:
        assert energy_raw <= energy_max, 'energy_max must be greater than or equal to %d' % energy_raw
    except:
        correct_energy_max = energy_raw

    rv = (energy_raw - energy_min) / (energy_max - energy_min)
    return rv

def p(old, new, temp):
    try:
        rv = math.e ** (-1 * ((new - old) / temp))
    except ZeroDivisionError:
        return 0

    with open('plog.txt', 'a') as f:
        f.write(str(rv) + ': {}, {}, {}'.format(old, new, temp) + '\n')
    return rv


space_min = -(10 ** 5)
space_max = 10 ** 5
rand = lambda: random.randint(space_min, space_max)

seed = None
random.seed(seed)

init = rand()

assert init


solution = (init, energy(init))
state = solution

print(str(init) + ' ', end='')
kmax = 50 * 20
for k in range(kmax):

    neighbor_input = random.choice(range(
        max(solution[0] - 500, space_min),
        min(solution[0] + 500, space_max)
    ))
    neighbor = (neighbor_input, energy(neighbor_input))

    if neighbor[1] < solution[1]:
        solution = neighbor
        energy_min = solution[1]
        print('!', end='')

    if neighbor[1] < state[1]:
        state = neighbor
        print('+', end='')
    elif p(state[1], neighbor[1], k/kmax) < random.random():
        state = neighbor
        print('?', end='')

    print('.', end='')
    if k % 50 == 0 and k != 0:
        print('\n' + str(solution[0]) + ' ', end='')

print('\n\n' + str(solution[0]))
print("min: " + str(correct_energy_min))
print("emax: " + str(correct_energy_max))
