#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy
import pandas as pd
import random
from random import randint
from time import sleep


# In[2]:


def authenticate_twitter(twitter_api_key
                        ,twitter_api_secret
                        ,twitter_access_token
                        ,twitter_access_token_secret):
    auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_secret)
    auth.set_access_token(twitter_access_token,twitter_access_token_secret)
    # Create API object
    try:
        api = tweepy.API(auth)
        print("API Twitter connected!")
    except:
        print("Authentication failed. Perhaps wrong Keys and Tokens?")
    return api

def twitter_update_status(api,status):
    try:
        api.update_status(status)
    except:
        print("Update status failed. Perhaps API connection failed?")
def print_line(line_count):
    for x in range(line_count):
          print("\n")

def browser_show_tweet_by_id(id):
    print("https://twitter.com/anyuser/status/{}".format(id))

def search_tweet_to_dataframe(api,query,is_search_all=False):
    search_result = api.search(query)
    json_data = [r._json for r in search_result]
    df = pd.json_normalize(json_data)
    print("{} tweets are found.".format(df.shape[0]))
    return df

def like_tweet_in_df(df_search_result,commit_state=False,rand_sleep_seconds_min=1,rand_sleep_seconds_max=5):
    tweet_to_like = pd.DataFrame()
    try:
        liked_tweet = pd.read_csv('liked_tweet.csv',header=None).rename(columns={0:'id'})
        tweet_to_like = df_search_result[~df_search_result.id.isin(liked_tweet.id)][['id']]
    except:
        print("file_not_found. Search Result will be liked")

    if len(tweet_to_like)>0:
        for items in tweet_to_like.id:
            if commit_state:
                    try:
                        api.create_favorite(items)
                    except:
                        print("Failed favorite tweet id '{}'. Perhaps it's already favorited?".format(items))
            print("commit_state = {}. Liking tweet id {}".format(commit_state,items))
#             sleep(randint(rand_sleep_seconds_min,rand_sleep_seconds_max))
    else:
        for items in df_search_result.id:
            if commit_state:
                    try:
                        api.create_favorite(items)
                    except:
                        print("Failed favorite tweet id '{}'. Perhaps it's already favorited?".format(items))
            print("commit_state = {}. Liking tweet id {}".format(commit_state,items))
#             sleep(randint(rand_sleep_seconds_min,rand_sleep_seconds_max))

    print("Like done.")

# In[3]:


api = authenticate_twitter("OgH43uPp4wZFjNmm2QgIMB9P9"
                          ,"nfyeLiVBUN66WoD1dmqwBjExo6OepHdY2MzpUnHYCgec4q8oAO"
                          ,"1501572162548744192-K6ruRdHw89pbzlSZ9qo1lwndBBxqLK"
                          ,"e10TT2Vbtfpvqgyl15RWLdv0kgUiLN08LNZsSFBNlseDF")


# In[4]:


df_search_result = search_tweet_to_dataframe(api,"tebak tebakan -filter:mentions")
like_tweet_in_df(df_search_result,commit_state=True)


# In[ ]:




