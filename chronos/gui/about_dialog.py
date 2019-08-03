from PyQt5 import uic
from .qt_wrapper import QtWidgets, Qt, QtCore
import logging


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("src/gui/about_dialog.ui", self)
