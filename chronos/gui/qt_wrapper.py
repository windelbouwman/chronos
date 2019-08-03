from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

import os
import functools


@functools.lru_cache(maxsize=None)
def get_icon(filename):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    fullpath = os.path.join(this_dir, "..", "..", "icons", f"icons8-{filename}-48.png")
    return QtGui.QIcon(fullpath)
