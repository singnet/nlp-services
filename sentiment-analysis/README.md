# Sentiment Analysis Services

#### This repository contains a sentiment analysis service.

##### Avaliable methods of sentiment analysis:

- Twitter Stream Search Service - Capture and analyse all streamed twitter messages.
- Twitter Historical Search - Capture and analyse all twitter messages since 2006.
- Intensivity Analysis - Simple Sentiment Analysis.
- Consensus Analysis - The sentences are analyzed by seven trained classifiers.

WIP = Work in Progress

## Deployment:

#### Deploy a new service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/deploy_service.sh | bash
```

#### Update a running service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/update_service.sh | bash
```

#### Remove a running service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/remove_service.sh | bash
```

#### Start a running container service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/start_running_service.sh | bash
```

#### Stop a running container service
```bash
$ curl https://raw.githubusercontent.com/singnet/nlp-services/sentiment_analysis/sentiment_analysis/deploy/stop_running_service.sh | bash
```

## Usage:

### Twitter Stream Search:
#### Method signature: 
streamAnalysis()

To use this services, you must fill the input parameters below:

#### Input Message Attributes:
- credentials - Twitter credentials (get on twitter for developers page)
- languages - languages the service will consider in the analysis. For unique language: "en". For multiple languages: "en,pt,es".
- keywords - This parameter can be used for one word or a sentence. E.g: For one word: => "happiness". For a sentence => "People are discussing about Donald Trump decisions".
- msg_limit - number of messages to analyse.
- time_limit - duration of the analysis (in seconds).

#### Service call example:
```
$ snet client call streamAnalysis '{"credentials":{"consumer_key":"TscHeuS3vQN7bY82vNhE419ka","consumer_secret":"5rCTzeRgwT0rTx56KCIQm0OUvgCmQ2WF9BLBC8NdkpmDpNYVoH","access_token":"91892303-CUT4ZuJTqAxX2Ra2Bj7g1Hw0WmRPRtaiCPW2qm8CD","token_secret":"SK7TVAL4QC9O93rhiyv1W4vLJUP0tUMWnjLbO7GkQ0IvE"},"languages":"en","keywords":"happy","time_limit":"3","msg_limit":"3"}' --no-confirm
```

#### Output example:
The result of analysis will be a base64 text including the result of analysis for each captured message.

Output example:

```
This t-shirt is awesome.
{'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}

Bad people are coming.
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}

```

### Twitter Historical Search:
#### Method signature: 
historicalAnalysis()

To use this services, you must fill the input parameters below:

#### Input Message Attributes:
- credentials - Twitter credentials (get on twitter for developers page)
- languages - languages the service will consider in the analysis. For unique language: "en". For multiple languages: "en,pt,es".
- keywords - This parameter can be used for one word or a sentence. E.g: For one word: => "happiness". For a sentence => "People are discussing about Donald Trump decisions".
- from_date - Start date range. Date format: yyyymmddhhmmss E.g =>  20180110091005.
- to_date - End date range. Date format: yyyymmddhhmmss E.g =>  20180110091005.
- max_results - Number of results per page. 
- product - Twitter search product. e.g 'premiun' or 'enterprise'
- environment - Environment name on Twitter Developer Profile Page

#### Service call example:
```
$ snet client call historicalAnalysis '{"credentials":{"consumer_key":"TscHeuS3vQN7bY82vNhE419ka","consumer_secret":"5rCTzeRgwT0rTx56KCIQm0OUvgCmQ2WF9BLBC8NdkpmDpNYVoH","access_token":"91892303-CUT4ZuJTqAxX2Ra2Bj7g1Hw0WmRPRtaiCPW2qm8CD","token_secret":"SK7TVAL4QC9O93rhiyv1W4vLJUP0tUMWnjLbO7GkQ0IvE"},"languages":"en","keywords":"happy","max_results":"10", "from_date":"200801010910", "to_date":"200801150910", "product": "fullarchive", "environment":"SentimentAnalysis01"}' --no-confirm
```

#### Output example:
The result of analysis will be a base64 text including the result of analysis for each captured message.

Output example:

```
This t-shirt is awesome.
{'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}

Bad people are coming.
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}

```

### Intensivity Analysis:
#### Method signature: 
intensivityAnalysis()

To use this method, you must build the input message as shown below:

#### Input Message Attributes:
- value - Base64 text

#### Service call example:
```
$ snet client call intensivityAnalysis '{"value": "VGVzdGluZyBzZXJ2aWNl"}' --no-confirm
```

#### Output example:
The result of analysis will be a base64 text including the result of analysis for each captured message.

Output example:

```
This t-shirt is awesome.
{'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}

Bad people are coming.
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}

```

### Consensus Analysis:
#### Method signature: 
consensusAnalysis()

To use this method, you must build the input message as shown below:

#### Input Message Attributes:
- value - Base64 text

#### Service call example:
```
$ snet client call intensivityAnalysis '{"value": "VGVzdGluZyBzZXJ2aWNl"}' --no-confirm
```

#### Output example:
The result of analysis will be a base64 text including the result of analysis for each captured message.

Output example:

```
This t-shirt is awesome.
{'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}

Bad people are coming.
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}

```