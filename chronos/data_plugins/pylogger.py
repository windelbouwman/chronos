""" Datasource which records python logger events.
"""
import logging
from ..data import LogTrace, LogRecord, TraceDataSource, TimeStamp, TraceGroup


class PyLoggerPlugin:
    name = "py_logger"


class InnerLogHandler(logging.Handler):
    """ Log handler which re-routes the message to the logger source. """

    def __init__(self, logger_source):
        super().__init__()
        self._logger_source = logger_source

    def emit(self, record):
        self._logger_source.on_record(record)


class PyLoggerSource:
    def __init__(self):
        self.data_source = TraceDataSource("py_logger")

        self._log_trace = LogTrace("messages")
        self.data_source.add_item(self._log_trace)
        self._handler = InnerLogHandler(self)
        logger = logging.getLogger()
        logger.addHandler(self._handler)

    def on_record(self, record):
        ts = TimeStamp.now()
        record = LogRecord(ts, record.levelname, record.message)
        sample = (ts, record)
        self._log_trace.add(sample)
