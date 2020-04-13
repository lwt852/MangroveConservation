from MangroveConservation import clean_text1 as clean_txt
import pytest
import datetime
import numpy as np

def test_ImportComment():
    data = clean_txt.ImportComment("/home/gongmimi/CMSE802/MangroveConservation/MangroveConservation/test/test_tweet.csv", "text")
    assert type(data) == np.ndarray

def test_TextCleaner():
    data = clean_txt.CommentCleaner("@MplsPedestrian yes, good!")
    assert data == "yes good"
    
def test_ImportTweet_time():
    data = clean_txt.ImportTweet("/home/gongmimi/CMSE802/MangroveConservation/MangroveConservation/test/test_tweet.csv")
    assert data["time"].iloc[0].date()== datetime.date(2019, 12, 28)

    
def test_ImportTweet_tweet():
    data = clean_txt.ImportTweet("/home/gongmimi/CMSE802/MangroveConservation/MangroveConservation/test/test_tweet.csv")
    assert data["tweet"].iloc[0]==""
    
