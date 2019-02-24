""" Demo data source not requiring any hardware.
"""

import math
from ..data import Trace, TraceDataSource, TimeStamp, TraceGroup


class DemoPlugin:
    name = 'demo'

    def create_data_source(self):
        return DemoDataSource()


class DemoDataSource:
    def __init__(self):
        xs = range(300)
        self.data_source = TraceDataSource('demo')

        group1 = TraceGroup('group1')
        self.data_source.add_item(group1)

        trace1 = Trace('trace1')
        points1 = [(TimeStamp(x), math.sin(x * 0.2) * 80 + 40) for x in xs]
        trace1.add(points1)
        group1.add_item(trace1)

        trace2 = Trace('trace2')
        points2 = [(TimeStamp(x), math.sin(x * 0.6) * 30 + 20) for x in xs]
        trace2.add(points2)
        group1.add_item(trace2)

        trace3 = Trace('trace3')
        points3 = [(TimeStamp(x), math.cos(x * 0.6) * 20 - 20) for x in xs]
        trace3.add(points3)
        self.data_source.add_item(trace3)
