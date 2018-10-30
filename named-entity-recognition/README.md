# Named Entity Recognition Services

#### This repository contains a named entity recognition service.

## Usage:

### Named Entity Recognition:
#### Method signature: 
Recognize()

To use this method, you must build the input message as shown below:


#### Input data example:

For this example sentence as input data:
Our concept of operations is to flow in our military assets with a priority to build up southern Texas, and then Arizona, and then California," Donald Trump said Monday, adding that the soldiers normally assigned weapons will be carrying them at the border. "We'll reinforce along priority points of entry, and while this happens, Trump Hotels is falling down in stock market.

Encode in base64 utf-8 text and the result will be like this:
```
T3VyIGNvbmNlcHQgb2Ygb3BlcmF0aW9ucyBpcyB0byBmbG93IGluIG91ciBtaWxpdGFyeSBhc3NldHMgd2l0aCBhIHByaW9yaXR5IHRvIGJ1aWxkIHVwIHNvdXRoZXJuIFRleGFzLCBhbmQgdGhlbiBBcml6b25hLCBhbmQgdGhlbiBDYWxpZm9ybmlhLCIgRG9uYWxkIFRydW1wIHNhaWQgTW9uZGF5LCBhZGRpbmcgdGhhdCB0aGUgc29sZGllcnMgbm9ybWFsbHkgYXNzaWduZWQgd2VhcG9ucyB3aWxsIGJlIGNhcnJ5aW5nIHRoZW0gYXQgdGhlIGJvcmRlci4gIldlJ2xsIHJlaW5mb3JjZSBhbG9uZyBwcmlvcml0eSBwb2ludHMgb2YgZW50cnksIGFuZCB3aGlsZSB0aGlzIGhhcHBlbnMsIFRydW1wIEhvdGVscyBpcyBmYWxsaW5nIGRvd24gaW4gc3RvY2sgbWFya2V0Lg==
```

#### Service call example:
```
$ snet client call Recognize '{"value": "T3VyIGNvbmNlcHQgb2Ygb3BlcmF0aW9ucyBpcyB0byBmbG93IGluIG91ciBtaWxpdGFyeSBhc3NldHMgd2l0aCBhIHByaW9yaXR5IHRvIGJ1aWxkIHVwIHNvdXRoZXJuIFRleGFzLCBhbmQgdGhlbiBBcml6b25hLCBhbmQgdGhlbiBDYWxpZm9ybmlhLCIgRG9uYWxkIFRydW1wIHNhaWQgTW9uZGF5LCBhZGRpbmcgdGhhdCB0aGUgc29sZGllcnMgbm9ybWFsbHkgYXNzaWduZWQgd2VhcG9ucyB3aWxsIGJlIGNhcnJ5aW5nIHRoZW0gYXQgdGhlIGJvcmRlci4gIldlJ2xsIHJlaW5mb3JjZSBhbG9uZyBwcmlvcml0eSBwb2ludHMgb2YgZW50cnksIGFuZCB3aGlsZSB0aGlzIGhhcHBlbnMsIFRydW1wIEhvdGVscyBpcyBmYWxsaW5nIGRvd24gaW4gc3RvY2sgbWFya2V0Lg=="}'
```

#### Output example:

The result will be a base64 text like this:

```
WygnVGV4YXMnLCAnTE9DQVRJT04nLCAnU3RhcnQgc3BhbjonLCA5NywgJ0VuZCBzcGFuOicsIDEwMiksICgnQXJpem9uYScsICdMT0NBVElPTicsICdTdGFydCBzcGFuOicsIDExMywgJ0VuZCBzcGFuOicsIDEyMCksICgnQ2FsaWZvcm5pYScsICdMT0NBVElPTicsICdTdGFydCBzcGFuOicsIDEzMSwgJ0VuZCBzcGFuOicsIDE0MSksICgnRG9uYWxkIFRydW1wJywgJ1BFUlNPTicsICdTdGFydCBzcGFuOicsIDE0NCwgJ0VuZCBzcGFuOicsIDE1NiksICgnVHJ1bXAgSG90ZWxzJywgJ09SR0FOSVpBVElPTicsICdTdGFydCBzcGFuOicsIDMzMSwgJ0VuZCBzcGFuOicsIDM0Myld
```

After you decode the base64 result the output will be like this:

```
$ [('Texas', 'LOCATION', 'Start span:', 97, 'End span:', 102), ('Arizona', 'LOCATION', 'Start span:', 113, 'End span:', 120), ('California', 'LOCATION', 'Start span:', 131, 'End span:', 141), ('Donald Trump', 'PERSON', 'Start span:', 144, 'End span:', 156), ('Trump Hotels', 'ORGANIZATION', 'Start span:', 331, 'End span:', 343)]

```