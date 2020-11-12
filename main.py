#!/usr/bin/env python3
"""
Main file where 2 simulations are triggered
"""

import config as c
from simulation import Simulation, SimType


def simulate(simulation_type):
    """
    Simulate function which handles common queue and continous queue
    """

    sim = Simulation(simulation_type)
    for _ in range(c.REPLICANTS):
        for lambda_value in c.LAMBDA_RATES:
            result = sim.run(lambda_value)
            sim.clear()


if __name__ == '__main__':
    simulate(SimType.COM_SIM)
    simulate(SimType.CON_SIM)
