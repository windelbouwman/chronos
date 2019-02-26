from .qt_wrapper import QtWidgets, Qt
from .data_source_model import DataSourceModel
from ..data import Trace
from ..data_plugins.demo import DemoDataSource


class SignalSourceWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        l = QtWidgets.QVBoxLayout()
        self.setLayout(l)

        add_data_source = QtWidgets.QPushButton('Add data source')
        l.addWidget(add_data_source)
        
        expand_all_button = QtWidgets.QPushButton('Expand all')
        l.addWidget(expand_all_button)

        self.signalsTreeView = QtWidgets.QTreeView()
        l.addWidget(self.signalsTreeView)

        self.signal_model = DataSourceModel()
        self.signalsTreeView.setModel(self.signal_model)

        self.signalsTreeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.signalsTreeView.customContextMenuRequested.connect(self._on_context_menu)
        self.signalsTreeView.setDragEnabled(True)

        expand_all_button.clicked.connect(self.signalsTreeView.expandAll)
        # What must happen when data source is added:
        add_data_source.clicked.connect(self._add_data_source)

    def _add_data_source(self):
        print("add data")
        # TODO: show wizard to select proper plugin.
        self.signal_model.sources.append(DemoDataSource())
        self.signal_model.modelReset.emit()

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
