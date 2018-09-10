# Sentiment Analysis Services

This repository contains a number of [SingularityNET](http://singularitynet.io) services for understanding or manipulating natural language.

- Twitter Stream Search Service - Capture and analyse all streamed twitter messages.
- Twitter Historical Search - Capture and analyse all twitter messages since 2006.
- Consensus Analysis - WIP
- Named Entity Recognition - WIP
- Topic Classification - WIP
- Language Generation - WIP
#####WIP = Work in Progress

## Deployment:

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

#### Start a running container service
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/start_running_service.sh | bash
```

#### Stop a running container service
```
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/stop_running_service.sh | bash
```

## Usage:

To use this services, you must fill the input parameters below:

#### Input Parameters:
- languages - languages the service will consider in the analysis. For unique language: "en". For multiple languages: "en,pt,es".
- keywords - This parameter can be used for one word or a sentence. E.g: For one word: => "happiness". For a sentence => "People are discussing about Donald Trump decisions".
- msg_limit - number of messages to analyse.
- time_limit - duration of the analysis (in seconds).

#### Output content:
The result of analysis will be a base64 text including the result of analysis for each captured message.

Output example:

```
This t-shirt is awesome.
{'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}

Bad people are coming.
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}

```
