# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 12:00:23 2019
@author: bnsmith3
"""

from twarc import Twarc
import configparser
import argparse
import pickle


config = configparser.ConfigParser()
config.read('config.cfg')

def get_tweets(terms, or_terms=True):
    try:    
        ts = Twarc(
                consumer_key = config['twitter']['consumer_key'],
                consumer_secret = config['twitter']['consumer_secret'],
                access_token = config['twitter']['access_token'],
                access_token_secret = config['twitter']['access_token_secret']
            )

        if or_terms:
            search_string = ' OR '.join(terms)
        else:
            search_string = ' '.join(terms)
        all_tweets = list(ts.search(search_string))
    
    except Exception as e: # take care of all those ugly errors if there are some
        print(e)
        
    return all_tweets

def get_user_tweets(user_id=None, screen_name=None):
    try:    
        ts = Twarc(
                consumer_key = config['twitter']['consumer_key'],
                consumer_secret = config['twitter']['consumer_secret'],
                access_token = config['twitter']['access_token'],
                access_token_secret = config['twitter']['access_token_secret']
            )

        if user_id:
            all_tweets = list(ts.timeline(user_id=user_id))
        elif screen_name:
            all_tweets = list(ts.timeline(screen_name=screen_name))
        else:
            all_tweets = []
    
    except Exception as e: # take care of all those ugly errors if there are some
        print(e)
        
    return all_tweets

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=('Grab tweets via the Twitter API'))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--term', '-t', action='append',
                        help='A term to search for on Twitter. This flag can '
                        'be used multiple times.')
    group.add_argument('--terms_file', '-tf', action='store',
                        help='The file that holds the terms to be '
                        'searched. Each line holds one term.')
    group.add_argument('--screen_name', '-s', action='store',
                        help='The username of a user whose tweets to retrieve.')
    group.add_argument('--user_id', '-u', action='store',
                        help='The user ID of a user whose tweets to retrieve.')    
    parser.add_argument('--tweets_file', '-f', action='store', required=True,
                        help='The pickle file to which to write the list of retrieved tweets.')
    parser.add_argument('--or_terms', '-o', action='store_true',
                        help='Include this flag if multiple terms should be ORed.'
                        'The default is that the terms will be ANDed.')
    
    args = parser.parse_args()
    
    if args.term:
        tweets = get_tweets(args.term, args.or_terms)
    elif args.screen_name:
        tweets = get_user_tweets(screen_name=args.screen_name)
    elif args.user_id:
        tweets = get_user_tweets(user_id=args.user_id)
    else:
        with open(args.terms_file, 'r') as f:
            terms = list(map(lambda x: x.strip(), f.readlines()))
        tweets = get_tweets(terms, args.or_terms)    
    
    with open(args.tweets_file, 'wb') as w:
        pickle.dump(tweets, w)
        
    print('{:,} tweets were written to {}.'.format(len(tweets), args.tweets_file))
