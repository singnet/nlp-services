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
```
Great price, fast shipping, great product.

@Olielayus I want to go to promote GEAR AND GROOVE but unfornately no ride there  I may b going to the one in Anaheim in May though.

@maja_dren2, is still sick, and worrying the orange she just ate is going to come back up... ugh. 
```

Ps: You must break line between the sentences before encoding

Encode in base64 utf-8 text and the result will be like this:
```
R3JlYXQgcHJpY2UsIGZhc3Qgc2hpcHBpbmcsIGdyZWF0IHByb2R1Y3QuCgpAT2xpZWxheXVzIEkgd2FudCB0byBnbyB0byBwcm9tb3RlIEdFQVIgQU5EIEdST09WRSBidXQgdW5mb3JuYXRlbHkgbm8gcmlkZSB0aGVyZSAgSSBtYXkgYiBnb2luZyB0byB0aGUgb25lIGluIEFuYWhlaW0gaW4gTWF5IHRob3VnaC4KCkBtYWphX2RyZW4yLCBpcyBzdGlsbCBzaWNrLCBhbmQgd29ycnlpbmcgdGhlIG9yYW5nZSBzaGUganVzdCBhdGUgaXMgZ29pbmcgdG8gY29tZSBiYWNrIHVwLi4uIHVnaC4=
```

##### Service call example:
```
$ snet client call 0 0.00000001 54.203.198.53:7010 ConsensusAnalysis '{"value": "put your encoded input data here"}'
```

##### Output example:

The result will be a base64 text like this:

```
R3JlYXQgcHJpY2UsIGZhc3Qgc2hpcHBpbmcsIGdyZWF0IHByb2R1Y3QuCnsnbmVnJzogMC4wLCAnbmV1JzogMC4zMjgsICdwb3MnOiAwLjY3MiwgJ2NvbXBvdW5kJzogMC44NDgxfQoKQE9saWVsYXl1cyBJIHdhbnQgdG8gZ28gdG8gcHJvbW90ZSBHRUFSIEFORCBHUk9PVkUgYnV0IHVuZm9ybmF0ZWx5IG5vIHJpZGUgdGhlcmUgIEkgbWF5IGIgZ29pbmcgdG8gdGhlIG9uZSBpbiBBbmFoZWltIGluIE1heSB0aG91Z2guCnsnbmVnJzogMC4xMDUsICduZXUnOiAwLjc4NSwgJ3Bvcyc6IDAuMTEsICdjb21wb3VuZCc6IC0wLjIxNDR9CgpAbWFqYV9kcmVuMiwgaXMgc3RpbGwgc2ljaywgYW5kIHdvcnJ5aW5nIHRoZSBvcmFuZ2Ugc2hlIGp1c3QgYXRlIGlzIGdvaW5nIHRvIGNvbWUgYmFjayB1cC4uLiB1Z2guCnsnbmVnJzogMC4zNjIsICduZXUnOiAwLjYzOCwgJ3Bvcyc6IDAuMCwgJ2NvbXBvdW5kJzogLTAuODE3Nn0KCg==
```

After you decode the base64 result the output will be like this:

```
Great price, fast shipping, great product.
{'neg': 0.0, 'neu': 0.328, 'pos': 0.672, 'compound': 0.8481}

@Olielayus I want to go to promote GEAR AND GROOVE but unfornately no ride there  I may b going to the one in Anaheim in May though.
{'neg': 0.105, 'neu': 0.785, 'pos': 0.11, 'compound': -0.2144}

@maja_dren2, is still sick, and worrying the orange she just ate is going to come back up... ugh.
{'neg': 0.362, 'neu': 0.638, 'pos': 0.0, 'compound': -0.8176}
```