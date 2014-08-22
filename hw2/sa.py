from __future__ import print_function

import random
import math


f1 = lambda x: x ** 2
f2 = lambda x: (x - 2) ** 2

energy = lambda x: f1(x) + f2(x)
#energy = lambda x: (f1(x) + f2(x) - min) / (max - min)

def p(o, n, t):
    try:
        return math.e * (-1 * (o - n) / t)
    except ZeroDivisionError:
        return 0


rand = lambda: random.randint(-(10 ** 5), 10 ** 5)

seed = None
random.seed(seed)

init = rand()

print(init)
assert init

energy_max = 1416184202

# state := s0; energy := E(state)                  // Initial state, energy.
# state_best := s; energy_best := energy                    // Initial "best" solution
solution = (init, energy(init))
state = solution

# k := 0                              // Energy evaluation count.
kmax = 100
# WHILE k < kmax and energy > emax         // While time remains & not good enough:
for k in range(kmax):
#   state_neighbor := neighbor(s)                 //   Pick some neighbor.
#   energy_neighbor := E(state_neighbor)                       //   Compute its energy.
    neighbor_input = random.choice((solution[0] - 1, solution[0] + 1))
    neighbor = (neighbor_input, energy(neighbor_input))

#   IF    energy_neighbor > energy_best                     //   Is this a new best?
    if neighbor[1] > solution[1]:
#   THEN  state_best := state_neighbor; energy_best := energy_neighbor          //     Yes, save it.
#         print "!"
        solution = neighbor
        energy_best = solution[1]
        print('!', end='')
#   FI

#   IF    energy_neighbor < e                      // Should we jump to better?
    if neighbor[1] > state[1]:
#   THEN  s := state_neighbor; e := energy_neighbor            //    Yes!
#         print "+"
        state = neighbor
        print('+', end='')
#   FI
#   ELSE IF P(e, energy_neighbor, k/kmax) > rand() // Should we jump to worse?
    elif p(state[1], neighbor[1], k/kmax) > random.random():
        state = neighbor
        print('?', end='')
#   THEN  s := state_neighbor; e := energy_neighbor            //    Yes, change state.
#         print "?"
#   FI

    print('.', end='')
#   print "."
    if k % 50 == 0 and k != 0:
        print('\n' + str(solution[0]), end='')
#   if k % 50 == 0: print "\n",state_best
# RETURN state_best                           // Return the best solution found.

print('\n\n' + str(solution[0]))

print('energy_best = ' + str(energy_best))
