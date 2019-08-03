""" Keeps track of the current zoom level.

Also the current cursor position.
"""

import logging
from .qt_wrapper import QtCore

from ..data import TimeStamp, TimeSpan, Duration
from .transform import TimeTransform


class MouseMode:
    ZOOM_HORIZONTAL = 1
    PANNING = 3


class ZoomAgent(QtCore.QObject):
    zoom_changed = QtCore.pyqtSignal()
    cursor_changed = QtCore.pyqtSignal(TimeStamp)
    cursor_hidden = QtCore.pyqtSignal()
    selection_changed = QtCore.pyqtSignal(TimeSpan)
    selection_removed = QtCore.pyqtSignal()

    logger = logging.getLogger("zoom_agent")

    def __init__(self):
        super().__init__()
        self.mouse_mode = MouseMode.ZOOM_HORIZONTAL
        # Linear zoom: y=a*x+b
        # Assume 400 pixels of screen?
        self._width = 400

        # The current timespan:
        # self._timespan = TimeSpan(begin, end)
        self._transform = TimeTransform()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._on_timeout)
        self._timer.setInterval(70)
        self._follow_duration = None

    def _on_timeout(self):
        assert self._follow_duration
        now = TimeStamp.now()
        t2 = now + Duration.from_seconds(1)
        t1 = now - self._follow_duration - Duration.from_seconds(1)
        timespan = TimeSpan(t1, t2)
        self._inner_zoom_to(timespan)

    def start_to_follow(self, duration):
        """ Start to track a certain last x time. """
        self._follow_duration = duration
        if not self._timer.isActive():
            self._timer.start()

    def stop_follow(self):
        """ Stop scrolling the time axis. """
        if self._timer.isActive():
            self._timer.stop()

    def pixel_to_timestamp(self, value):
        return self._transform.inverse(value)

    def timestamp_to_pixel(self, value):
        return self._transform.forward(value)

    def pixels_to_duration(self, pixels):
        t0 = self.pixel_to_timestamp(0)
        t1 = self.pixel_to_timestamp(pixels)
        return t1 - t0

    def get_current_timespan(self):
        # Calculate current timespan:
        return TimeSpan(
            self.pixel_to_timestamp(0), self.pixel_to_timestamp(self._width)
        )

    # Manual zoom commands:
    def zoom_out(self):
        self.logger.info("Zoom out!")
        timespan = self.get_current_timespan()
        duration = timespan.duration()
        timespan.begin -= duration / 7
        timespan.end += duration / 7
        self.zoom_to(timespan)

    def zoom_in(self):
        self.logger.info("Zoom in!")
        timespan = self.get_current_timespan()
        duration = timespan.duration()
        timespan.begin += duration / 7
        timespan.end -= duration / 7
        self.zoom_to(timespan)

    def pan_left(self):
        self.logger.info("Pan left!")
        timespan = self.get_current_timespan()
        duration = timespan.duration()
        timespan.begin -= duration / 7
        timespan.end -= duration / 7
        self.zoom_to(timespan)

    def pan_right(self):
        self.logger.info("Pan right!")
        timespan = self.get_current_timespan()
        duration = timespan.duration()
        timespan.begin += duration / 7
        timespan.end += duration / 7
        self.zoom_to(timespan)

    def zoom_to(self, timespan):
        """ Zoom to the given timespan. """
        self.stop_follow()
        self.logger.info("Zoom to %s", timespan)
        self._inner_zoom_to(timespan)

    def _inner_zoom_to(self, timespan):
        """ This is a non-manual zoom, used by the tracking timer. """
        # Calculate new factor and offset values!
        # current_timespan = self.get_current_timespan()

        self._transform = TimeTransform.from_points((0, self._width), timespan)

        self.zoom_changed.emit()

    def zoom_around(self, timestamp, amount):
        current_timespan = self.get_current_timespan()
        assert timestamp > current_timespan.begin
        left_duration = timestamp - current_timespan.begin
        assert current_timespan.end > timestamp
        right_duration = current_timespan.end - timestamp
        # print(left_duration, right_duration)

        percentage = (100 + amount) / 100
        left_duration *= percentage
        right_duration *= percentage

        timespan = TimeSpan(timestamp - left_duration, timestamp + right_duration)
        self.zoom_to(timespan)

    def set_selection(self, timespan):
        self.selection_changed.emit(timespan)

    def clear_selection(self):
        self.selection_removed.emit()

    def set_cursor(self, timestamp):
        """ Set current cursor to timestamp.
        
        Can be none!
        """
        self.cursor_changed.emit(timestamp)

    def hide_cursor(self):
        self.cursor_hidden.emit()
