from .duration import Duration


class TimeStamp:
    def __init__(self, stamp):
        self.stamp = stamp  # attos since epoch?

    @classmethod
    def now(cls):
        stamp = 1
        return cls(stamp)

    def copy(self):
        return TimeStamp(self.stamp)

    def __str__(self):
        return f"t={self.stamp}"

    def __gt__(self, other):
        return self.stamp > other.stamp

    def __sub__(self, other):
        if isinstance(other, TimeStamp):
            return Duration(self.stamp - other.stamp)
        else:
            raise NotImplementedError()

    def __isub__(self, other):
        assert isinstance(other, Duration)
        self.stamp -= other.attos
        return self

    def __iadd__(self, other):
        assert isinstance(other, Duration)
        self.stamp += other.attos
        return self

    def round_down(self, duration):
        """ Round this timestamp to multiples of duration. """
        self.stamp -= self.stamp % duration.attos
