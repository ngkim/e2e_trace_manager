'''
data = { 
          'traceseq':1, 
          'title':'test', 
          'mainclass':'monitoring-manager',
          'subclass':'orchestrator-m'
          }
'''

class Trace(object):
       
    def __init__(self, traceseq, customerseq, title, mainclass, subclass):
        self.traceseq = traceseq
        self.customerseq = customerseq
        self.title = title
        self.mainclass = mainclass
        self.subclass = subclass
            
    def __str__(self, *args, **kwargs):
        return "traceseq = %d customerseq= %d title= %s mainclass= %s subclass= %s" % ( self.traceseq,
                                                                                        self.customerseq,
                                                                                        self.title,
                                                                                        self.mainclass, 
                                                                                        self.subclass)  


