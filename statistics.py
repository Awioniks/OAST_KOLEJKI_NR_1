"""
Generate all important statistics value
"""
import numpy as np
from collections import defaultdict
from random import random
import config as c
from simulation import SimType, EventType
import matplotlib.pyplot as mpl


def show_statistics(simulation_type, results, client_results):
    """
    Show statistics from queue.
    """
    title = '\n\n\n{} Avg Delays for {} simulation {}'.format(
        10 * '*', simulation_type, 10 * '*')
    print(title)
    if simulation_type == SimType.COM_SIM:
        avg_delays, p0_x, p0_y = calculate_delays_pO_values(results)
        avg_delay = calculate_avg_delay_wait(avg_delays)
        for lambda_rate in avg_delay:
            avg = avg_delay[lambda_rate]
            # Caculate analytical delay.
            delay_analytical = 1 / (c.MI_RATE - lambda_rate)
            stat = '\n{}. - lambda_rate, {:f} - avg, {:f} - avg analytical '.format(
                lambda_rate, avg, delay_analytical)
            print(stat)
            # draw plot
            x = np.array(p0_x[lambda_rate])
            y = np.array(p0_y[lambda_rate])
            m, b = np.polyfit(x, y, 1)
            mpl.plot(x, m * x + b, 'r-')
            mpl.xlabel('Time')
            mpl.ylabel('Probability')
            mpl.title("p0(t) for lambda = {:f} ".format(lambda_rate))
            mpl.show()

    elif simulation_type == SimType.CON_SIM:
        qu_times, avg_delays = calculate_avg_time_in_queue(results)
        avg_delay = calculate_avg_delay_wait(avg_delays)
        avg_qu = calculate_avg_delay_wait(qu_times)
        cl_stats = calculate_client_stats(client_results)
        for lambda_rate in avg_delay:
            avg_d = avg_delay[lambda_rate]
            avg_q = avg_qu[lambda_rate]
            # Calculate analytical delay and wait time.
            rate = lambda_rate / c.MI_RATE
            delay_analytical = ((2 - rate) * rate) / (lambda_rate * (1 - rate))
            wait_analytical = rate / (lambda_rate * (1 - rate))
            stat = '\n{}. - lambda_rate, {:f} - avg_delay, {:f} - avg_delay_analytical'.format(
                lambda_rate, avg_d, delay_analytical)
            print(stat)
            stat = '{:f} - avg_wait, {:f} - avg_wait_analytical'.format(
                avg_q, wait_analytical)
            print(stat)
            # Calculate analytical clients rates.
            in_sys, in_q = (
                cl_stats[lambda_rate]["in_system"], cl_stats[lambda_rate]["in_queue"])
            an_nr_clients_in_queue = rate / (1 - rate)
            an_nr_clients_in_system = ((2 - rate) * rate) / (1 - rate)
            stat = '{:f} - avg_client_in_system, {:f} - avg_client_in_system_analytical'.format(
                in_sys, an_nr_clients_in_system)
            print(stat)
            stat = '{:f} - avg_client_in_queue, {:f} - avg_client_in_queue_analytical\n'.format(
                in_q, an_nr_clients_in_queue)
            print(stat)


def calculate_client_stats(client_results):
    """
    Calculate avg nr of clients in system and queue.
    """
    nr_in_system, nr_in_queue = 0, 0
    clients_stats = defaultdict(dict)
    for lambda_rate, result in client_results.items():
        for nr_in_qu, nr_in_serv in result:
            nr_in_system += (nr_in_qu + nr_in_serv)
            nr_in_queue += nr_in_qu
        clients_stats[lambda_rate]["in_system"] = (
                nr_in_system / len(result))
        clients_stats[lambda_rate]["in_queue"] = (
                nr_in_queue / len(result))
    return clients_stats


def calculate_avg_time_in_queue(results):
    """
    Calculate avg time for waiting and running through system.
    """
    qu_times = defaultdict(list)
    delay_times = defaultdict(list)
    for lambda_rate, ev_result in results.items():
        for rep in ev_result:
            for client_id, client_stats in rep[EventType.IN_EVENT].items():
                oc_in_time = client_stats[0]
                oc_out_time = rep[EventType.OUT_EVENT][client_id][0]
                qu_time = rep[EventType.OUT_EVENT][client_id][1]
                delay = oc_out_time - oc_in_time
                qu_times[lambda_rate].append(qu_time)
                delay_times[lambda_rate].append(delay)
    return qu_times, delay_times


def calculate_avg_delay_wait(avg_delays):
    """
    Calculate average delay or waiting value.
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
    p0_x = defaultdict(list)
    p0_y = defaultdict(list)
    for lambda_param, result in results.items():
        for rep in result:
            for client_id, client_stats in rep[EventType.IN_EVENT].items():
                oc_in_time = client_stats[0]
                oc_out_time = rep[EventType.OUT_EVENT][client_id][0]
                qu_time = rep[EventType.OUT_EVENT][client_id][1]
                # Calculate avg delays and p0(t) here.
                delay = oc_out_time - oc_in_time
                p0 = (delay - qu_time) / (delay)
                avg_delays[lambda_param].append(delay)
                p0_x[lambda_param].append(oc_in_time)
                p0_y[lambda_param].append(p0)
    return avg_delays, p0_x, p0_y


def expotential_value(lambda_value):
    w = 1 - random()
    return -1 * (np.log(w) / lambda_value)
