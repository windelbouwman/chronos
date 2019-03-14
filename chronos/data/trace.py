""" Hierarchy of trace data.

"""


class TreeItem:
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


class TraceGroup(TreeItem):
    """ A trace group / folder. """

    def __init__(self, name):
        super().__init__()
        self.name = name

    def get_uri(self):
        return 'tracegroup://{}'.format(id(self))


class Event:
    """ Simple event type which supports multiple handlers. """
    def __init__(self):
        self._subscribers = []
    
    def __call__(self):
        for s in self._subscribers:
            s()
    
    def subscribe(self, handler):
        self._subscribers.append(handler)
    
    def unsubscribe(self, handler):
        self._subscribers.remove(handler)


class Trace(TreeItem):
    """ A single trace source. """
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._type = "value"  # or log message / function call enter?
        self.samples = []
        self.data_changed = Event()
    
    @property
    def size(self):
        return len(self.samples) * 8 + 13

    @property
    def has_samples(self):
        return len(self.samples) > 0

    def add(self, sample):
        if isinstance(sample, list):
            self.samples.extend(sample)
        else:
            self.samples.append(sample)

        self.data_changed()


class SignalTrace(Trace):
    """ A signal trace of scalar values over time. """
    def get_uri(self):
        return 'signaltrace://{}'.format(id(self))


class LogTrace(Trace):
    """ A trace with log events. """
    def get_uri(self):
        return 'logtrace://{}'.format(id(self))


class FunctionCallTrace(Trace):
    pass




class VideoTrace(Trace):
    pass


class AudioTrace(Trace):
    """ An audio recording. """
    pass
