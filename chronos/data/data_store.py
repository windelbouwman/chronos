

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

    def get_trace(self, uri):
        """ Retrieve a trace object for a given uri. """
        for source in self.sources:
            for tree in source.data_source.dfs():
                print(id(tree), tree)
                if id(tree) == uri:
                    return tree
        raise KeyError(str(uri))