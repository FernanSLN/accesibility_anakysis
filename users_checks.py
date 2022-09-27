import tweepy
from api_access import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
consumer_key = API_KEY

consumer_secret = API_SECRET
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, )
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

user = "cstrackproject"

id_cstrack = api.get_user(screen_name=user)

print(api.get_favorites(id=id_cstrack.id))

