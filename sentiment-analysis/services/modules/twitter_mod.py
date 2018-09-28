import sqlite3

import requests
import time
import json

from requests_oauthlib import OAuth1
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from log import log_config

logger = log_config.getLogger('twitter_mod.py')

# Custom listener
# Extend Tweetpy StreamListener


class SnetListener(StreamListener):

    def __init__(self, msg_limit=0, time_limit=0):
        logger.debug("SnetListener INIT")
        self.start_time = time.time()
        self.time_limit = time_limit
        self.msg_limit = msg_limit
        self.msg_counter = 0
        self.sentences = []
        self.status_error_code = None
        super(SnetListener, self).__init__()

    def on_data(self, data):

        try:
            logger.debug("SnetListener on_data")
            # Counter Increment
            self.msg_counter += 1

            # Check limits
            if self.check_limits() is not True:
                return False

            # Converting json
            all_data = json.loads(data)
            tweet = all_data["text"]

            # Check if has text
            if tweet is not None:
                logger.debug(str(tweet))
                logger.debug(str(self.analizer.polarity_scores(tweet)))
                # item = (tweet, self.analizer.polarity_scores(tweet))
                self.sentences.append(tweet)

            # sentiment_value, confidence = s.sentiment(tweet)
            # logger.debug(tweet, sentiment_value, confidence)
            # if confidence * 100 >= 80:
            #     output = open("output/twitter-out.txt", "a")
            #     output.write(sentiment_value)
            #     output.write('\n')
            #     output.close()
            # return True

            return True

        except KeyError:
            return True

    def on_error(self, status_code):
        logger.debug("SnetListener on_error")
        self.status_error_code = status_code
        # if status_code > 400:
        # returning False in on_data disconnects the stream
        return False

    # Check search limits
    def check_limits(self):
        logger.debug("SnetListener check_limits")
        if self.time_limit > 0 and ((time.time() - self.start_time) > self.time_limit):
            logger.debug("SORRY, TIME LIMIT IS OVER !")
            return False
        if self.msg_limit > 0 and (self.msg_counter > self.msg_limit):
            logger.debug("SORRY, MSGS LIMIT IS OVER !")
            return False
        return True


# Stream Manager class
# Used for manage twitter connections based on it's limits


class SnetStreamManager:
    auth = ''
    stream = ''

    def __init__(self, consumer_key, consumer_secret, access_token, token_secret, msg_limit=0, time_limit=0):
        logger.debug("SnetStreamManager INIT")
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, token_secret)
        self.stream = Stream(self.auth, SnetListener(msg_limit=msg_limit, time_limit=time_limit))

    def filter(self, languages, keywords, async=False):
        logger.debug("SnetStreamManager filter")
        # logger.debug("")
        # self.stream.filter(languages=['en'], track=['happy'])
        self.stream.filter(languages=languages, track=keywords, async=async)
        # self.stream.disconnect()

    # Check search limits
    def check_limits(self):
        return self.stream.check_limits()

    # Check connection is finished
    def isrunning(self):
        return self.stream.running

    # Get status error code
    def status_error_code(self):
        return self.stream.listener.status_error_code

    # Disconnect session
    def disconnect(self):
        self.stream.disconnect()

    # Get sentences
    def sentences(self):
        # logger.debug("MANAGER SENTENCES...")
        # if self.stream.listener.sentences is not None:
        #     logger.debug("sentences populated...")
        return self.stream.listener.sentences


class TwitterApiReader:

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token,
                 token_secret,
                 msg_limit=0,
                 time_limit=0,
                 max_requests_limit=0,
                 db_name=None):

        self.auth = OAuth1(consumer_key, consumer_secret, access_token, token_secret)
        self.start_time = time.time()
        self.time_limit = time_limit
        self.msg_limit = msg_limit
        self.db_name = db_name
        self.messages = []
        self.max_requests_limit = max_requests_limit
        self.request_counter = 0
        self.start_time = time.time()
        self.reading = False

    def read(self, url, params):

        try:
            logger.debug("Start reading...")
            self.reading = True

            if self.check_limits():
                self.request_counter += 1
                print("Requesting page number : " + str(self.request_counter))
                response = requests.post(auth=self.auth, url=url, json=params)
                json_data = response.json()

                if response.status_code == requests.codes.ok:
                    if len(json_data['results']) > 0:
                        self.messages.append(json_data['results'])

                        if self.db_name is not None:
                            # Writing on database
                            with sqlite3.connect(self.db_name) as conn:
                                cur = conn.cursor()
                                cur.execute('''create table if not exists messages(original_data json)''')
                                temp_msg_counter = 0
                                for item in json_data['results']:
                                    temp_msg_counter += 1
                                    cur.execute("insert into messages values (?)", [json.dumps(item)])
                                    print("Inserting into database message number: " + str(temp_msg_counter))

                    if json_data['next']:
                        # Set next page hash to call
                        params['next'] = str(json_data['next'])
                        # Twitter sandbox rate limits: 30 RPM, 10RPS
                        time.sleep(2.2)
                        # Call next page of data
                        self.read(url, params)

                    self.reading = False
                else:
                    logger.debug("Error found => " + json_data['error']['message'])
                    raise Exception(str(json_data['error']['message']))

        except Exception as e:
            self.reading = False
            logger.debug("Reader error => " + str(e))

    def messages(self):
        return self.messages

    def reading(self):
        return self.reading

    # Check search limits
    def check_limits(self):
        logger.debug("SnetListener check_limits")
        if self.time_limit > 0 and ((time.time() - self.start_time) > self.time_limit):
            logger.debug("SORRY, TIME LIMIT IS OVER !")
            raise Exception("SORRY, TIME LIMIT IS OVER !")
        if self.msg_limit > 0 and (len(self.messages) > self.msg_limit):
            logger.debug("SORRY, MSGS LIMIT IS OVER !")
            raise Exception("SORRY, MSGS LIMIT IS OVER !")
        if self.request_counter > 0 and self.request_counter >= self.max_requests_limit:
            logger.debug("SORRY, REQUESTS LIMIT IS OVER !")
            raise Exception("SORRY, REQUESTS LIMIT IS OVER !")
        return True

# Especificação:
#
# 25000 mensagens relacionadas a politicos
# 25000 mensagens relacionadas a organizações não governamentais
# 25000 mensagens relacionadas as marcas mais influentes
#
# Output
# user_id named_entity named_entity_type sentiment analysis
