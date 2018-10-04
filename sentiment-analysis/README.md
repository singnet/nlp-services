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
Fair drama/love story movie that focuses on the lives of blue collar people finding new life thru new love.

I guess he was trying to make a stylish movie. Any way I think this movie is a total waste of time and effort. 
```

Ps: You must break line between the sentences before encoding


Encode in base64 utf-8 text and the result will be like this:
```
RmFpciBkcmFtYS9sb3ZlIHN0b3J5IG1vdmllIHRoYXQgZm9jdXNlcyBvbiB0aGUgbGl2ZXMgb2YgYmx1ZSBjb2xsYXIgcGVvcGxlIGZpbmRpbmcgbmV3IGxpZmUgdGhydSBuZXcgbG92ZS4KCkkgZ3Vlc3MgaGUgd2FzIHRyeWluZyB0byBtYWtlIGEgc3R5bGlzaCBtb3ZpZS4gQW55IHdheSBJIHRoaW5rIHRoaXMgbW92aWUgaXMgYSB0b3RhbCB3YXN0ZSBvZiB0aW1lIGFuZCBlZmZvcnQuIAo
```

#### Service call example:
```
$ snet client call ConsensusAnalysis '{"value": "put your encoded input data here"}'
```

#### Output example:

The result will be a base64 text like this:

```
RmFpciBkcmFtYS9sb3ZlIHN0b3J5IG1vdmllIHRoYXQgZm9jdXNlcyBvbiB0aGUgbGl2ZXMgb2YgYmx1ZSBjb2xsYXIgcGVvcGxlIGZpbmRpbmcgbmV3IGxpZmUgdGhydSBuZXcgbG92ZS4KKCdwb3MnLCAxLjApCgpJIGd1ZXNzIGhlIHdhcyB0cnlpbmcgdG8gbWFrZSBhIHN0eWxpc2ggbW92aWUuIEFueSB3YXkgSSB0aGluayB0aGlzIG1vdmllIGlzIGEgdG90YWwgd2FzdGUgb2YgdGltZSBhbmQgZWZmb3J0LiAKKCduZWcnLCAxLjApCg==
```

After you decode the base64 result the output will be like this:

```
Fair drama/love story movie that focuses on the lives of blue collar people finding new life thru new love.
('pos', 1.0)

