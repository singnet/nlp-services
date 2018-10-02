#!/usr/bin/env bash

docker build -t singularitynet/sentiment_analysis:latest https://raw.githubusercontent.com/singnet/nlp-services/master/sentiment-analysis/Dockerfile
docker run --name SENTIMENT_ANALYSIS -p 7010:7010 -idt singularitynet/sentiment_analysis:latest