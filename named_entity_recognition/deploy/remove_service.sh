#!/usr/bin/env bash

#Removing service

# Removing running container
CONTAINER_ID="$(docker ps -a | grep NAMED_ENTITY_RECOGNITION | awk '{print $1}')"
docker rm -f $CONTAINER_ID

# Removing current docker image for the respective service
IMAGE_ID="$(docker images -a | grep singularitynet/named_entity_recognition | awk '{print $3}')"
docker rmi $IMAGE_ID