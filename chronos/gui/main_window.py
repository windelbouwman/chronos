from PyQt5 import uic, QtWidgets

# from .graph_widget import GraphWidget
from .fubar import Fubar
from .timespan_widget import TimeSpanWidget
from .data_source_model import DataSourceModel
from .zoom_agent import ZoomAgent


class ChronosMainWindow(QtWidgets.QMainWindow):
    """ Main window which includes a lot of sub windows """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('src/gui/mainwindow.ui', self)
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

    def load_data(self, data):
        # data = [1, 2, 3, 1, 2, 3, 4, 5, 3, 2, 4, 5]
        # axes = self.graph_widget.set_data(data)
        pass

        self.signal_model = DataSourceModel()
        self.signalsTreeView.setModel(self.signal_model)
