from enum import Enum

class EventInitiator(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"

class EventType(str, Enum):
    MESSAGE = "MESSAGE"
    COMMAND = "COMMAND"
    ERROR = "ERROR"