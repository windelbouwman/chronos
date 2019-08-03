""" Plugin which receives data send over REST api in json format.
"""

import threading
import logging

from ..data import SignalTrace, SignalRecord, LogTrace, LogRecord
from ..data import TraceDataSource, TraceGroup, TimeStamp


class WebReceiver:
    logger = logging.getLogger("web-receiver")

    def __init__(self):
        self.data_source = TraceDataSource("web-receiver")
        self._group1 = TraceGroup("Signals")
        self.data_source.add_item(self._group1)
        self._trace_map = {}
        self._running = False
        self.start()

    def start(self):
        self.logger.info("Starting web receiver!")
        self._running = True
        import tornado.ioloop

        self.event_loop = tornado.ioloop.IOLoop()
        self._thread = threading.Thread(target=run_web_app, args=(self,))
        self._thread.start()

    def stop(self):
        self.logger.info("Stopping web receiver!")
        self._running = False

        # This is a tweak to stop the event loop in another thread:
        self.event_loop.add_callback(self.event_loop.stop)

        # Wait for the thread to finish off:
        self._thread.join()
        self.logger.info("Web receiver halted.")

    def add_sample(self, name, ts, value):
        if name in self._trace_map:
            trace = self._trace_map[name]
        else:
            trace = self._trace1 = SignalTrace(name)
            self._group1.add_item(self._trace1)
            self._trace_map[name] = trace
        trace.add(SignalRecord(ts, value))


def run_web_app(web_receiver):
    """ Run a tornado web application. """
    # Try to open a tornado app now:
    import tornado.web
    import tornado.escape

    event_loop = web_receiver.event_loop

    # Install the event loop on this thread:
    event_loop.make_current()

    class LogHandler(tornado.web.RequestHandler):
        def post(self):
            print("body:", self.request.body)
            data = tornado.escape.json_decode(self.request.body)
            samples = data["samples"]
            # self.
            ts = TimeStamp.now()
            print("data!", samples)
            for name, value in samples.items():
                print(name, value)
                value = float(value)
                web_receiver.add_sample(name, ts, value)

    app = tornado.web.Application([("/log", LogHandler)])
    app.listen(8883)
    web_receiver.logger.info("Entering tornado io loop in thread..")
    event_loop.start()
    web_receiver.logger.info("Tornado start function just returned! Quiting thread.")
