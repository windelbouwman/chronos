
import itertools
from ..qt_wrapper import QtWidgets, QtGui, Qt, QtCore
from .graph_widget import GraphWidget
from .trace_visualizer import TraceVisualizer


class Trace2:
    """ A visualized signal.
    
    Contains a reference to the traced signal.
    Contains information about style and coloring.
    """
    def __init__(self, trace, color):
        self.color = color
        self.trace = trace


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
        self._signal_list_model = SignalListModel()
        self._signal_view = QtWidgets.QListView()
        self._signal_view.setFixedWidth(70)
        self._signal_view.setModel(self._signal_list_model)
        self._signal_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self._signal_view.customContextMenuRequested.connect(self._on_signal_view_context_menu)

        l2.addWidget(self._signal_view)
        self._zoom_in = QtWidgets.QPushButton('+')
        self._zoom_out = QtWidgets.QPushButton('-')
        l2.addWidget(self._zoom_in)
        l2.addWidget(self._zoom_out)
        l.addLayout(l2)

        self._color_wheel = itertools.cycle([
            Qt.blue,
            Qt.green,
            Qt.red,
            Qt.cyan,
            Qt.magenta,
            Qt.yellow,
            Qt.darkGray,
        ])

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
    
    def _on_signal_view_context_menu(self, pos):
        index = self._signal_view.indexAt(pos)
        if index.isValid():
            trace = self._signal_list_model._traces[index.row()]
            menu = QtWidgets.QMenu()
            def do_delete():
                print('Delete!!')
                self._graph.remove_trace(trace)
                self._signal_list_model.remove_trace(trace)
            
            deleteAction = QtWidgets.QAction('Delete')
            deleteAction.triggered.connect(do_delete)
            menu.addAction(deleteAction)

            def do_properties():
                print('Properties!')
                dialog = PlottedSignalPropertiesDialog(self._signal_view, trace)
                dialog.exec()

            propertiesAction = QtWidgets.QAction('Properties')
            propertiesAction.triggered.connect(do_properties)
            menu.addAction(propertiesAction)

            pos2 = self._signal_view.viewport().mapToGlobal(pos)
            menu.exec(pos2)

    def get_next_color(self):
        return next(self._color_wheel)

    def handle_drop(self, o):
        trace_id = int(o.netloc)
        trace = self._database.get_trace(trace_id)
        color = self.get_next_color()
        trace = Trace2(trace, color)
        self._graph.add_trace(trace)
        self._signal_list_model.add_trace(trace)


class SignalListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super().__init__()
        self._traces = []
    
    def add_trace(self, trace):
        # self.beginInsertRows()
        self._traces.append(trace)
        # TODO: this is very brute force:
        self.modelReset.emit()

    def remove_trace(self, trace):
        self._traces.remove(trace)
        self.modelReset.emit()

    def data(self, index, role):
        if index.isValid():
            row = index.row()
            trace = self._traces[row]
            if role == Qt.DisplayRole:
                return trace.trace.name
            elif role == Qt.DecorationRole:
                # Create wopping icon:
                pixmap = QtGui.QPixmap(10, 10)
                pixmap.fill(trace.color)
                return pixmap

    def rowCount(self, index):
        if index.isValid():
            pass
        else:
            return len(self._traces)


class PlottedSignalPropertiesDialog(QtWidgets.QDialog):
    def __init__(self, parent, trace):
        super().__init__(parent)
        self.trace = trace
        self.setWindowTitle('Properties of {}'.format(trace.trace.name))

        l1 = QtWidgets.QVBoxLayout()

        l = QtWidgets.QGridLayout()
        label = QtWidgets.QLabel('Name')
        l.addWidget(label, 0, 0)
        label = QtWidgets.QLabel(trace.trace.name)
        l.addWidget(label, 0, 1)
        label = QtWidgets.QLabel('Color')
        l.addWidget(label, 1, 0)
        # icon = 
        color_button = QtWidgets.QPushButton()
        color_button.clicked.connect(self.on_color_clicked)
        l.addWidget(color_button, 1, 1)
        l1.addLayout(l)

        ok_button = QtWidgets.QPushButton('Ok')
        l1.addWidget(ok_button)
        ok_button.clicked.connect(self.on_ok)
        self.setLayout(l1)
    
    def on_ok(self):
        self.close()

    def on_color_clicked(self):
        color = QtWidgets.QColorDialog.getColor()
        self.trace.color = color
