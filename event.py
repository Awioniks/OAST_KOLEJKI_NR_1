import time
import uuid

from enum import Enum


class EventType(Enum):
    """
    Event properties
    """
    IN_EVENT = "IN_EVENT"
    OUT_EVENT = "OUT_EVENT"


class ClientType(Enum):
    """
    Event properties
    """
    IMAGINED_CLIENT = "IMAGINED_CLIENT"
    REAL_CLIENT = "REAL_CLIENT"


class Event():
    """
    Represent event class which is added to queue
    """
    def __init__(self, time_to_save, event_type, client_type, client_id=None):
        self.occurrence_time = time_to_save
        self.event_type = event_type
        self.client_type = client_type
        if not client_id:
            self.client_id = str(uuid.uuid4())
        else:
            self.client_id = client_id
        self.time_in_queue = 0

    def __repr__(self):
        """
        Show event.
        """
        repr = "{} - cl_id, {} - ev_type, {} - cl_type, {} - oc_time, {} - time_queue\n"
        return repr.format(
            self.client_id, self.event_type,
            self.client_type, self.occurrence_time,
            self.time_in_queue)

    def set_time_in_queue(self, time_in_queue):
        """
        Set time in queue
        """
        self.time_in_queue = time_in_queue

    def get_event_stats(self):
        """
        Get important stats from out events.
        """
        return {
            'oc_time': self.occurrence_time,
            'qu_time': self.time_in_queue,
            'client_id': self.client_id,
            'event_type': self.event_type
        }
