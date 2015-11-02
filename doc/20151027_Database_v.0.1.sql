'211.224.204.203:5432
'e2e_trace_manager

CREATE TABLE tb_e2e_trace_list (
  trace_seq integer not null,
  customer_seq integer not null,
  trace_title character varying(100),
  result_status boolean,
  result_message character varying(255),
  result_detail text,
  current_step integer,
  create_dttm timestamp with time zone, -- trace 생성 시간
  update_dttm timestamp with time zone,
  CONSTRAINT tb_e2e_trace_list_pk PRIMARY KEY (trace_seq)
);

-- current_step: 매 step이 완료될 때 마다 tb_e2e_trace_list에 현재 step의 결과를 업데이트 해서 trace목록만 봐도 현재 상태를 확인할 수 있도록 함
-- 1) trace_seq 생성: trace_seq=1, customer_seq = 1
-- 2) tb_e2e_trace_list에 신규 trace 생성
INSERT INTO tb_e2e_trace_list (trace_seq, customer_seq, trace_title, create_dttm) VALUES (       1,           1,    '테스트',       now());
-- 3) 매 step에 대해서 tb_e2e_trace_list에 그 결과를 업데이트
--    3-1) 성공한 스텝
update tb_e2e_trace_list set
							result_status = TRUE, 
							result_message = "hello", 
							result_detail = "",
							current_step = 1, 
							update_dttm = now()
						where
							trace_seq = 1 and customer_seq = 1

--    3-2) 실패한 스텝
update tb_e2e_trace_list set
							result_status = FALSE, 
							result_message = "ERROR: no result", 
							result_detail = "",
							current_step = 2, 
							update_dttm = now()
						where
							trace_seq = 1 and customer_seq = 1
							


CREATE TABLE tb_e2e_trace_steps (
  step_seq integer,  
  trace_seq integer,
  step_title character varying(100),  
  mainclass character varying(30),
  subclass character varying(30),
  request_cmd character varying(200),
  request_param text,
  request_time timestamp with time zone,
  response_status boolean,
  response_time timestamp with time zone,
  message_detail text,
  CONSTRAINT tb_e2e_trace_steps_pk PRIMARY KEY (step_seq, trace_seq),
  CONSTRAINT tb_e2e_trace_steps_trace_seq_fkey FOREIGN KEY (trace_seq)
      REFERENCES  tb_e2e_trace_list(trace_seq) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- 1) step_seq 생성: step_seq = 1, trace_seq=1
-- 새로운 step 생성
INSERT INTO tb_e2e_trace_steps (step_seq, trace_seq, step_title, mainclass, subclass, request_cmd, reqeust_param, request_time)
                        VALUES (       1,         1,   '테스트',  'ORCH-M', 'MonMng',      'cat ',  '/etc/hosts',        now());

update tb_e2e_trace_list set
							response_status = TRUE, 
						    response_time = now()
							message_detail = 'hello'							
						where
							step_seq = 1 and trace_seq = 1					
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						
						