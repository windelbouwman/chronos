""" Timespan selector widget.

Implement a convenient time period selection box.
"""

import math
import logging
from .qt_wrapper import QtWidgets, QtCore

from ..data import TimeSpan, TimeStamp, Duration

logger = logging.getLogger("timespan_selection")


RANGES = [
    # TODO: use trigger for this: last 30 nanoseconds
    ("last 5 seconds", Duration.from_seconds(5)),
    ("last 10 seconds", Duration.from_seconds(10)),
    ("last 15 seconds", Duration.from_seconds(15)),
    ("last 30 seconds", Duration.from_seconds(30)),
    ("last minute", Duration.from_minutes(1)),
    ("last 5 minutes", Duration.from_minutes(5)),
    ("last 10 minutes", Duration.from_minutes(10)),
    ("last 15 minutes", Duration.from_minutes(15)),
    ("last 30 minutes", Duration.from_minutes(30)),
    ("last hour", Duration.from_minutes(60)),
    ("last day", Duration.from_days(1)),
    ("last week", Duration.from_days(7)),
    ("last month", Duration.from_days(30)),
    ("last year", Duration.from_days(365)),
]


class TimeSpanToolButton(QtWidgets.QToolButton):
    def __init__(self, zoom_agent):
        super().__init__()
        self._zoom_agent = zoom_agent
        dialog = False
        if dialog:
            self.zoomToAction = QtWidgets.QAction("Zoom to ...")
            self.setDefaultAction(self.zoomToAction)
            self.zoomToAction.triggered.connect(self._show_zoom_to_dialog)
        else:
            # Menu
            self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
            self.setText("Zoom to..")
            range_menu = QtWidgets.QMenu()
            for name, duration in RANGES:
                self._make_range_handler(range_menu, name, duration)
            self.setMenu(range_menu)

    def _show_zoom_to_dialog(self):
        dialog = TimeSpanDialog(self)
        dialog.exec()

    def _make_range_handler(self, menu, name, duration):
        def handler():
            self.update_function(name, duration)

        zoom_action = menu.addAction(name)
        zoom_action.triggered.connect(handler)

    def update_function(self, name, duration):
        logger.debug("Zooming to %s", name)
        self._zoom_agent.start_to_follow(duration)


class TimeSpanQuick(QtWidgets.QWidget):
    """ Quick tab for often used time spans """

    def __init__(self, update_function):
        super().__init__()
        self._update_function = update_function
        l = QtWidgets.QGridLayout(self)
        n_cols = max(1, int(math.sqrt(len(RANGES))))
        for i, name in enumerate(RANGES):
            row, col = i // n_cols, i % n_cols
            button = self.add_button(name)
            l.addWidget(button, row, col)

    def add_button(self, name):
        button = QtWidgets.QPushButton()
        button.setText(name)
        button.clicked.connect(lambda: self._update_function(name))
        return button


class TimeSpanDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        l = QtWidgets.QVBoxLayout()
        self.quick = TimeSpanQuick(self.update_function)
        l.addWidget(self.quick)
        self.setLayout(l)

    def update_function(self, name):
        print(name)
        # self.range_button.setChecked(False)
        timespan = 1  # TODO!
        # self._zoom_agent.zoom_to(timespan)
        self.close()
