from __future__ import print_function, division

from random import random as rand
import random
import math

f1 = lambda x: x ** 2
f2 = lambda x: (x - 2) ** 2

def energy(x):
    energy_max = 20400
    energy_min = 1

    # assumes the input is something like (x, f1(x), f2(x))
    energy_raw = x[1] + x[2]

    return (energy_raw - energy_min) / (energy_max - energy_min)

def p(old, new, temp):
    try:
        rv = math.e ** -((new - old) / temp)
    except ZeroDivisionError:
        return 0
    return rv

input_max = 10 ** 2
input_min = -input_max
new_input = lambda: random.uniform(input_min, input_max)

init = new_input()
solution = (init, f1(init), f2(init))
state = solution

jumps = 0

results = { state }

print(str(init) + ' ', end='')
kmax = 50 * 20
for k in range(kmax):
    neighbor_input = new_input()

    neighbor = (neighbor_input, f1(neighbor_input), f2(neighbor_input))
    results.add(neighbor)

    if energy(neighbor) < energy(solution):
        solution = neighbor
        energy_min = energy(solution)
        print('!', end='')

    if energy(neighbor) < energy(state):
        state = neighbor
        print('+', end='')
    elif p(energy(state), energy(neighbor), k/kmax) < rand():
        state = neighbor
        jumps += 1
        print('?', end='')

    print('.', end='')
    if k % 50 == 0 and k != 0:
        print('\n' + str(solution[0]) + ' ', end='')

print()
