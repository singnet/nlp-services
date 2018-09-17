#!/usr/bin/env bash

#Stopping a service

# Removing running container
CONTAINER_ID="$(docker ps -a | grep NAMED_ENTITY_RECOGNITION | awk '{print $1}')"
docker start $CONTAINER_ID

