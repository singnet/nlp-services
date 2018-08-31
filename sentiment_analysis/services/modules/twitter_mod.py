from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from services.modules import complex_mod

# consumer key, consumer secret, access token, access secret.
ckey = "TscHeuS3vQN7bY82vNhE419ka"
csecret = "5rCTzeRgwT0rTx56KCIQm0OUvgCmQ2WF9BLBC8NdkpmDpNYVoH"
atoken = "91892303-CUT4ZuJTqAxX2Ra2Bj7g1Hw0WmRPRtaiCPW2qm8CD"
asecret = "SK7TVAL4QC9O93rhiyv1W4vLJUP0tUMWnjLbO7GkQ0IvE"


class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]
        sentiment_value, confidence = complex_mod.sentiment(tweet)
        print(tweet, sentiment_value, confidence)

        if confidence * 100 >= 80:
            output = open("output/twitter-out.txt", "a")
            output.write(sentiment_value)
            output.write('\n')
            output.close()

        return True

    def on_error(self, status_code):
        print("ERROR")
        print(status_code)
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False


def analyze(languages, sentences):

    print('MOD => Language')
    print(languages)
    print('MOD => Sentences')
    print(sentences)

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    twitterStream = Stream(auth, Listener())
    twitterStream.filter(languages=languages, track=sentences)
