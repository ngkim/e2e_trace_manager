#-*- coding: utf-8 -*-

import Queue
import psycopg2

from util import logm


class Singleton(object):
    _instance = {}
    _inst_key = None
    
#     def __new__(self, *args, **kwargs):
#         if not isinstance( self._instance, self ) :
#             print "---------------------db----------------------------------------------------"
#             print args[1]
#             self._instance = object.__new__(self, *args, **kwargs)
#         return self._instance

    def __new__(self, *args, **kwargs):
        if not self._instance.has_key(args[0]):
            print "---------------------db----------------------------------"
            self._instance[args[0]] = object.__new__(self, *args, **kwargs)
            self._inst_key = args[0]
        return self._instance[args[0]]
    
    def __del__(self):
        try:
            self._instance.pop(self._inst_key)
        except :
            None
        


class dbManager(Singleton):
    
    def __init__(self, name, dbName, dbUser, dbPass, dbAddr, dbPort, 
                 connCnt=1, autocommit=True, qTimeout=5, _logger=None):
        self.dbName = dbName
        self.dbUser = dbUser
        self.dbPass = dbPass
        self.dbAddr = dbAddr
        self.dbPort = dbPort
        self.connCnt = connCnt
        self.dbPool = Queue.Queue(connCnt)
        self.autocommit = autocommit
        self.qTimeout = qTimeout
        self.logger = _logger
        self.create()
        
    def create(self):
        try:
            for i in range(0, self.connCnt):
                dbConn = psycopg2.connect( database=self.dbName, user=self.dbUser, password=self.dbPass,
                                     host=self.dbAddr, port=int(self.dbPort) )
                dbConn.autocommit = self.autocommit
                self.dbPool.put_nowait( dbConn )
                
            return True
        
        # Queue.Empty, Queue.Full
        except Exception, e:
            logm.exc(e, 'DBManager[%s]'%self._inst_key)
            self.exception(e)
            return False
    
    def _execute(self, sql, column=None, isSelect=True):
        dbConn = None
        cur = None
        dic = None
        try:
            dbConn = self.dbPool.get( True, self.qTimeout )
            cur = dbConn.cursor()
            cur.execute( sql )
            
            if isSelect:
                dic = []
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                for row in rows:
                    d = dict(zip(columns, row))
                    if column != None and column != "" :
                        dic.append( d[column] )
                    else:
                        dic.append(d)
            else:
                dic = int(cur.rowcount)
            
        except Exception, e:
            logm.exc(e, 'DBManager[%s]'%self._inst_key)
            self.exception(e)
        
        if cur != None:
            cur.close()
        
        try:
            if dbConn != None:
                logm.debug('DBConn[%s] Closed=%s'%(self._inst_key, str(dbConn.closed)))
                self.dbPool.put( dbConn, True, self.qTimeout )
        except Exception, e:
            logm.exc(e, 'DBManager[%s]'%self._inst_key)
            self.exception(e)
        
        if dic != None:
            return dic
        else:
            if isSelect:
                return None
            else:
                return 0
    
    def select(self, sql, column=None):
        return self._execute(sql, column, True)
    
    def execute(self, sql):
        return self._execute(sql, None, False)
    
    
    def getTotalSize(self):
        return self.dbPool.maxsize
    
    def getCurrSize(self):
        return self.dbPool.qsize()
    
    def debug(self, msg):
        if self.logger != None: self.logger.debug(msg)
        else:   print 'DEBUG:'+str(msg)
        
    def info(self, msg):
        if self.logger != None: self.logger.info(msg)
        else:   print 'INFO:'+str(msg)
    
    def warning(self, msg):
        if self.logger != None: self.logger.warning(msg)
        else:   print 'WARNING:'+str(msg)

    def error(self, msg):
        if self.logger != None: self.logger.error(msg)
        else:   print 'ERROR:'+str(msg)

    def exception(self, msg):
        if self.logger != None: self.logger.exception(msg)
        else:   print 'EXCEPTION:'+str(msg)


    def __del__(self):
        Singleton.__del__(self)
        try:
            while not self.dbPool.empty():
                dbConn = self.dbPool.get_nowait()
                if dbConn != None :
                    dbConn.close()
        except Exception, e:
            logm.exc(e, 'DBManager')
            self.exception(e)
    

if __name__ == '__main__':
    dbm = dbManager('test', 'orch_v1', 'nfv', 'ohhberry3333', '211.224.204.203', '5432')
    dbm.select("select * from tb_curalarm")





