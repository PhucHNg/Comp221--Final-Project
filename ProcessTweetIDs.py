"""Retrieve tweets from tweets IDS using sample number 6 from the ICWSM Morstatter data.
These tweets were sampled from Twitter's Firehose data collected from Syria for
Dec. 18, 19, 24, 27, 29 in 2011"""

#Import
import tweepy
import random
import nltk
from tweepy import OAuthHandler
import traceback

#Initialization of API
consumer_key = '88oRCF3AvjHlJPVR7vTF1M3Nl'
consumer_secret = 'AKH7Cni82aLCbbZpg2vLNWCGfve4otKufXpzomH1hHSwjeqb68'
access_token = '4503314773-hwgeFvOe1tezDIq4hxkEmiIBLlW9uDlWAceoIZM'
access_secret = 'TNZghvuqDLILk7vdrips3xOoof788JPRE3bUhJckQdrqp'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


#Function definition
def processTweets(file_name, write_to_file):
    tweet_ids = [w.strip() for w in open(file_name)]

    tweet_file = open(write_to_file,'w')

    for i in range(367000, len(tweet_ids)):
        print(i)
        try:
            tweet = api.get_status(tweet_ids[i])
            try:
                tweet_file.write(tweet.text + '\n')
            except UnicodeEncodeError:
                print("encodeerror") #this eliminates foreign language tweets
        except tweepy.error.TweepError:
            print("tweeperror") #this eliminates deleted tweets

    tweet_file.close()


#Main Program
processTweets("all_streaming_api.txt","all_streaming_api_tweets4.0.txt")

## On average, out of ~20 000 tweets we only got about ~200 valid, English tweets. Is that reasonable?