""" Data package.

Two types of data are considered:
- Measured quantities (time-stamped real-valued measurements)
- textual log messages (time-stamped logging)

"""

from .duration import Duration
from .timespan import TimeSpan
from .timestamp import TimeStamp
from .trace import TraceDataSource, TraceGroup
from .trace import Trace, SignalTrace, LogTrace
from .trace import TreeItem
from .data_store import DataStore


class DataSource:
    pass


class Record:
    def __init__(self, timestamp):
        self.timestamp = timestamp


class LogRecord(Record):
    def __init__(self, timestamp, level, message):
        super().__init__(timestamp)
        self.level = level
        self.message = message


class SignalRecord(Record):
    def __init__(self, timestamp, value):
        super().__init__(timestamp)
        self.value = value
