from PyQt5 import uic
from .qt_wrapper import QtWidgets, Qt

# from .graph_widget import GraphWidget
from .fubar import Fubar
from .timespan_widget import TimeSpanWidget
from .signal_widget import SignalSourceWidget
from .zoom_agent import ZoomAgent


class ChronosMainWindow(QtWidgets.QMainWindow):
    """ Main window which includes a lot of sub windows """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi("src/gui/mainwindow.ui", self)
        self._zoom_agent = ZoomAgent()
        self.bar_charts = Fubar(self._zoom_agent)
        self.setCentralWidget(self.bar_charts)
        self.timeSpanWidget = TimeSpanWidget(self._zoom_agent)
        self.timeSpanDockWidget.setWidget(self.timeSpanWidget)

        self.signalsDockWidget.setWindowTitle("Signals")
        self._signal_widget = SignalSourceWidget()
        self.signalsDockWidget.setWidget(self._signal_widget)

        self.menuView.addAction(self.timeSpanDockWidget.toggleViewAction())
        self.menuView.addAction(self.signalsDockWidget.toggleViewAction())

        self.actionZoomFit.triggered.connect(self._zoom_agent.zoom_fit)
        self.actionZoomOut.triggered.connect(self._zoom_agent.zoom_out)
        self.actionZoomIn.triggered.connect(self._zoom_agent.zoom_in)
        self.actionPanLeft.triggered.connect(self._zoom_agent.pan_left)
        self.actionPanRight.triggered.connect(self._zoom_agent.pan_right)

        self.actionSaveSession.triggered.connect(self._save_session)

    def _save_session(self):
        """ Save current datasources and views into a session.

        A session file is a xml file of settings for a recording.
        """
        pass
