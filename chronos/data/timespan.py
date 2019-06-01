
from .timestamp import TimeStamp


class TimeSpan:
    """ A timespan is a period of time with fixed start and end dates. """
    def __init__(self, begin, end):
        if not isinstance(begin, TimeStamp):
            raise ValueError('begin must be TimeStamp')

        if not isinstance(end, TimeStamp):
            raise ValueError('end must be TimeStamp')

        if begin > end:
            raise ValueError("Timespan begin must be before end.")
        self.begin = begin
        self.end = end

    def __str__(self):
        return f"Timespan from {self.begin}-{self.end}"

    def duration(self):
        """ Get the duration of this timespan. """
        return self.end - self.begin
