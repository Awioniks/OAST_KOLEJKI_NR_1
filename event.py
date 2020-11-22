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
    def __init__(self, time_to_save, event_type, client_type, id=None):
        self.occurrence_time = time_to_save
        self.event_type = event_type
        self.client_type = client_type
        self.client_id = uuid.UUID() if not id else id
        self.time_in_queue = 0

    def set_time_in_queue(self, time_in_queue):
        """
        Set time in queue
        """
        self.set_time_in_queue = time_in_queue

    def get_event_stats(self):
        """
        Get important stats from out events.
        """
        key_format = "{}_{}".format(self.client_id, self.event_type)
        return {
            'oc_time': self.occurrence_time,
            'qu_time': self.time_in_queue,
            'key': key_format
        }
