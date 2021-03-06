import abc
import math

from ..data import TimeStamp


class Transform(metaclass=abc.ABCMeta):
    def forward(self, value):
        pass

    @abc.abstractmethod
    def backward(self, value):
        pass

    def inverse(self, value):
        return self.backward(value)


class TimeTransform(Transform):
    """ Transform timestamps into pixels.
    """

    def __init__(self, a=1, b=0):
        self._a = a
        self._b = b

    @classmethod
    def from_points(cls, pixels, timespan):
        # First, determine a:
        # Solve line from two points
        # y = a*x + b
        dy = pixels[1] - pixels[0]
        dx = timespan.end.stamp - timespan.begin.stamp
        a = dy / dx
        # b = y - a*x
        b = pixels[0] - a * timespan.begin.stamp
        # b2 = pixels[1] - a*timespan.end.stamp
        # print('b=', b, b2)
        return cls(a=a, b=b)

    def forward(self, value: TimeStamp):
        """ Take timestamp into pixel. """
        return value.stamp * self._a + self._b

    def backward(self, value) -> TimeStamp:
        return TimeStamp((value - self._b) / self._a)

    def __mul__(self, other):
        """ Chain two transforms. """
        raise NotImplementedError()


class ValueTransform(Transform):
    def __init__(self, a=1, b=0):
        self._a = a  # pixels per unit
        self._b = b

    def zoom_to(self, y_min, y_max):
        pass

    @classmethod
    def from_points(cls, pixels, values):
        # First, determine a:
        # Solve line from two points
        # y = a*x + b
        dy = pixels[1] - pixels[0]
        dx = values[1] - values[0]
        a = dy / dx
        # b = y - a*x
        b = pixels[0] - a * values[0]
        # b2 = pixels[1] - a*timespan.end.stamp
        # print('b=', b, b2)
        return cls(a=a, b=b)

    def forward(self, value: float):
        """ Take value into pixel. """
        return value * self._a + self._b

    def backward(self, value) -> float:
        return (value - self._b) / self._a
