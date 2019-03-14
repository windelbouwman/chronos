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


class LogRecord:
    def __init__(self, timestamp, level, message):
        self.timestamp = timestamp
        self.level = level
        self.message = message


