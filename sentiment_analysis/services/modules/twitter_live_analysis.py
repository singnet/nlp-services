import time
import json

from nltk.sentiment import SentimentIntensityAnalyzer
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Twitter Credentials
# consumer key, consumer secret, access token, access secret.
consumer_key = "TscHeuS3vQN7bY82vNhE419ka"
consumer_secret = "5rCTzeRgwT0rTx56KCIQm0OUvgCmQ2WF9BLBC8NdkpmDpNYVoH"
access_token = "91892303-CUT4ZuJTqAxX2Ra2Bj7g1Hw0WmRPRtaiCPW2qm8CD"
token_secret = "SK7TVAL4QC9O93rhiyv1W4vLJUP0tUMWnjLbO7GkQ0IvE"


class SnetListener(StreamListener):

    def __init__(self, msg_limit=0, time_limit=0):
        self.analizer = SentimentIntensityAnalyzer()
        self.start_time = time.time()
        self.time_limit = time_limit
        self.msg_limit = msg_limit
        self.msg_counter = 0
        self.sentences = []
        super(SnetListener, self).__init__()

    def on_data(self, data):

        try:
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
                item = (tweet, self.analizer.polarity_scores(tweet))
                self.sentences.append(item)

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
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False

    # Check search limits
    def check_limits(self):
        if self.time_limit > 0 and ((time.time() - self.start_time) > self.time_limit):
            print("SORRY, TIME LIMIT IS OVER !")
            return False
        if self.msg_limit > 0 and (self.msg_counter > self.msg_limit):
            print("SORRY, MSGS LIMIT IS OVER !")
            return False
        return True


class StreamManager:

    auth = ''
    stream = ''

    def __init__(self, consumer_key, consumer_secret, access_token, token_secret, msg_limit=0, time_limit=0):
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, token_secret)
        self.stream = Stream(self.auth, SnetListener(msg_limit=msg_limit, time_limit=time_limit))

    def filter(self, languages, keywords, async=False):
        self.stream.filter(languages=languages, track=keywords, async=async)
        self.stream.disconnect()

    def disconnect(self):
        self.stream.disconnect()

    def sentences(self):
        return self.stream.listener.sentences


manager = StreamManager(consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        access_token=access_token,
                        token_secret=token_secret,
                        msg_limit=1,
                        time_limit=0)

manager.filter(languages=["en"], keywords=["happy", "Trump", "USA"])
print("TOTAL OF SENTENCES: " + str(len(manager.sentences())))
