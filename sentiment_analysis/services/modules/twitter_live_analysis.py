import json

import requests

from TwitterAPI import TwitterAPI

# Twitter Credentials
# consumer key, consumer secret, access token, access secret.
from requests_oauthlib import OAuth1

consumer_key = "TscHeuS3vQN7bY82vNhE419ka"
consumer_secret = "5rCTzeRgwT0rTx56KCIQm0OUvgCmQ2WF9BLBC8NdkpmDpNYVoH"
access_token = "91892303-CUT4ZuJTqAxX2Ra2Bj7g1Hw0WmRPRtaiCPW2qm8CD"
token_secret = "SK7TVAL4QC9O93rhiyv1W4vLJUP0tUMWnjLbO7GkQ0IvE"


# SEARCH_TERM = 'Obama'
# PRODUCT = 'fullarchive'
# LABEL = 'SentimentAnalysis01'

# api = TwitterAPI(consumer_key, consumer_secret, access_token, token_secret)
# result = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL), {"query": "Obama", "maxResults": "10", "fromDate": "200801010910", "toDate": "200801150910"})
# jsondata = result.json()
# print(str(jsondata['next']))

# for item in result:
#     print(str(item['text']))

class TwitterApiReader:

    auth = None

    received_msgs = []
    error_message = None
    finished = False

    def __init__(self, consumer_key, consumer_secret, access_token, token_secret):
        self.auth = OAuth1(consumer_key, consumer_secret, access_token, token_secret)

    # url example:
    # https://api.twitter.com/1.1/tweets/search/fullarchive/SentimentAnalysis01.json
    #
    # header example:
    # headers = {'content-type': 'application/json'}
    #
    # request_data example:
    # {
    #   "query":"Obama",
    #   "maxResults":"10",
    #   "fromDate":"200801010910",
    #   "toDate":"200801150910"
    # }
    def read(self, url, params):
        response = requests.post(auth=self.auth, url=url, json=params)
        json_data = response.json()

        if response.status_code == requests.codes.ok:
            if len(json_data['results']) > 0:
                self.received_msgs.append(json_data['results'])
            if json_data['next']:
                self.read(url, params)
            else:
                self.finished = True
        else:
            self.error_message = json_data['error']['message']
            print("Error found => " + self.error_message)


reader = TwitterApiReader(consumer_key, consumer_secret, access_token, token_secret)
url = "https://api.twitter.com/1.1/tweets/search/fullarchive/SentimentAnalysis01.json"
params = {"query":"Obama", "maxResults":"10", "fromDate":"200801010910", "toDate":"200801150910"}

reader.read(url=url, params=params)

print(str(reader.received_msgs))
