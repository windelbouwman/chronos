
import json
from urllib.parse import urlparse
from .qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from ..data import TimeSpan
from .mouse_select_widget import MouseSelectableWidget
from .graph_widget import GraphWidget
from .log_records_widget import LogRecordsWidget
from .time_axis_widget import TimeAxisWidget
from .trace_visualizer import TraceVisualizer


class SignalTraceVisualizer(TraceVisualizer):
    """ Visualizer for one or more signals.
    """

    def __init__(self, zoom_agent, database):
        super().__init__()
        self._database = database
        l = QtWidgets.QHBoxLayout()
        self.setLayout(l)
        # Some controls:
        self._label = QtWidgets.QLabel()
        self._label.setText("FubarPlot12345")
        l.addWidget(self._label)

        self._frame = QtWidgets.QFrame()
        self._frame.setLineWidth(2)
        self._frame.setFrameStyle(QtWidgets.QFrame.Sunken | QtWidgets.QFrame.Panel)
        l.addWidget(self._frame)
        l2 = QtWidgets.QVBoxLayout()
        self._frame.setLayout(l2)
        self._graph = GraphWidget(zoom_agent)
        l2.addWidget(self._graph)

        self.setAcceptDrops(True)
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasFormat('application/x-fubar'):
            event.accept()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasFormat('application/x-fubar'):
            data = mimeData.data('application/x-fubar').data()
            uris = json.loads(data.decode('ascii'))
            for uri in uris:
                print('Dropping', uri)
                o = urlparse(uri)
                # print(o)
                if o.scheme == 'trace':
                    trace_id = int(o.netloc)
                    trace = self._database.get_trace(trace_id)
                    self._graph.add_trace(trace)
                else:
                    print(f'Not supported scheme: {o.scheme}')
