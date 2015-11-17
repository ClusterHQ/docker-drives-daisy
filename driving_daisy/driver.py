import re

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = "130103248-UAaiajZHOjhQmlnLUi43LiXjthcsjetoTtmFmxfM"
access_token_secret = "eLNcyuPlZtRP5I6B201wf0sIHWEyOQ4n6PnmVNEo8umTb"
consumer_key = "9Oritx18QCc6zU4sGGLjJS2oA"
consumer_secret = "lFhyRVuBFcn7zxcV9Xl8HSUqTS7yhYWMgvECU9n7qPQKGDFkxI"

tweet_pattern = re.compile(r"#daisy\s+(\w+)", re.I)

def get_command(tweet):
    """
    Return the first character of the command tweeted.
    """
    match = tweet_pattern.search(tweet)
    if match:
        return match.group(1)[0]
    return None


class StdOutListener(StreamListener):

    def on_data(self, data):
        command = get_command(data)
        if command not in ["f", "b", "l", "r"]:
            return
        # do something with this command
        print "Saw command %s" % (command,)

    def on_error(self, status):
        print status


def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['#daisy'])
