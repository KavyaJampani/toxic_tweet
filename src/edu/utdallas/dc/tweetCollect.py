from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

# access tokens for twitter
access_token = "981309028490981376-YoTeZT7xidSEg1euxFbIzYshY16sVpI"
access_token_secret = "BK9P4xUY3zPgVZw6wpQxJkmjsmH4NsM8wJ2rEVOkH5Mv3"
consumer_key = "fg4pBbU44JUMRnDRbjtOmKCRR"
consumer_secret = "iN3k4V7MuA7M12rwZOvmyAfJudd4qm4mnt68kSTJuOSkfP0K7X"


def keywords():
    fp = open("../../../../resources/keywords.txt", "r")
    words = [w.strip() for w in fp.readlines() if w.strip() is not None and len(w.strip()) > 0]
    return words


"""
This is a basic listener that just prints received tweets to stdout.
"""


class StdOutListener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        with open("../../../../resources/raw-tweets.json", 'a') as tf:
            tf.write('\n')
            # Write the json data directly to the file
            json.dump(all_data, tf)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # This handles Twitter authentication and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data
    stream.filter(languages=["en"], track=keywords())
