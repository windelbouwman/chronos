
import math
from .qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from ..data import TimeSpan
from .mouse_select_widget import MouseSelectableWidget
from .graph_widget import GraphWidget
from .log_records_widget import LogRecordsWidget


class TraceVisualizer(QtWidgets.QWidget):
    """ Base visualizer.
    """
    pass


class LogTrace(TraceVisualizer):
    """ Visualizer for a series of log messages.
    """
    def __init__(self, zoom_agent):
        super().__init__()
        l = QtWidgets.QHBoxLayout()
        self.setLayout(l)
        self._label = QtWidgets.QLabel()
        self._label.setText("Log x")
        l.addWidget(self._label)

        self._graph = LogRecordsWidget(zoom_agent)
        l.addWidget(self._graph)


class SignalTrace(TraceVisualizer):
    """ Visualizer for one or more signals.
    """
    def __init__(self, zoom_agent):
        super().__init__()
        l = QtWidgets.QHBoxLayout()
        self.setLayout(l)
        self._label = QtWidgets.QLabel()
        self._label.setText("FubarPlot12345")
        l.addWidget(self._label)

        self._graph = GraphWidget(zoom_agent)
        l.addWidget(self._graph)


class TimeScale:
    pass


class TimeAxisWidget(MouseSelectableWidget):
    """ Top (or bottom) time axis from left to right.
    """
    def __init__(self, zoom_agent):
        super().__init__(zoom_agent)

        policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        self.setSizePolicy(policy)
        self.setMinimumSize(0, 70)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)

        self.draw_axis(painter)
        self.draw_cursor(painter, event.rect())
    
    def draw_axis(self, painter):
        painter.setPen(Qt.black)

        # TODO: draw correct stuff
        for tick in range(0, 600, 35):
            painter.drawLine(tick, 0, tick, 20)
            painter.drawText(tick, 30, str(tick))


class Fubar(QtWidgets.QWidget):
    def __init__(self, zoom_agent):
        super().__init__()
        self._zoom_agent = zoom_agent
        self._traces = []

        # TODO: scroll area with vbox layout for vertical scroll.
        l = QtWidgets.QVBoxLayout()
        self._axis_top = TimeAxisWidget(self._zoom_agent)
        l.addWidget(self._axis_top)
        self.setLayout(l)

        trace1 = SignalTrace(self._zoom_agent)
        l.addWidget(trace1)
        self._traces.append(trace1)

        log1 = LogTrace(self._zoom_agent)
        l.addWidget(log1)

        trace2 = SignalTrace(self._zoom_agent)
        l.addWidget(trace2)
        self._traces.append(trace2)
