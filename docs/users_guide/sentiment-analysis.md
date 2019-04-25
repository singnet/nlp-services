[issue-template]: ../../../issues/new?template=BUG_REPORT.md
[feature-template]: ../../../issues/new?template=FEATURE_REQUEST.md

![singnetlogo](../assets/singnet-logo.jpg?raw=true 'SingularityNET')

# Sentiment Analysis Service

It is part of our [NLP Services](https://github.com/singnet/nlp-services).

### Welcome

The service receives as sentences to be analyzed it's sentiment.

### What’s the point?

The service process input sentences and returns the analyzed sentence. 

### How does it work?

The user must provide the following inputs:

 - `value`: text sentence.
 

The output format is:
 - `value`: analyzed sentences in base64.
 
You can use this service from [SingularityNET DApp](http://beta.singularitynet.io/).

You can also call the service from SingularityNET CLI (`snet`).

Assuming that you have an open channel (`id: 0`) to this service:

##### Input data example:

For this example sentence as input data:

* Great price, fast shipping, great product.
* @Olielayus I want to go to promote GEAR AND GROOVE but unfornately no ride there  I may b going to the one in Anaheim in May though.
* @maja_dren2, is still sick, and worrying the orange she just ate is going to come back up... ugh. 

Convert the sentences to json format:
```
{"value": "[{\"id\": \"1\", \"sentence\": \"Grat price, fast shipping, great product.\"},{\"id\": \"2\", \"sentence\": \"@Oielayus I want to go to promote GEAR AND GROOVE but unfornately no ride there  I may b going to the one in Anaheim in May though.\"},{\"id\": \"3\" , \"sentence\": \"@mja_dren2, is still sick, and worrying the orange she just ate is going to come back up... ugh.\"}]"}
```
Then save it as json file like test.json

##### Service call example:
```
$ snet client call snet sentiment-analysis Analyze test.json -y
```

##### Output example:

The result will be like this:

```
{ value: [{"id": "1", "analysis": "{'neg': 0.0, 'neu': 0.328, 'pos': 0.672, 'compound': 0.8481}"}, {"id": "2", "analysis": "{'neg': 0.105, 'neu': 0.785, 'pos': 0.11, 'compound': -0.2144}"}, {"id": "3", "analysis": "{'neg': 0.362, 'neu': 0.638, 'pos': 0.0, 'compound': -0.8176}"}] }
```