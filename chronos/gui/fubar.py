
import math
from .qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from ..data import TimeSpan
from .mouse_select_widget import MouseSelectableWidget
from .graph_widget import GraphWidget
from .log_records_widget import LogRecordsWidget
from .time_axis_widget import TimeAxisWidget


class TraceVisualizer(QtWidgets.QFrame):
    """ Base visualizer.
    """
    def __init__(self):
        super().__init__()
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setAutoFillBackground(True)
        self.setFrameStyle(QtWidgets.QFrame.Raised | QtWidgets.QFrame.Panel)
        self.setLineWidth(2)


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


class Fubar(QtWidgets.QWidget):
    def __init__(self, zoom_agent):
        super().__init__()
        self._zoom_agent = zoom_agent
        self._traces = []

        l = QtWidgets.QVBoxLayout()
        self._axis_top = TimeAxisWidget(self._zoom_agent)
        l.addWidget(self._axis_top)
        self.setLayout(l)

        # Scroll area:
        self._scroll = QtWidgets.QScrollArea()
        self._scroll.setBackgroundRole(QtGui.QPalette.Dark)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        l.addWidget(self._scroll)

        # Inner widget:
        self._inner = QtWidgets.QWidget()
        self._scroll.setWidget(self._inner)
        l2 = QtWidgets.QVBoxLayout()
        self._inner.setLayout(l2)
        self._inner.setMinimumWidth(400)
        self._inner.setMinimumHeight(700)

        trace1 = SignalTrace(self._zoom_agent)
        l2.addWidget(trace1)
        self._traces.append(trace1)

        log1 = LogTrace(self._zoom_agent)
        l2.addWidget(log1)

        trace2 = SignalTrace(self._zoom_agent)
        l2.addWidget(trace2)
        self._traces.append(trace2)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # When resizing, ensure proper width of content view.
        width = event.size().width() - 50
        self._zoom_agent._width = width
        self._inner.setMinimumWidth(width)
        self._inner.setMaximumWidth(width)