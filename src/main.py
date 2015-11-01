#-*- coding: utf-8 -*-
'''
Created on 2015. 11. 01.

@author: Namgon Kim (day10000@gmail.com)

'''

import signal
import tornado.ioloop
import tornado.web

from tornado.ioloop import IOLoop
from handlers.trace_handler import MainHandler
from util.ko_logger import ko_logger as logger

log = logger(tag="E2E Trace Manager", logdir="./log/", loglevel="debug", logConsole=False).get_instance()

application = tornado.web.Application([
    (r"/", MainHandler, dict(logger=log)),
])

def sig_handler(signum, frame):
    print "caught signal %s. Shutdown..." % signum
    io_loop = IOLoop.instance()
    io_loop.add_callback(io_loop.stop)    

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)  
    
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
