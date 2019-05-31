import time
import math
from ..qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from ...data import TimeSpan, Duration
from ..zoom_agent import MouseMode


class MouseSelectableWidget(QtWidgets.QWidget):
    """ Widget which has mouse selection stuff.

    Handles:
    - Cursor location.
    - Zoom selection block.
    """

    def __init__(self, zoom_agent):
        super().__init__()
        self._zoom_agent = zoom_agent
        # Cursor and selection:
        self._cursor = None
        self._selection = None
        self._cursor_x2 = None

        self.setMouseTracking(True)

        # Some spiffy events:
        self._zoom_agent.cursor_changed.connect(self.on_cursor_changed)
        self._zoom_agent.cursor_hidden.connect(self.on_cursor_hidden)
        self._zoom_agent.selection_changed.connect(self.on_selection_changed)
        self._zoom_agent.selection_removed.connect(self.on_selection_removed)
        self._zoom_agent.zoom_changed.connect(self.on_zoom_changed)

    def pixel_to_timestamp(self, value):
        return self._zoom_agent.pixel_to_timestamp(value)

    def timestamp_to_pixel(self, timestamp):
        return self._zoom_agent.timestamp_to_pixel(timestamp)

    def pixels_to_duration(self, pixels):
        return self._zoom_agent.pixels_to_duration(pixels)

    def get_x_ticks(self):
        """ Return a list with x pixel positions and labels. """
        timespan, scale, major_ticks = self.calc_ticks()

        if scale.attos < 60:  # Below 1 minute step size
            fmt = '%H:%M:%S'
        elif scale.attos < 3600:  # Below 1 hour step size
            fmt = '%H:%M'
        else:  # Above 1 hour steps:
            fmt = '%Y-%m-%d %H:%M'

        def sensible_time_str(timestamp):
            """ Convert ticks into pixel positions and text labels """
            t2 = time.localtime(timestamp.stamp)
            return time.strftime(fmt, t2)

        x_ticks = [
            (self.timestamp_to_pixel(t), sensible_time_str(t))
            for t in major_ticks
        ]
        return x_ticks

    def calc_ticks(self):
        """ Calculate major ticks.
        """
        timespan = TimeSpan(
            self.pixel_to_timestamp(0),
            self.pixel_to_timestamp(self._zoom_agent._width),
        )

        tick_space = 80  # Minimum amount of pixels between tickzz
        duration = self.pixels_to_duration(tick_space)
        # print(duration)
        # Round duration upwards to sensible multiple:
        scales = [
            Duration.from_seconds(0.0001),
            Duration.from_seconds(0.001),
            Duration.from_seconds(0.01),
            Duration.from_seconds(0.1),
            Duration.from_seconds(1),
            Duration.from_seconds(5),
            Duration.from_seconds(10),
            Duration.from_seconds(30),
            Duration.from_minutes(1),
            Duration.from_minutes(5),
            Duration.from_minutes(10),
            Duration.from_minutes(30),
            Duration.from_hours(1),
            Duration.from_hours(5),
            Duration.from_hours(12),
            Duration.from_days(1),
            Duration.from_days(30),
            Duration.from_days(365),
        ]
        for scale in scales:
            if duration < scale:
                break

        # print(scale)
        ts = timespan.begin
        ts.round_down(scale)

        # Create ticks:
        ticks = []
        while ts < timespan.end:
            ticks.append(ts.copy())
            ts += scale

        return timespan, scale, ticks

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._zoom_agent.hide_cursor()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self._zoom_agent.mouse_mode == MouseMode.ZOOM_HORIZONTAL:
            self._cursor_x2 = event.x()
            self.update()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self._zoom_agent.mouse_mode == MouseMode.ZOOM_HORIZONTAL:
            self.emit_zoom(event.x())
        self._cursor_x2 = None
        self._zoom_agent.clear_selection()

    def wheelEvent(self, event):
        super().wheelEvent(event)
        if event.modifiers() & Qt.ControlModifier:
            event.accept()
            x = event.x()
            ts_center = self.pixel_to_timestamp(x)
            self._zoom_agent.zoom_around(ts_center, event.angleDelta().y())

    def emit_zoom(self, x):
        if x > self._cursor_x2:
            x1 = self._cursor_x2
            x2 = x
        elif x < self._cursor_x2:
            x1 = x
            x2 = self._cursor_x2
        else:
            print("No zooming")
            return

        zoom_begin = self.pixel_to_timestamp(x1)
        zoom_end = self.pixel_to_timestamp(x2)
        zoom_range = TimeSpan(zoom_begin, zoom_end)
        self._zoom_agent.zoom_to(zoom_range)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        x = event.x()
        timestamp = self.pixel_to_timestamp(x)
        self._zoom_agent.set_cursor(timestamp)
        # If we are pressed, emit selection:
        if self._cursor_x2 is not None and self._zoom_agent.mouse_mode == MouseMode.ZOOM_HORIZONTAL:
            x1 = min(x, self._cursor_x2)
            x2 = max(x, self._cursor_x2)
            timespan = TimeSpan(
                self.pixel_to_timestamp(x1), self.pixel_to_timestamp(x2)
            )
            self._zoom_agent.set_selection(timespan)

    def on_cursor_changed(self, timestamp):
        """ Current location changed! """
        self._cursor = timestamp
        self.update()

    def on_cursor_hidden(self):
        self._cursor = None
        self.update()

    def on_selection_changed(self, timespan):
        """ Current selection changed! """
        self._selection = timespan
        self.update()

    def on_selection_removed(self):
        self._selection = None
        self.update()

    def on_zoom_changed(self):
        self.update()

    def draw_cursor(self, painter, rect):
        # print('voodoo', rect)
        if self._selection is not None:
            # We have a selection!
            x = self.timestamp_to_pixel(self._selection.begin)
            w = self.timestamp_to_pixel(self._selection.end) - x

            color = QtGui.QColor(Qt.darkBlue)
            color.setAlphaF(0.2)
            brush = QtGui.QBrush(color)
            selection_rect = QtCore.QRect(x, rect.y(), w, rect.height())
            painter.fillRect(selection_rect, brush)

        if self._cursor is not None:
            x = self.timestamp_to_pixel(self._cursor)
            painter.setPen(Qt.blue)
            painter.drawLine(x, rect.y(), x, rect.height() + rect.y())
