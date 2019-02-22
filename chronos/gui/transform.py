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
    def __init__(self):
        self._a = 1
        self._b = 0
    
    def forward(self, value):
        return value.stamp * self._a + self._b
    
    def backward(self, value):
        return TimeStamp((value - self._b) / self._a)

    def __mul__(self, other):
        """ Chain two transforms. """
        raise NotImplementedError()

