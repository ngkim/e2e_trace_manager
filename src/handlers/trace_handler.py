from tornado.web import RequestHandler
import jsonpickle

'''
data = { 
          'traceseq':1, 
          'title':'test', 
          'mainclass':'monitoring-manager',
          'subclass':'orchestrator-m'
          }
'''
class Trace(object):
    
    def __init__(self, traceseq, title, mainclass, subclass):
        self.traceseq = traceseq
        self.title = title
        self.mainclass = mainclass
        self.subclass = subclass
            
    def __str__(self, *args, **kwargs):
        return "traceseq = %d title= %s mainclass= %s subclass= %s" % ( self.traceseq,
                                                                       self.title,
                                                                       self.mainclass, 
                                                                       self.subclass)  
        
class MainHandler(RequestHandler):
    def initialize(self, logger):        
        self.logger=logger
    
    def get(self):
        self.logger.info("Hello, world")
        trace = Trace(1, 'test', 'monitoring-manager', 'orchestrator-m')
        data_string= jsonpickle.encode(trace)
        self.write(data_string)
                
# USAGE:
# curl -v http://localhost:8888/ -X POST --data-binary '{"traceseq": 1, "title": "post-test", "mainclass":"monitoring-manager", "subclass":"orchestrator-m" }' -H "Content-type: application/json"

    def post(self):
        self.logger.info('POST= %s' % self.request.body)
        traceReq = jsonpickle.decode(self.request.body)
        trace = Trace(traceReq['traceseq'], traceReq['title'], traceReq['mainclass'], traceReq['subclass'])
        self.logger.info("Trace= %s" % trace)