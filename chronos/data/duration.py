class Duration:
    """ Relative duration of time.
    """

    def __init__(self, attos):
        self.attos = attos

    def __repr__(self):
        return f"Duration[{self.attos}]"

    @classmethod
    def from_days(cls, days):
        return cls.from_hours(days * 24)

    @classmethod
    def from_hours(cls, hours):
        return cls.from_minutes(hours * 60)

    @classmethod
    def from_minutes(cls, minutes):
        return cls.from_seconds(minutes * 60)

    @classmethod
    def from_seconds(cls, seconds):
        return cls(seconds)

    def to_seconds(self):
        return self.attos

    def __add__(self, other):
        assert isinstance(other, Duration)
        return Duration(self.attos + other.attos)
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Duration(self.attos * other)
        else:
            return NotImplemented

    def __truediv__(self, other):
        assert isinstance(other, (int, float))
        return Duration(self.attos / other)

    def __lt__(self, other):
        assert isinstance(other, Duration)
        return self.attos < other.attos
