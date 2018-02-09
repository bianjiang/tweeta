# -*- coding: utf-8 -*-

"""
tweeta.tweet
~~~~~~~~~~~~
This module contains functionality for extracting various data elements from a Tweet object 
"""

import json
import time

from . import __version__
from .exceptions import TweetaError
from .constants import PARSE_TIME_FORMAT, OUTPUT_TIME_FORMAT
from .text import fix_text, extract_mentions, extract_hashtags, lang, has_url

class TweetaTweet(object):
    def __init__(self, in_data):
        '''TweetaTweet class to extract tweet-related information

        :param json_str: (required) raw json string of the tweet
        '''

        if (not in_data):
            raise TweetaError("Missing input data")
        
        if (type(in_data) is dict):
            self._tweet = in_data
            self._json = json.dumps(self._tweet)
        elif (type(in_data) is str):
            self._json = in_data        
            self._tweet = json.loads(self._json)
        else:
            raise TweetaError("Wrong type of input data (only string or dict")
            
        ### The following variables are used often, so let's cache them
        #### The following only get assigned when it first accessed
        self._raw_text = None #self.__raw_text()
        self._fixed_text = None #self.__fixed_text()
        self._id = None
        self._user_id = None
    
    def __repr__(self):
        return '<TweetaTweet: %s>' % (self._tweet)
        
    def get(self, field_name):
        '''get arbitariry field values
        '''        
        if (field_name):
            if (field_name in self._tweet):
                return self._tweet[field_name]
            else:
                raise TweetaError("[%s] doesn't exist"%field_name)
    
    def tweet(self):
        '''return the raw tweet object
        '''
        return self._tweet
    
    def json(self):
        ''' Get the raw json
        '''
        return self._json
    
    def text(self):
        ''' Take full_text from extended tweet (default compatable mode for streaming api or 'full_text' in tweet, which replaces 'text' when use extended mode) https://developer.twitter.com/en/docs/tweets/tweet-updates
        '''
        if (not self._raw_text):
            self._raw_text = self._tweet['full_text'] if ('full_text' in self._tweet) else (self._tweet['extended_tweet']['full_text'] if ('extended_tweet' in self._tweet and self._tweet['extended_tweet'] and 'full_text' in self._tweet['extended_tweet']) else (self._tweet['text'] if 'text' in self._tweet else ''))            
        return self._raw_text               
    
    def fixed_text(self):
        ''' Fix some of the unicodes, and remove linebreaks [ftfy.fix_text(remove_lb(text)))]
        '''
        if (not self._fixed_text):
            self._fixed_text = fix_text(self.text())
        return self._fixed_text        
    
    def tweet_id(self):
        ''' Get tweet id (from 'id_str' first if avaliable) otherwise use 'id'
        '''
        if (not self._id):
            self._id = self._tweet['id_str'] if 'id_str' in self._tweet else (self._tweet['id'] if 'id' in self._tweet else '')
        return self._id
    
    def user_id(self):
        ''' Get user id (from tweet['user']['id_str'] first)
        '''
        if (not self._user_id):
            self._user_id = self._tweet['user']['id_str'] if ('user' in self._tweet and self._tweet['user'] and 'id_str' in self._tweet['user']) else (self._tweet['user']['id'] if ('user' in self._tweet and self._tweet['user'] and 'id' in self._tweet['user']) else '')            
        return self._user_id
        
    def created_at(self, output_time_format = 'YMD'):
        ''' Raw `created_at` are in constants.PARSE_TIME_FORMAT.  This converts the datetime to other formats, e.g., YMD (predefined) or %Y-%m-%d (user defined)   
        '''
        t = time.strptime(self.get('created_at'), PARSE_TIME_FORMAT)
        if (output_time_format in OUTPUT_TIME_FORMAT):
            return time.strftime(OUTPUT_TIME_FORMAT[output_time_format], t)
        else:
            return time.strftime(output_time_format, t)    
    
    def is_retweet(self):
        ''' Whether the tweet is a retweet (either start with ('RT|Rt|rT|rt @') or retweeted_status is not null )
            Note that there might be cases where a tweet is a retweet (starts with RT), but retweeted_status is not filled
            Note that only 'RT @' is a true retweet.  There are cases where tweets started with 'RT' but they are not retweets.
            e.g., "RT IF U NOT FRIENDLY.."
        '''
        return (self.text().lower().startswith('rt @') or (True if 'retweeted_status' in self._tweet and self._tweet['retweeted_status'] else False))
    
    def has_retweeted_status(self):
        ''' Whether the `retweeted_status` is not null
        '''
        return True if ('retweeted_status' in self._tweet and self._tweet['retweeted_status']) else False
    
    def is_quote(self):
        ''' Whether the tweet is a quote of another tweet (`quoted_status` is not null
        '''
        return True if ('quoted_status' in self._tweet and self._tweet['quoted_status']) else False
    
    def has_quoted_status(self):
        ''' Whether the `quoted_status` is not null
            Note that `quote` is different from retweet, is_quote == has_quoted_status
        '''
        return True if ('quoted_status' in self._tweet and self._tweet['quoted_status']) else False 
           
    def _mentions_from_text(self):
        ''' Extract mentions from text using re
        '''
        return extract_mentions(self.text())
        
    def _mentions_from_entities(self):
        ''' Extract mentions from `entities`
        '''
        if ('entities' in self._tweet and self._tweet['entities']):
            if ('user_mentions' in self._tweet['entities'] and self._tweet['entities']['user_mentions']):
                return ['@%s'%m['screen_name'] for m in self._tweet['entities']['user_mentions']]
        
        return []
    
    def mentions(self):
        '''  Use mentiones from `entities` first otherwise use text
        
        '''
        m = self._mentions_from_entities()        
        return m if m else self._mentions_from_text()
    
    def _hashtags_from_text(self):
        ''' Extract hashtags from text using re
        '''
        return extract_hashtags(self.text())
    
    def _hashtags_from_entities(self):
        ''' Extract hashtags from `entities`
        '''
        if ('entities' in self._tweet and self._tweet['entities']):
            if ('hashtags' in self._tweet['entities'] and self._tweet['entities']['hashtags']):
                return ['#%s'%m['text'] for m in self._tweet['entities']['hashtags']]
        
        return []
    
    def hashtags(self):
        '''  Use mentiones from `entities` first otherwise use text
        
        '''
        m = self._hashtags_from_entities()        
        return m if m else self._hashtags_from_text()
    
    def is_en(self):
        ''' Wether the tweet is written in English
            Use the `lang` attribute first if it exists, otherwise use langid
        '''
        if ('lang' in self._tweet and self._tweet['lang'].startswith('en')):
            return True
        elif ('lang' not in self._tweet):            
            return (lang(self.text()) == 'en')
        else:
            return False
            
    def is_user_en(self):
        ''' Whether the user is English speaking
        '''
        return (self._tweet['user']['lang'].startswith('en') if ('user' in self._tweet and self._tweet['user'] and 'lang' in self._tweet['user'] and self._tweet['user']['lang']) else False)
    
    def is_geotagged(self):
        ''' Whether the tweet has been geo-tagged (either has `geo` or `coordinates` or `place`) 
        '''
        return True if (('place' in self._tweet and self._tweet['place']) or ('geo' in self._tweet and self._tweet['geo']) or ('coordinates' in self._tweet and self._tweet['coordinates'])) else False 
        
        
    def is_deleted(self):
        ''' Whether th tweet has been deleted.  If the tweet is deleted, none of the other attributes will be populated
        '''
        return True if ('delete' in self._tweet) else False
    
    def user_location(self):
        ''' Get user location, return empty string if it doesn't exist
        '''
        return self._tweet['user']['location'] if ('user' in self._tweet and self._tweet['user'] and 'location' in self._tweet['user'] and self._tweet['user']['location']) else ''
    
    def user_name(self):
        ''' Get user name, return empty string if it doesn't exist
        '''
        return self._tweet['user']['name'] if ('user' in self._tweet and self._tweet['user'] and 'name' in self._tweet['user'] and self._tweet['user']['name']) else ''
    
    def user_screen_name(self):
        ''' Get user screen name, return empty string if it doesn't exist
        '''
        return self._tweet['user']['screen_name'] if ('user' in self._tweet and self._tweet['user'] and 'screen_name' in self._tweet['user'] and self._tweet['user']['screen_name']) else ''
    
    def user_description(self):
        ''' Get user description, return empty string if it doesn't exist
        '''
        return self._tweet['user']['description'] if ('user' in self._tweet and self._tweet['user'] and 'description' in self._tweet['user'] and self._tweet['user']['description']) else ''
    
    def has_url(self):
        ''' Whether the tweet contains urls (check entities first)
        '''
        if ('entities' in self._tweet and 'urls' in self._tweet['entities'] and self._tweet['entities']['urls'] and len(self._tweet['entities']['urls']) > 0):
            return True
        else:
            return has_url(self.text())
    
    def is_valid(self):
        ''' Whether the tweet contains all the root elements
            ('text' in tweet and 'id' in tweet and 'created_at' in tweet and 'user' in tweet)
        '''
        return (('text' in self._tweet or 'full_text' in self._tweet) and 'id' in self._tweet and 'created_at' in self._tweet and 'user' in self._tweet)
        