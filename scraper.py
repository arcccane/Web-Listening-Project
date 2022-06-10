import os
import time
import pandas as pd
from time import sleep
from codetiming import Timer
from loguru import logger
from twitter import twitter as twt
from reddit import reddit as rd
from facebook import facebook as fb
from hwz import hwz1, hwz2
from analysis_in_use import Data_Preprocessing, Sentiment_Analysis_Vader, Topic_Modelling_sklearnLDA

"""Integration of all web scraping and analysis codes"""

@Timer(text="Total time taken: {minutes:.2f}m", logger=logger.info)
def run_all(keywords):
    if len(keywords) == 2:
        start = time.perf_counter()
        print('Starting web scrape\n')
        run_twitter(keywords)
        run_reddit(keywords)
        run_facebook(keywords)
        run_hwz(keywords)
        combine_csv()
        print('Starting analysis\n')
        run_analysis()
        print('Launching Power BI ...\n')
        sleep(1)
        os.startfile('Dashboard.pbix')
        stop = time.perf_counter()
        print(f"Total time taken: {(stop - start)/60:0.2f} minutes")
        raise SystemExit(0)
    else:
        print('Invalid input')

@Timer(text="Total downloading time for Twitter: {minutes:.2f}m", logger=logger.info)
def run_twitter(li):
    start = time.perf_counter()
    twt.fetch_data(li, 'twitter/dataset', "2021-12-31", 7500)
    stop = time.perf_counter()
    print(f"Total downloading time for Twitter: {(stop - start)/60:0.2f} minutes\n")

@Timer(text="Total downloading time for Reddit: {minutes:.2f}m", logger=logger.info)
def run_reddit(li):
    start = time.perf_counter()
    rd.fetch_data(li, 'reddit/dataset', "2021-12-31", 7500)
    stop = time.perf_counter()
    print(f"Total downloading time for Reddit: {(stop - start)/60:0.2f} minutes\n")

@Timer(text="Total downloading time for Facebook: {minutes:.2f}m", logger=logger.info)
def run_facebook(li):
    start = time.perf_counter()
    fb.async_fetch(li, 'facebook/dataset')
    stop = time.perf_counter()
    print(f"Total downloading time for Facebook: {(stop - start)/60:0.2f} minutes")

@Timer(text="Total downloading time for HardwareZone: {minutes:.2f}m", logger=logger.info)
def run_hwz(li):
    start = time.perf_counter()
    hwz1.fetch_urls(li, 'hwz/urls')
    hwz2.fetch_data()
    stop = time.perf_counter()
    print(f"Total downloading time for HardwareZone: {(stop - start)/60:0.2f} minutes\n")

@Timer(text="Total execution time for analysis: {minutes:.2f}m", logger=logger.info)
def run_analysis():
    start = time.perf_counter()
    print("Preprocessing data ...")
    Data_Preprocessing.data_preprocessing()
    print("Analyzing Sentiment ...")
    Sentiment_Analysis_Vader.sentiment_analysis()
    print("Discovering Topics ...")
    Topic_Modelling_sklearnLDA.topic_modelling()
    stop = time.perf_counter()
    print(f"Total execution time for analysis: {(stop - start)/60:0.2f} minutes\n")

def combine_csv():
    try:
        twitter = pd.read_csv(f'twitter/dataset/{os.listdir("twitter/dataset")[0]}',
                              usecols=['platform', 'about', 'date', 'content']
                              ).rename(columns={'content': 'body'})
    except FileNotFoundError or ValueError:
        twitter = pd.DataFrame(list())
    try:
        reddit = pd.read_csv(f'reddit/dataset/{os.listdir("reddit/dataset")[0]}',
                             usecols=['platform', 'about', 'created', 'body']
                             ).rename(columns={'created': 'date'})
    except FileNotFoundError or ValueError:
        reddit = pd.DataFrame(list())
    try:
        facebook = pd.read_csv(f'facebook/dataset/{os.listdir("facebook/dataset")[0]}',
                               usecols=['platform', 'about', 'comment_time', 'comment_text']
                               ).rename(columns={'comment_time': 'date', 'comment_text': 'body'})
    except FileNotFoundError or ValueError:
        facebook = pd.DataFrame(list())
    try:
        hwz = pd.read_csv(f'hwz/dataset/{os.listdir("hwz/dataset")[0]}',
                          usecols=['platform', 'forum_title', 'date', 'body']
                          ).rename(columns={'forum_title': 'about'})
    except FileNotFoundError or ValueError:
        hwz = pd.DataFrame(list())

    frames = [twitter, reddit, facebook, hwz]
    result = pd.concat(frames)
    result.to_csv(f'result.csv', index=False)
    return result
