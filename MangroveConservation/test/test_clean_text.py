from MangroveConservation import clean_text1 as clean_txt
import pytest
import datetime
import numpy as np
import os
path = os.getcwd()
def test_import_comment():
    data = clean_txt.import_comment(path +r'\MangroveConservation\test\test_tweet.csv', 'text')
    assert len(data['text']) == 2

def test_text_cleaner():
    data = clean_txt.comment_cleaner("@MplsPedestrian yes, good!")
    assert data == "yes good"
    
def test_import_tweet_time():
    data = clean_txt.import_tweet(path + r'\MangroveConservation\test\test_tweet.csv')
    assert data["time"].iloc[0].date()== datetime.date(2019, 12, 11)

    
def test_import_tweet():
    data = clean_txt.import_tweet(path + r'\MangroveConservation\test\test_tweet.csv')
    assert data["lat"].iloc[1]==145.7169445
    
