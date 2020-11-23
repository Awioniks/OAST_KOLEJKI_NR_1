"""
Generate all important statistics value
"""
import numpy as np
from collections import defaultdict
from random import random
import config as c
from simulation import SimType, EventType


def show_statistics(simulation_type, results):
    """
    Show statistics from queue.
    """

    title = '{} Avg Delays for {} simulation {}'.format(
        10*'*', simulation_type,  10*'*')
    print(title)
    if simulation_type == SimType.COM_SIM:
        avg_delays, p0_t = calculate_delays_pO_values(results)
        avg_delay = calculate_avg_delay(avg_delays)
        for lambda_rate in avg_delay:
            avg = avg_delay[lambda_rate]
            # Caculate analytical delay.
            delay_analytical = 1 / (c.MI_RATE - lambda_rate)
            stat = '{}. - lambda_rate, {:f} - avg, {:f} - avg analytical '.format(
                lambda_rate, avg, delay_analytical)
            print(stat)
    elif simulation_type == SimType.CON_SIM:
        pass


def calculate_avg_client_in_queue():
    """
    Calculate avg number in queue.
    """
    pass


def calculate_avg_delay(avg_delays):
    """
    Calculate average delay value.
    """
    avg_delays_dict = {}
    for lambda_rate, avg_delay_list in avg_delays.items():
        avg_value = sum(avg_delay_list) / len(avg_delay_list)
        avg_delays_dict[lambda_rate] = avg_value
    return avg_delays_dict


def calculate_delays_pO_values(results):
    """
    Calculate avg delays for normal queue.
    """
    avg_delays = defaultdict(list)
    p0_t = defaultdict(list)
    for lambda_param, result in results.items():
        for rep in result:
            for client_id, client_stats in rep[EventType.IN_EVENT].items():
                oc_in_time = client_stats[0]
                oc_out_time = rep[EventType.OUT_EVENT][client_id][0]
                qu_time = rep[EventType.OUT_EVENT][client_id][1]
                # Calculate avg delays and p0(t) here.
                delay = oc_out_time - oc_in_time
                p0 = delay / (delay + qu_time)
                avg_delays[lambda_param].append(delay)
                p0_t[lambda_param].append((oc_in_time, p0))
    return avg_delays, p0_t


def expotential_value(lambda_value):
    w = 1 - random()
    return -1 * (np.log(w)/lambda_value)
