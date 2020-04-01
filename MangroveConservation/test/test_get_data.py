
import pytest
import numpy as np 
import get_twitter_data1 as get_data



def test_load_jsonl():
    #test if runction returns numpy arrary for good good input file
    data = get_data.load_jonsnl("test_tweet.jsonl")
    assert type(data) ==np.ndarray