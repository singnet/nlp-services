#!/usr/bin/env bash

docker build --no-cache -t singularitynet/named_entity_recognition:latest https://raw.githubusercontent.com/singnet/nlp-services/master/named-entity-recognition/Dockerfile
docker run --name NAMED_ENTITY_RECOGNITION -p 7012:7012 -idt singularitynet/named_entity_recognition:latest