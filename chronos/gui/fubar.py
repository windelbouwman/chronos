
import math
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt


class TraceVisualizer(QtWidgets.QWidget):
    """ Base visualizer.
    """
    pass


class LogTrace(TraceVisualizer):
    """ Visualizer for a series of log messages.
    """
    pass


class SignalTrace(TraceVisualizer):
    """ Visualizer for one or more signals.
    """
    def __init__(self):
        super().__init__()
        l = QtWidgets.QHBoxLayout()
        self._label = QtWidgets.QLabel()
        self._label.setText("FubarPlot12345")
        l.addWidget(self._label)
        self._view = QtWidgets.QGraphicsView()
        l.addWidget(self._view)
        self.setLayout(l)
        self._scene = QtWidgets.QGraphicsScene()
        self._view.setScene(self._scene)
        lp = LinePiece()
        self._scene.addItem(lp)


class TimeAxis(QtWidgets.QWidget):
    """ Top (or bottom) time axis from left to right.
    """
    def __init__(self):
        pass


class LinePiece(QtWidgets.QGraphicsItem):
    """ A piece of a signal trace.
    """
    def __init__(self):
        super().__init__()
        # Create random data:
        xs = range(100)
        self.points = [(x, math.sin(x * 0.2) * 80 + 40) for x in xs]

    def boundingRect(self):
        xmax = max(p[0] for p in self.points)
        xmin = min(p[0] for p in self.points)
        ymax = max(p[1] for p in self.points)
        ymin = min(p[1] for p in self.points)
        return QtCore.QRectF(xmin, ymin, xmax, ymax)

    def paint(self, painter, option, widget):
        painter.setPen(Qt.green)

        for p1, p2 in zip(self.points[:-1], self.points[1:]):
            painter.drawLine(p1[0], p1[1], p2[0], p2[1])


class TraceItem(QtWidgets.QGraphicsItemGroup):
    def boundingRect(self):
        pass
    
    def paint(self, painter, option, widget):
        pass


class TimeAxisItem(QtWidgets.QGraphicsItem):
    def boundingRect(self):
        return QtCore.QRectF(0, 0, 200, 30)
    
    def paint(self, painter, option, widget):
        # painter.fill
        painter.setPen(Qt.red)
        for tick in range(0, 600, 35):
            painter.drawLine(tick, 0, tick, 20)
            painter.drawText(tick, 30, str(tick))


class CursorItem(QtWidgets.QGraphicsItem):
    """ Draw current mouse cursor line.
    """
    def boundingRect(self):
        return QtCore.QRectF(0, 0, 200, 30)
    
    def paint(self, painter, option, widget):
        self._x = 20
        # painter.fill
        painter.setPen(Qt.black)
        painter.drawLine(self._x, 0, self._x, self.height())


class Fubar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.traces = []
        l = QtWidgets.QVBoxLayout()
        
        self.setLayout(l)

        self._view = QtWidgets.QGraphicsView()
        l.addWidget(self._view)

        self._scene = QtWidgets.QGraphicsScene()
        self._view.setScene(self._scene)
        self._axis_item = TimeAxisItem()
        self._scene.addItem(self._axis_item)
        lp = LinePiece()
        self._scene.addItem(lp)

        # 1st trace:
        trace1 = SignalTrace()
        l.addWidget(trace1)
        self.traces.append(trace1)

        # 2nd trace:
        trace2 = SignalTrace()
        self.traces.append(trace2)
        l.addWidget(trace2)

        # 3rd trace:
        trace3 = SignalTrace()
        self.traces.append(trace3)
        l.addWidget(trace3)

        self._selection_overlay = TimeSelectorWidget(parent=self)


class TimeSelectorWidget(QtWidgets.QWidget):
    """ Widget showing time selection cursors and a list of visualizers.

    This is an overlay kind of widget.

    See also: https://github.com/D3f0/pyqt4-widget-overlay/blob/master/overlay.py
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.crosshair = 0
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        # print(event)
        self.crosshair = event.x()
        self.update()
        # print(self.geometry())

    def updatePosition(self):
        parentRect = self.parent().rect()
        if not parentRect:
            return
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updatePosition()

    def showEvent(self, event):
        super().showEvent(event)
        self.updatePosition()

    def paintEvent(self, event):
        # print(event)
        painter = QtGui.QPainter(self)

        # Draw time scale (X-axis):

        # Draw selection block

        # Draw the current cursor:
        painter.setPen(Qt.blue)
        painter.drawLine(self.crosshair, 0, self.crosshair, 100)
        painter.end()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    f = Fubar()
    f.show()
    f.traces.append(SignalTrace())
    app.exec()

