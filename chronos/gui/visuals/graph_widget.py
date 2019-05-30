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
        self._zoom_levels = []
        self._padding = 3
        self._tick_length = 5
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
    
    def remove_trace(self, trace):
        assert isinstance(trace.trace, Trace)
        self._traces.remove(trace)
        trace.trace.data_changed.unsubscribe(self.on_data_changed)
        self.update()

    def on_data_changed(self):
        self.update()

    def value_to_pixel(self, value):
        zero_pixel = self._div_size * (self._num_vertical_divs // 2)
        pixel_per_value = -self._div_size / self._unit_per_div
        pixel = zero_pixel + pixel_per_value * value
        return pixel

    def paintEvent(self, event):
        """ And so the journey begins. The drawing of a plot...

        A journey of a thousand miles begins with
        the first step... lets clear the background ;)
        """
        super().paintEvent(event)

        # Clear background:
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)

        x_ticks = self.get_x_ticks()

        # Calculate the height of the bottom tick markers
        font_metrics = painter.fontMetrics()
        text_height = max(font_metrics.boundingRect(t[1]).height() for t in x_ticks)

        y_top = self._padding
        y_bottom = self.height() - 1 - self._padding - text_height - self._padding - self._tick_length

        y_ticks = self.get_y_ticks(y_top, y_bottom)

        max_y_label_width = max(font_metrics.boundingRect(t[1]).width() for t in y_ticks)
        x_left = self._padding + max_y_label_width + self._padding + self._tick_length
        x_right = self.width() - 1 - self._padding

        top_left = QtCore.QPoint(x_left, y_top)
        bottom_right = QtCore.QPoint(x_right, y_bottom)
        chart_rect = QtCore.QRect(top_left, bottom_right)

        # Paint the several thingies:
        self.draw_square(painter, x_left, y_top, x_right, y_bottom)
        self.draw_value_axis(painter, font_metrics, y_ticks, x_left, y_top, y_bottom)
        self.draw_time_axis(painter, font_metrics, x_ticks, y_bottom, x_left)

        # Now set clipping region to valid graph region:
        painter.setClipRect(chart_rect)
        painter.setClipping(True)
        self.draw_grid(painter, x_ticks, y_ticks, x_left, y_top, x_right, y_bottom)
        self.draw_signals(painter)
        self.draw_cursor(painter, event.rect())
        self.draw_current_value(painter)

    def draw_square(self, painter, x_left, y_top, x_right, y_bottom):
        painter.setPen(Qt.black)
        painter.drawLine(x_left, y_top, x_right, y_top)
        painter.drawLine(x_left, y_bottom, x_right, y_bottom)
        painter.drawLine(x_left, y_top, x_left, y_bottom)
        painter.drawLine(x_right, y_top, x_right, y_bottom)

    def draw_signals(self, painter):
        # this line below renders top-notch stuff, but also slows down the drawing a bit!
        # painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        for trace in self._traces:
            # TODO: instead of getting all samples, only get
            # samples in view, and also resample the samples
            # so that we do not draw millions of points.
            # print(trace)
            points = trace.trace.samples
            pen = QtGui.QPen(trace.color)
            pen.setWidth(2)
            painter.setPen(pen)

            # Create Qt points at pixel locations:
            qpoints = [
                QtCore.QPoint(self.timestamp_to_pixel(p.timestamp), self.value_to_pixel(p.value))
                for p in points
            ]

            painter.drawPolyline(QtGui.QPolygon(qpoints))

    def get_y_ticks(self, y_top, y_bottom):
        """ Get a series of y,value pairs. """
        ticks = []
        for i in range(self._num_vertical_divs + 1):
            y = i * self._div_size
            text = str(((self._num_vertical_divs // 2) - i) * self._unit_per_div)
            ticks.append((y, text))
        return ticks

    def draw_time_axis(self, painter, font_metrics, x_ticks, y_bottom, x_left):
        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        for x, text in x_ticks:
            if x < x_left:
                continue
            painter.drawLine(x, y_bottom, x, y_bottom + self._tick_length)
            text_rect = font_metrics.boundingRect(text)
            text_height = text_rect.height()
            text_width = text_rect.width()
            y = y_bottom + self._tick_length + self._padding + text_height
            painter.drawText(x - text_width // 2, y, text)

    def draw_value_axis(self, painter, font_metrics, y_ticks, x_left, y_top, y_bottom):
        """ Draw Y-axis ticks. """
        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        for y, text in y_ticks:
            if y < y_top:
                continue
            elif y > y_bottom:
                continue
            painter.drawLine(x_left - self._tick_length, y, x_left, y)
            text_rect = font_metrics.boundingRect(text)
            dy = text_rect.y() + (text_rect.height() // 2)
            text_y = y - dy
            text_width = text_rect.width()
            # print(y, text_height, text)
            x = x_left - self._tick_length - self._padding - text_width
            # print(y, text, text_y, font_metrics, font_metrics.ascent(), text_rect)
            painter.drawText(x, text_y, text)

    def draw_grid(self, painter, x_ticks, y_ticks, x_left, y_top, x_right, y_bottom):
        """ Draw gridlines. """
        # TODO: fixed grid, variable legend on the ticks.

        # First draw a lightgray grid
        painter.setPen(Qt.lightGray)

        for y, _ in y_ticks:
            painter.drawLine(x_left, y, x_right, y)

        # Now drow major ticks:
        pen = QtGui.QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)
        
        # for x in range(x0, x2, spacing * 5):
        for x, _ in x_ticks:
            painter.drawLine(x, y_top, x, y_bottom)

        # for y in range(y0, y2, spacing * 5):
        #     painter.drawLine(x0, y, x2, y)

    def draw_current_value(self, painter):
        if self._cursor is not None:
            # x = self.timestamp_to_pixel(self._cursor) + 4
            # y = 25

            for trace in self._traces:
                nearest_sample = trace.trace.find_nearest_sample(self._cursor)
                if nearest_sample:
                    painter.setPen(trace.color)

                    x2 = self.timestamp_to_pixel(nearest_sample.timestamp)
                    y2 = self.value_to_pixel(nearest_sample.value)

                    # Draw marker circle:
                    painter.drawEllipse(x2 - 5, y2 - 5, 10, 10)

                    # Draw label:
                    cursor_value = nearest_sample.value
                    text = '{}={}'.format(trace.trace.name, cursor_value)
                    painter.drawText(x2 + 10, y2 + 10, text)


class ValueAxis:
    def draw(self):
        pass
