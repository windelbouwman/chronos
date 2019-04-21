""" Graph widget showing a signal over time.

"""

import math
from ..qt_wrapper import QtWidgets, QtGui, Qt, QtCore
from .mouse_select_widget import MouseSelectableWidget
from ...data import TimeStamp, Trace


class ValueAxis:
    def draw(self):
        pass


class GraphWidget(MouseSelectableWidget):
    """ Implements plotting of a signal by using paintEvent.
    """

    def __init__(self, zoom_agent):
        super().__init__(zoom_agent)
        self._traces = []
        self._zoom_levels = []
        for a in range(-2, 20):
            for b in [1, 2, 5]:
                self._zoom_levels.append(b * 10**a)
        self._current_zoom_level = 3
        self._unit_per_div = self._zoom_levels[self._current_zoom_level]
        self._div_size = 30  # Pixels per division, horizontal as well as vertical.
        self._num_vertical_divs = 10  # take 10 divs, like on oscilloscope.

        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        self.setSizePolicy(policy)
        self.setFixedHeight(self._div_size * self._num_vertical_divs)

        self.setToolTip("Drag data signals into this plot them!")

    def zoom_in(self):
        self.set_zoom_level(self._current_zoom_level - 1)
    
    def zoom_out(self):
        self.set_zoom_level(self._current_zoom_level + 1)
    
    def set_zoom_level(self, level):
        if level < 0:
            level = 0
        elif level >= len(self._zoom_levels):
            level = len(self._zoom_levels) - 1
        
        self._current_zoom_level = level
        self._unit_per_div = self._zoom_levels[self._current_zoom_level]
        self.update()

    def add_trace(self, trace):
        """ Add a trace to this graph. """
        assert isinstance(trace.trace, Trace)
        self._traces.append(trace)
        trace.trace.data_changed.subscribe(self.on_data_changed)
        self.update()

    def on_data_changed(self):
        self.update()

    def value_to_pixel(self, value):
        zero_pixel = self._div_size * (self._num_vertical_divs // 2)
        pixel_per_value = -self._div_size / self._unit_per_div
        pixel = zero_pixel + pixel_per_value * value
        return pixel

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)

        # Draw square
        painter.setPen(Qt.black)
        painter.drawLine(0, 0, self.width() - 1, 0)
        painter.drawLine(0, self.height() - 1, self.width() - 1, self.height() - 1)
        painter.drawLine(0, 0, 0, self.height() - 1)
        painter.drawLine(self.width() - 1, 0, self.width() - 1, self.height() - 1)

        # Paint the several thingies:
        self.draw_grid(painter, event.rect())
        self.draw_value_axis(painter, event.rect())
        self.draw_signals(painter, event.rect())
        self.draw_cursor(painter, event.rect())
        self.draw_current_value(painter)

    def draw_signals(self, painter, rect):
        for trace in self._traces:
            # TODO: instead of getting all samples, only get
            # samples in view, and also resample the samples
            # so that we do not draw millions of points.
            # print(trace)
            points = trace.trace.samples
            pen = QtGui.QPen(trace.color)
            pen.setWidth(2)
            painter.setPen(pen)

            for p1, p2 in zip(points[:-1], points[1:]):
                x1 = self.timestamp_to_pixel(p1.timestamp)
                y1 = self.value_to_pixel(p1.value)
                x2 = self.timestamp_to_pixel(p2.timestamp)
                y2 = self.value_to_pixel(p2.value)
                painter.drawLine(x1, y1, x2, y2)

    def get_y_ticks(self):
        """ Get a series of y,value pairs. """
        ticks = []
        for i in range(self._num_vertical_divs + 1):
            y = i * self._div_size
            value = ((self._num_vertical_divs // 2) - i) * self._unit_per_div
            ticks.append((y, value))
        return ticks

    def draw_value_axis(self, painter, rect):
        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        font_metrics = painter.fontMetrics()
        ticks = self.get_y_ticks()

        x0 = 0
        for y, value in ticks:
            painter.drawLine(x0, y, x0 + 15, y)
            text = str(value)
            text_height = font_metrics.boundingRect(text).height()
            # print(y, text_height, text)
            painter.drawText(x0 + 20, y + (text_height / 2), text)


    def draw_grid(self, painter, rect):
        """ Draw gridlines. """
        # TODO: fixed grid, variable legend on the ticks.

        # First draw a lightgray grid
        painter.setPen(Qt.lightGray)

        x0, y0 = rect.x(), rect.y()
        y2 = rect.y() + rect.height()
        x2 = rect.x() + rect.width()

        y_ticks = self.get_y_ticks()
        for y, _ in y_ticks:
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
                continue
                # TODO: figure proper value.
                cursor_value = 12
                text = '{}={}'.format(trace.trace.name, cursor_value)
                painter.drawText(x, y, text)
                y += 15
