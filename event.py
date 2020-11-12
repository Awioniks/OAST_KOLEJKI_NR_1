import time
import uuid

from enum import Enum


class EventType(Enum):
    """
    Event properties
    """
    PUT_EVENT = "PUT_EVENT"
    GET_EVENT = "GET_EVENT"


class ClientType(Enum):
    """
    Event properties
    """
    IMAGINED_CLIENT = "PUT_EVENT"
    REAL_CLIENT = "GET_EVENT"


class Event():
    """
    Represent event class which is added to queue
    """
    def __init__(self, time_to_save, event_type, client_type, id=None):
        self.time = time_to_save
        self.event_type = event_type
        self.client_type = client_type
        self.client.id = uuid.UUID() if not id else id
