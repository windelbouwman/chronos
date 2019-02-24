class TimeSpan:
    def __init__(self, begin, end):
        if begin > end:
            raise ValueError("Timespan begin must be before end.")
        self.begin = begin
        self.end = end

    def __str__(self):
        return f"Timespan from {self.begin}-{self.end}"

    def duration(self):
        """ Get the duration of this timespan. """
        return self.end - self.begin
