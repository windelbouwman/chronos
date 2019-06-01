""" Hierarchy of trace data.

"""

import abc
from .event import Event
from .timeseries import TimeSeries


class TreeItem(metaclass=abc.ABCMeta):
    def __init__(self):
        self.children = []
        self.parent = None

    def add_item(self, item):
        if isinstance(item, list):
            for i in item:
                self.add_item(i)
        else:
            item.parent = self
            self.children.append(item)

    def dfs(self):
        for c in self.children:
            for i in c.dfs():
                yield i
        yield self

    @property
    def size(self):
        return sum(c.size for c in self.children)

    @abc.abstractmethod
    def type_name(self):
        raise NotImplementedError()


class TraceDataSource(TreeItem):
    """ A source of tracedata.

    This can be provided by a plugin, for example
    cpu usage over time.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name

    def get_uri(self):
        return 'tracedatasource://{}'.format(id(self))

    def type_name(self):
        return 'DataSource'


class TraceGroup(TreeItem):
    """ A trace group / folder. """

    def __init__(self, name):
        super().__init__()
        self.name = name

    def get_uri(self):
        return 'tracegroup://{}'.format(id(self))

    def type_name(self):
        return 'TraceGroup'


class Trace(TreeItem):
    """ A single trace source. """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._type = "value"  # or log message / function call enter?
        self.samples = TimeSeries()
        self.data_changed = Event()
    
    @property
    def size(self):
        return len(self.samples) * 8 + 13

    @property
    def has_samples(self):
        return len(self.samples) > 0

    def add(self, sample):
        # TODO: do aggregation!
        if isinstance(sample, list):
            for s in sample:
                self._inner_add(s)
        else:
            self._inner_add(sample)

        self.data_changed()

    def _inner_add(self, sample):
        self.samples.append(sample)

    def get_samples(self, timespan):
        """ Get samples which are within the given timespan. """
        return self.samples.get_samples(timespan)

    def find_nearest_sample(self, timestamp):
        """ Find sample which is nearest to the given timestamp. """
        if self.has_samples:
            if timestamp < self.samples[0].timestamp:
                return self.samples[0]
            elif self.samples[-1].timestamp < timestamp:
                return self.samples[-1]
            else:
                assert len(self.samples) > 1
                # Ow snap, we need to find a sample..
                i1 = 0
                i2 = 0
                i3 = len(self.samples) - 1
                # print(i1, i2, i3)
                while i1 + 1 != i3:
                    assert i3 > i1
                    i2 = (i1 + i3) // 2  # mid sample
                    mid_sample = self.samples[i2]
                    if timestamp < mid_sample.timestamp:
                        i3 = i2
                    else:
                        i1 = i2
                    # print(i1, i2, i3)
                # TODO: pick closest of two? Nah, just pick index 1.
                return self.samples[i1]
        # while i1 != i2:


class SignalTrace(Trace):
    """ A signal trace of scalar values over time. """
    def get_uri(self):
        return 'signaltrace://{}'.format(id(self))

    def type_name(self):
        return 'SignalTrace'


class LogTrace(Trace):
    """ A trace with log events. """
    def get_uri(self):
        return 'logtrace://{}'.format(id(self))

    def type_name(self):
        return 'LogTrace'


class FunctionCallTrace(Trace):
    pass


class VideoTrace(Trace):
    pass


class AudioTrace(Trace):
    """ An audio recording. """
    pass
