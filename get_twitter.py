import requests
import os
import json
import pdb
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from tqdm import tqdm
import sys

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TWITTER_START_DATE = datetime.strptime('2006-03-21T00:00:00.000Z', DATE_FORMAT)
SOME_DATE = datetime.strptime('2021-12-01T00:00:00.000Z', DATE_FORMAT)
TODAY_DATE = datetime.now()

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAERzUwEAAAAAt7fYxbA7j2P4n7R80nlo9GvnVUc%3DNFjB0C9tMJ1BjrhHr7AHj6p56d2Ux0EnKeS0a7pVJNdE55BfQY'

search_url = "https://api.twitter.com/2/tweets/search/all"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
def send_query(params):
    response = requests.request("GET", search_url, auth=bearer_oauth, params=params)
    if response.status_code != 200:
        print(response.status_code, response.text)
        if response.status_code == 429:
            print('Sleep for 15 mins')
            for i in tqdm(range(15*60)):
                time.sleep(1)
            return send_query(params)
        else:
            #pdb.set_trace()
            print('Unexpected case')
            raise Exception(response.status_code, response.text)
    time.sleep(1)
    return response.json()

def id_to_username(twitter_id):
    response = requests.request("GET", f'https://api.twitter.com/2/users/{twitter_id}', auth=bearer_oauth)
    time.sleep(1)
    return response.json()

def pull_tweets(keyword, filename):
    count = 0
    filename_base = filename.split('.')[0]
    os.makedirs(filename_base, exist_ok=True)
    start_time = SOME_DATE

    with open(filename, 'w', encoding='utf-8') as fout:
        tweets = []
        params ={ 'query': keyword, 'tweet.fields': 'id,text,author_id,created_at', 'max_results': 100, 'start_time': SOME_DATE.strftime(DATE_FORMAT), 'end_time': TODAY_DATE.strftime(DATE_FORMAT)}
        response = send_query(params)

        if response['meta']['result_count'] == 0:
            print('No tweet found')
            fout.write('No tweet found')
            return

        fout.write('id, author_id, created_at, text\n')

        tweets += response['data']
        page = 0
        with open(f'{filename_base}/{start_time.strftime("%Y_%m_%d")}_{page}.json', 'w') as f:
            json.dump(response, f)

        while 'next_token' in response['meta']:
            print('next_token', response['meta']['next_token'])
            params = {'query': keyword, 'tweet.fields': 'id,text,author_id,created_at', 'next_token': response['meta']['next_token'], 'max_results': 100, 'start_time': SOME_DATE.strftime(DATE_FORMAT), 'end_time': TODAY_DATE.strftime(DATE_FORMAT)}
            response = send_query(params)
            tweets += response['data']
            page += 1
            with open(f'{filename_base}/{start_time.strftime("%Y_%m_%d")}_{page}.json', 'w') as f:
                json.dump(response, f)

        tweets.reverse()
        count += len(tweets)

        for t in tweets:
            fout.write('{}, {}, {}, {}\n'.format(t['id'], t['author_id'], t['created_at'], t['text'].replace('\n', ' ')))
        fout.flush()

if __name__ == "__main__":
    keyswords = [
        'video.foxbusiness.com/v/6285838417001',
        'www.foxbusiness.com/technology/amazon-web-services-outage-impacts-thousands-of-users-online-services-what-to-know',
        'www.foxbusiness.com/media/internet-experts-warning-on-another-amazon-web-services-outage',
        'www.foxbusiness.com/technology/amazon-outage-disrupts-lives-surprising-people-cloud-dependency',
        'video.foxbusiness.com/v/6285830607001',
        'www.foxbusiness.com/lifestyle/amazon-rebuild-illinois-warehouse-tornado',
        'www.foxbusiness.com/lifestyle/midwestern-tornadoes-walmart-lowes-donate-supplies-help-recovery-efforts',
        'video.foxbusiness.com/v/6286489522001',
        'www.foxbusiness.com/politics/kentucky-ag-daniel-cameron-tornado-price-gouging-scams-hotline',
        'www.foxbusiness.com/economy/amazon-warehouse-collapse-6-fatalities-after-deadly-tornado-rips-through-area',
        'www.foxbusiness.com/economy/tornado-amazon-deaths-warehouse-statement',
        'www.foxbusiness.com/economy/tornadoes-extreme-weather-3-billion-insured-damage-report',
        'video.foxbusiness.com/v/6286600650001',
        'www.foxbusiness.com/lifestyle/power-outages-kentucky-deadly-tornadoes',
        'video.foxbusiness.com/v/6286657045001/',
        'www.foxbusiness.com/business-leaders/kentucky-candle-factory-ceo-says-staff-working-during-deadly-tornado-still-missing'
    ]

    for idx, k in enumerate(keyswords):
        pull_tweets(k, f'search_{idx}.csv')

    #twitter_id = '17941960'
    #res = id_to_username(twitter_id)
    #print(res)
