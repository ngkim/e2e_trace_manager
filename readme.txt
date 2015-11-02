
1. prerequisite
	>> pip install jsonpickle

2. TABLE: tb_e2e_trace_list
	>> sudo -u postgres psql -d e2e_trace_manager -c "select * from tb_e2e_trace_list"

3. dbManager 
	>> self.dbm = dbManager('e2e_trace_manager', 'e2e_trace_manager', 'nfv', 'ohhberry3333', '211.224.204.203', '5432')
        