# Twitter parameters for Historical and Stream Apis
# consumer_key = None  # i.e hash string - consumer_key of twitter developer account
# consumer_secret = None  # i.e hash string - consumer_secret of twitter developer account
# access_token = None  # i.e hash string - access_token of twitter developer account
# token_secret = None  # i.e hash string - token_secret of twitter developer account
# product = None  # i.e string '30day' - twitter product options '30day' or 'fullarchive' apis.
# environment = None  # i.e string 'development' - name/label of the created environment on twitter developer account
# query = None  # i.e string 'Donaldo Trump OR Hilary Cliont OR North Korea' - query used to capture messages
# messages_per_request = None  # i.e int 250 - number of messages per request
# max_requests_limit = None  # i.e int 10 - number of http requests on api
# msg_limit = None  # i.e int 10000 - capture 10000 messages
# time_limit = None  # i.e int 120 - in seconds
# from_date = None  # i.e string '20181231070810' - datetime module pattern %Y%m%d%H%M%S
# to_date = None  # i.e string '20181231070810' - datetime module pattern %Y%m%d%H%M%S
# db_name = None  # i.e string 'twitter_messages.db'
# languages = None  # i.e 'en' or 'en,pt,es' - optional - Specific for Stream Api


# BRANNY
consumer_key = "UnxeNduqo1tprEo3PFstjcNLi"
consumer_secret = "LscAUbeo1CbU4xgOKVPFP82q3NM2eHTUM4CafV2n6ZdETjEsAD"
access_token = "377003839-W8asPdKOP9JTqJKOmgraTWJwPJIz2MeLoJlXBvya"
token_secret = "FUUSX7LLa5MazHmoXsoqilEaqQ6Ou0ZU5f2JqCIOnlT1t"
product = '30day'
environment = 'SentimentAnalysis30Days'

query = 'Trump OR Clinton'
messages_per_request = 100
max_requests_limit = 2
time_limit = 30
msg_limit = 10
from_date = '201809260000'
to_date = '201809270000'
db_name = "twitter_messages"
languages = 'en'
