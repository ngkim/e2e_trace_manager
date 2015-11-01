
import signal, time, threading
from ko_logger import ko_logger as mylogger
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
import tornado.ioloop as ioloop

TITLE = 'HTTP_SERVER'
logging = mylogger(tag=TITLE, logdir="./log/", loglevel="debug", logConsole=False).get_instance()

MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3
        
class httpSvrThread(threading.Thread):

    def __init__(self, applictions, port, proc):
        threading.Thread.__init__(self)
        self.svr = HTTPServer(applictions)
        self.svr.bind(port)
        self.svr.start(proc)

    def run(self):
        logging.info('Run HTTP Server')
        
        IOLoop.current().start()