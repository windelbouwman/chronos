

from .trace import Trace
from .timespan import TimeSpan
from .timestamp import TimeStamp
from .duration import Duration


class DataStore:
    """ Some data backed thingy! """

    def __init__(self):
        self.sources = []

    def shutdown(self):
        # Signal quit signal:
        for source in self.sources:
            source.stop()

    def get_data(self):
        return []

    def add_data(self):
        pass

    def all_trees(self):
        """ Return all trees in this data store. """
        for source in self.sources:
            for tree in source.data_source.dfs():
                yield tree

    def get_timespan(self):
        starts = []
        ends = []
        for tree in self.all_trees():
            if isinstance(tree, Trace) and tree.has_samples:
                starts.append(tree.samples[0].timestamp)
                ends.append(tree.samples[-1].timestamp)

        if not starts:
            now = TimeStamp.now()
            start = now - Duration.from_minutes(5)
            end = now + Duration.from_minutes(5)
        else:
            start = min(starts)
            end = max(ends)
        return TimeSpan(start, end)

    def get_trace(self, uri):
        """ Retrieve a trace object for a given uri. """
        for tree in self.all_trees():
            print(id(tree), tree)
            if id(tree) == uri:
                return tree
        raise KeyError(str(uri))