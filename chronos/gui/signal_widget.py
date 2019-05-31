from .qt_wrapper import QtWidgets, Qt
from .data_source_model import DataSourceModel
from ..data import Trace
from ..data_plugins import DemoDataSource
from ..data_plugins import LinuxDataSource
from ..data_plugins import PyLoggerSource
from ..data_plugins import WebReceiver


class SignalSourceWidget(QtWidgets.QWidget):
    """ A widget with data sources. """
    def __init__(self, database):
        super().__init__()
        self._database = database
        l = QtWidgets.QVBoxLayout()
        self.setLayout(l)

        add_data_source = QtWidgets.QToolButton()
        add_data_source.setText('Add data source...')
        add_data_source.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        l.addWidget(add_data_source)
        
        expand_all_button = QtWidgets.QPushButton('Expand all')
        l.addWidget(expand_all_button)

        self.signalsTreeView = QtWidgets.QTreeView()
        l.addWidget(self.signalsTreeView)

        self.signal_model = DataSourceModel(database)
        self.signalsTreeView.setModel(self.signal_model)

        self.signalsTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.signalsTreeView.customContextMenuRequested.connect(self._on_context_menu)
        self.signalsTreeView.setDragEnabled(True)

        expand_all_button.clicked.connect(self.signalsTreeView.expandAll)
        # What must happen when data source is added:
        # add_data_source.clicked.connect(self._add_data_source)

        menu = QtWidgets.QMenu()
        source_types = [
            ("Demo", DemoDataSource),
            ("Linux", LinuxDataSource),
            ("Python logger", PyLoggerSource),
            ("Web receiver", WebReceiver),
        ]
        for name, cls in source_types:
            self.create_add_source_menu(menu, name, cls)
        add_data_source.setMenu(menu)

    def create_add_source_menu(self, menu, name, cls):
        def handle():
            self.signal_model._database.sources.append(cls())
            self.signal_model.modelReset.emit()
        action = menu.addAction(name)
        action.triggered.connect(handle)

    def _on_context_menu(self, pos):
        # print(pos)
        index = self.signalsTreeView.indexAt(pos)
        if index.isValid():
            # print(index)
            tree = index.internalPointer()
            if isinstance(tree, Trace):
                menu = QtWidgets.QMenu()
                def do_plot():
                    print('Plot!')
                    self.bar_charts.add_trace(tree)

                plotAction = QtWidgets.QAction('Plot!')
                plotAction.triggered.connect(do_plot)
                menu.addAction(plotAction)
                propertiesAction = QtWidgets.QAction('Properties')
                menu.addAction(propertiesAction)
                pos2 = self.signalsTreeView.viewport().mapToGlobal(pos)
                menu.exec(pos2)
            else:
                print(tree)
