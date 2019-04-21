""" Demo data source not requiring any hardware.
"""

import math
import threading
import time
from ..data import SignalTrace, SignalRecord, LogTrace, LogRecord
from ..data import TraceDataSource, TimeStamp, TraceGroup
from ..data import DataSource


class DemoPlugin:
    name = 'demo'

    def create_data_source(self):
        return DemoDataSource()


class DemoDataSource(DataSource):
    """ Demo data source. """
    def __init__(self):
        self._x = int(TimeStamp.now())
        xs = range(self._x - 300, self._x)
        self.data_source = TraceDataSource('demo')

        group1 = TraceGroup('group1')
        self.data_source.add_item(group1)

        self._trace1 = SignalTrace('trace1')
        points1 = [SignalRecord(TimeStamp(x), math.sin(x * 0.03) * 80 + 40) for x in xs]
        self._trace1.add(points1)
        group1.add_item(self._trace1)

        trace2 = SignalTrace('trace2')
        points2 = [SignalRecord(TimeStamp(x), math.sin(x * 0.6) * 30 + 20) for x in xs]
        trace2.add(points2)
        group1.add_item(trace2)

        self._trace3 = SignalTrace('sine3')
        points3 = [SignalRecord(TimeStamp(x), math.cos(x * 0.6) * 20 + 70) for x in xs]
        self._trace3.add(points3)
        self.data_source.add_item(self._trace3)

        self._trace4 = SignalTrace('ramp1')
        self.data_source.add_item(self._trace4)

        self._log_trace = LogTrace('logs')
        self.data_source.add_item(self._log_trace)

        self.start()

    @property
    def is_running(self):
        return self._running

    def start(self):
        """ Start the data source capture. """
        self._running = True
        self._thread = threading.Thread(target=self._run_func)
        self._thread.start()
    
    def _run_func(self):
        while self._running:
            time.sleep(0.1)
            self._x += 1
            # print('running!')
            ts = TimeStamp(self._x)
            point = SignalRecord(ts, math.sin(self._x * 0.2) * 80 + 40)
            self._trace1.add(point)
            point = SignalRecord(ts, math.cos(self._x * 0.6) * 20 + 70)
            self._trace3.add(point)
            point = SignalRecord(ts, self._x % 50)
            self._trace4.add(point)
            if self._x % 37 == 0:
                sample = LogRecord(ts, 0, 'x divisable by 37!!')
                self._log_trace.add(sample)

    def stop(self):
        self._running = False
        self._thread.join()
