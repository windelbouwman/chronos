from ..qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from ...data import TimeSpan
from .log_records_widget import LogRecordsWidget
from .trace_visualizer import TraceVisualizer


class LogTraceVisualizer(TraceVisualizer):
    """ Visualizer for a series of log messages.
    """

    def __init__(self, zoom_agent, database):
        super().__init__("logtrace")
        self._database = database
        l = QtWidgets.QHBoxLayout()
        self.setLayout(l)
        self._label = QtWidgets.QLabel()
        self._label.setText("Log x")
        self._label.setFixedWidth(70)
        l.addWidget(self._label)

        self._logs = LogRecordsWidget(zoom_agent)
        l.addWidget(self._logs)

    def handle_drop(self, o):
        trace_id = int(o.netloc)
        trace = self._database.get_trace(trace_id)
        self._logs.add_trace(trace)
