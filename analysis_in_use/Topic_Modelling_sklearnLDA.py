#!/usr/bin/env python
# coding: utf-8

# <h1>Topic Modelling (sklearn LDA)</h1>
# <p>Topic Modeling is an unsupervised learning approach to clustering documents, to discover topics based on their contents.</p>

# In[1]:


import pandas as pd
import numpy as np
import matplotlib
import openpyxl
import pyLDAvis
import pyLDAvis.sklearn
import warnings

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
warnings.filterwarnings("ignore",category=DeprecationWarning)
warnings.filterwarnings("ignore",category=FutureWarning)
warnings.filterwarnings("ignore",category=UserWarning)

def topic_modelling():

    # In[2]:


    df = pd.read_csv('result_sentiment.csv')
    df[['platform','clean_body','label']]


    # In[3]:


    # no_of_words = df['clean_body'].apply(lambda x: len(str(x).split(' ')))
    # avg = round(no_of_words.sum()/len(no_of_words), 2)
    # print("Average no of words for each row: ", avg)


    # <h2>CountVectorizer</h2>
    # <p>To turn the text into a matrix, where each row in the matrix encodes which words appeared in each individual text. We will also filter the words max_df=0.9 means we discard any words that appear in >90% of the data. We will also filter words using min_df = 25, so words that appear in less than 25 rows will be discarded. We discard high appearing words since they are too common to be meaningful in topics. We discard low appearing words because we won’t have a strong enough signal and they will just introduce noise to our model.</p>
    #
    # <p>Using this matrix the topic modelling algorithms will form topics from the words. Each of the algorithms does this in a different way, but the basics are that the algorithms look at the co-occurrence of words in the text and if words often appearing in the same text together, then these words are likely to form a topic together. The algorithm will form topics which group commonly co-occurring words. A topic in this sense, is just list of words that often appear together and also scores associated with each of these words in the topic. The higher the score of a word in a topic, the higher that word’s importance in the topic. Each topic will have a score for every word found in the text, in order to make sense of the topics we usually only look at the top words - the words with low scores are irrelevant.</p>

    # In[4]:


    # vectorizer object used to transform text to vector form
    vectorizer = CountVectorizer(max_df=0.9, min_df=25, analyzer='word')

    # apply transformation
    tf = vectorizer.fit_transform(df['clean_body'].astype('U')).toarray()

    # tf_feature_names tells us what word each column in the matrix represents
    tf_feature_names = vectorizer.get_feature_names_out()
    tf_feature_names


    # In[5]:


    # len(tf_feature_names)


    # <h2>LDA</h2>

    # In[6]:


    lda_model = LDA(n_components=10, random_state=0)
    lda_model.fit(tf)
    topic_results = lda_model.transform(tf)


    # In[7]:


    # def display_topics(model, feature_names, no_top_words):
    #     topic_dict = {}
    #     cols = 0
    #     for topic_idx, topic in enumerate(model.components_):
    #         if cols < 5:
    #             topic_dict["Topic words %d" % (topic_idx + 1)] = ['{}'.format(feature_names[i])
    #                             for i in topic.argsort()[:-no_top_words - 1:-1]]
    #             topic_dict["Topic weights %d" % (topic_idx + 1)] = ['{:.1f}'.format(topic[i])
    #                             for i in topic.argsort()[:-no_top_words - 1:-1]]
    #             cols += 1
    #     return pd.DataFrame(topic_dict)


    no_top_words = 10
    # display_topics(lda_model, tf_feature_names, no_top_words)


    # In[8]:


    # pyLDAvis.enable_notebook()
    # tf = np.matrix(tf)
    # vis = pyLDAvis.sklearn.prepare(lda_model, tf, vectorizer)
    # vis


    # In[9]:


    df['topic_no'] = topic_results.argmax(axis=1)
    df[['platform','date','body','clean_body','label','topic_no']]


    # In[10]:


    def map_topics(model, feature_names):
        topic_dict = {}
        for topic_idx, topic in enumerate(model.components_):
            topic_dict[topic_idx] = ['{}'.format(feature_names[i])
                            for i in topic.argsort()[:-no_top_words - 1:-1]]
        return topic_dict

    topics_map = map_topics(lda_model, tf_feature_names)
    df['topic_words'] = df['topic_no'].map(topics_map)
    df[['platform','date','body','clean_body','label','topic_no','topic_words']]


    # In[11]:


    # df.groupby('topic_no').size().plot(kind='bar', title='Topics distribution')


    # In[12]:


    df.to_excel('result_topics.xlsx', index=False)

