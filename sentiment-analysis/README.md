[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../docs/assets/singnet-logo.jpg?raw=true 'SingularityNET')

# Sentiment Analysis Services

This repository contains a SingularityNET service to analyze sentiment of sentences.
 
It is part of our [NLP Services](https://github.com/singnet/nlp-services).

## Getting Started

### Requirements

- [Python 3.6+](https://www.python.org/downloads/)


### Development

Clone this repository:

```
$ git clone https://github.com/singnet/nlp-services.git
$ cd nlp-services/sentiment-analysis
```

### Running the service:

To get the `ORGANIZATION_ID` and `SERVICE_ID` you must have already published a service 
(check this [link](https://dev.singularitynet.io/tutorials/publish/)).

Create the `SNET Daemon`'s config JSON file (`snetd.config.json`).

```
{
   "DAEMON_END_POINT": "DAEMON_HOST:DAEMON_PORT",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://kovan.infura.io",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "0xe331bf20044a5b24c1a744abc90c1fd711d2c08d",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "SERVICE_GRPC_HOST:SERVICE_GRPC_PORT",  
   "ORGANIZATION_ID": "ORGANIZATION_ID",
   "SERVICE_ID": "SERVICE_ID",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
           "TYPE": "stdout"
           }
   }
}
```

For example:

```
$ cat snetd.config.json
{
   "DAEMON_END_POINT": "http://54.203.198.53:7076",
   "ETHEREUM_JSON_RPC_ENDPOINT": "https://kovan.infura.io",
   "IPFS_END_POINT": "http://ipfs.singularitynet.io:80",
   "REGISTRY_ADDRESS_KEY": "0xe331bf20044a5b24c1a744abc90c1fd711d2c08d",
   "PASSTHROUGH_ENABLED": true,
   "PASSTHROUGH_ENDPOINT": "http://localhost:7003",
   "ORGANIZATION_ID": "snet",
   "SERVICE_ID": "opennmt-romance-translator",
   "LOG": {
       "LEVEL": "debug",
       "OUTPUT": {
           "TYPE": "stdout"
           }
   }
}
```
Install all dependencies:
```
$ pip3 install -r requirements.txt
```

Generate the gRPC codes:
```
$ sh buildproto.sh
```

Start the service and `SNET Daemon`:
```
$ python3 run_service.py
```

### Calling the service:

In another terminal, test your service with:
```
$ cd tests
$ python3 run_test_service.py

```

## Contributing and Reporting Issues

Please read our [guidelines](https://dev.singularitynet.io/docs/contribute/contribution-guidelines/#submitting-an-issue) before submitting an issue. 
If your issue is a bug, please use the bug template pre-populated [here][issue-template]. 
For feature requests and queries you can use [this template][feature-template].

## Authors

* **Glauter Lemos** - *Maintainer* - [SingularityNET](https://www.singularitynet.io)