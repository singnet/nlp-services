#! /bin/bash
python3.6 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. services/model/sentiment_analysis_rpc.proto
