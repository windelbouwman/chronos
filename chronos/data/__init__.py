""" Data package.

Two types of data are considered:
- Measured quantities (time-stamped real-valued measurements)
- textual log messages (time-stamped logging)

"""

from .duration import Duration
from .timestamp import TimeSpan
from .timestamp import TimeStamp

class LogRecord:
    def __init__(self, timestamp, level, message):
        self.timestamp = timestamp
        self.level = level
        self.message = message

class DataStore:
    """ Some data backed thingy! """
    def __init__(self):
        pass
    
    def get_data(self):
        return []
    
    def add_data(self):
        pass
