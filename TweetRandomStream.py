import requests
import random
import twitter
import os

# TWITCH API ENV VARS
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
TWITCH_TOKEN = os.environ.get('TWITCH_TOKEN')

# TWITTER API ENV VARS
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
TWITTER_API_TOKEN = os.environ.get('TWITTER_API_TOKEN')
TWITTER_API_TOKEN_SECRET = os.environ.get('TWITTER_API_TOKEN_SECRET')

CHANNELS_PER_PAGE = 100
MAX_PAGE_CHANNEL = 10


def get_streams(after=""):
    url = "https://api.twitch.tv/helix/streams?language=en&first={}".format(CHANNELS_PER_PAGE)
    if (after != ""):
        url += "&after={}".format(after)
    headers = { "Authorization": "Bearer {}".format(TWITCH_TOKEN), "Content-Type": "application/json", "Client-Id": CLIENT_ID }
    res = requests.get(url, headers=headers)
    return res

def send_tweet(tweet):
    api = twitter.Api(consumer_key=TWITTER_API_KEY, consumer_secret=TWITTER_API_SECRET, access_token_key=TWITTER_API_TOKEN, access_token_secret=TWITTER_API_TOKEN_SECRET)
    api.PostUpdate(tweet)
    print("Tweet sent.")

def format_tweet(username, title):
    tweet = "🔴 LIVE NOW \n\n {title}\n\n twitch.tv/{username}".format(
        title=title, username=username)
    return tweet

def get_random_stream():
    random_page = random.randint(0, MAX_PAGE_CHANNEL)
    cursor = ""
    data = {}
    for i in range(random_page):
        response = get_streams(cursor)
        if (response.status_code != 200):
            print(response.json())
            print("Received non 200 response")
            break
        json = response.json()
        data = json['data']
        cursor = json['pagination']['cursor']


    random_streamer_on_page = random.randint(0, CHANNELS_PER_PAGE)
    if (len(data) == 0):
        return None
    stream = data[random_streamer_on_page]
    return stream

stream = get_random_stream()
if stream is not None:
    tweet = format_tweet(stream["user_name"], stream["title"])
    send_tweet(tweet)
else:
    print("Couldn't get a stream")

