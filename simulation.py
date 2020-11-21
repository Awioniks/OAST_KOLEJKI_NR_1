from enum import Enum

import config as c
import statistics as stat
from event import Event, EventType
from server import Server


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
        self.events = []
        self.stats_event = {}
        self.server = Server()

    def init_events(self, lambda_param):
        """
        Generate initial events.
        """

        occurrence_time = 0
        while occurrence_time > c.SIMULATION_TIME:
            event_duration = stat.expotential_value(
                lambda_param)
            occurrence_time += event_duration
            self.events.append(Event(occurrence_time, EventType.IN_EVENT))

    def handle_events(self, lambda_param):
        """
        Handle consecutive events in system.
        """

        while self.events:
            current_event = self.events.pop()
            current_time = current_event.occurrence_time
            if current_event.event_type == EventType.IN_EVENT:
                if not self.server.clients_in_server:
                    time_in_server = stat.expotential_value(lambda_param)
                    new_event = self.create_event(
                        time_in_server + current_time,
                        EventType.OUT_EVENT,
                        current_event.client_id)
                    self.events.append(new_event)
                    self.server.add_client(
                        current_event.client_id, current_time)
                else:
                    self.server.add_client(
                        current_event.client_id, current_time)
            elif current_event.event_type == EventType.OUT_EVENT:
                # Delete client from system and get stats.
                self.server.delete_client(current_event.client_id)
                # Create new out event from queue.
                time_in_server = stat.expotential_value(lambda_param)
                client_time, client_id = self.server.get_queue_first_client()
                new_event = self.create_event(
                    current_time + time_in_server,
                    EventType.OUT_EVENT,
                    client_id)
                new_event.set_time_in_queue(current_time - client_time)
                self.events.append(new_event)
                self.server.add_client(current_event.client_id, current_time)


            # Sort events on event list and get stats
            self.add_stats(current_event)
            self.sort_events()

        return self.stats_event

    def add_stats(self, current_event):
        """
        Add stats to dict stats which will be calculated.
        """
        stats_event = current_event.get_event_stats()
        key = stats_event['key']
        self.stats_event[key] = (
            stats_event['oc_time'], stats_event['qu_time'])

    def create_event(self, finish_time, event_type, client_id):
        """
        Create event object.
        """
        return Event(
            finish_time,
            event_type,
            client_type)

    def sort_events(self):
        """
        Sort events according to timestamps.
        """
        sorted(
            self.events,
            key=lambda timestamp: getattr(timestamp, 'occurrence_time'),
            reverse=True)

    def run(self, lambda_param):
        """
        Method which handle all processing methods.
        """
        self.init_events(lambda_param)
        self.handle_events(lambda_param)

    def clear(self):
        self.events.clear()
        self.stats_event.clear()
