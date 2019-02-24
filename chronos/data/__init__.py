""" Data package.

Two types of data are considered:
- Measured quantities (time-stamped real-valued measurements)
- textual log messages (time-stamped logging)

"""

from .duration import Duration
from .timespan import TimeSpan
from .timestamp import TimeStamp
from .trace import TraceDataSource, TraceGroup
from .trace import Trace, SignalTrace
from .trace import TreeItem

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
