curl -v http://localhost:8888/ -X POST --data-binary '{"traceseq": 2, "customerseq": 100, "title": "post-test", "mainclass":"monitoring-manager", "subclass":"orchestrator-m" }' -H "Content-type: application/json"