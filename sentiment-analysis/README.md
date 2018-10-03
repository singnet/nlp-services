# Sentiment Analysis Services

#### This repository contains a sentiment analysis service.

##### Available methods of sentiment analysis:

- Consensus Analysis - The sentences are analyzed by seven trained classifiers.
- Twitter Historical Search - Capture and analyse all twitter messages since 2006.
- Twitter Stream Search Service - Capture and analyse all streamed twitter messages.

## Usage:

### Consensus Analysis:
#### Method signature: 
ConsensusAnalysis()

To use this method, you must build the input message as shown below:


#### Input data example:

For this example sentence as input data:
```
Bromwell High is a cartoon comedy. It ran at the same time as some other programs about school life, such as "Teachers". My 35 years in the teaching profession lead me to believe that Bromwell High's satire is much closer to reality than is "Teachers". The scramble to survive financially, the insightful students who can see right through their pathetic teachers' pomp, the pettiness of the whole situation, all remind me of the schools I knew and their students. When I saw the episode in which a student repeatedly tried to burn down the school, I immediately recalled at High. A classic line: INSPECTOR: I'm here to sack one of your teachers. STUDENT: Welcome to Bromwell High. I expect that many adults of my age think that Bromwell High is far fetched. What a pity that it isn't!

Story of a man who has unnatural feelings for a pig. Starts out with a opening scene that is a terrific example of absurd comedy. A formal orchestra audience is turned into an insane, violent mob by the crazy chantings of it's singers. Unfortunately it stays absurd the WHOLE time with no general narrative eventually making it just too off putting. Even those from the era should be turned off. The cryptic dialogue would make Shakespeare seem easy to a third grader. On a technical level it's better than you might think with some good cinematography by future great Vilmos Zsigmond. Future stars Sally Kirkland and Frederic Forrest can be seen briefly.
```

Ps: You must break line between the sentences


Encode in base64 utf-8 text and the result will be like this:
```
QnJvbXdlbGwgSGlnaCBpcyBhIGNhcnRvb24gY29tZWR5LiBJdCByYW4gYXQgdGhlIHNhbWUgdGltZSBhcyBzb21lIG90aGVyIHByb2dyYW1zIGFib3V0IHNjaG9vbCBsaWZlLCBzdWNoIGFzICJUZWFjaGVycyIuIE15IDM1IHllYXJzIGluIHRoZSB0ZWFjaGluZyBwcm9mZXNzaW9uIGxlYWQgbWUgdG8gYmVsaWV2ZSB0aGF0IEJyb213ZWxsIEhpZ2gncyBzYXRpcmUgaXMgbXVjaCBjbG9zZXIgdG8gcmVhbGl0eSB0aGFuIGlzICJUZWFjaGVycyIuIFRoZSBzY3JhbWJsZSB0byBzdXJ2aXZlIGZpbmFuY2lhbGx5LCB0aGUgaW5zaWdodGZ1bCBzdHVkZW50cyB3aG8gY2FuIHNlZSByaWdodCB0aHJvdWdoIHRoZWlyIHBhdGhldGljIHRlYWNoZXJzJyBwb21wLCB0aGUgcGV0dGluZXNzIG9mIHRoZSB3aG9sZSBzaXR1YXRpb24sIGFsbCByZW1pbmQgbWUgb2YgdGhlIHNjaG9vbHMgSSBrbmV3IGFuZCB0aGVpciBzdHVkZW50cy4gV2hlbiBJIHNhdyB0aGUgZXBpc29kZSBpbiB3aGljaCBhIHN0dWRlbnQgcmVwZWF0ZWRseSB0cmllZCB0byBidXJuIGRvd24gdGhlIHNjaG9vbCwgSSBpbW1lZGlhdGVseSByZWNhbGxlZCBhdCBIaWdoLiBBIGNsYXNzaWMgbGluZTogSU5TUEVDVE9SOiBJJ20gaGVyZSB0byBzYWNrIG9uZSBvZiB5b3VyIHRlYWNoZXJzLiBTVFVERU5UOiBXZWxjb21lIHRvIEJyb213ZWxsIEhpZ2guIEkgZXhwZWN0IHRoYXQgbWFueSBhZHVsdHMgb2YgbXkgYWdlIHRoaW5rIHRoYXQgQnJvbXdlbGwgSGlnaCBpcyBmYXIgZmV0Y2hlZC4gV2hhdCBhIHBpdHkgdGhhdCBpdCBpc24ndCEKClN0b3J5IG9mIGEgbWFuIHdobyBoYXMgdW5uYXR1cmFsIGZlZWxpbmdzIGZvciBhIHBpZy4gU3RhcnRzIG91dCB3aXRoIGEgb3BlbmluZyBzY2VuZSB0aGF0IGlzIGEgdGVycmlmaWMgZXhhbXBsZSBvZiBhYnN1cmQgY29tZWR5LiBBIGZvcm1hbCBvcmNoZXN0cmEgYXVkaWVuY2UgaXMgdHVybmVkIGludG8gYW4gaW5zYW5lLCB2aW9sZW50IG1vYiBieSB0aGUgY3JhenkgY2hhbnRpbmdzIG9mIGl0J3Mgc2luZ2Vycy4gVW5mb3J0dW5hdGVseSBpdCBzdGF5cyBhYnN1cmQgdGhlIFdIT0xFIHRpbWUgd2l0aCBubyBnZW5lcmFsIG5hcnJhdGl2ZSBldmVudHVhbGx5IG1ha2luZyBpdCBqdXN0IHRvbyBvZmYgcHV0dGluZy4gRXZlbiB0aG9zZSBmcm9tIHRoZSBlcmEgc2hvdWxkIGJlIHR1cm5lZCBvZmYuIFRoZSBjcnlwdGljIGRpYWxvZ3VlIHdvdWxkIG1ha2UgU2hha2VzcGVhcmUgc2VlbSBlYXN5IHRvIGEgdGhpcmQgZ3JhZGVyLiBPbiBhIHRlY2huaWNhbCBsZXZlbCBpdCdzIGJldHRlciB0aGFuIHlvdSBtaWdodCB0aGluayB3aXRoIHNvbWUgZ29vZCBjaW5lbWF0b2dyYXBoeSBieSBmdXR1cmUgZ3JlYXQgVmlsbW9zIFpzaWdtb25kLiBGdXR1cmUgc3RhcnMgU2FsbHkgS2lya2xhbmQgYW5kIEZyZWRlcmljIEZvcnJlc3QgY2FuIGJlIHNlZW4gYnJpZWZseS4=
```

