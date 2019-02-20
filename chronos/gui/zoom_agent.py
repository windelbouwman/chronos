""" Keeps track of the current zoom level.

Also the current cursor position.
"""

from .qt_wrapper import QtCore

from ..data import TimeStamp, TimeSpan

class ZoomAgent(QtCore.QObject):
    zoom_changed = QtCore.pyqtSignal()
    cursor_changed = QtCore.pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        # Linear zoom: y=a*x+b
        self._factor = 1
        self._offset = 0
    
    def pixel_to_timestamp(self, value):
        return value
    
    def timestamp_to_pixel(self, value):
        return value

    def zoom_to(self, timespan):
        self.zoom_changed.emit()
    
    def set_cursor(self, timestamp):
        self.cursor_changed.emit(timestamp)

