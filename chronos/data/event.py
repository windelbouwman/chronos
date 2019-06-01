

class Event:
    """ Simple event type which supports multiple handlers. """
    def __init__(self):
        self._subscribers = []
    
    def __call__(self):
        for s in self._subscribers:
            s()
    
    def subscribe(self, handler):
        self._subscribers.append(handler)
    
    def unsubscribe(self, handler):
        self._subscribers.remove(handler)