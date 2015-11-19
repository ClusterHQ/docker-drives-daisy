import json
import re
import requests

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_token = "130103248-UAaiajZHOjhQmlnLUi43LiXjthcsjetoTtmFmxfM"
access_token_secret = "eLNcyuPlZtRP5I6B201wf0sIHWEyOQ4n6PnmVNEo8umTb"
consumer_key = "9Oritx18QCc6zU4sGGLjJS2oA"
consumer_secret = "lFhyRVuBFcn7zxcV9Xl8HSUqTS7yhYWMgvECU9n7qPQKGDFkxI"

tweet_pattern = re.compile(r"#daisy\s+(\w+)", re.I)

daisy_id = "00e04c02eff0"
daisy_access_token = \
    "4c88e0c345836cb4d7bcb6473f282206bb9a7a21e8fe8fb8339fa1b60e396595"
daisy_url = \
    'https://api-http.littlebitscloud.cc/v2/devices/' + daisy_id + '/output'

req_header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + daisy_access_token
}


def get_command(tweet):
    """
    Return the first character of the command tweeted.
    """
    match = tweet_pattern.search(tweet)
    if match:
        return match.group(1)[0]
    return None


def make_request_go():
    """
    Send a request to the Daisy cloudbit to run at 100% indefinitely.

    See: http://developer.littlebitscloud.cc/#-devices-device-id-output
    """
    body = {"percent": 100, "duration_ms": -1}
    r = requests.post(daisy_url, headers=req_header, data=json.dumps(body))

    # TODO: Check the response code
    print r


def make_request_stop():
    """
    Send a request to the Daisy cloudbit to run for 0ms.
    This will interrupt the "go" request.

    See: http://developer.littlebitscloud.cc/#-devices-device-id-output
    """
    body = {"percent": 100, "duration_ms": 1}
    r = requests.post(daisy_url, headers=req_header, data=json.dumps(body))

    # TODO: Check the response code
    print r


class StdOutListener(StreamListener):

    def on_data(self, data):
        command = get_command(data)
        if command not in ["g", "s"]:
            return
        if command == "g":
            make_request_go()
        elif command == "s":
            make_request_stop()
        print "Saw command %s" % (command,)

    def on_error(self, status):
        print status


def main():
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    stream.filter(track=['#daisy'])
