#!/usr/bin/env bash

#Removing service

# Removing running container
CONTAINER_ID="$(docker ps -a | grep SENTIMENT_ANALYSIS | awk '{print $1}')"
docker rm -f $CONTAINER_ID
