import math
from ..data import TimeStamp
from .transform import TimeTransform


def test_transform():
    stamp = TimeStamp(22)
    transform = TimeTransform()
    value = transform.forward(stamp)
    stamp2 = transform.inverse(value)
    math.isclose(stamp.stamp, stamp2.stamp)
