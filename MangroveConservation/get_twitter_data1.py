# Collecting Twitter historical data using TwitterAPI

import json_lines
import pandas as pd
import yaml
import json

# Script prints an update to the CLI every time it collected another X Tweets
PRINT_AFTER_X = 1000


def get_data(SEARCH_QUERY, DEV_ENVIRONMENT_LABEL, API_SCOPE, API_KEY, API_SECRET_KEY, TO_DATE, FROM_DATE, FILENAME):
    """ get twitter data through twitter API from full archive search sand box and return all twitters in JSONL file
    based on 
     search term, 
     the geographic location of interest
     the time period of interest.
     and personal twitter account information.

     Reference: https://github.com/geduldig/TwitterAPI/tree/master/TwitterAPI
     Reference: https://developer.twitter.com/en/docs/tweets/search/overview
    """

    config = dict(
        search_tweets_api=dict(
            account_type='premium',
            endpoint=f"https://api.twitter.com/1.1/tweets/search/{API_SCOPE}/{DEV_ENVIRONMENT_LABEL}.json",
            consumer_key=API_KEY,
            consumer_secret=API_SECRET_KEY
        )
    )

    with open('twitter_keys.yaml', 'w') as config_file:
        yaml.dump(config, config_file, default_flow_style=False)

    from searchtweets import load_credentials, gen_rule_payload, ResultStream

    premium_search_args = load_credentials("twitter_keys.yaml",
                                           yaml_key="search_tweets_api",
                                           env_overwrite=False)

    rule = gen_rule_payload(SEARCH_QUERY,
                            results_per_call=100,
                            from_date=FROM_DATE,
                            to_date=TO_DATE
                            )

    rs = ResultStream(rule_payload=rule,
                      max_results=100000,
                      **premium_search_args)

    with open(FILENAME, 'a', encoding='utf-8') as f:
        n = 0
        for tweet in rs.stream():
            n += 1
            if n % PRINT_AFTER_X == 0:
                print('{0}: {1}'.format(str(n), tweet['created_at']))
            json.dump(tweet, f)
            f.write('\n')
    print('done')


def load_jsonl(file):
    """explore the jsonl file and only pick up the indicators of interests from all twitter data, such as

    user related indicators: 
    ID:twitter ID
    username:twitter user name
    user_joined: the year when user created an twitter account
    user_bio: the description of user
    follower_count: the numbers of followers of the user

    tweets related indicators:
    text: the full text of what user has twitted related to search term
    place: where user send out the tweet.

   user network related indicators:
   retweeted_user: whether the tweet is retweeted from someone else's original tweet
   and information related to the retweeted user.
    reference: https://lucahammer.com/2019/11/05/creating-a-retweet-network-for-gephi-from-a-local-file-with-python/
    """
    tweets = []
    with open(file, 'rb') as f:
        for tweet in json_lines.reader(f, broken=True):
            reduced_tweet = {
                'created_at': tweet['created_at'],
                'id': tweet['id_str'],
                'username': tweet['user']['name'],
                'user_joined': tweet['user']['created_at'][-4:],
                'user_location': tweet['user']['location'],
                'user_bio': tweet['user']['description'],
                'follower_count': tweet['user']['followers_count']
            }

            if 'extended_tweet' in tweet:
                reduced_tweet['text'] = tweet['extended_tweet']['full_text']

            else:
                reduced_tweet['text'] = tweet['text']

            if tweet['place'] is not None:
                reduced_tweet['country_code'] = tweet['place']['country_code'],
                reduced_tweet['place'] = tweet['place']['full_name']
                reduced_tweet['coordinates']=tweet['place']['bounding_box']['coordinates']

            if 'retweeted_status' in tweet:
                reduced_tweet['retweeted_user'] = {
                    'user_id': tweet['retweeted_status']['user']['id_str'],
                    'username': tweet['retweeted_status']['user']['screen_name'],
                    'user_joined': tweet['retweeted_status']['user']['created_at'][-4:],
                    'user_location': tweet['retweeted_status']['user']['location'],
                    'user_bio': tweet['retweeted_status']['user']['description'],
                    'follower_count': tweet['retweeted_status']['user']['followers_count']
                }

            tweets.append(reduced_tweet)

    return (tweets)


def create_csv(tweets, filename):
    """
    turn the selected information from jsonl file into formated CSV file.
    every record is one row
    """
    results=pd.DataFrame.from_dict(tweets)
    results.to_csv(filename, index=False, header=True)
    return results
