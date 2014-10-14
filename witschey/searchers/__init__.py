from searcher import Searcher, SearcherConfig
from simulated_annealer import SimulatedAnnealer
from maxwalksat import MaxWalkSat
from genetic_algorithm import GeneticAlgorithm

SEARCHER_SHORTNAMES = {
    SimulatedAnnealer: 'SA',
    MaxWalkSat: 'MWS',
    GeneticAlgorithm: 'GA'
}
SEARCHER_SHORTNAMES.update(
    {cls.__name__: shortname
    for cls, shortname in SEARCHER_SHORTNAMES.iteritems()})
