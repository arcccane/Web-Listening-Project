#!/usr/bin/env python
# coding: utf-8

# <h1>Sentiment Analysis</h1>
# 
# <p>Sentiment analysis is the practice of using algorithms to classify various samples of related text into overall positive and negative categories.</p>
# 
# <p>Using Natural Language Toolkit's (NLTK) Sentiment Intensity Analyzer, we are able to determine the ratio of positive to negative engagements about a specific topic.</p>

# In[1]:


import pandas as pd
import matplotlib
import warnings
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon', quiet=True)
warnings.filterwarnings("ignore",category=DeprecationWarning)

def sentiment_analysis():

    # In[2]:


    df = pd.read_csv('result_clean.csv')
    df


    # In[3]:


    sid = SentimentIntensityAnalyzer()

    df['scores'] = df['clean_body'].apply(lambda text: sid.polarity_scores(str(text)))
    df


    # In[4]:


    df['compound'] = df['scores'].apply(lambda score_dict: score_dict['compound'])
    df['sentiment_type'] = ''
    df.loc[df.compound > 0, 'sentiment_type'] = 'POSITIVE'
    df.loc[df.compound == 0, 'sentiment_type'] = 'NEUTRAL'
    df.loc[df.compound < 0, 'sentiment_type'] = 'NEGATIVE'
    df


    # In[5]:


    # df[df['sentiment_type'] == 'POSITIVE'].sample(n = 5)


    # In[6]:


    # df[df['sentiment_type'] == 'NEGATIVE'].sample(n = 5)


    # In[7]:


    # df[df['sentiment_type'] == 'NEUTRAL'].sample(n = 5)


    # In[8]:


    # keywords = df['label'].value_counts()[:2].index.tolist()
    # keywords


    # In[9]:


    # s = f'Overall Sentiment ({keywords[0]} OR {keywords[1]})'
    # print(s)
    # print('POSTIVE: ' + str((df['sentiment_type'] =='POSITIVE').sum()))
    # print('NEGATIVE: ' + str((df['sentiment_type'] =='NEGATIVE').sum()))
    # print('NEUTRAL: ' + str((df['sentiment_type'] =='NEUTRAL').sum()))


    # In[10]:


    # df.groupby('sentiment_type').size().plot(kind='pie',  autopct='%1.2f%%', title=s)


    # In[11]:


    # df1 = df[df['label'] == keywords[0]]
    #
    # s1 = f'Sentiment for {keywords[0]}'
    # print(s1)
    # print('POSTIVE: ' + str((df1['sentiment_type'] =='POSITIVE').sum()))
    # print('NEGATIVE: ' + str((df1['sentiment_type'] =='NEGATIVE').sum()))
    # print('NEUTRAL: ' + str((df1['sentiment_type'] =='NEUTRAL').sum()))


    # In[12]:


    # print('No of rows: ', df1.shape[0])


    # In[13]:


    # df1.groupby('sentiment_type').size().plot(kind='pie',  autopct='%1.2f%%', title=s1)


    # In[14]:


    # df2 = df[df['label'] == keywords[1]]
    #
    # s2 = f'Sentiment for {keywords[1]}'
    # print(s2)
    # print('POSTIVE: ' + str((df2['sentiment_type'] =='POSITIVE').sum()))
    # print('NEGATIVE: ' + str((df2['sentiment_type'] =='NEGATIVE').sum()))
    # print('NEUTRAL: ' + str((df2['sentiment_type'] =='NEUTRAL').sum()))


    # In[15]:


    # print('No of rows: ', df2.shape[0])


    # In[16]:


    # df2.groupby('sentiment_type').size().plot(kind='pie',  autopct='%1.2f%%', title=s2)


    # In[17]:


    # df3 = df[(df['label'] == f'{keywords[0]} and {keywords[1]}') | (df['label'] == f'{keywords[1]} and {keywords[0]}')]
    #
    # s3 = f'Sentiment for {keywords[0]} AND {keywords[1]}'
    # print(s3)
    # print('POSTIVE: ' + str((df3['sentiment_type'] =='POSITIVE').sum()))
    # print('NEGATIVE: ' + str((df3['sentiment_type'] =='NEGATIVE').sum()))
    # print('NEUTRAL: ' + str((df3['sentiment_type'] =='NEUTRAL').sum()))


    # In[18]:


    # print('No of rows: ', df3.shape[0])


    # In[19]:


    # df3.groupby('sentiment_type').size().plot(kind='pie',  autopct='%1.2f%%', title=s3)


    # In[20]:


    # df_time = df.groupby(['date','sentiment_type']).size()
    # df_time = df_time.to_frame().reset_index()
    # df_time = df_time.rename(columns={"index": "date", 0:"values"})
    #
    # df_time['date'] = pd.to_datetime(df_time['date'])
    # df_time = df_time.set_index('date')
    # df_mavg = df_time.groupby([pd.Grouper(freq='M'), 'sentiment_type'])['values'].sum()
    #
    # df_mavg = df_mavg.to_frame()
    # df_mavg = df_mavg.reset_index()
    # df_mavg.set_index('date', inplace=True)
    # df_mavg.groupby('sentiment_type')['values'].plot(figsize=(15,5), legend=True, title=s)


    # In[21]:


    # df_time = df1.groupby(['date','sentiment_type']).size()
    # df_time = df_time.to_frame().reset_index()
    # df_time = df_time.rename(columns={"index": "date", 0:"values"})
    #
    # df_time['date'] = pd.to_datetime(df_time['date'])
    # df_time = df_time.set_index('date')
    # df_mavg = df_time.groupby([pd.Grouper(freq='M'), 'sentiment_type'])['values'].sum()
    #
    # df_mavg = df_mavg.to_frame()
    # df_mavg = df_mavg.reset_index()
    # df_mavg.set_index('date', inplace=True)
    # df_mavg.groupby('sentiment_type')['values'].plot(figsize=(15,5), legend=True, title=s1)


    # In[22]:


    # df_time = df2.groupby(['date','sentiment_type']).size()
    # df_time = df_time.to_frame().reset_index()
    # df_time = df_time.rename(columns={"index": "date", 0:"values"})
    #
    # df_time['date'] = pd.to_datetime(df_time['date'])
    # df_time = df_time.set_index('date')
    # df_mavg = df_time.groupby([pd.Grouper(freq='M'), 'sentiment_type'])['values'].sum()
    #
    # df_mavg = df_mavg.to_frame()
    # df_mavg = df_mavg.reset_index()
    # df_mavg.set_index('date', inplace=True)
    # df_mavg.groupby('sentiment_type')['values'].plot(figsize=(15,5), legend=True, title=s2)


    # In[23]:


    # df_time = df3.groupby(['date','sentiment_type']).size()
    # df_time = df_time.to_frame().reset_index()
    # df_time = df_time.rename(columns={"index": "date", 0:"values"})
    #
    # df_time['date'] = pd.to_datetime(df_time['date'])
    # df_time = df_time.set_index('date')
    # df_mavg = df_time.groupby([pd.Grouper(freq='M'), 'sentiment_type'])['values'].sum()
    #
    # df_mavg = df_mavg.to_frame()
    # df_mavg = df_mavg.reset_index()
    # df_mavg.set_index('date', inplace=True)
    # df_mavg.groupby('sentiment_type')['values'].plot(figsize=(15,5), legend=True, title=s3)


    # In[24]:


    df.to_csv('result_sentiment.csv', index=False)

