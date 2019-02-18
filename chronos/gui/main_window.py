from PyQt5 import uic, QtWidgets

# from .graph_widget import GraphWidget
from .fubar import Fubar
from .timespan_widget import TimeSpanWidget
from .data_source_model import DataSourceModel


class ChronosMainWindow(QtWidgets.QMainWindow):
    """ Main window which includes a lot of sub windows """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('src/gui/mainwindow.ui', self)
        # self.graph_widget = GraphWidget(self)
        self.bar_charts = Fubar()
        self.setCentralWidget(self.bar_charts)
        self.timeSpanWidget = TimeSpanWidget()
        self.timeSpanDockWidget.setWidget(self.timeSpanWidget)

    def load_data(self, data):
        # data = [1, 2, 3, 1, 2, 3, 4, 5, 3, 2, 4, 5]
        # axes = self.graph_widget.set_data(data)
        pass

        # self.signal_model = DataSourceModel()
        # self.signalsTreeView.setModel(self.signal_model)
