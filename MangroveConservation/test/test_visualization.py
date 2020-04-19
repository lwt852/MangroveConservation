from MangroveConservation import visualization as visual
from MangroveConservation import clean_text1 as clean
import geopandas
import os
import pytest


def test_clip_polygon():
    #test if function returns geopandas dataframe for spatial visualization
    path = os.getcwd()
    tweets = clean.import_tweet(path +r'\MangroveConservation\test\test_tweet.csv')
    data,basemap = visual.clip_polygon(tweets)
    assert type(data) == geopandas.geodataframe.GeoDataFrame