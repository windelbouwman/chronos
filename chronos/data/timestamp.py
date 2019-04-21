import time
from .duration import Duration


class TimeStamp:
    def __init__(self, stamp):
        self.stamp = stamp  # attos since epoch?

    @classmethod
    def now(cls):
        stamp = time.time()
        return cls(stamp)

    def __int__(self):
        return int(self.stamp)

    def copy(self):
        return TimeStamp(self.stamp)

    def __str__(self):
        return f"t={time.ctime(self.stamp)}"

    def __gt__(self, other):
        if isinstance(other, TimeStamp):
            return self.stamp > other.stamp
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, TimeStamp):
            return Duration(self.stamp - other.stamp)
        elif isinstance(other, Duration):
            return TimeStamp(self.stamp - other.attos)
        else:
            return NotImplemented

    def __isub__(self, other):
        assert isinstance(other, Duration)
        self.stamp -= other.attos
        return self

    def __add__(self, other):
        if isinstance(other, Duration):
            return TimeStamp(self.stamp + other.attos)
        else:
            return NotImplemented

    def __iadd__(self, other):
        assert isinstance(other, Duration)
        self.stamp += other.attos
        return self

    def round_down(self, duration):
        """ Round this timestamp to multiples of duration. """
        self.stamp -= self.stamp % duration.attos
