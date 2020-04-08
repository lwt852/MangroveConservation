from MangroveConservation import clean_text1 as clean_txt
import pytest
import datetime

def test_ImportComment():
    data = clean_txt.ImportComment("test_tweet.csv", "text")
    assert len(data)== 1

def test_TextCleaner():
    data = clean_txt.TextCleaner("@MplsPedestrian yes, good!")
    assert data == "yes good"
    
def test_ImportTweet_time():
    data = clean_txt.ImportTweet("test_tweet.csv")
    assert data["time"].iloc[0].date()== datetime.date(2019, 12, 28)

    
def test_ImportTweet_tweet():
    data = clean_txt.ImportTweet("test_tweet.csv")
    assert data["tweet"].iloc[0]=="yes good"
    
