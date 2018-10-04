#! /bin/bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services/service_spec/sentiment_analysis_rpc.proto
