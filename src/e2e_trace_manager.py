#-*- coding: utf-8 -*-
'''
Created on 2015. 11. 01.

@author: Namgon Kim (day10000@gmail.com)

'''

import os, sys, signal, yaml, json, psycopg2, threading

handler_path=[ "./handlers","./util"] 
for hpath in handler_path:
    if os.path.abspath(hpath) not in sys.path:
        sys.path.append(os.path.abspath(hpath))

print "sys.path= %s" % sys.path
    
import trace_handler
from time import sleep

from tornado.web import Application, RequestHandler
from http_serv import httpSvrThread
from gsf import VarShared
from ko_logger import ko_logger as mylogger

from tornado.ioloop import IOLoop

TITLE="E2E Trace Handler"
logger = mylogger(tag=TITLE, logdir="./log/", loglevel="debug", logConsole=False).get_instance()

# configuration
def loadConfig(cfgName):
    logger.info('load Config : fName=%s' % cfgName)
    with open(cfgName, "r") as f:
        cfgf = yaml.load(f)
    
    gVar = VarShared( cfgf['gVar'] )
    cfgf['gVar'] = gVar
    return cfgf

# Get info for operation
def getInitInfo(cfg):
    logger.info('get Init Info: %s'%cfg)

# Set up config and Reload components
def setup(info):
    logger.info('setup: %s'%info)

def startScheduler( cfg ):
    logger.info( 'start OrchM Scheduler' )

    
def startAPI(app, cfg):
    logger.info('start API : port=%s, procNum=%s, url=%s' % (cfg['port'], cfg['procNum'], app))

    def sig_handler(signum, frame):
        print "caught signal %s" % signum
        io_loop = IOLoop.instance()
        io_loop.add_callback(io_loop.stop)
        svr.stop()
    
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)  
    
    svr = httpSvrThread(app, cfg['port'], cfg['procNum'])
    svr.start()

def makeApp( _cfg ):    
    app = Application(trace_handler.url())
    
    return app

def main(cfgName):
    
    print "Main Start"
    logger.info("---------------Main Start---------")
    
    cfg = loadConfig(cfgName)
    
    app = makeApp( cfg )
    
    startScheduler( cfg )
    
    sleep(1)
    
    startAPI( app, cfg )    
    
    logger.info("---------------Main END---------")

if __name__ == '__main__':
    
    cfgName = './cfg/orchm.cfg'
    if len(sys.argv) >= 2:
        cfgName = sys.argv[1]
    
    main(cfgName)
