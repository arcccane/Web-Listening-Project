import os
import time
import pandas as pd
from datetime import datetime
from psaw import PushshiftAPI

def to_datetime(generator):
    for data in generator:
        data['created'] = datetime.utcfromtimestamp(int(data['created_utc'])).strftime('%d/%m/%Y %I:%M:%S %p')

def to_epoch(dt):
    return int(time.mktime(time.strptime(dt,'%Y-%m-%d')))

def fetch_data(keywords_list, filepath, before, limit):

    file = ' '.join(keywords_list)
    limit_each = int(limit/2)
    df1 = []
    df2 = []
    count = 0

    try:
        for f in os.listdir(filepath):
            os.remove(os.path.join(filepath, f))

        for keyword in keywords_list:
            count += 1
            print(f'Fetching data from reddit keyword: {keyword} ...')
            api = PushshiftAPI(shards_down_behavior=None)
            comments = api.search_comments(q=keyword, limit=limit_each, before=to_epoch(before))
            comment_list = [comment.d_ for comment in comments]
            to_datetime(comment_list)
            if count == 1:
                df1 = pd.DataFrame(comment_list, columns=['subreddit','created','id','body','score'])
                df1['platform'] = 'Reddit'
                df1['about'] = keyword
            else:
                df2 = pd.DataFrame(comment_list, columns=['subreddit','created','id','body','score'])
                df2['platform'] = 'Reddit'
                df2['about'] = keyword
        frames = [df1,df2]
        result = pd.concat(frames)
        result.to_csv(f'{filepath}/{file}.csv', index=False)
    except IOError:
        print("File issue")
