from PyQt5 import uic
from .qt_wrapper import QtWidgets

# from .graph_widget import GraphWidget
from .fubar import Fubar
from .timespan_widget import TimeSpanWidget
from .data_source_model import DataSourceModel
from .zoom_agent import ZoomAgent
from ..data_plugins.demo import DemoDataSource


class ChronosMainWindow(QtWidgets.QMainWindow):
    """ Main window which includes a lot of sub windows """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi("src/gui/mainwindow.ui", self)
        # self.graph_widget = GraphWidget(self)
        self._zoom_agent = ZoomAgent()
        self.bar_charts = Fubar(self._zoom_agent)
        self.setCentralWidget(self.bar_charts)
        self.timeSpanWidget = TimeSpanWidget(self._zoom_agent)
        self.timeSpanDockWidget.setWidget(self.timeSpanWidget)

        self.signalsDockWidget.setWindowTitle("Signals")
        # self.signalsTreeView.setModel()
        self.load_data(1)

        self.menuView.addAction(self.timeSpanDockWidget.toggleViewAction())
        self.menuView.addAction(self.signalsDockWidget.toggleViewAction())

        self.actionZoomFit.triggered.connect(self._zoom_agent.zoom_fit)
        self.actionZoomOut.triggered.connect(self._zoom_agent.zoom_out)
        self.actionZoomIn.triggered.connect(self._zoom_agent.zoom_in)
        self.actionPanLeft.triggered.connect(self._zoom_agent.pan_left)
        self.actionPanRight.triggered.connect(self._zoom_agent.pan_right)

        # What must happen when data source is added:
        self.pushButtonAddDataSource.clicked.connect(self._add_data_source)

    def _add_data_source(self):
        print("add data")
        # TODO: show wizard to select proper plugin.
        self.signal_model.sources.append(DemoDataSource())
        self.signal_model.modelReset.emit()

    def load_data(self, data):
        # data = [1, 2, 3, 1, 2, 3, 4, 5, 3, 2, 4, 5]
        # axes = self.graph_widget.set_data(data)
        pass

        self.signal_model = DataSourceModel()
        self.signalsTreeView.setModel(self.signal_model)
