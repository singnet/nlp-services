# Sentiment Analysis Services

This repository contains a number of [SingularityNET](http://singularitynet.io) services for understanding or manipulating natural language.

- Twitter Stream Search Service - Capture and analyse all streamed twitter messages.
- Twitter Historical Search - Capture and analyse all twitter messages since 2006.
- Consensus Analysis - WIP
- Named Entity Recognition - WIP
- Topic Classification - WIP
- Language Generation - WIP
#####WIP = Work in Progress

## Deployment utils:

#### Deploy a new service
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/deploy_service.sh | bash
```

#### Update a running service
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/update_service.sh | bash
```

#### Remove a running service
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/remove_service.sh | bash
```

#### Update a docker service image
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/update_docker_image.sh | bash
```

#### Run a service container
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/run_service_container.sh | bash
```

#### Remove a service container
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/remove_service_container.sh | bash
```

#### Start a running container service
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/start_running_service.sh | bash
```

#### Stop a running container service
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/stop_running_service.sh | bash
```