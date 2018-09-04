import time
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener


# Custom listener
# Extend Tweetpy StreamListener


class SnetListener(StreamListener):

    def __init__(self, msg_limit=0, time_limit=0):
        print("SnetListener INIT")
        self.start_time = time.time()
        self.time_limit = time_limit
        self.msg_limit = msg_limit
        self.msg_counter = 0
        self.sentences = []
        self.status_error_code = None
        super(SnetListener, self).__init__()

    def on_data(self, data):

        try:
            print("SnetListener on_data")
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
                print(str(tweet))
                print(str(self.analizer.polarity_scores(tweet)))
                # item = (tweet, self.analizer.polarity_scores(tweet))
                self.sentences.append(tweet)

            # sentiment_value, confidence = s.sentiment(tweet)
            # print(tweet, sentiment_value, confidence)
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
        print("SnetListener on_error")
        self.status_error_code = status_code
        # if status_code > 400:
        # returning False in on_data disconnects the stream
        return False

    # Check search limits
    def check_limits(self):
        print("SnetListener check_limits")
        if self.time_limit > 0 and ((time.time() - self.start_time) > self.time_limit):
            print("SORRY, TIME LIMIT IS OVER !")
            return False
        if self.msg_limit > 0 and (self.msg_counter > self.msg_limit):
            print("SORRY, MSGS LIMIT IS OVER !")
            return False
        return True


# Stream Manager class
# Used for manage twitter connections based on it's limits


class SnetStreamManager:
    auth = ''
    stream = ''

    def __init__(self, consumer_key, consumer_secret, access_token, token_secret, msg_limit=0, time_limit=0):
        print("SnetStreamManager INIT")
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, token_secret)
        self.stream = Stream(self.auth, SnetListener(msg_limit=msg_limit, time_limit=time_limit))

    def filter(self, languages, keywords, async=False):
        print("SnetStreamManager filter")
        # print("")
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
        # print("MANAGER SENTENCES...")
        # if self.stream.listener.sentences is not None:
        #     print("sentences populated...")
        return self.stream.listener.sentences
