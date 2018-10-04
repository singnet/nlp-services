# Named Entity Recognition Services

#### This repository contains a named entity recognition service.

## Usage:

### Named Entity Recognition:
#### Method signature: 
Recognize()

To use this method, you must build the input message as shown below:


#### Input data example:

For this example sentence as input data:
'Donald Trump is the president of United States and owner of Trump Tower company.'

Encode in base64 utf-8 text and the result will be like this:
```
RG9uYWxkIFRydW1wIGlzIHRoZSBwcmVzaWRlbnQgb2YgVW5pdGVkIFN0YXRlcyBhbmQgb3duZXIgb2YgVHJ1bXAgVG93ZXIgY29tcGFueS4=
```

#### Service call example:
```
$ snet client call Recognize '{"value": "RG9uYWxkIFRydW1wIGlzIHRoZSBwcmVzaWRlbnQgb2YgVW5pdGVkIFN0YXRlcyBhbmQgb3duZXIgb2YgVHJ1bXAgVG93ZXIgY29tcGFueS4"}' --no-confirm
```

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
$ [('Donald Trump', 'PERSON', 'Start index:', 0, 'End index:', 12), ('United States', 'LOCATION', 'Start index:', 29, 'End index:', 42), ('Trump Tower', 'ORGANIZATION', 'Start index:', 56, 'End index:', 67)]

```