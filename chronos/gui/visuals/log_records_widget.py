from ..qt_wrapper import QtGui, Qt, QtWidgets
from .mouse_select_widget import MouseSelectableWidget
from ...data import LogRecord, TimeStamp


class LogRecordsWidget(MouseSelectableWidget):
    def __init__(self, zoom_agent):
        super().__init__(zoom_agent)
        self._traces = []

        policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding,
        )
        self.setSizePolicy(policy)
        self.setFixedHeight(120)

        self.setToolTip("Drag log traces onto me to show them!")

    def add_trace(self, trace):
        self._traces.append(trace)
        trace.data_changed.subscribe(self.on_data_changed)
        self.update()

    def on_data_changed(self):
        self.update()

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
        ticks = self.get_x_ticks()
        y0 = 0
        y2 = self.height()

        for x, _ in ticks:
            painter.drawLine(x, y0, x, y2)

    def draw_logs(self, painter, rect):
        """ Draw log records in w00t-style cool way. """
        _num_lanes = 5  # Try to print non-overlapping log messages.
        timespan = self._zoom_agent.get_current_timespan()
        for trace in self._traces:
            for record in trace.get_samples(timespan):
                self.draw_record(painter, record)

    def draw_record(self, painter, record):
        font_metrics = painter.fontMetrics()
        x = self.timestamp_to_pixel(record.timestamp)

        # Draw marker:
        radius = 5
        painter.setPen(Qt.red)
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
