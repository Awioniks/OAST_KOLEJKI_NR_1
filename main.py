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
    client_results = defaultdict(list)
    for lambda_value in c.LAMBDA_RATES:
        for _ in range(c.REPLICANTS):
            result, client_result = sim.run(lambda_value)
            results[lambda_value].append(result.copy())
            client_results[lambda_value] = (client_result.copy())
            sim.clear()
    return results, client_results


if __name__ == '__main__':
    results, client_results = {}, {}
    for sim_type in [SimType.COM_SIM, SimType.CON_SIM]:
        results[sim_type], client_results[sim_type] = simulate(sim_type)
    for sim_type in [SimType.COM_SIM, SimType.CON_SIM]:
        stats.show_statistics(
            sim_type, results[sim_type], client_results[sim_type])

