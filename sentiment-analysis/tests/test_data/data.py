# Twitter parameters for Historical and Stream Apis
consumer_key = None  # i.e hash string - consumer_key of twitter developer account
consumer_secret = None  # i.e hash string - consumer_secret of twitter developer account
access_token = None  # i.e hash string - access_token of twitter developer account
token_secret = None  # i.e hash string - token_secret of twitter developer account
product = None  # i.e string '30day' - twitter product options '30day' or 'fullarchive' apis.
environment = None  # i.e string 'development' - name/label of the created environment on twitter developer account
query = None  # i.e string 'Donaldo Trump OR Hilary Cliont OR North Korea' - query used to capture messages
messages_per_request = None  # i.e int 250 - number of messages per request
max_requests_limit = None  # i.e int 10 - number of http requests on api
msg_limit = None  # i.e int 10000 - capture 10000 messages
time_limit = None  # i.e int 120 - in seconds
from_date = None  # i.e string '20181231070810' - datetime module pattern %Y%m%d%H%M%S
to_date = None  # i.e string '20181231070810' - datetime module pattern %Y%m%d%H%M%S
db_name = None  # i.e string 'twitter_messages.db'
languages = None  # i.e 'en' or 'en,pt,es' - optional - Specific for Stream Api