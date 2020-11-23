#!/usr/bin/env python3
"""
Main file where 2 simulations are triggered
"""

from collections import defaultdict
import config as c
import statistics as stats
from simulation import Simulation, SimType


def simulate(simulation_type):
    """
    Simulate function which handles common queue and continous queue
    """

    sim = Simulation(simulation_type)
    results = defaultdict(list)
    for lambda_value in c.LAMBDA_RATES:
        for _ in range(c.REPLICANTS):
            result = sim.run(lambda_value)
            results[lambda_value].append(result.copy())
            sim.clear()
    return results


if __name__ == '__main__':
    for sim_type in [SimType.CON_SIM]:
        results = simulate(sim_type)
        stats.show_statistics(sim_type, results)
