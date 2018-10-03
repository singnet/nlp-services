#!/usr/bin/env bash

#Update docker image
docker build -t singularitynet/named_entity_recognition:latest https://raw.githubusercontent.com/singnet/nlp-services/master/named-entity-recognition/Dockerfile
#Removing current container running
CONTAINER_ID="$(docker ps -a | grep NAMED_ENTITY_RECOGNITION | awk '{print $1}')"
docker rm -f $CONTAINER_ID
docker run --name NAMED_ENTITY_RECOGNITION -p 7010:7010 -idt singularitynet/named_entity_recognition:latest
