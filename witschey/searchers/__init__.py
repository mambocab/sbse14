from searcher import Searcher, SearcherConfig, SearchReport
from simulated_annealer import SimulatedAnnealer
from maxwalksat import MaxWalkSat
from genetic_algorithm import GeneticAlgorithm
from differential_evolution import DifferentialEvolution
from particle_swarm_optimizer import ParticleSwarmOptimizer

SEARCHER_SHORTNAMES = {
    SimulatedAnnealer:     'SA',
    MaxWalkSat:            'MWS',
    GeneticAlgorithm:      'GA',
    DifferentialEvolution: 'DE'
}

for searcher_cls, shortname in SEARCHER_SHORTNAMES.iteritems():
    searcher_cls.shortname = shortname

__all__ = [Searcher, SearcherConfig, SearchReport,
           SimulatedAnnealer, MaxWalkSat,
           GeneticAlgorithm, DifferentialEvolution, ParticleSwarmOptimizer]
