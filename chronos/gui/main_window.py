from PyQt5 import uic, QtWidgets

from .graph_widget import GraphWidget
from .timespan_widget import TimeSpanWidget


class ChronosMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi('src/gui/mainwindow.ui', self)
        self.graph_widget = GraphWidget(self)
        self.setCentralWidget(self.graph_widget)
        self.timeSpanWidget = TimeSpanWidget()
        self.timeSpanDockWidget.setWidget(self.timeSpanWidget)

    def load_data(self, data):
        data = [1, 2, 3, 1, 2, 3, 4, 5, 3, 2, 4, 5]
        axes = self.graph_widget.set_data(data)
