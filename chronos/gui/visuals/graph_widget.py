""" Graph widget showing a signal over time.

"""

import math
from ..qt_wrapper import QtWidgets, QtGui, Qt, QtCore
from .mouse_select_widget import MouseSelectableWidget
from ...data import TimeStamp, Trace


class GraphWidget(MouseSelectableWidget):
    """ Implements plotting of a signal by using paintEvent.
    """

    def __init__(self, zoom_agent):
        super().__init__(zoom_agent)
        self._traces = []

        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        self.setSizePolicy(policy)
        self.setMinimumHeight(300)

    def add_trace(self, trace):
        """ Add a trace to this graph. """
        assert isinstance(trace, Trace)
        self._traces.append(trace)
        trace.data_changed.subscribe(self.on_data_changed)
        self.update()

    def on_data_changed(self):
        self.update()

    def sizeHint(self):
        return QtCore.QSize(40, 300)

    def value_to_pixel(self, value):
        return value

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)

        # Paint the several thingies:
        self.draw_grid(painter, event.rect())
        self.draw_value_axis(painter, event.rect())
        self.draw_signals(painter, event.rect())
        self.draw_cursor(painter, event.rect())
        self.draw_current_value(painter)
        self.draw_legend(painter, event.rect())

    def draw_signals(self, painter, rect):
        for trace in self._traces:
            # TODO: instead of getting all samples, only get
            # samples in view, and also resample the samples
            # so that we do not draw millions of points.
            # print(trace)
            points = trace.samples
            pen = QtGui.QPen(Qt.red)
            pen.setWidth(2)
            painter.setPen(pen)

            for p1, p2 in zip(points[:-1], points[1:]):
                x1 = self.timestamp_to_pixel(p1[0])
                y1 = self.value_to_pixel(p1[1])
                x2 = self.timestamp_to_pixel(p2[0])
                y2 = self.value_to_pixel(p2[1])
                painter.drawLine(x1, y1, x2, y2)

    def get_y_ticks(self):
        ticks = []
        y_max = self.height()
        spacing = 35
        for y in range(0, y_max, spacing):
            ticks.append(y)
        return ticks

    def draw_value_axis(self, painter, rect):
        # TODO: draw y-axis here..

        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        ticks = self.get_y_ticks()

        x0 = 0
        for y in ticks:
            painter.drawLine(x0 + 10, y, x0 + 20, y)
            painter.drawText(x0, y, str(y))


    def draw_grid(self, painter, rect):
        """ Draw gridlines. """
        # TODO: fixed grid, variable legend on the ticks.

        # First draw a lightgray grid
        painter.setPen(Qt.lightGray)

        x0, y0 = rect.x(), rect.y()
        y2 = rect.y() + rect.height()
        x2 = rect.x() + rect.width()

        y_ticks = self.get_y_ticks()
        for y in y_ticks:
            painter.drawLine(x0, y, x2, y)

        # Now drow major ticks:
        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        major_ticks = self.calc_ticks()
        # for x in range(x0, x2, spacing * 5):
        for tick in major_ticks:
            x = self.timestamp_to_pixel(tick)
            painter.drawLine(x, y0, x, y2)

        # for y in range(y0, y2, spacing * 5):
        #     painter.drawLine(x0, y, x2, y)

    def draw_current_value(self, painter):
        if self._cursor is not None:
            painter.setPen(Qt.black)
            x = self.timestamp_to_pixel(self._cursor) + 4
            y = 25

            for trace in self._traces:
                cursor_value = 12
                text = '{}={}'.format(trace.name, cursor_value)
                painter.drawText(x, y, text)
                y += 15

    def draw_legend(self, painter, rect):
        if self._traces:
            font_metrics = painter.fontMetrics()
            width = max(font_metrics.boundingRect(t.name).width() for t in self._traces)
            height = font_metrics.boundingRect("X").height()

            pen = QtGui.QPen(Qt.black)
            pen.setWidth(1)
            painter.setPen(pen)
            x = 10
            y = 10
            legend_rect = QtCore.QRect(x - 4, y - 2, width + 8, height*len(self._traces)+8)
            painter.fillRect(legend_rect, Qt.white)
            painter.drawRect(legend_rect)
            for trace in self._traces:
                y += height
                painter.drawText(x, y, trace.name)
                