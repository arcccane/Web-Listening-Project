#!/usr/bin/env python
# coding: utf-8

# <h1>Data Preprocessing</h1>
# 
# <p>Convert raw dataset into a clean dataset for analysis</p>

# In[1]:


import pandas as pd
import matplotlib
import re
import nltk

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from dateutil.parser import parse
pd.options.mode.chained_assignment = None
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

def data_preprocessing():

    # In[2]:


    df = pd.read_csv('result.csv').dropna()
    df


    # In[3]:


    # df.groupby('platform').size().plot(kind='pie',  autopct='%1.2f%%', title='Platforms')


    # <h2>Tokenization</h2>

    # In[4]:


    df['token_words'] = df['body'].str.split()
    df


    # <h2>Normalize date and clean text</h2>

    # In[5]:


    df['date'] = list(map(lambda x: parse(str(x)).strftime("%d-%m-%Y %H:%M:%S"), df['date']))


    # In[6]:


    def clean(body):
        processed = []
        try:
            for i in body:
                i = re.sub(r"(@\[A-Za-z]+)|([^A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", i)
                i = i.lower()
                processed.append(i)
            clean_words = processed[:]
            sw_file = open("stopwords.txt", "r", encoding='utf-8')
            sw = sw_file.read().split('\n')
            sw.append('')
            for word in processed:
                if word in sw:
                    clean_words.remove(word)
            return clean_words
        except:
            return []


    df['token_words'] = df['token_words'].apply(clean)
    df


    # In[7]:


    # words = df['token_words'].sum()
    # print('Total number of words: ', len(words))


    # In[8]:


    # def word_frequency(series_sum):
    #     freq = nltk.FreqDist(series_sum)
    #     i = 0
    #     total = 0
    #     top = []
    #
    #     for key, val in freq.most_common():
    #         print(f'{key}: {val}')
    #         total += 1
    #         if i < 5:
    #             top.append(str(key))
    #             i += 1
    #     return total

    # f = word_frequency(words)


    # In[9]:


    # print('Total number of unique strings: ', f)


    # <h2>Lemmatizing</h2>
    #
    # <p>The process of converting a word to its base form.</p>

    # In[10]:


    # Part of Speech tagging: Adding a tag with a particular word defining its type (verb, noun, adjective etc)
    def pos_tagger(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None

    lemmatizer = WordNetLemmatizer()

    words = []
    pos_tag = []
    for i in df['token_words']:
        pos_tagged = nltk.pos_tag(i)
        wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))
        appendlist = []
        for word,tag in wordnet_tagged:
            if tag is None:
                words.append(lemmatizer.lemmatize(word))
                appendlist.append(lemmatizer.lemmatize(word))
            else:
                words.append(lemmatizer.lemmatize(word,tag))
                appendlist.append(lemmatizer.lemmatize(word))
        pos_tag.append(appendlist)


    # In[11]:


    df['lemmatized'] = pos_tag
    df


    # In[12]:


    # lemmatized_sum = df['lemmatized'].sum()
    # f = word_frequency(lemmatized_sum)


    # In[13]:


    # print('Total number of unique strings: ', f)


    # In[14]:


    df['clean_body'] = list(map(lambda x: ' '.join(x), list(df['lemmatized'])))
    df


    # <h2>Labelling each row to their respective keyword(s) according to their text</h2>

    # In[15]:


    keywords = df['about'].value_counts()[:2].index.tolist()
    keywords


    # In[16]:


    def keyword(text):
        text = text.lower()
        if all([word in text for word in keywords]):
            return ' and '.join(keywords)
        elif keywords[0] in text:
            return keywords[0]
        elif keywords[1] in text:
            return keywords[1]
        else:
            return 'nil'

    # Check if 'clean_body' contains any of the two keywords and label accordingly
    df['label'] = df['clean_body'].apply(keyword)
    df


    # In[17]:


    # Using 'about' column instead if 'clean_body' contains none of the keywords
    df.loc[df['label'] == 'nil', 'label'] = df['about'].apply(keyword)
    df


    # In[18]:


    # df.groupby('label').size().plot(kind='pie',  autopct='%1.2f%%', title='Labelled')


    # In[19]:


    df.drop('about', axis=1, inplace=True)

    # Remove nil
    df = df[df['label'] != 'nil']
    df


    # <h2>Removing the two keywords from 'clean_body' since it doesn't provide insight</h2>

    # In[20]:


    keywords


    # In[21]:


    def remove_keywords(text):
        text = text.replace(keywords[0], '')
        text = text.replace(keywords[1], '')
        return text.strip()

    df['clean_body'] = df['clean_body'].apply(remove_keywords)
    df


    # In[22]:


    # clean_body_sum = df['clean_body'].str.split().sum()
    # f = word_frequency(clean_body_sum)


    # In[23]:


    # print('Total number of unique strings: ', f)


    # In[24]:


    df = df[df['clean_body'] != '']
    df


    # In[25]:


    df.to_csv('result_clean.csv', index=False)

