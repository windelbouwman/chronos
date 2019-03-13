""" Demo data source not requiring any hardware.
"""

import math
import threading
import time
from ..data import Trace, TraceDataSource, TimeStamp, TraceGroup
from ..data import DataSource


class DemoPlugin:
    name = 'demo'

    def create_data_source(self):
        return DemoDataSource()


class DemoDataSource(DataSource):
    """ Demo data source. """
    def __init__(self):
        self._x = 300
        xs = range(300)
        self.data_source = TraceDataSource('demo')

        group1 = TraceGroup('group1')
        self.data_source.add_item(group1)

        self._trace1 = Trace('trace1')
        points1 = [(TimeStamp(x), math.sin(x * 0.2) * 80 + 40) for x in xs]
        self._trace1.add(points1)
        group1.add_item(self._trace1)

        trace2 = Trace('trace2')
        points2 = [(TimeStamp(x), math.sin(x * 0.6) * 30 + 20) for x in xs]
        trace2.add(points2)
        group1.add_item(trace2)

        self._trace3 = Trace('trace3')
        points3 = [(TimeStamp(x), math.cos(x * 0.6) * 20 + 70) for x in xs]
        self._trace3.add(points3)
        self.data_source.add_item(self._trace3)

        # self._log_trace = LogTrace('logs')
        # self.data_source.add_item(self._log_trace)

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
            point = (ts, math.sin(self._x * 0.2) * 80 + 40)
            self._trace1.add(point)
            point = (ts, math.cos(self._x * 0.6) * 20 + 70)
            self._trace3.add(point)

    def stop(self):
        self._running = False
        self._thread.join()
