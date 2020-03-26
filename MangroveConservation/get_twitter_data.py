# Collecting Twitter historical data using TwitterAPI

from TwitterAPI import TwitterAPI, TwitterPager
import csv
def get_data(SEARCH_TERM,key,secret, access_token, access_token_secret,start_time,end_time,file_name):
    """ get twitter data through twitter API from full archive search sand box and return all twitters
    based on 
     search term, 
     the geographic location of interest
     the time period of interest.
     and personal twitter account information.
    
     Reference: https://github.com/geduldig/TwitterAPI/tree/master/TwitterAPI
     Reference: https://developer.twitter.com/en/docs/tweets/search/overview
    """

    api = TwitterAPI(key,
                 secret,
                 access_token,
                 access_token_secret)
    

    r = api.request('tweets/search/%s/:%s' % ("fullarchive", "mangroveConservation"),
                    {'query':SEARCH_TERM,
                     'max_results': 6000,
                     'fromDate':start_time, 
                     'toDate':end_time,
                     })

# write tweets into a csv file

    csvFile = open(file_name,'a')
    csvWriter = csv.writer(csvFile)
#    counter = 0
    for item in r:
        if 'extended_tweet' in item: # to avoid truncated tweets
            csvWriter.writerow([item['created_at'],item['user']['screen_name'], item['user']['location'], 
                            item['user']['followers_count'], item['user']['friends_count'], 
                            item['user']['verified'], item['coordinates'], item['retweet_count'], item['favorite_count'], 
                                item['extended_tweet']['full_text'].encode('utf-8') if 'full_text' in item['extended_tweet'] else item['extended_tweet'] ])
        else:
            csvWriter.writerow([item['created_at'],item['user']['screen_name'], item['user']['location'], 
                            item['user']['followers_count'], item['user']['friends_count'], 
                            item['user']['verified'], item['coordinates'], item['retweet_count'], 
                            item['favorite_count'], item['text'].encode('utf-8') if 'text' in item else item])
#        counter = counter + 1
#        if (counter == 100): # rate limit 100 responses per request
#            break

    csvFile.close()
    print("{} is successfully created.".format(file_name))
    return
