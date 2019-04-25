[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../assets/singnet-logo.jpg?raw=true 'SingularityNET')

# Named Entity Recognition Service

It is part of our [NLP Services](https://github.com/singnet/nlp-services).

### Welcome

The service receives as sentences and identify ORGANIZATION, PLACE and PERSON entities.

### What’s the point?

The service process input sentences and returns all the identified entities. 

### How does it work?

The user must provide the following inputs:

 - `value`: text sentence.
 

The output format is:
 - `value`: identified entities it's positions in the input sentence in base64.
 
You can use this service from [SingularityNET DApp](http://beta.singularitynet.io/).

You can also call the service from SingularityNET CLI (`snet`).

Assuming that you have an open channel (`id: 0`) to this service:

#### Input data example:

For this example use these three sentences as input data:

* Microsoft is headquartered in the United States
* United States is a big country
* Mike lives in Brazil

Convert the sentences to json format:
```
{"value": "[{\"id\": \"1\", \"sentence\": \"Microsoft is headquartered in the United States\"}, {\"id\": \"2\", \"sentence\": \"United States is a big country\"}, {\"id\": \"3\", \"sentence\": \"Mike lives in Brazil\"}]"}
```
Then save it as json file like test.json

#### Service call example:
```

$ snet client call snet named-entity-recognition Recognize test.json -y
```

#### Output example:

The result will be like this:

```
{ value : [{"id": "1", "entities": [{"name": "Microsoft", "type": "ORGANIZATION", "Start span": 0, "End span": 9}, {"name": "United States", "type": "LOCATION", "Start span": 34, "End span": 47}]}, {"id": "2", "entities": [{"name": "United States", "type": "LOCATION", "Start span": 0, "End span": 13}]}, {"id": "3", "entities": [{"name": "Mike", "type": "PERSON", "Start span": 0, "End span": 4}, {"name": "Brazil", "type": "LOCATION", "Start span": 14, "End span": 20}]}] }
```

For more details about how to call SingularityNET services, please read our [How to publish a service](https://github.com/singnet/wiki/tree/master/tutorials/howToPublishService) tutorial.