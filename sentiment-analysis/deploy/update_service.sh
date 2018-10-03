#!/usr/bin/env bash

#Update docker image
docker build -t singularitynet/sentiment_analysis:latest https://raw.githubusercontent.com/singnet/nlp-services/master/sentiment-analysis/Dockerfile
#Removing current container running
CONTAINER_ID="$(docker ps -a | grep SENTIMENT_ANALYSIS | awk '{print $1}')"
docker rm -f $CONTAINER_ID
docker run --name SENTIMENT_ANALYSIS -p 7010:7010 -idt singularitynet/sentiment_analysis:latest
