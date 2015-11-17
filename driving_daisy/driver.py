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



#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
