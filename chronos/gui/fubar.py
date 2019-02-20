
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
    def __init__(self, zoom_agent):
        super().__init__()
        l = QtWidgets.QHBoxLayout()
        self._label = QtWidgets.QLabel()
        self._label.setText("FubarPlot12345")
        l.addWidget(self._label)
        print('woot')

        # Method 3:
        self._graph = GraphWidget(zoom_agent)
        l.addWidget(self._graph)
        self.setLayout(l)

    
    def method2(self):
        self._view = QtWidgets.QGraphicsView()
        l.addWidget(self._view)
        self.setLayout(l)
        self._scene = QtWidgets.QGraphicsScene()
        self._view.setScene(self._scene)
        lp = LinePiece()
        self._scene.addItem(lp)


class TimeScale:
    pass


class GraphWidget(QtWidgets.QWidget):
    """ Implements plotting of a signal by using paintEvent.
    """
    def __init__(self, zoom_agent):
        super().__init__()
        self._zoom_agent = zoom_agent
        self._zoom_agent.cursor_changed.connect(self.on_cursor_change)
        self._cursor_x = None
        self._cursor_x2 = None
        self.setMouseTracking(True)
    
    def mousePressEvent(self, event):
        print('Press!')
        self._cursor_x2 = event.x()
        self.update()
    
    def mouseReleaseEvent(self, event):
        print('Release!')
        self._cursor_x2 = None
        self.update()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        timestamp = self._zoom_agent.pixel_to_timestamp(event.x())
        self._zoom_agent.set_cursor(timestamp)

    def on_cursor_change(self, timestamp):
        """ Current location changed! """
        self._cursor_x = self._zoom_agent.timestamp_to_pixel(timestamp)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        # Paint the several thingies:
        self.draw_grid(painter, event.rect())
        self.draw_signals(painter, event.rect())
        self.draw_cursor(painter, event.rect())
    
    def draw_signals(self, painter, rect):
        pass

    def draw_cursor(self, painter, rect):
        # print('voodoo', rect)
        if self._cursor_x is not None:
            if self._cursor_x2 is not None:
                # We have a selection!
                painter.fillRect(self._cursor_x, rect.y(), self._cursor_x2, rect.y() + rect.height(), Qt.darkYellow)
            painter.setPen(Qt.blue)
            painter.drawLine(self._cursor_x, rect.y(), self._cursor_x, rect.height() + rect.y())
        
    
    def draw_grid(self, painter, rect):
        painter.setPen(Qt.black)

        # TODO: draw correct stuff
        for x in range(rect.x(), rect.x() + rect.width(), 35):
            painter.drawLine(x, rect.y(), x, rect.y() + rect.height())

        for y in range(rect.y(), rect.y() + rect.height(), 35):
            painter.drawLine(rect.x(), y, rect.x() + rect.width(), y)


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


class TimeAxisWidget(QtWidgets.QWidget):
    """ Top (or bottom) time axis from left to right.
    """
    def __init__(self, zoom_agent):
        super().__init__()
        self._zoom_agent = zoom_agent

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        print('voodoo')

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self)
        painter.setPen(Qt.blue)

        # TODO: draw correct stuff
        for tick in range(0, 600, 35):
            painter.drawLine(tick, 0, tick, 20)
            painter.drawText(tick, 30, str(tick))

        # print('fubar')


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
    def __init__(self, zoom_agent):
        super().__init__()
        self._zoom_agent = zoom_agent
        self._traces = []
        self.method3()
        # self.method1()
        # self.method2()
    
    def method3(self):
        # TODO: scroll area with vbox layout for vertical scroll.
        l = QtWidgets.QVBoxLayout()
        self._axis_top = TimeAxisWidget(self._zoom_agent)
        l.addWidget(self._axis_top)
        self.setLayout(l)

        trace1 = SignalTrace(self._zoom_agent)
        l.addWidget(trace1)
        self._traces.append(trace1)


    def method2(self):
        # Make 1 view on a scene. All items in scene!
        l = QtWidgets.QVBoxLayout()
        self._view = QtWidgets.QGraphicsView()
        l.addWidget(self._view)
        self.setLayout(l)

        self._scene = QtWidgets.QGraphicsScene()
        self._view.setScene(self._scene)

        # Create some clever anchor:
        container_widget = QtWidgets.QGraphicsWidget()
        l2 = QtWidgets.QGraphicsAnchorLayout()
        container_widget.setLayout(l2)
        self._scene.addItem(container_widget)


    def method1(self):
        # Make traces as widgets, but signals as graphics scene.
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

        # self._scene.

        # 3rd trace:
        # trace3 = SignalTrace()
        # self.traces.append(trace3)
        # l.addWidget(trace3)

        # self._selection_overlay = TimeSelectorWidget(parent=self)


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

