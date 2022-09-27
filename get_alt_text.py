import tweepy
import pandas as pd
from api_access import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import pymongo
import json

consumer_key = API_KEY

consumer_secret = API_SECRET
auth = tweepy.OAuthHandler(consumer_key, consumer_secret, )
access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


def get_ids(path, drop_rts):
    """
    Function designed to get the ids of the tweets to analyse.

    :param df: dataframe to be used in the extraction of ids
    :param drop_rts:Boolean. True if we want to drop RTs. False if not.
    :return: Returns a DataFrame containing the ids of the tweets.
    """

    #We select the columns of interest

    lynguo_tweets = pd.read_csv(path, sep=";", encoding="latin-1", error_bad_lines=False, decimal=",")
    lynguo_tweets = lynguo_tweets[["Usuario", "Texto", "Fecha", "Enlace", "Opinion", "Impacto", "Marca"]]

    #If we want to drop the rts select True:

    if drop_rts == True:
        lynguo_tweets = lynguo_tweets.loc[~lynguo_tweets["Texto"].str.contains("RT @")]

    else:
        pass

    #Drop the duplicates:

    lynguo_tweets = lynguo_tweets.drop_duplicates(subset=["Usuario", "Texto"], keep="first")
    list_links = list(lynguo_tweets["Enlace"])

    #Extraction of ids selecting the last element inside the column with the Link to the tweet:

    ids = []

    for i in list_links:
        a = i.split("/")[-1]
        ids.append(a)

    #Create a column for this ID and make it numeric, better for Tweepy:

    lynguo_tweets["id"] = ids
    lynguo_tweets["id"] = pd.to_numeric(lynguo_tweets["id"])

    return lynguo_tweets

def save_statuses_mongo (ids):
    db_connect = pymongo.MongoClient("gigas.clipit.es", 21000)

    db = db_connect["cstrack"]

    for id in ids:
        try:
            status_tweepy = api.get_status(id=id, include_ext_alt_text=True, tweet_mode="extended")
            db.statuses_extended.insert_one(status_tweepy._json)
            print("status inserted")
        except Exception as e:
            print(e)

    return print("Collection inserted")

no_rts = get_ids("C:/Users/ferno/Downloads/Lynguo_consulta_20-09-2022_09_00_20-09-2022_10_00.csv", drop_rts=True)

rts = get_ids("C:/Users/ferno/Downloads/Lynguo_consulta_20-09-2022_09_00_20-09-2022_10_00.csv", drop_rts=False)

#Usa rts? comprobar si se retweetean mas con alt o no. Si no se puede calcular con los stats del status (mas dificil

#contar los rts del CS comunity)

save_statuses_mongo(rts["id"])

#Esto son notas para mi David, pegale al script con los 10 Tokens para sacarlo "rapido".

# Comparisons of length of the elements in alt_text, also based in media type (photo ot gif):

#Upload a GIF to twitter and check the alternative text and how it is stored in media:

#Note: make it with pandas grouping and plot it using pandas, if not plotly.

#Check the discourse inside the alt text

#References:

#https://dl.acm.org/doi/pdf/10.1145/3308558.3313605
#https://www.microsoft.com/en-us/research/wp-content/uploads/2017/08/scalable_social_alttext.pdf


