# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:05:58 2020

@author: Mimi Gong
Adopted from Meng Cai
"""
"""A few functions for processing text data."""




import pandas as pd
import numpy as np
import re
from datetime import datetime, timezone
def ImportComment(file, text_column):
    """
    Load a csv file with survey comments, remove rows with empty text or illegible words or N/A answer.

    Input: 
    file -- the name of a csv file; 
    text_column -- the name of the target text column.
    Output: 
    a Pandas dataframe.
    """
    raw = pd.read_csv(file, encoding="ISO-8859-1")
    # remove the rows where texts are missing
    df = raw[~raw[text_column].isnull()]
    # remove the rows containing illegible words or N/A
    df = df[df[text_column].str.contains("illegible|Illegible|N/A") == False]
    return df


def CommentCleaner(dirty_text):
    """
    Remove blank lines and special characters from text data collected from surveys.

    Input:
    dirty_text -- raw text data. 
    Output:
    clean text data
    """
    if dirty_text is not None:
        text = dirty_text.replace("(<br>)", "")  # remove blank line
        text = text.replace('(<a).*(>).*(</a>)', "")  # remove <a> tag
        text = text.replace('(&amp)', "")  # remove "&"
        text = text.replace('(&gt)', '')  # remove ">"
        text = text.replace('(&lt)', '')  # remove "<"
        text = text.replace('nan', '')  # remove NA
#        text = text.replace('mangrove forest','')  # remove the search term
        # remove non-breaking space in ISO 8859-1
        clean_text = text.replace('(\xa0)', "")
    return clean_text


def TweetCleaner(dirty_text):
    """
    Remove links and special characters from a tweet.

    Input:
    dirty_text -- a raw tweet.
    Output:
    a clean tweet.
    """
    clean_text = " ".join(re.sub(
        "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", dirty_text).split())
    return clean_text


def ImportTweet(file):
    """
    Load a csv file with tweets, drop all columns except time, location, and tweet content.

    Input: 
    file -- the name of a csv file. 
    Output: 
    a Pandas dataframe with clean time (in UTC), location (latitude and longitude), and text.
    """
    raw = pd.read_csv(file, header=None)
    raw.columns = ['created_at', 'follower_count', 'id', 'text',
                   'user_bio', 'user_joined', 'user_location', 'username']
    # convert time format to UTC
    time = []
    for i in raw["created_at"]:
        time.append(datetime.strptime(i, '%a %b %d %H:%M:%S %z %Y').replace(
            tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
    raw.insert(0, "time", time)
    raw["time"] = pd.to_datetime(raw["time"], utc=True)
    raw2 = raw.drop(columns="created_at")

    # clean text
    cleantweet = []
    for i in raw2["text"]:
        temp = CommentCleaner(i)
        cleantweet.append(TweetCleaner(temp))
    raw2.insert(3, "tweet", cleantweet)
    raw3 = raw2.drop(columns="text")

    # clean user_bio
    cleantweet1 = []
    for i in raw3["user_bio"]:
        i = CommentCleaner(str(i))
        cleantweet1.append(TweetCleaner(i))
    raw3.insert(3, "user_description", cleantweet1)
    raw4 = raw3.drop(columns="user_bio")

    # clean username
    cleantweet2 = []
    for i in raw4["username"]:
        i = CommentCleaner(str(i))
        cleantweet2.append(TweetCleaner(i))
    raw4.insert(3, "name", cleantweet2)
    df = raw4.drop(columns="username")
    return df
