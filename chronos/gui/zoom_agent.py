""" Keeps track of the current zoom level.

Also the current cursor position.
"""

import logging
from .qt_wrapper import QtCore

from ..data import TimeStamp, TimeSpan
from .transform import TimeTransform


class ZoomAgent(QtCore.QObject):
    zoom_changed = QtCore.pyqtSignal()
    cursor_changed = QtCore.pyqtSignal(TimeStamp)
    cursor_hidden = QtCore.pyqtSignal()
    selection_changed = QtCore.pyqtSignal(TimeSpan)
    selection_removed = QtCore.pyqtSignal()

    logger = logging.getLogger('zoom_agent')
    
    def __init__(self):
        super().__init__()
        # Linear zoom: y=a*x+b
        # Assume 400 pixels of screen?
        self._width = 400

        # The current timespan:
        # self._timespan = TimeSpan(begin, end)
        self._transform = TimeTransform()
    
    def pixel_to_timestamp(self, value):
        return self._transform.inverse(value)
    
    def timestamp_to_pixel(self, value):
        return self._transform.forward(value)

    def zoom_fit(self):
        self.logger.info('Zoom fit!!')

        # TODO: fit to data, for now reset transform..
        self._transform._a = 1
        self._transform._b = 0
        self.zoom_changed.emit()

    def get_current_timespan(self):
        # Calculate current timespan:
        return TimeSpan(
            self.pixel_to_timestamp(0),
            self.pixel_to_timestamp(self._width))

    def zoom_out(self):
        self.logger.info('Zoom out!')
        timespan = self.get_current_timespan()
        duration = timespan.duration()
        timespan.begin -= duration / 2
        timespan.end += duration / 2
        self.zoom_to(timespan)

    def zoom_in(self):
        self.logger.info('Zoom in!')
        timespan = self.get_current_timespan()
        duration = timespan.duration()
        timespan.begin += duration / 3
        timespan.end -= duration / 3
        self.zoom_to(timespan)

    def zoom_to(self, timespan):
        """ Zoom to the given timespan. """
        # Calculate new factor and offset values!
        current_timespan = self.get_current_timespan()
        self.logger.info('Zoom from %s to %s', current_timespan, timespan)

        self._transform = TimeTransform.from_points((0, self._width), timespan)
        
        self.zoom_changed.emit()
    
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
