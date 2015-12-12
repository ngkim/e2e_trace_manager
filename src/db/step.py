
class StepSql:
    
    def add(self, step):
        query= "insert into tb_e2e_trace_steps \
                    (step_seq, trace_seq, step_title, mainclass, subclass, request_cmd, request_param, request_time) \
                    values (%d, %s, '%s', '%s', '%s', '%s',  '%s', now())" % (step.seq, step.traceseq, step.title, step.mainclass, step.subclass, step.requestcmd, step.requestparam)
        return query       
                    
    def get_max_seq(self, trace_seq):
        query= "select max(step_seq) as seq from tb_e2e_trace_steps \
                    where trace_seq = %s" % (trace_seq)
        return query
    
    def delete(self):
        query = "delete from tb_e2e_trace_steps \
        where step_seq = %d and trace_seq = %d" % (self.seq, self.traceseq)
        
        return query
        
    def update(self):
        query = "update tb_e2e_trace_list \
                            set response_status = %d, message_detail = '%s', response_time = now() \
                            where step_seq = %d and trace_seq = %d" % (self.responsestatus, self.responsemessage, self.seq, self.traceseq)       
            
        return query

class Step(object):
       
    def __init__(self, seq, traceseq, title, mainclass, subclass, requestcmd, requestparam):
        self.seq = seq
        self.traceseq = traceseq
        self.title = title
        self.mainclass = mainclass
        self.subclass = subclass
        self.requestcmd = requestcmd
        self.requestparam = requestparam
        
    def set_request(self, request_cmd, request_param):
        self.requestcmd = request_cmd
        self.requestparam = request_param
        
    def set_response(self, response_status, response_message):
        self.responsestatus = response_status
        self.responsemessage = response_message           
        