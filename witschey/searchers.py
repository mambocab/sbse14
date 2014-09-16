from __future__ import division, unicode_literals

class Searcher(object):
    def __init__(self, iterations, model):
        self.iterations = iterations
        self.model = model

class SimulatedAnnealer(Searcher):
    def __init__(self, iterations=1000, p_mutation=1/3 *args, **kwargs):
        super(SimulatedAnnealer, self).__init__(
            iterations=iterations,
            model=model
            *args, **kwargs
            )

        self.p_mutation = p_mutation

    def search(text_report=True):
        rv = memo(report='')

        def report_append(s):
            if text_report:
                rv.report += s

        for k in range(self.iterations):
            neighbor_candidate = model.random_input_vector()
            neighbor = tuple(neighbor_candidate[i]
                if rand() < p_mutation else v
                for i, v in state.enumerate()))

            solution_energy = model(solution)
            neighbor_energy = model(neighbor)
            current_energy  = model(state)

            if neighbor_energy < solution_energy:
                solution = neighbor
                energy_min = solution_energy
                report_append('!')

            if neighbor_energy < current_energy:
                state = neighbor
                report_append('+')
            elif p(current_energy, neighbor_energy, k/model.iterations) < rand():
                state = neighbor
                report_append('?')

            report_append('.')
            if k % 50 == 0 and k != 0:
                report_append('\n' + pretty_input(solution) + ': ' 
                                    + '{: .2}'.format(energy_min) + ' ')

