from searcher import Searcher, SearcherConfig
from simulated_annealer import SimulatedAnnealer
from maxwalksat import MaxWalkSat
from genetic_algorithm import GeneticAlgorithm
from differential_evolution import DifferentialEvolution

SEARCHER_SHORTNAMES = {
    SimulatedAnnealer:     'SA',
    MaxWalkSat:            'MWS',
    GeneticAlgorithm:      'GA',
    DifferentialEvolution: 'DE'
}
SEARCHER_SHORTNAMES.update(
    {cls.__name__: shortname
    for cls, shortname in SEARCHER_SHORTNAMES.iteritems()})
