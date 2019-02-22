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
        self._transform._a = 1
        self.zoom_changed.emit()

    def zoom_out(self):
        self.logger.info('Zoom out!')
        self._transform._a *= 0.9
        self.zoom_changed.emit()

    def zoom_in(self):
        self.logger.info('Zoom in!')
        self._transform._a *= 1.2
        self.zoom_changed.emit()

    def zoom_to(self, timespan):
        # Calculate new factor and offset values!
        # Calculate current timespan:
        current_timespan = TimeSpan(
            self.pixel_to_timestamp(0),
            self.pixel_to_timestamp(self._width))
        self.logger.info('Zoom from %s to %s', current_timespan, timespan)
        
        self._transform._a = timespan.duration().to_seconds() / self._width

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
