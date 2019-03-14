
from ..qt_wrapper import QtWidgets, QtGui, Qt
from .graph_widget import GraphWidget
from .trace_visualizer import TraceVisualizer


class SignalTraceVisualizer(TraceVisualizer):
    """ Visualizer for one or more signals in a plot.
    """

    def __init__(self, zoom_agent, database):
        super().__init__("signaltrace")
        self._database = database
        l = QtWidgets.QHBoxLayout()
        self.setLayout(l)
        # Some controls:
        # self._label = QtWidgets.QPushButton("FubarPlot12345")
        self._label = QtWidgets.QLabel()
        self._label.setText("Fubarplot12345")
        self._label.setFixedWidth(70)
        l2 = QtWidgets.QVBoxLayout()
        l2.addWidget(self._label)
        self._zoom_in = QtWidgets.QPushButton('+')
        self._zoom_out = QtWidgets.QPushButton('-')
        l2.addWidget(self._zoom_in)
        l2.addWidget(self._zoom_out)
        l.addLayout(l2)

        # self._frame = QtWidgets.QFrame()
        # self._frame.setLineWidth(2)
        # self._frame.setFrameStyle(QtWidgets.QFrame.Sunken | QtWidgets.QFrame.Panel)
        # l.addWidget(self._frame)
        # l2 = QtWidgets.QVBoxLayout()
        # self._frame.setLayout(l2)
        self._graph = GraphWidget(zoom_agent)
        l.addWidget(self._graph)

        self._zoom_in.clicked.connect(self._graph.zoom_in)
        self._zoom_out.clicked.connect(self._graph.zoom_out)
    
    def handle_drop(self, o):
        trace_id = int(o.netloc)
        trace = self._database.get_trace(trace_id)
        self._graph.add_trace(trace)
