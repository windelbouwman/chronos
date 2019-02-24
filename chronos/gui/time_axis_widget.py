from .qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from .mouse_select_widget import MouseSelectableWidget
from ..data import Duration, TimeSpan


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

        tick_space = 35  # Minimum amount of pixels between tickzz
        duration = self.pixels_to_duration(tick_space)
        # print(duration)
        # Round duration upwards to sensible multiple:
        scales = [
            Duration.from_seconds(1),
            Duration.from_seconds(10),
            Duration.from_minutes(1),
            Duration.from_minutes(5),
        ]
        for scale in scales:
            if duration < scale:
                break

        # print(scale)
        timespan = TimeSpan(
            self.pixel_to_timestamp(rect.x()),
            self.pixel_to_timestamp(rect.x() + rect.width()),
        )
        ts = timespan.begin
        ts.round_down(scale)
        while ts < timespan.end:
            tick = self.timestamp_to_pixel(ts)
            painter.drawLine(tick, 0, tick, 20)
            painter.drawText(tick, 30, str(ts))

            ts += scale

        # TODO: draw correct stuff
        # for tick in range(0, 600, 35):
        #     painter.drawLine(tick, 0, tick, 20)
        #     painter.drawText(tick, 30, str(tick))
