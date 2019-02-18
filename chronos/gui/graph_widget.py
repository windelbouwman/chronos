""" Graph widget showing a signal over time.

Idea: use matplotlib for the plotting here.
"""

from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_qt5agg import FigureCanvas
# import vispy.mpl_plot as plt


class GraphWidget(QtWidgets.QWidget):
    """ Widget showing a graph over time """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.figure = Figure((5.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.canvas)

    def on_press(self, event):
        self.press_event = event
        print('Mouse pressed', event)

    def on_motion(self, event):
        # print(event)
        pass

    def on_release(self, event):
        e1 = self.press_event
        e2 = event
        x1, x2 = e1.xdata, e2.xdata
        self.axes.set_xlim(x1, x2)
        print(event)
        # TODO: adjust time scale
        self.canvas.update()

    def set_data(self, data):
        # def mpl(self):
        axes = self.figure.add_subplot(111)
        axes.clear()
        # print(data)
        # axes.plot(d[1, 2, 3, 1, 2, 3, 4, 5, 3, 2, 4, 5], 'x-')
        axes.plot(data, 'x-')

        self.axes = axes

        # Use cursor:
        cursor = Cursor(
            axes, useblit=True, color='red', linewidth=3, marker='x')
