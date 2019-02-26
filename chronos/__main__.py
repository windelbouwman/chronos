"""
Run chronos with:

python -m chronos

"""

import sys
import time
import logging
from .gui.qt_wrapper import QtWidgets, QtGui, Qt

from .gui.main_window import ChronosMainWindow
from .data.data import load_data


def main():
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Start with epic splash screen!
    pixmap = QtGui.QPixmap('img/splash.png')
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()
    if False:
        splash.showMessage("Doing important stuff..", Qt.AlignHCenter, Qt.red);
        time.sleep(0.4)
        splash.showMessage("Loading cool things", Qt.AlignHCenter, Qt.red);
        time.sleep(0.4)
        splash.showMessage("Starting spiffy tools!", Qt.AlignHCenter, Qt.red);
        time.sleep(0.4)

    w = ChronosMainWindow()
    w.show()
    splash.finish(w)
    app.exec()


main()
