#!/usr/bin/env bash

#Removing service

# Removing running container
CONTAINER_ID="$(docker ps -a | grep SENTIMENT_ANALYSIS | awk '{print $1}')"
docker rm -f $CONTAINER_ID

# Removing current docker imager for the respective service
IMAGE_ID="$(docker images -a | grep singularitynet/sentiment_analysis | awk '{print $3}'"
docker rmi -f $CONTAINER_ID
