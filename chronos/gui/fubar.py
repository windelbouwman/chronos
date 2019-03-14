from .qt_wrapper import QtWidgets, QtGui, QtCore, Qt
from .visuals import TimeAxisWidget, SignalTraceVisualizer, LogTraceVisualizer


class Fubar(QtWidgets.QWidget):
    """ Overview widget with coupled time axis.
    """
    def __init__(self, zoom_agent, database):
        super().__init__()
        self._zoom_agent = zoom_agent
        self._database = database
        self._traces = []

        l = QtWidgets.QVBoxLayout()
        self.setLayout(l)

        l2 = QtWidgets.QHBoxLayout()
        l.addLayout(l2)
        l2.addSpacing(100)
        self._axis_top = TimeAxisWidget(self._zoom_agent)
        l2.addWidget(self._axis_top)
        l2.addSpacing(40)

        # Scroll area:
        self._scroll = QtWidgets.QScrollArea()
        self._scroll.setBackgroundRole(QtGui.QPalette.Dark)
        self._scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        l.addWidget(self._scroll)

        # Inner widget:
        self._inner = QtWidgets.QWidget()
        
        l3 = QtWidgets.QVBoxLayout()
        self._trace_layout = QtWidgets.QVBoxLayout()
        l3.addLayout(self._trace_layout)

        # Add visual option:
        add_visual_button = QtWidgets.QToolButton()
        add_visual_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        add_visual_button.setText("Add visual..")
        add_visual_menu = QtWidgets.QMenu()
        # TODO: where to retrieve this list from?
        visualizer_types = [
            ("Add trace visualizer", SignalTraceVisualizer),
            ("Add log visualizer", LogTraceVisualizer)
        ]
        for name, typ in visualizer_types:
            self.make_add_visualizer_handler(add_visual_menu, name, typ)
        add_visual_button.setMenu(add_visual_menu)

        l3.addWidget(add_visual_button)
        l3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self._inner.setLayout(l3)

        # Important: must be after setting layout on inner:
        self._scroll.setWidget(self._inner)

        self.fill_demo_data()

        self.setToolTip("Add visualizers first, then drag in signals into the plots from the left.")

    def add_trace(self, trace):
        self._trace_layout.addWidget(trace)
        self._traces.append(trace)

    def make_add_visualizer_handler(self, menu, name, visual_cls):
        def handler():
            trace1 = visual_cls(self._zoom_agent, self._database)
            self.add_trace(trace1)
        add_trace_action = menu.addAction(name)
        add_trace_action.triggered.connect(handler)
        
    def fill_demo_data(self):
        # Fill demo data:
        trace1 = SignalTraceVisualizer(self._zoom_agent, self._database)
        self.add_trace(trace1)

        log1 = LogTraceVisualizer(self._zoom_agent, self._database)
        self.add_trace(log1)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # When resizing, ensure proper width of content view.
        width = self._scroll.width() - 22
        self._inner.setFixedWidth(width)
