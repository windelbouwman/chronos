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
        self.setMinimumSize(0, 70)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)

        self.draw_axis(painter, event.rect())
        self.draw_cursor(painter, event.rect())



    def draw_axis(self, painter, rect):
        painter.setPen(Qt.black)

        # Determine tick per scale some how?
        major_ticks = self.calc_tick()

        fontMetrics = painter.fontMetrics()
        for tick in major_ticks:
            x = self.timestamp_to_pixel(tick)
            painter.drawLine(x, 0, x, 10)
            label_text = str(tick.stamp)
            rect = fontMetrics.boundingRect(label_text)
            painter.drawText(x - rect.width()/2, 30, label_text)

        # TODO: draw correct stuff
        # for tick in range(0, 600, 35):
        #     painter.drawLine(tick, 0, tick, 20)
        #     painter.drawText(tick, 30, str(tick))
