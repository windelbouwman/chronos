from .duration import Duration


class TimeStamp:
    def __init__(self, stamp):
        self.stamp = stamp  # attos since epoch?
    
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

class TimeSpan:
    def __init__(self, begin, end):
        if begin > end:
            raise ValueError('Timespan begin must be before end.')
        self.begin = begin
        self.end = end
    
    def __str__(self):
        return f'Timespan from {self.begin}-{self.end}'
    
    def duration(self):
        """ Get the duration of this timespan. """
        return self.end - self.begin
