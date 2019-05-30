from PyQt5 import uic
from .qt_wrapper import QtWidgets, Qt, QtCore, get_icon
import logging
import os

# from .graph_widget import GraphWidget
from .fubar import Fubar
from .timespan_widget import TimeSpanToolButton
from .signal_widget import SignalSourceWidget
from .zoom_agent import ZoomAgent
from .about_dialog import AboutDialog
from ..data import DataStore, TimeSpan
from ..data_plugins.demo import DemoDataSource


class Context:
    """ Sort of global state container.

    Contains:
    - zoom agent: for shared zooming.
    - database: all data goes in and out here.
    """

    logger = logging.getLogger("Data-glu0r")

    def __init__(self):
        self.zoom_agent = ZoomAgent()
        self.database = DataStore()

    def zoom_fit(self):
        # Has to be done on context, must loop over all data, and determine date range!
        self.logger.info("Zoom fit!!")
        # TODO: This might fail when no data source is selected and there can be no min / max.
        timespan = self.database.get_timespan()
        self.zoom_agent.zoom_to(timespan)


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

        self.signalsDockWidget.setWindowTitle("Signals")
        self._signal_widget = SignalSourceWidget(self._context.database)
        self.signalsDockWidget.setWidget(self._signal_widget)

        # self.menuView.addAction(self.timeSpanDockWidget.toggleViewAction())
        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.menuView.addAction(self.signalsDockWidget.toggleViewAction())

        self.add_zoom_buttons()
        self.mainToolBar.addSeparator()
        self.make_mouse_mode_buttons()
        self.mainToolBar.addSeparator()

        self.actionSaveSession.triggered.connect(self._save_session)

        # Restore position:
        settings = QtCore.QSettings("lcfos", "chronos")
        settings.beginGroup("MainWindow")
        self.resize(settings.value("size", QtCore.QSize(400, 300)))
        self.move(settings.value("pos", QtCore.QPoint(50, 50)))
        settings.endGroup()

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()

    def add_zoom_buttons(self):
        self.actionZoomFit.setIcon(get_icon('zoom-to-extents'))
        self.actionZoomFit.triggered.connect(self._context.zoom_fit)
        self.actionZoomOut.setIcon(get_icon('zoom-out'))
        self.actionZoomOut.triggered.connect(self._context.zoom_agent.zoom_out)
        self.actionZoomIn.setIcon(get_icon('zoom-in'))
        self.actionZoomIn.triggered.connect(self._context.zoom_agent.zoom_in)
        self.actionPanLeft.setIcon(get_icon('back-arrow'))
        self.actionPanLeft.triggered.connect(self._context.zoom_agent.pan_left)
        self.actionPanRight.setIcon(get_icon('forward-button'))
        self.actionPanRight.triggered.connect(self._context.zoom_agent.pan_right)

        self.zoomToToolButton = TimeSpanToolButton(self._context.zoom_agent)
        self.mainToolBar.addWidget(self.zoomToToolButton)

    def make_mouse_mode_buttons(self):
        # Construct zoom mode buttons:
        self._zoom_mode_button_group = QtWidgets.QButtonGroup()

        zoom_horizontal = QtWidgets.QToolButton()
        zoom_horizontal.setCheckable(True)
        zoom_horizontal.setChecked(True)
        zoom_horizontal.setText("Zoom horizontal")
        zoom_horizontal.setIcon(get_icon('zoom'))
        self.mainToolBar.addWidget(zoom_horizontal)
        self._zoom_mode_button_group.addButton(zoom_horizontal, 1)

        # zoom = QtWidgets.QToolButton()
        # zoom.setCheckable(True)
        # zoom.setText("Zoom")
        # self.mainToolBar.addWidget(zoom)
        # self._zoom_mode_button_group.addButton(zoom, 2)

        pan_horizontal = QtWidgets.QToolButton()
        pan_horizontal.setCheckable(True)
        pan_horizontal.setText("Pan horizontal")
        pan_horizontal.setIcon(get_icon('move'))
        self.mainToolBar.addWidget(pan_horizontal)
        self._zoom_mode_button_group.addButton(pan_horizontal, 3)

    def _save_session(self):
        """ Save current datasources and views into a session.

        A session file is a xml file of settings for a recording.
        """
        pass

    def closeEvent(self, event):
        settings = QtCore.QSettings("lcfos", "chronos")
        settings.beginGroup("MainWindow")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.endGroup()

        nr = len(self._context.database.sources)
        progress = QtWidgets.QProgressDialog("Shutting down..", "Cancel", 0, nr, self)
        progress.show()
        self._context.database.shutdown()
        progress.setValue(1)
        super().closeEvent(event)