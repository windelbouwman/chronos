from ..qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from .mouse_select_widget import MouseSelectableWidget
from ...data import Duration, TimeSpan


class TimeAxisWidget(MouseSelectableWidget):
    """ Top (or bottom) time axis from left to right.
    """

    def __init__(self, zoom_agent):
        super().__init__(zoom_agent)

        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred
        )
        self.setSizePolicy(policy)
        self.setMinimumHeight(70)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)

        self.draw_axis(painter, event.rect())
        self.draw_cursor(painter, event.rect())

        if self._cursor is not None:
            painter.setPen(Qt.black)
            x = self.timestamp_to_pixel(self._cursor)
            text = '{}'.format(self._cursor)
            y = 25
            painter.drawText(x + 4, y, text)

    def draw_axis(self, painter, rect):
        painter.setPen(Qt.black)

        # Determine tick per scale some how?
        major_ticks = self.calc_ticks()
        y2 = self.height() - 1
        y1 = y2 - 10

        painter.drawLine(rect.x(), y2, rect.x() + rect.width(), y2)

        fontMetrics = painter.fontMetrics()
        for tick in major_ticks:
            x = self.timestamp_to_pixel(tick)
            painter.drawLine(x, y1, x, y2)
            label_text = str(tick.stamp)
            label_rect = fontMetrics.boundingRect(label_text)

            painter.drawText(x - label_rect.width()/2, y1 - 5, label_text)

        # TODO: draw correct stuff
        # for tick in range(0, 600, 35):
        #     painter.drawLine(tick, 0, tick, 20)
        #     painter.drawText(tick, 30, str(tick))

    def resizeEvent(self, event):
        width = event.size().width()
        self._zoom_agent._width = width
