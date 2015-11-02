from tornado.web import RequestHandler
import jsonpickle

from util.database import TraceDatabase
from trace import Trace

class StepHandler(RequestHandler):
    
    def initialize(self, logger):        
        self.logger=logger
        
        traceDB = TraceDatabase()        
        self.dbengine = traceDB.get_engine()
    
    def print_result(self, records):
        for row in records:
            print "trace_seq= %s customer_seq= %s trace_title= %s create_dttm= %s\n" % (row['trace_seq'], row['customer_seq'], row['trace_title'], row['create_dttm'])
    
    def get(self):
        trace = Trace(1, 100, 'test', 'monitoring-manager', 'orchestrator-m')
        data_string= jsonpickle.encode(trace)
        self.write(data_string)
        
        traceSelectSql = "select * from tb_e2e_trace_list"        
        records = self.dbengine.execute(traceSelectSql)
        self.print_result(records)
                
    def post(self):
        self.logger.info('POST= %s' % self.request.body)
        
        traceReq = jsonpickle.decode(self.request.body)
        trace = Trace(traceReq['traceseq'], traceReq['customerseq'], traceReq['title'], traceReq['mainclass'], traceReq['subclass'])
        
        traceAddSql = "INSERT INTO tb_e2e_trace_list (trace_seq, customer_seq, trace_title, create_dttm) \
                        VALUES (       %d,           %d,    '%s',       now())" % (trace.traceseq, trace.customerseq, trace.title)
        self.logger.info("traceAddSql= %s" % traceAddSql)
        self.dbengine.execute(traceAddSql)