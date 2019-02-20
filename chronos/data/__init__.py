""" Data package.

Two types of data are considered:
- Measured quantities (time-stamped real-valued measurements)
- textual log messages (time-stamped logging)

"""

class TimeStamp:
    pass


class TimeSpan:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end


class DataStore:
    """ Some data backed thingy! """
    def __init__(self):
        pass
    
    def get_data(self):
        return []
    
    def add_data(self):
        pass
