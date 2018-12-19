# Sentiment Analysis Services

#### This repository contains a SingularityNET service to analyze sentiment of sentences.

## Getting Started

### Requiments
- [Python 3.6+](https://www.python.org/downloads/)


### Development

Clone this repository and download the dependencies.

```
$ git clone https://github.com/singnet/nlp-services.git
$ cd sentiment-analysis
$ pip3 install -r requirements.txt
$ ./buildproto.sh
```

### Running the service

Start the server with:
```
$ python3 run_service.py

```

In another terminal, test your service with:
```
$ cd tests
$ python3 run_test_service.py

```

### For more details
- [User guide](/sentiment-analysis/USER_GUIDE.md)
- [How to publish a service](https://github.com/singnet/wiki/tree/master/tutorials/howToPublishService)

