
1. prerequisite
	>> pip install jsonpickle

2. TABLE: tb_e2e_trace_list
	>> sudo -u postgres psql -d e2e_trace_manager -c "select * from tb_e2e_trace_list"

3. dbManager 
	>> self.dbm = dbManager('e2e_trace_manager', 'e2e_trace_manager', 'nfv', 'ohhberry3333', '211.224.204.203', '5432')

4. test 폴더의 list.sh를 통해 database에서 e2e_trace_list의 내용을 확인할 수 있다.
5. test 폴더의 add_trace.sh를 통해 database의 e2e_trace_list에 새로운 trace를 추가할 수 있다.
6. 추가 개발이 필요한 부분
   - 새로운 step의 추가 (DONE, 2015-12-12 04:14)
   - step 추가시에 request parameter 추가
   - step update를 통한 response 입력
   - trace를 입력하면 step을 시간순으로 표시
   - design pattern 적용: MVC? database 입력 부분을 처리 로직에서 분리 필요