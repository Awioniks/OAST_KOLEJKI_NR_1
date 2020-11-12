from enum import Enum

import config as c
import statistics as stat
from event import Event, EventType


class SimType(Enum):
    """
    Simulation properties
    """

    CON_SIM = "CONTINOUS_SIMULATION"
    COM_SIM = "COMMON_SIMULATION"


class Simulation():
    """
    Represents Simulation class which handle next events
    """

    def __init__(self, sim_type):
        self.sim_type = sim_type
        self.initial_events = []

    def init_events(self, lambda_param):
        """
        Generate initial events
        """

        start_time = 0
        while start_time > c.SIMULATION_TIME:
            event_duration = stat.expotential_value(
                lambda_param)
            start_time += event_duration
            self.initial_events.append(Event(start_time, EventType.PUT_EVENT))

    def run(self, lambda_param):
        self.init_events(lambda_param)

    def clear(self):
        self.initial_events = []
