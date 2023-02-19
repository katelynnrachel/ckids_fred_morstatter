import requests
import os
import json
import pdb
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from tqdm import tqdm
import sys
import pandas as pd
import csv

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
TWITTER_START_DATE = datetime.strptime('2006-03-21T00:00:00.000Z', DATE_FORMAT)
# ACD_DATE = datetime.strptime('2023-01-21T00:00:00.000Z', DATE_FORMAT)
# # TODAY_DATE = datetime.now()
# STT_DATE = ACD_DATE - timedelta(2)
# END_DATE = ACD_DATE + timedelta(14)
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAERzUwEAAAAAt7fYxbA7j2P4n7R80nlo9GvnVUc%3DNFjB0C9tMJ1BjrhHr7AHj6p56d2Ux0EnKeS0a7pVJNdE55BfQY'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

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

def pull_tweets(keyword, acd_time, filename):
    count = 0
    filename_base = filename.split('.')[0]
    os.makedirs(filename_base, exist_ok=True)
    acd_time = datetime.strptime(acd_time, DATE_FORMAT)
    # acd_time = acd_time.replace(year=2023)
    stt_time = acd_time - timedelta(2)
    end_time = acd_time + timedelta(14)

    with open(filename, 'w', encoding='utf-8') as fout:
        tweets = []
        params ={ 'query': keyword, 'tweet.fields': 'id,text,author_id,created_at', 'max_results': 100, 'start_time': stt_time.strftime(DATE_FORMAT), 'end_time': end_time.strftime(DATE_FORMAT)}
        response = send_query(params)

        if response['meta']['result_count'] == 0:
            print('No tweet found')
            fout.write('No tweet found')
            return

        fout.write('id, author_id, created_at, text\n')

        tweets += response['data']
        page = 0
        with open(f'{filename_base}/{acd_time.strftime("%Y_%m_%d")}_{page}.json', 'w') as f:
            json.dump(response, f)

        while 'next_token' in response['meta']:
            print('next_token', response['meta']['next_token'])
            params = {'query': keyword, 'tweet.fields': 'id,text,author_id,created_at', 'next_token': response['meta']['next_token'], 'max_results': 100, 'start_time': stt_time.strftime(DATE_FORMAT), 'end_time': end_time.strftime(DATE_FORMAT)}
            response = send_query(params)
            tweets += response['data']
            page += 1
            with open(f'{filename_base}/{acd_time.strftime("%Y_%m_%d")}_{page}.json', 'w') as f:
                json.dump(response, f)

        tweets.reverse()
        count += len(tweets)

        for t in tweets:
            fout.write('{}, {}, {}, {}\n'.format(t['id'], t['author_id'], t['created_at'], t['text'].replace('\n', ' ')))
        fout.flush()

if __name__ == "__main__":
    # d = pd.read_csv('deathdates_formatted.csv')
    # # format the date to DATE_FORMAT
    # month_map = {
    #     "Jan": "01",
    #     "Feb": "02",
    #     "Mar": "03",
    #     "Apr": "04",
    #     "May": "05",
    #     "Jun": "06",
    #     "Jul": "07",
    #     "Aug": "08",
    #     "Sep": "09",
    #     "Oct": "10",
    #     "Nov": "11",
    #     "Dec": "12",
    # }
    #
    # with open("deathdates-v3.csv", "r") as f:
    #     reader = csv.reader(f)
    #     header = next(reader)
    #     death_dates = []
    #     for row in reader:
    #         date_parts = row[0].split(".")
    #         death_date = f"{row[1]}-{month_map[date_parts[0]]}-{int(date_parts[1]):02d}T00:00:00.000Z"
    #         death_dates.append([death_date, row[2]])
    # with open("deathdates_formatted-v3.csv", "w") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["Death Date", "Victim Name"])
    #     writer.writerows(death_dates)

    d2 = pd.read_csv('deathdates_formatted-v3.csv')
    for i in range(4789, d2.shape[0]):
        pull_tweets(d2.iloc[i,1], d2.iloc[i,0], f'search_{d2.iloc[i,1]}.csv')

    #twitter_id = '17941960'
    #res = id_to_username(twitter_id)
    #print(res)
