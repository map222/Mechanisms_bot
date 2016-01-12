import tweepy
from Mechanisms_bot.twitter_api_key import *
import pickle
import pdb
import logging

def tweet_new_sentence( new_sentences, tweeted_sentences):
    '''
    Check if a "new" sentence has been tweeted. If not, tweet it
    
    Returns: an updated tweeted_sentences, containing tweeted sentence
    '''
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    twitter_api = tweepy.API(auth)
    
    pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/{}'
    
    for cur_sent in new_sentences:
        if cur_sent not in tweeted_sentences:
            #pdb.set_trace()
            twitter_api.update_status(cur_sent['mech_sent'][:115] + ' ' + pubmed_url.format(cur_sent['PMID']))
            tweeted_sentences.append(cur_sent)
            return tweeted_sentences