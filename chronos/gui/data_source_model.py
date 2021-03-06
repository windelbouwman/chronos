""" This file defines a Qt datamodel for a signal set.

Hierarchy is as follows:
- root
  - data source
    - trace group
      - trace group
        - trace
      - trace
    - trace
  - data source
"""

from .qt_wrapper import QtCore, Qt, get_icon
import json
from ..data import TreeItem, Trace, TraceGroup, TraceDataSource
from ..data import LogTrace, SignalTrace


class DataSourceModel(QtCore.QAbstractItemModel):
    def __init__(self, database):
        super().__init__()
        self._headers = [
            "Signal",
            "Last value",
            "Samples",
            # "Type", --> obsolete, given by icon
            "First time",
            "Last time",
        ]

        self._database = database

    def columnCount(self, parent):
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self._headers[section]
        else:
            pass

    def rowCount(self, parent):
        if parent.isValid():
            tree = parent.internalPointer()
            assert isinstance(tree, TreeItem), str(type(tree))
            return len(tree.children)
        else:
            return len(self._database.sources)

    def index(self, row, column, parent):
        if parent.isValid():
            parent_tree = parent.internalPointer()
            assert isinstance(parent_tree, TreeItem)
            tree = parent_tree.children[row]
        else:
            tree = self._database.sources[row].data_source
        assert isinstance(tree, TreeItem)
        return self.createIndex(row, column, tree)

    def parent(self, index):
        if index.isValid():
            child_tree = index.internalPointer()
            parent_tree = child_tree.parent
            if parent_tree is None:
                return QtCore.QModelIndex()
            else:
                grandparent = parent_tree.parent
                if grandparent is None:
                    data_sources = [s.data_source for s in self._database.sources]
                    row = data_sources.index(parent_tree)
                    return self.createIndex(row, 0, parent_tree)
                else:
                    row = grandparent.children.index(parent_tree)
                    return self.createIndex(row, 0, parent_tree)
        else:
            return QtCore.QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return

        row = index.row()
        column = index.column()
        tree_item = index.internalPointer()
        if role == Qt.DisplayRole:
            if column == 0:
                value = tree_item.name
            elif column == 1:  # last value.
                if isinstance(tree_item, Trace) and tree_item.has_samples:
                    value = str(tree_item.samples.last_sample())
                else:
                    value = ""
            elif column == 2:  # num samples
                if isinstance(tree_item, Trace):
                    value = str(len(tree_item.samples))
                else:
                    value = ""
            # elif column == 3:  # type
            #    value = tree_item.type_name()
            elif column == 3:  # first time
                if isinstance(tree_item, Trace) and tree_item.has_samples:
                    value = str(tree_item.samples.first_sample().timestamp)
                else:
                    value = ""
            elif column == 4:  # end time
                if isinstance(tree_item, Trace) and tree_item.has_samples:
                    value = str(tree_item.samples.last_sample().timestamp)
                else:
                    value = ""
            else:
                raise NotImplementedError(str(column))
            return value
        elif role == Qt.DecorationRole:
            if column == 0:
                if isinstance(tree_item, TraceGroup):
                    return get_icon("folder")
                elif isinstance(tree_item, TraceDataSource):
                    return get_icon("database")
                elif isinstance(tree_item, SignalTrace):
                    return get_icon("graph")
                elif isinstance(tree_item, LogTrace):
                    return get_icon("event-log")

    def flags(self, index):
        flags = super().flags(index)
        if index.isValid():
            flags |= Qt.ItemIsDragEnabled
        return flags

    def mimeTypes(self):
        return ["application/x-fubar"]

    def mimeData(self, indexes):
        mimeData = QtCore.QMimeData()
        uris = []
        for index in indexes:
            if not index.isValid():
                continue

            if index.column() > 0:
                continue

            tree = index.internalPointer()
            # if isinstance(tree, TraceDataSource):
            # tree = tree.source
            uris.append(tree.get_uri())
        print(uris)
        json_data = json.dumps(uris)
        encodedData = json_data.encode("ascii")
        mimeData.setData("application/x-fubar", encodedData)
        return mimeData
