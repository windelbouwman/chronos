""" Timespan selector widget.

Implement a convenient time period selection box.
"""

import math
from PyQt5 import QtWidgets, QtCore


RANGES = [
    'last 30 minutes',
    'last 15 minutes',
    'past hour',
    'last 30 nanoseconds',
    'last week',
    'last month',
    'last year',
]


class TimeSpanQuick(QtWidgets.QWidget):
    """ Quick tab for often used time spans """
    def __init__(self, update_function):
        super().__init__()
        l = QtWidgets.QGridLayout(self)
        n_cols = max(1, int(math.sqrt(len(RANGES))))
        for i, name in enumerate(RANGES):
            btn = QtWidgets.QPushButton()
            row, col = i // n_cols, i % n_cols
            l.addWidget(btn, row, col)
            btn.setText(name)
            btn.clicked.connect(lambda: update_function(name))


class TimeSpanWidget(QtWidgets.QWidget):
    """ Show the current timespan and provide options to modify it. """
    def __init__(self):
        super().__init__()
        vbox = QtWidgets.QVBoxLayout(self)
        self.range_button = QtWidgets.QPushButton()
        self.range_button.setCheckable(True)
        self.range_button.setText('Last week')
        vbox.addWidget(self.range_button)
        self.quick = TimeSpanQuick(self.updateTimespan)
        self.quick.setVisible(False)
        vbox.addWidget(self.quick)

        # Connect events:
        self.range_button.toggled.connect(self.quick.setVisible)

    def updateTimespan(self, name):
        self.range_button.setChecked(False)
        print(name)
