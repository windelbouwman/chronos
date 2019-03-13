from ..qt_wrapper import QtGui, Qt, QtWidgets
from .mouse_select_widget import MouseSelectableWidget
from ...data import LogRecord, TimeStamp


class LogRecordsWidget(MouseSelectableWidget):
    def __init__(self, zoom_agent):
        super().__init__(zoom_agent)
        self._logs = [
            LogRecord(TimeStamp(10), 1, "Event 1"),
            LogRecord(TimeStamp(70), 3, "Event 2"),
            LogRecord(TimeStamp(200), 1, "Event 3"),
            LogRecord(TimeStamp(204), 1, "Event 4"),
            LogRecord(TimeStamp(400), 1, "Event 5"),
            LogRecord(TimeStamp(600), 1, "FUU"),
        ]

        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        self.setSizePolicy(policy)
        self.setMinimumHeight(120)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), Qt.white)
        # Paint the several thingies:
        self.draw_grid(painter, event.rect())
        self.draw_logs(painter, event.rect())
        self.draw_cursor(painter, event.rect())

    def draw_grid(self, painter, rect):
        painter.setPen(Qt.black)
        ticks = self.calc_ticks()
        x0, y0 = rect.x(), rect.y()
        y2 = rect.y() + rect.height()
        x2 = rect.x() + rect.width()

        for tick in ticks:
            x = self.timestamp_to_pixel(tick)
            painter.drawLine(x, y0, x, y2)

    def draw_logs(self, painter, rect):
        """ Draw log records in w00t-style cool way. """
        num_lanes = 5  # Try to print non-overlapping log messages.
        font_metrics = painter.fontMetrics()
        for record in self._logs:
            x = self.timestamp_to_pixel(record.timestamp)

            painter.setPen(Qt.red)

            # Draw marker:
            radius = 5
            painter.drawEllipse(x - radius / 2, 10 - radius / 2, radius, radius)

            painter.setPen(Qt.green)
            painter.drawLine(x, 10, x + 5, 30)

            # TODO: properly draw balloons in lanes.
            # Draw text baloon:
            text_rect = font_metrics.boundingRect(record.message)
            text_rect.adjust(-4, -2, 4, 2)
            text_rect.translate(x + 5, 30)
            painter.drawRoundedRect(text_rect, 4, 4)
            painter.drawText(x + 5, 30, record.message)
