
"""
Graph widget showing a signal over time.
"""

from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_qt5agg import FigureCanvas


class GraphWidget(QtWidgets.QWidget):
    """ Widget showing a graph over time """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.figure = Figure((5.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.canvas)

    def set_data(self, data):
        axes = self.figure.add_subplot(111)
        axes.plot([1, 2, 3, 1, 2, 3, 4, 5, 3, 2, 4, 5])

        # Use cursor:
        cursor = Cursor(axes, useblit=True, color='red', linewidth=3)
