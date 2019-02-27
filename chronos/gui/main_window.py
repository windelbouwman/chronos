from PyQt5 import uic
from .qt_wrapper import QtWidgets, Qt

# from .graph_widget import GraphWidget
from .fubar import Fubar
from .timespan_widget import TimeSpanWidget
from .signal_widget import SignalSourceWidget
from .zoom_agent import ZoomAgent
from ..data import DataStore
from ..data_plugins.demo import DemoDataSource

class Context:
    """ Sort of global state container.

    Contains:
    - zoom agent: for shared zooming.
    - database: all data goes in and out here.
    """
    def __init__(self):
        self.zoom_agent = ZoomAgent()
        self.database = DataStore()


class ChronosMainWindow(QtWidgets.QMainWindow):
    """ Main window which includes a lot of sub windows """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        uic.loadUi("src/gui/mainwindow.ui", self)
        self._context = Context()
        # Add some demo data sources:
        self._context.database.sources.extend([DemoDataSource(), DemoDataSource()])

        # self._zoom_agent = ZoomAgent()
        self.bar_charts = Fubar(self._context.zoom_agent, self._context.database)
        self.setCentralWidget(self.bar_charts)
        self.timeSpanWidget = TimeSpanWidget(self._context.zoom_agent)
        self.timeSpanDockWidget.setWidget(self.timeSpanWidget)

        self.signalsDockWidget.setWindowTitle("Signals")
        self._signal_widget = SignalSourceWidget(self._context.database)
        self.signalsDockWidget.setWidget(self._signal_widget)

        self.menuView.addAction(self.timeSpanDockWidget.toggleViewAction())
        self.menuView.addAction(self.signalsDockWidget.toggleViewAction())

        self.actionZoomFit.triggered.connect(self._context.zoom_agent.zoom_fit)
        self.actionZoomOut.triggered.connect(self._context.zoom_agent.zoom_out)
        self.actionZoomIn.triggered.connect(self._context.zoom_agent.zoom_in)
        self.actionPanLeft.triggered.connect(self._context.zoom_agent.pan_left)
        self.actionPanRight.triggered.connect(self._context.zoom_agent.pan_right)

        self.actionSaveSession.triggered.connect(self._save_session)

    def _save_session(self):
        """ Save current datasources and views into a session.

        A session file is a xml file of settings for a recording.
        """
        pass
