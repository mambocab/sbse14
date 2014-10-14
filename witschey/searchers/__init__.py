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

for searcher_cls, shortname in SEARCHER_SHORTNAMES.iteritems():
    searcher_cls.shortname = shortname
