'''
Created on 2015. 9. 12.

@author: ohhara
'''

import os, fcntl
from time import sleep
import yaml
import logging

logger=logging.getLogger('oba')

class VarShared():
    
    def __init__(self, varName):
        self.varName = varName
    
    def locked_read(self):
        fd = os.open(self.varName, os.O_RDWR|os.O_CREAT)
        fcntl.flock(fd, fcntl.LOCK_EX)
        fileobj = os.fdopen(fd, 'r+b')
    
        logger.debug("lock file read")
        
        data = fileobj.read()
        xdata = yaml.safe_load(data)
        
        fileobj.flush()
        os.fdatasync(fd)
        fcntl.flock(fd, fcntl.LOCK_UN)
        logger.debug("unlock file read")
        fileobj.close()
        
        return xdata
    
    def locked_read_param(self, field):
        fd = os.open(self.varName, os.O_RDWR|os.O_CREAT)
        fcntl.flock(fd, fcntl.LOCK_EX)
        fileobj = os.fdopen(fd, 'r+b')
    
        logger.debug("lock file Parameter read")
        
        data = fileobj.read()
        xdata = yaml.safe_load(data)
        
        fileobj.flush()
        os.fdatasync(fd)
        fcntl.flock(fd, fcntl.LOCK_UN)
        logger.debug("unlock file read")
        fileobj.close()
        
        try:
            return xdata[field]
        except Exception, e:
            return None
    
    def locked_write(self, data):
        fd = os.open(self.varName, os.O_RDWR|os.O_CREAT)
        fcntl.flock(fd, fcntl.LOCK_EX)
        fileobj = os.fdopen(fd, 'w+b')
    
        logger.debug("lock file write")

        yaml.dump(data, fileobj)
    
        fileobj.flush()
        os.fdatasync(fd)
        fcntl.flock(fd, fcntl.LOCK_UN)
        logger.debug("unlock file write")
        fileobj.close()
        
        return data

    def locked_write_param(self, field, value):
        fd = os.open(self.varName, os.O_RDWR|os.O_CREAT)
        fcntl.flock(fd, fcntl.LOCK_EX)
        fileobj = os.fdopen(fd, 'w+b')
    
        logger.debug("lock file write")

        data = fileobj.read()
        xdata = yaml.safe_load(data)
        xdata[field] = value
        
        yaml.dump(xdata, fileobj)
    
        fileobj.flush()
        os.fdatasync(fd)
        fcntl.flock(fd, fcntl.LOCK_UN)
        logger.debug("unlock file write")
        fileobj.close()
        
        return xdata
