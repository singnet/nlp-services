#!/usr/bin/env bash

#Running container service
docker run --name SENTIMENT_ANALYSIS -p 7010:7010 -idt singularitynet/sentiment_analysis:latest
