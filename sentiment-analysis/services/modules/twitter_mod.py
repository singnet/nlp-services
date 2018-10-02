import datetime
import sqlite3

import requests
import time
import json

from requests_oauthlib import OAuth1
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from log import log_config

logger = log_config.getLogger('twitter_mod.py')


class SnetListener(StreamListener):
    """ Extended Tweet Listener
    """

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
        """Called when raw data is received from connection.
        
            Override this method if you wish to manually handle
            the stream data. Return False to stop stream and close connection.
        """

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
                self.sentences.append(tweet)

            # work in progress
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
            logger.debug("SnetListener on_data catch error")
            return True

    def on_error(self, status_code):
        """ Called when a non-200 status code is returned

        if status_code > 400:
        returning False in on_data disconnects the stream

        :param status_code:
        :return:
        """
        logger.debug("SnetListener on_error status_code =>" + str(status_code))
        self.status_error_code = status_code

        return False

    def check_limits(self):
        """ Check search limits
        :return:
        """
        logger.debug("SnetListener check_limits")
        if self.time_limit > 0 and ((time.time() - self.start_time) > self.time_limit):
            logger.debug("Sorry, time limit is over !")
            return False

        if self.msg_limit > 0 and (self.msg_counter > self.msg_limit):
            logger.debug("Sorry, message limit is over !")
            return False

        return True


class SnetStreamManager:
    """Stream manager class

    Used to manage streamming messages from twitter
    according to service parameters
    """
    auth = ''
    stream = ''

    def __init__(self, consumer_key, consumer_secret, access_token, token_secret, msg_limit=0, time_limit=0):
        logger.debug("SnetStreamManager Init")
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, token_secret)
        self.stream = Stream(self.auth, SnetListener(msg_limit=msg_limit, time_limit=time_limit))

    def filter(self, languages, query, async=False):
        """ Start filtering messages on twitter
        :param languages:
        :param query:
        :param async:
        :return:
        """
        logger.debug("SnetStreamManager filter")
        # logger.debug("")
        self.stream.filter(languages=['en'], track=['happy'])
        # self.stream.filter(languages=languages, track=query, async=async)
        self.stream.disconnect()

    def check_limits(self):
        """ Check search limits
        :return:
        """

        return self.stream.check_limits()

    def isrunning(self):
        """ Check connection is finished
        :return:
        """

        return self.stream.running

    def status_error_code(self):
        """ Get status error code
        :return:
        """

        return self.stream.listener.status_error_code

    def disconnect(self):
        """ Disconnect session
        :return:
        """

        self.stream.disconnect()

    def sentences(self):
        """ Get sentences
        :return:
        """

        return self.stream.listener.sentences


class TwitterApiReader:
    """
    Twitter api reader
    """

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token,
                 token_secret,
                 product,
                 environment,
                 query,
                 messages_per_request,
                 max_requests_limit=0,
                 msg_limit=0,
                 time_limit=0,
                 from_date=datetime.date.today().strftime('%Y%m%d%H%M%S'),
                 to_date=datetime.date.today().strftime('%Y%m%d%H%M%S'),
                 db_name="twitter_messages.temp.db"):

        self.auth = OAuth1(consumer_key, consumer_secret, access_token, token_secret)
        self.product = product
        self.environment = environment
        self.query = query
        self.messages_per_request = messages_per_request
        self.from_date = from_date
        self.to_date = to_date
        self.start_time = time.time()
        self.time_limit = time_limit
        self.msg_limit = msg_limit
        self.db_name = db_name
        self.messages = []
        self.max_requests_limit = max_requests_limit
        self.request_counter = 0
        self.start_time = time.time()
        self.reading = False
        self.url = "https://api.twitter.com/1.1/tweets/search/" + self.product + "/" + self.environment + '.json'
        self.params = {"query": self.query,
                       "maxResults": self.messages_per_request,
                       "fromDate": self.from_date,
                       "toDate": self.to_date}

    def read(self):
        """ Start reading messages on twitter
        :param url:
        :param params:
        :return:
        """

        try:
            logger.debug("Start reading...")
            self.reading = True

            if self.check_limits():

                self.request_counter += 1

                response = requests.post(auth=self.auth, url=self.url, json=self.params)
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

                    # Get next page of data,
                    if json_data['next']:

                        # Set next page hash to call
                        self.params['next'] = str(json_data['next'])
                        # Twitter sandbox rate limits: 30 RPM, 10RPS
                        time.sleep(2.2)
                        # Call next page of data
                        self.read()

                    self.reading = False

                else:
                    self.reading = False
                    if len(str(json_data['error']['message'])) > 10:
                        raise Exception("Twitter error => " + str(json_data['error']['message']))

                    else:
                        logger.debug("Connection error => " + response.status_code)
                        raise Exception("Connection error => " + str(response.status_code))

        except requests.exceptions.RequestException as e:
            self.reading = False
            logger.debug("Connection error")
            raise Exception("Connection error")

        except Exception as e:
            self.reading = False
            logger.debug(str(e))
            raise Exception(str(e))

    def messages(self):
        """ Return captured messages from twitter
        :return:
        """

        return self.messages

    def reading(self):
        """ Return reading status of the reader
        :return:
        """

        return self.reading

    def check_limits(self):
        """ Check limits parameters
        :return:
        """

        if self.time_limit > 0 and ((time.time() - self.start_time) > self.time_limit):
            logger.debug("Sorry, your time limit is over!")
            return False

        if self.msg_limit > 0 and (len(self.messages) > self.msg_limit):
            logger.debug("Sorry, your message limit is over!")
            return False

        if self.request_counter > 0 and self.request_counter >= self.max_requests_limit:
            logger.debug("Sorry, your request limit is over!")
            return False

        return True
