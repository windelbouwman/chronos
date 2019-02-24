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


class TraceGroup(TreeItem):
    """ A trace group / folder. """

    def __init__(self, name):
        super().__init__()
        self.name = name


class Trace(TreeItem):
    """ A single trace source. """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self._type = "value"  # or log message / function call enter?
        self.samples = []
    
    @property
    def size(self):
        return len(self.samples) * 8 + 13

    def add(self, sample):
        self.samples.append(sample)


def EventTrace(Trace):
    """ A trace with events. """
    pass


def SignalTrace(Trace):
    """ A signal trace of scalar values over time. """
    pass


def VideoTrace(Trace):
    pass