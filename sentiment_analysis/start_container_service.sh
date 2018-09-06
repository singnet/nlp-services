#!/usr/bin/env bash

docker build -t singularitynet/sentiment_analysis:v1.0 https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/Dockerfile &
wait; docker run --name SENTIMENT_ANALYSIS -p 7010:7010 -idt singularitynet/sentiment_analysis_test:latest

