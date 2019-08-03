import threading
import time

from ..data import SignalTrace, TraceDataSource, TimeStamp, TraceGroup
from ..data import TimeStamp, SignalRecord


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
        self._field_names = ["user", "nice", "system", "idle"]
        self.data_source = TraceDataSource("linux")
        self._trace_map = {}
        self._running = False

        for field_name in self._field_names:
            trace = SignalTrace(field_name)
            self.data_source.add_item(trace)
            self._trace_map[field_name] = trace

        self.start()

    @property
    def is_running(self):
        return self._running

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._run_func)
        self._thread.start()

    def _run_func(self):
        while self._running:
            time.sleep(0.78)
            self._sample()

    def stop(self):
        self._running = False
        self._thread.join()

    def _sample(self):
        """ perform a one of sample. """
        timestamp = TimeStamp.now()
        with open("/proc/stat") as f:
            for line in f:
                # print(line)
                if line.startswith("cpu "):
                    # Got cpu!
                    parts = list(filter(None, line.split(" ")))
                    # print(parts)

                    # name = parts[0]

                    for i, field_name in enumerate(self._field_names, 1):
                        value = int(parts[i])
                        sample = SignalRecord(timestamp, value)
                        trace = self._trace_map[field_name]
                        trace.add(sample)
