import logging
from enum import Enum
from collections import defaultdict

import config as c
import statistics as stat
from event import Event, EventType, ClientType
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
        self.stats_event = defaultdict(dict)
        self.server = Server()
        self.real_clients = 0
        self.configure_logging()

    def configure_logging(self):
        """
        Configure loggingging.
        """
        logging.basicConfig(
            format='%(asctime)s %(message)s', level=logging.INFO)

    def init_events(self, lambda_param):
        """
        Generate initial events.
        """

        occurrence_time = 0
        while occurrence_time < c.SIMULATION_TIME:
            event_occurance = stat.expotential_value(
                lambda_param)
            occurrence_time += event_occurance
            new_event = self.create_event(
                occurrence_time,
                EventType.IN_EVENT,
                ClientType.REAL_CLIENT)
            self.events.append(new_event)
        self.events = self.sort_events()
        self.real_clients = len(self.events)

    def handle_events(self, lambda_param):
        """
        Handle consecutive events in system.
        """

        while self.events:
            current_event = self.events.pop()
            current_time = current_event.occurrence_time
            logging.info(current_event)
            if current_event.event_type == EventType.IN_EVENT:
                if self.server.is_server_empty():
                    time_in_server = stat.expotential_value(c.MI_RATE)
                    new_event = self.create_event(
                        time_in_server + current_time,
                        EventType.OUT_EVENT,
                        current_event.client_type,
                        current_event.client_id)
                    self.events.append(new_event)
                    self.server.add_client(
                        current_event.client_id, current_time)
                else:
                    self.server.add_client_to_queue(
                        current_event.client_id, current_time)
            elif current_event.event_type == EventType.OUT_EVENT:
                # Delete client from system and get stats.
                if current_event.client_type == ClientType.REAL_CLIENT:
                    self.real_clients -= 1
                self.server.delete_client(current_event.client_id)
                # Create new out event from queue.
                time_in_server = stat.expotential_value(c.MI_RATE)
                if not self.server.is_queue_empty():
                    logging.info("Server occupied")
                    cl_id, cl_time = self.server.get_queue_first_client()
                    self.server.delete_client_from_queue(cl_id)
                    new_event = self.create_event(
                        current_time + time_in_server,
                        EventType.OUT_EVENT,
                        ClientType.REAL_CLIENT,
                        cl_id)
                    self.server.add_client(cl_id, current_time)
                    new_event.set_time_in_queue(current_time - cl_time)
                    self.events.append(new_event)
                # Create event with imagined client.
                elif self.sim_type == SimType.CON_SIM and self.real_clients:
                    logging.info("Imagined client created")
                    new_event = self.create_event(
                        current_time,
                        EventType.IN_EVENT,
                        ClientType.IMAGINED_CLIENT)
                    self.events.append(new_event)
            # Sort events on event list and get stats
            self.add_stats(current_event)
            self.events = self.sort_events()

        return self.stats_event

    def all_server_stats(self):
        """
        Return server stats
        """
        return {
            "all_clients": self.server.all_clients,
            "all_clients_queue": self.server.all_clients_in_queue
        }

    def add_stats(self, current_event):
        """
        Add stats to dict stats which will be calculated.
        """
        stats_event = current_event.get_event_stats()
        ev_type = stats_event['event_type']
        cl_id = stats_event['client_id']
        cu_nr_in_serv, cu_nr_in_qu = self.server.get_server_stats()

        self.stats_event[ev_type][cl_id] = (
            stats_event['oc_time'], stats_event['qu_time'],
            cu_nr_in_serv, cu_nr_in_qu)

    def create_event(self, finish_time, ev_type, client_type, client_id=None):
        """
        Create event object.
        """
        return Event(
            finish_time,
            ev_type,
            client_type,
            client_id)

    def sort_events(self):
        """
        Sort events according to timestamps.
        """
        return sorted(
                self.events,
                key=lambda timestamp: getattr(timestamp, 'occurrence_time'),
                reverse=True)

    def run(self, lambda_param):
        """
        Method which handle all processing methods.
        """
        self.init_events(lambda_param)
        return self.handle_events(lambda_param)

    def clear(self):
        self.events.clear()
        self.stats_event.clear()
        self.server.clear_server()
