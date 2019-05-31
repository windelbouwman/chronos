
""" Plugin which receives data send over REST api in json format.
"""

import threading
import logging

from ..data import SignalTrace, SignalRecord, LogTrace, LogRecord
from ..data import TraceDataSource, TraceGroup, TimeStamp


class WebReceiver:
    logger = logging.getLogger('web-receiver')

    def __init__(self):
        self.data_source = TraceDataSource('demo')

        group1 = TraceGroup('group1')
        self.data_source.add_item(group1)

        self._trace1 = SignalTrace('trace1')
        # points1 = [SignalRecord(TimeStamp(x), math.sin(x * 0.03) * 80 + 40) for x in xs]
        # self._trace1.add(points1)
        group1.add_item(self._trace1)

        self._running = False
        self.start()
    
    def start(self):
        self.logger.info('Starting web receiver!')
        self._running = True
        self._thread = threading.Thread(target=run_web_app, args=(self,))
        self._thread.start()

    def stop(self):
        self.logger.info('Stopping web receiver!')
        self._running = False
        # TODO: find out a way to kill the event loop in another thread!
        # self._thread.join()
        self.logger.info('Web receiver halted.')


def run_web_app(web_receiver):
    # Try to open a tornado app now:
    import tornado.ioloop
    import tornado.web

    # Create an event loop for this thread:
    event_loop = tornado.ioloop.IOLoop()
    event_loop.make_current()

    class LogHandler(tornado.web.RequestHandler):
        def post(self):
            value = float(self.get_body_argument('value2'))
            print('value', value)
            ts = TimeStamp.now()
            # value = 42
            print('data!', value)
            web_receiver._trace1.add(SignalRecord(ts, value))

    app = tornado.web.Application([
        ("/log", LogHandler)
    ])
    app.listen(8883)
    web_receiver.logger.info('Entering tornado io loop in thread..')

    event_loop.start()