#### Service call example:
```
$ snet client call ConsensusAnalysis '{"value": "put your encoded input data here"}'
```
*******************************************************
*******************************************************
*******************************************************
*******************************************************
#### Output example:

The result will be a base64 text like this:

```
WygnRG9uYWxkIFRydW1wJywgJ1BFUlNPTicsICdTdGFydCBpbmRleDonLCAwLCAn
RW5kIGluZGV4OicsIDEyKSwgKCdVbml0ZWQgU3RhdGVzJywgJ0xPQ0FUSU9OJywg
J1N0YXJ0IGluZGV4OicsIDI5LCAnRW5kIGluZGV4OicsIDQyKSwgKCdUcnVtcCBU
b3dlcicsICdPUkdBTklaQVRJT04nLCAnU3RhcnQgaW5kZXg6JywgNTYsICdFbmQg
aW5kZXg6JywgNjcpXQo=
```

After you decode the base64 result the output will be like this:

```
This t-shirt is awesome.
{'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}

Bad people are coming.
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}
```

### Consensus Analysis:
#### Method signature: 
ConsensusAnalysis()

To use this method, you must build the input message as shown below:

#### Input Message Attributes:
- value - Base64 text

#### Service call example:
```
$ snet client call GetConsensusAnalysis '{"value": "VGVzdGluZyBzZXJ2aWNl"}' --no-confirm
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

### Twitter Stream Search:

#### Method signature: 
StreamAnalysis()

To use this services, you must fill the input parameters below:

#### Input Message Attributes:
- credentials - Twitter credentials (get on twitter for developers page)
- languages - languages the service will consider in the analysis. For unique language: "en". For multiple languages: "en,pt,es".
- keywords - This parameter can be used for one word or a sentence. E.g: For one word: => "happiness". For a sentence => "People are discussing about Donald Trump decisions".
- msg_limit - number of messages to analyse.
- time_limit - duration of the analysis (in seconds).

#### Service call example:
```
$ snet client call StreamAnalysis '{"credentials":{"consumer_key":"TscHeuS3vQN7bY82vNhE419ka","consumer_secret":"5rCTzeRgwT0rTx56KCIQm0OUvgCmQ2WF9BLBC8NdkpmDpNYVoH","access_token":"91892303-CUT4ZuJTqAxX2Ra2Bj7g1Hw0WmRPRtaiCPW2qm8CD","token_secret":"SK7TVAL4QC9O93rhiyv1W4vLJUP0tUMWnjLbO7GkQ0IvE"},"languages":"en","keywords":"happy","time_limit":"3","msg_limit":"3"}' --no-confirm
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
HistoricalAnalysis()

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
$ snet client call HistoricalAnalysis '{"credentials":{"consumer_key":"TscHeuS3vQN7bY82vNhE419ka","consumer_secret":"5rCTzeRgwT0rTx56KCIQm0OUvgCmQ2WF9BLBC8NdkpmDpNYVoH","access_token":"91892303-CUT4ZuJTqAxX2Ra2Bj7g1Hw0WmRPRtaiCPW2qm8CD","token_secret":"SK7TVAL4QC9O93rhiyv1W4vLJUP0tUMWnjLbO7GkQ0IvE"},"languages":"en","keywords":"happy","max_results":"10", "from_date":"200801010910", "to_date":"200801150910", "product": "fullarchive", "environment":"SentimentAnalysis01"}' --no-confirm
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