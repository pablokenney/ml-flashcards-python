#!/usr/bin/env python

import requests
import tweepy
import re
import os

# create a file twitter_keys.py and add the tokens/keys below as variables
# in the file
from twitter_keys import consumer_key, consumer_secret

# Create the OAuthHandler
auth = tweepy.OAuthHandler(consumer_key=consumer_key,
                           consumer_secret=consumer_secret)
# Construct the API instance
api = tweepy.API(auth)

# query parameter excludes the intentional photo to dirty the data
params = {'q': '-"are%20-being%20-made"%20-"your%20-data%20-dirty"%20%23machinelearningflashcards-filter:retweets',
          'from': 'chrisalbon',
          'since': '2017-04-01', }

ml_flashcards_json = api.search(**params)

media_urls = []
titles = []
for i in range(len(ml_flashcards_json)):
    txt = ml_flashcards_json[i]
    json = txt._json
    title = re.sub("#\S*", "", str(json['text']))  # removes hashtag
    title = re.sub("https\S*", "", title)  # removes url
    title = str(title.strip())
    media_url = json['entities']['media'][0]['media_url']
    media_urls.append(media_url)
    titles.append(title)

# change directory to flashcards folder
current_dirctory = os.getcwd()
os.chdir(current_dirctory + "/flashcards")

# write images to the flashcards directory
for i in zip(media_urls, titles):
    img = requests.get(i[0])
    f = open(str(i[1]) + ".jpg", mode='wb')
    f.write(img.content)
    f.close()
