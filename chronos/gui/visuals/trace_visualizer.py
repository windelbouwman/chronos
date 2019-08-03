import json
from urllib.parse import urlparse

from ..qt_wrapper import QtWidgets, QtGui, QtCore, Qt


class TraceVisualizer(QtWidgets.QFrame):
    """ Base visualizer.

    Supports dropping of traces.
    """

    def __init__(self, accepted_drop_scheme):
        super().__init__()
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setAutoFillBackground(True)
        self.setFrameStyle(QtWidgets.QFrame.Raised | QtWidgets.QFrame.Panel)
        self.setLineWidth(2)

        # Enable drop of traces:
        self.setAcceptDrops(True)
        self._accepted_drop_scheme = accepted_drop_scheme

    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasFormat("application/x-fubar"):
            data = mimeData.data("application/x-fubar").data()
            uris = json.loads(data.decode("ascii"))
            for uri in uris:
                o = urlparse(uri)
                if o.scheme == self._accepted_drop_scheme:
                    event.accept()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasFormat("application/x-fubar"):
            data = mimeData.data("application/x-fubar").data()
            uris = json.loads(data.decode("ascii"))
            for uri in uris:
                print("Dropping", uri)
                o = urlparse(uri)
                # print(o)
                if o.scheme == self._accepted_drop_scheme:
                    self.handle_drop(o)
                else:
                    print(f"Not supported scheme: {o.scheme}")

    def handle_drop(self, o):
        raise NotImplementedError()
