""" Graph widget showing a signal over time.

"""

import math
from .qt_wrapper import QtWidgets, QtGui, Qt
from .mouse_select_widget import MouseSelectableWidget
from ..data import TimeStamp


class GraphWidget(MouseSelectableWidget):
    """ Implements plotting of a signal by using paintEvent.
    """
    def __init__(self, zoom_agent):
        super().__init__(zoom_agent)

        # Create random data:
        xs = range(300)
        points1 = [(TimeStamp(x), math.sin(x * 0.2) * 80 + 40) for x in xs]
        points2 = [(TimeStamp(x), math.sin(x * 0.6) * 30 + 20) for x in xs]
        self.signals = [points1, points2]

        policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        self.setSizePolicy(policy)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)
        # Paint the several thingies:
        self.draw_grid(painter, event.rect())
        self.draw_signals(painter, event.rect())
        self.draw_cursor(painter, event.rect())
    
    def draw_signals(self, painter, rect):
        for points in self.signals:
            pen = QtGui.QPen(Qt.red)
            pen.setWidth(2)
            painter.setPen(pen)

            for p1, p2 in zip(points[:-1], points[1:]):
                x1 = self.timestamp_to_pixel(p1[0])
                x2 = self.timestamp_to_pixel(p2[0])
                painter.drawLine(x1, p1[1], x2, p2[1])
    
    def draw_grid(self, painter, rect):
        # First draw a lightgray grid
        painter.setPen(Qt.lightGray)

        # TODO: draw correct stuff
        x0 = rect.x()
        y0 = rect.y()
        y2 = rect.y() + rect.height()
        x2 = rect.x() + rect.width()
        spacing = 13
        for x in range(x0, x2, spacing):
            painter.drawLine(x, y0, x, y2)

        for y in range(y0, y2, spacing):
            painter.drawLine(x0, y, x2, y)
        
        # Now drow major ticks:
        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        for x in range(x0, x2, spacing * 5):
            painter.drawLine(x, y0, x, y2)

        for y in range(y0, y2, spacing * 5):
            painter.drawLine(x0, y, x2, y)

