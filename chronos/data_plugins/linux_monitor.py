
from ..data import TimeStamp


class DataPlugin:
    pass


class LinuxDataPlugin(DataPlugin):
    name = "linux"

    def create_source(self):
        return LinuxDataSource()


# TODO: plugins.register(LinuxDataPlugin)


class LinuxDataSource(DataPlugin):
    """ Simple data plugin which reads the file /proc/stat """
    def __init__(self):
        self._field_names = ['user', 'nice', 'system', 'idle']
        self._traces = []
        self._trace_map = {}
        for field_name in self._field_names:
            trace = Trace()
            self._traces.append(trace)
            self._trace_map[field_name] = trace

    def start(self):
        pass

    def get_traces(self):
        pass
    
    def _sample(self):
        """ perform a one of sample. """
        timestamp = TimeStamp.now()
        with open('/proc/stat') as f:
            for line in f:
                print(line)
                if line.startswith('cpu '):
                    # Got cpu!
                    parts = line.split(' ')
                    
                    # name = parts[0]

                    for i, field_name in enumerate(self._field_names, 1):
                        value = int(parts[i])
                        sample = TimeSample(timestamp, value)
                        trace = self._trace_map[field_name]
                        trace.add(sample)
