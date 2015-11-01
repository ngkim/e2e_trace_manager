from sqlalchemy import create_engine


class TraceDatabase:

    user="onebox"
    password="onebox1234!"
    host="211.224.204.203"
    database="e2e_trace_manager"
    
    def __init__(self, db_host, db_name, db_user, db_pass):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        
        self.dbengine = create_engine(self.get_postgres_dsn(), pool_recycle=500, pool_size=5, max_overflow=20, echo=False, echo_pool=True)
        
    def get_postgres_dsn(self):
        return "postgresql://%s:%s@%s/%s" % (self.db_user, self.db_pass, self.db_host, self.db_name)
    
    def get_engine(self):        
        return self.dbengine

        