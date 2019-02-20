""" This file defines a Qt datamodel for a signal set.
"""

from PyQt5.QtCore import QAbstractItemModel, Qt
from PyQt5 import QtCore


class TreeItem:
    pass


class TraceGroup(TreeItem):
    def __init__(self, name):
        self.name = name
        self.items = []

    @property
    def children(self):
        return self.items

class Trace(TreeItem):
    def __init__(self, name):
        pass
    
    @property
    def children(self):
        return []


class DataSourceModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self.sources = ['a', 'b', 'c']

    def columnCount(self, parent):
        return 1

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.sources)
    
    def index(self, row, column, parent):
        return self.createIndex(row, column)
    
    def parent(self, index):
        return QtCore.QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return
    
        row = index.row()
        if role == Qt.DisplayRole:
            return self.sources[row]
