#!/usr/bin/env bash

#Removing service

# Removing running container
CONTAINER_ID="$(docker ps -a | grep SENTIMENT_ANALYSIS | awk '{print $1}')"
docker rm $CONTAINER_ID -f

# Removing current docker imager for the respective service
IMAGE_ID="$(docker images -a | grep singularitynet/sentiment_analysis | awk '{print $3}'"
docker rmi $CONTAINER_ID -f
