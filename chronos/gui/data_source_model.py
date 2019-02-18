""" This file defines a Qt datamodel for a signal set.
"""

from PyQt5.QtCore import QAbstractItemModel


class DataSourceModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()

    def columnCount(self):
        return 1

    def rowCount(self):
        return 0
