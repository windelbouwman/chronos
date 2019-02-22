from .qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from .mouse_select_widget import MouseSelectableWidget


class TimeAxisWidget(MouseSelectableWidget):
    """ Top (or bottom) time axis from left to right.
    """

    def __init__(self, zoom_agent):
        super().__init__(zoom_agent)

        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred
        )
        self.setSizePolicy(policy)
        self.setMinimumSize(0, 70)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)

        self.draw_axis(painter)
        self.draw_cursor(painter, event.rect())

    def draw_axis(self, painter):
        painter.setPen(Qt.black)

        # TODO: draw correct stuff
        for tick in range(0, 600, 35):
            painter.drawLine(tick, 0, tick, 20)
            painter.drawText(tick, 30, str(tick))