I guess he was trying to make a stylish movie. Any way I think this movie is a total waste of time and effort. 
('neg', 1.0)
```

#### Twitter input message attributes:
##### Used on the next two method:

- consumer_key:
    - Description: Consumer key of your twitter developer account
    - Type: Required string.
    - Example: '5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj'.
    
- consumer_secret:
    - Description: Consumer secret of your twitter developer account
    - Type: Required string.
    - Example: '5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj'.

- access_token:
    - Description: Token secret of your twitter developer account
    - Type: Required string.
    - Example: '5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj'.

- token_secret:
    - Description: Token secret of your twitter developer account
    - Type: Required string.
    - Example: '5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj'.
  
- product:
    - Description: Twitter product label.
    - Type: Required string.
    - Example: '30day' or 'fullarchive'.
    
- environment:
    - Description: Environment label of the created on twitter developer account. 
    - Type: Required string field.
    - Example: 'development'.
    
- query: 
    - Description: Query used to capture messages. 
    - Type: Required string field. 
    - Example: 'Donaldo Trump OR Hilary Cliont OR North Korea'
    
- messages_per_request -> 
    - Description: Number of messages per request.
    - Type: optional int, max of 100 for sandbox accounts and 500 for paid accounts. This Twitter information, please search for "Twitter Api Prices"
    - Example: 100
    - Note: If you don't send a value, twitter will assume default value for your type of account.
    
- max_requests_limit:
    - Description: number of http requests on api
    - Type: Optional int 10
    - Example: 10, 
    - Note: If you don't send a value, you will continue to request data until your account limit expires.  
    
- msg_limit:
    - Description: You can limit your request by message number
    - Type: Optional int
    - Example: 1250
    - Note: If you don't send a value, you will continue to request data until your account limit expires.
    
- time_limit:
    - Description: You can limit your request by time in seconds
    - Type: optional int
    - Example: 600 seconds or 10 minutes. 
    - Note: If you don't send a value, you will continue to request data until your account limit expires.
    
- from_date:
    - Description: Initial date range
    - Type: required date string
    - Example: '20181201235959'
    - Note: Pattern yyyymmddhhmmss
    
- to_date:
    - Description: Final date range
    - Type: required date string
    - Example: '20181231235959'
    - Note: -> Pattern yyyymmddhhmmss 

- languages:
    - Description: Selected language to be use on querying data
    - Type: optional string
    - Example: 'en' or 'en,pt,es'
    - Note:

JSON example:
```
{
    "credentials":{
        "consumer_key":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj",
        "consumer_secret":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj",
        "access_token":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj",
        "token_secret":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj"
    },
    "product":"30day",
    "environment":"development",
    "query":"Nike OR Adidas",
    "messages_per_request":"250",
    "max_requests_limit":"130",
    "msg_limit":"5000",
    "time_limit":"1200",
    "from_date":"20181201235959",
    "to_date":"20181231235959",
    "languages":"en"
}
```

### Twitter Historical Search:
#### Method signature: 
HistoricalAnalysis()

Note: This method request data on Twitter Search API, it captures twitter messages depending of the selected Twitter product.

Search Api has two products:
- 30 days: Capture last 30 days periodo
- fullarchive: Capture messages since 2006

To use this services, you must fill the method with the Twitter input message parameters according to message details above:
 

#### Service call example:
```
$ snet client call HistoricalAnalysis '{"credentials":{"consumer_key":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj","consumer_secret":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj","access_token":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj","token_secret":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj"},"product":"30day","environment":"development","query":"Nike OR Adidas","messages_per_request":"250","max_requests_limit":"130","msg_limit":"5000","time_limit":"1200","from_date":"20181201235959","to_date":"20181231235959","languages":"en"}'
```

#### Output example:

The result will be a base64 text like this:

```
RmFpciBkcmFtYS9sb3ZlIHN0b3J5IG1vdmllIHRoYXQgZm9jdXNlcyBvbiB0aGUgbGl2ZXMgb2YgYmx1ZSBjb2xsYXIgcGVvcGxlIGZpbmRpbmcgbmV3IGxpZmUgdGhydSBuZXcgbG92ZS4KKCdwb3MnLCAxLjApCgpJIGd1ZXNzIGhlIHdhcyB0cnlpbmcgdG8gbWFrZSBhIHN0eWxpc2ggbW92aWUuIEFueSB3YXkgSSB0aGluayB0aGlzIG1vdmllIGlzIGEgdG90YWwgd2FzdGUgb2YgdGltZSBhbmQgZWZmb3J0LiAKKCduZWcnLCAxLjApCg==
```

After you decode the base64 result the output will be like this:

```
This t-shirt is awesome.
{'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}

Bad people are coming.
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}
```

### Twitter Stream Search:

#### Method signature: 
StreamAnalysis()

Note: This method request data on twitter stream api, it captures live twitter messages. 

To use this services, you must fill the method with the Twitter input message parameters according to message details above:
 

#### Service call example:
```
$ snet client call StreamAnalysis '{"credentials":{"consumer_key":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj","consumer_secret":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj","access_token":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj","token_secret":"5ROv9lN1WBfmFtJKmNU4m0hNyFu6J1GB3eSFMbJMwBbmj"},"product":"30day","environment":"development","query":"Nike OR Adidas","messages_per_request":"250","max_requests_limit":"130","msg_limit":"5000","time_limit":"1200","from_date":"20181201235959","to_date":"20181231235959","languages":"en"}'
```

#### Output example:

The result will be a base64 text like this:

```
RmFpciBkcmFtYS9sb3ZlIHN0b3J5IG1vdmllIHRoYXQgZm9jdXNlcyBvbiB0aGUgbGl2ZXMgb2YgYmx1ZSBjb2xsYXIgcGVvcGxlIGZpbmRpbmcgbmV3IGxpZmUgdGhydSBuZXcgbG92ZS4KKCdwb3MnLCAxLjApCgpJIGd1ZXNzIGhlIHdhcyB0cnlpbmcgdG8gbWFrZSBhIHN0eWxpc2ggbW92aWUuIEFueSB3YXkgSSB0aGluayB0aGlzIG1vdmllIGlzIGEgdG90YWwgd2FzdGUgb2YgdGltZSBhbmQgZWZmb3J0LiAKKCduZWcnLCAxLjApCg==
```

After you decode the base64 result the output will be like this:

```
This t-shirt is awesome.
{'neg': 0.0, 'neu': 0.423, 'pos': 0.577, 'compound': 0.6249}

Bad people are coming.
{'neg': 0.538, 'neu': 0.462, 'pos': 0.0, 'compound': -0.5423}
```
