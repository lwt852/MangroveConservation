# Collecting Twitter historical data using TwitterAPI
# Reference: https://github.com/geduldig/TwitterAPI/tree/master/TwitterAPI
# Reference: https://developer.twitter.com/en/docs/tweets/search/overview
search term = (mangrove ecosystems)OR(mangrove forests)OR(Mangrove Ecosystems)OR(Mangrove Forests)OR(Mangrove Ecosystems)OR(Mangrove Forests)
search_location = CH
start_time =20150101
end_time=20191231
from TwitterAPI import TwitterAPI, TwitterPager
import csv
def get_data(search_term,search_location,start_time,end_time):
    """this function is to get twitter data through twitter API from full archive search sand box and return all twitters
    based on certain search term, the geographic location of interest and the time period of interest.
    """

    api = TwitterAPI("eNpG2G70aY2KKujwtlWkvcJoS",
                 "fgk44fdHs9WpYEDtKm1w3UKpSLN2Md61cD0RNmlftrKmifykuB",
                 "2972155805-0NuM9ND8aZ0PA77G5kUBzHNFOefI4090JAxszws",
                 "E7idsdPtc6VlvIRNUrROx5pTvzTon38alLZ9PooHVVhBe")
    SEARCH_TERM = '-RT'+ search_term+  'lang:en' # sandbox does not support "has:geo"
    
    PRODUCT = 'fullarchive' 
    LABEL = 'search'
    r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL),
                    {'query':SEARCH_TERM,
                     'fromDate':start_time +'0000', 
                     'toDate':end_time+'0000',
                     })
    return r
# write tweets into a csv file
file_name = 'mangrove_twitters_'+search_location +start_time+end_time
def write_twitter(r, file_name):
    """this function is to store the twitters into 
        a file with only attributed of interest
    """

    csvFile = open(file_name,'a')
    csvWriter = csv.writer(csvFile)

    counter = 0
    for item in r:
        if 'extended_tweet' in item: # to avoid truncated tweets
            csvWriter.writerow([item['created_at'],item['user']['screen_name'], item['user']['location'], 
                            item['user']['followers_count'], item['user']['friends_count'], 
                            item['user']['verified'], item['coordinates'], item['retweet_count'], 
                            item['favorite_count'], item['extended_tweet']['full_text']])
        else:
            csvWriter.writerow([item['created_at'],item['user']['screen_name'], item['user']['location'], 
                            item['user']['followers_count'], item['user']['friends_count'], 
                            item['user']['verified'], item['coordinates'], item['retweet_count'], 
                            item['favorite_count'], item['text']])
        counter = counter + 1
        if (counter == 100): # rate limit 100 responses per request
        break

    csvFile.close()
