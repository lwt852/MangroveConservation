import re
from datetime import datetime, timezone
import pandas as pd
import numpy as np
"""
Created on Thu Feb 27 14:05:58 2020
@author: Mimi Gong
Partly Adopted from Meng Cai
A few functions for processing text data.
"""
def import_comment(file, text_column):
    """
    Load a csv file with survey comments, 
    remove rows with empty text or illegible words or N/A answer.
    Input: 
    file -- the name of a csv file; 
    text_column -- the name of the target text column.
    Output: 
    a Pandas dataframe.
    """
    raw = pd.read_csv(file, encoding="ISO-8859-1")
    temp = raw[~raw[text_column].isnull()] # remove the rows where texts are missing
    temp = temp[temp[text_column].str.contains("illegible|Illegible|N/A|NA|(no comment)") == False]
    return temp
def comment_cleaner(dirty_text):
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
        semi_clean_text = " ".join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", dirty_text).split())
        clean_text = " ".join(re.sub(r"\d+", "", semi_clean_text).split()) # remove numbers
        return clean_text
def find_centroid(row):
    '''
    Helper function to return the centroid of a polygonal 
    bounding box of longitude, latitude coordinates
    Reference: https://github.com/shawn-terryah/Twitter_Geolocation
    '''
    try:
        row_ = eval(row)
        lst_of_coords = [item for sublist in row_ for item in sublist]
        longitude = [p[0] for p in lst_of_coords]
        latitude = [p[1] for p in lst_of_coords]
        return (sum(latitude) / float(len(latitude)), sum(longitude) / float(len(longitude)))
    except:
        return None
def import_tweet(file):
    """
    Load a csv file with tweets, drop all columns except time, location, and tweet content.
    Input: 
    file -- the name of a csv file. 
    Output: 
    a Pandas dataframe with clean time (in UTC), location (latitude and longitude), and text.
    """
    raw = pd.read_csv(file, header=0)
    raw.columns = ['created_at', 'id', 'username', 'user_joined', 'user_location',
                   'user_bio', 'follower_count', 'text', 'country_code', 'place','coordinates']
    #set the centroid of the bounding box of coordinates
    raw['centroid'] = list(map(lambda row: find_centroid(row), raw['coordinates']))
    # convert time format to UTC
    time = []
    for i in raw["created_at"]:
        time.append(datetime.strptime(str(i), '%a %b %d %H:%M:%S %z %Y').
                    replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%Y-%m-%d %H:%M:%S'))
    raw.insert(0, "time", time)
    raw["time"] = pd.to_datetime(raw["time"], utc=True)
    raw2 = raw.drop(columns="created_at")
    # clean text
    cleantweet = []
    for i in raw2["text"]:
        cleantweet.append(comment_cleaner(str(i)))
    raw2.insert(3, "tweet", cleantweet)
    raw3 = raw2.drop(columns="text")
    # clean user_bio
    cleantweet1 = []
    for i in raw3["user_bio"]:
        cleantweet1.append(comment_cleaner(str(i)))
    raw3.insert(3, "user_description", cleantweet1)
    raw4 = raw3.drop(columns="user_bio")
    # clean username
    cleantweet2 = []
    for i in raw4["username"]:
        cleantweet2.append(comment_cleaner(str(i)))
    raw4.insert(3, "name", cleantweet2)
    raw5 = raw4.drop(columns="username")
    #clean coordinates
    long = []
    lat = []
    for i in range(len(raw5)):
        num = re.findall(r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",str(raw5["centroid"].iloc[i]))
        if len(num) == 0:
            long.append(np.NaN)
            lat.append(np.NaN)
        else:
            long.append(float(num[0]))
            lat.append(float(num[1]))
    raw5.insert(2, "long", long)
    raw5.insert(2, "lat", lat)
#    raw6 = raw5.drop(columns="coordinates")
    result = raw5.drop(columns="centroid")
    return result
