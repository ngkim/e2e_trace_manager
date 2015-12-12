from tornado.web import RequestHandler
import jsonpickle

from db.database import TraceDatabase
from db.trace import Trace
from db.step import StepSql, Step

class StepHandler(RequestHandler):
    
    def initialize(self, logger):        
        self.logger=logger
        
        traceDB = TraceDatabase()        
        self.dbengine = traceDB.get_engine()
    
    def print_result(self, records):
        for row in records:
            print "trace_seq= %s customer_seq= %s trace_title= %s create_dttm= %s\n" % (row['trace_seq'], row['customer_seq'], row['trace_title'], row['create_dttm'])
    
    def get(self, trace_seq):
        trace = Trace(1, 100, 'test', 'monitoring-manager', 'orchestrator-m')
        data_string= jsonpickle.encode(trace)
        self.write(data_string)
        
        traceSelectSql = "select * from tb_e2e_trace_list"        
        records = self.dbengine.execute(traceSelectSql)
        self.print_result(records)
                
    def post(self, trace_seq):
        stepReq = jsonpickle.decode(self.request.body)
        
        stepSql = StepSql()
        sql=stepSql.get_max_seq(trace_seq)
        records = self.dbengine.execute(sql)
        
        result="0"
        for row in records:
            result=row['seq']
        
        if((result == None) or (result == "")):
            seq = 0
        else:
            seq = int(result)
        stepseq=seq+1        
        self.logger.info("stepseq= %d" % stepseq)        
        
        title=stepReq['title']
        mainclass=stepReq['mainclass']
        subclass=stepReq['subclass']        
        
        step = Step(stepseq, trace_seq, title, mainclass, subclass, "", "")
        addStepSql = stepSql.add(step)
        self.logger.info("addStepSql= %s" % addStepSql)
        
        self.dbengine.execute(addStepSql)
        
        
        
        