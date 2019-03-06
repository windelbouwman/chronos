from .qt_wrapper import QtWidgets, QtGui, QtCore, Qt


class TraceVisualizer(QtWidgets.QFrame):
    """ Base visualizer.
    """

    def __init__(self):
        super().__init__()
        self.setBackgroundRole(QtGui.QPalette.Window)
        self.setAutoFillBackground(True)
        self.setFrameStyle(QtWidgets.QFrame.Raised | QtWidgets.QFrame.Panel)
        self.setLineWidth(2)
        
