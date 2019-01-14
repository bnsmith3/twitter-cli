# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 13:51:37 2019
@author: bnsmith3
"""

import pandas as pd
import pickle
from itertools import chain
from collections import Counter
from functools import partial

def _clean_source(source):
    first_end = source.find('>')+1
    second_start = source[first_end:].find('<')+first_end
    return source[first_end:second_start]

def get_tweet_info(tweet):
    return {'tweet_time': tweet['created_at'], \
            'id': tweet['id'], \
            'in_reply_to': tweet['in_reply_to_status_id'], \
            'lang': tweet['lang'], \
            'tweet': tweet['full_text'].strip(), \
            'unique_hashtags': '|'.join(set([a['text'].lower() for a in tweet['entities']['hashtags']])), \
            'favorite_count': tweet['favorite_count'], \
            'retweet_count': tweet['retweet_count'], \
            'possibly_sensitive': tweet['possibly_sensitive'] if ('possibly_sensitive' in tweet) else 'N/A', \
            'geo': tweet['geo'], \
            'coordinates': tweet['coordinates'], \
            'user_id': tweet['user']['id'], \
            'user_location': tweet['user']['location'], \
            'username': tweet['user']['name'], \
            'screenname': tweet['user']['screen_name'], \
            'user_description': tweet['user']['description'], \
            'verified': tweet['user']['verified'], \
            'user_timezone': tweet['user']['time_zone'], \
            'user_utc_offset': tweet['user']['utc_offset'], \
            'user_lang': tweet['user']['lang'], \
            'user_creation_time': tweet['user']['created_at'], \
            'source': _clean_source(tweet['source']), \
            'engagement': int(tweet['favorite_count']) + int(tweet['retweet_count'])}

def flatten_pickle(pickle_file, outfile=None):
    tweets = pickle.load(open(pickle_file, 'rb'))
    dframe = pd.DataFrame(list(map(get_tweet_info, tweets)))
    if outfile:
        dframe.to_csv(outfile, index=False, encoding='utf-8', sep='\t')
    return dframe

def flatten_list(items, delim='|'):
    return list(chain.from_iterable(map(lambda x: x.split(delim), [a for a in items if (pd.notnull(a) and (len(a) > 0))])))

def _get_screennames(user, dframe, delim='|'):
    user_id, count = user
    return delim.join(set(dframe[dframe['user_id'] == user_id]['screenname'])), user_id, count

def get_summaries(dframe, num_items=50):
    """Return the number of tweets, users, the dates covered, a list of the top 
    hashtags, top users, and the tweet with the highest engagement."""
    num_tweets = len(dframe)
    num_users = len(set(dframe['user_id']))
    dates = Counter(list(map(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d'), \
                             dframe['tweet_time'])))
    top_hashtags = Counter(flatten_list(dframe['unique_hashtags'])).most_common(num_items)
    top_users = list(map(partial(_get_screennames, dframe=dframe), Counter(dframe['user_id']).most_common(num_items)))
    top_tweet = dframe.loc[dframe['engagement'].idxmax()]
    
    return num_tweets, num_users, dates, top_hashtags, top_users, top_tweet
    
def tuples_to_file(filename, tuples, headers, delim='|', sep='\t'):
    with open(filename, 'w', encoding='utf-8') as w:
        w.write('{}\n'.format(sep.join(headers.split(delim))))
        for entry in tuples:
            w.write('{}\n'.format(sep.join(map(str, entry))))
        
