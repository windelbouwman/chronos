"""
Run chronos with:

python -m chronos

"""

import sys
from PyQt5.QtWidgets import QApplication

from .gui.main_window import ChronosMainWindow
from .data.data import load_data


def main():
    app = QApplication(sys.argv)
    w = ChronosMainWindow()
    w.show()
    data = load_data('demos/noize.hdf5')
    w.load_data(data)
    app.exec()


main()
