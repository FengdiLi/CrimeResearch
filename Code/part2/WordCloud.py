# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 13:45:21 2018

@author: lifen
"""
import tweepy
from tweepy import OAuthHandler
from nltk.tokenize import TweetTokenizer
import re
from nltk.corpus import stopwords
# Twitter API
consumer_key = 'tqXNKc7lbSSZ0n6Lc6PHql9tL'
consumer_secret = 'zKhWuZ9k3K32LTGmO6raj9NWJsX6yKHMzoqSt08XU1JcMQKM1r'
access_token = '701822223875706881-g68PHPO3RwG47KPsqUpXdaV2F17F6SB'
access_secret = 'PCWA33wkdO4JgP29eoREIw3LsN63xNxknkmkKRxSqBSGS'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth, wait_on_rate_limit = True)
tweets = api.search(q = 'Maryland+crime', count=100, result_type = 'recent', tweet_mode = 'extended')
#status = []
#time = []
#for tweet in tweets:
#    status.append(tweet.full_text)
#    time.append(tweet.created_at)
BagOfWords=[]
BagOfHashes=[]
for tweet in tweets:
    line = tweet.full_text
    tweetSplitter = TweetTokenizer(strip_handles=True, reduce_len=True)
    WordList=tweetSplitter.tokenize(line)
    regex1=re.compile('^#.+') #hashtag
    regex2=re.compile('[^\W\d]') #no non-word, no numbers
    regex3=re.compile('^http.*') #url
    regex4=re.compile('.+\..+') 
    for item in WordList:
        if(len(item)>2):
            if((re.match(regex1,item))):
                #print(item)
                newitem=item[1:] #remove the hash
                BagOfHashes.append(newitem)
            elif(re.match(regex2,item)):
                if (re.match(regex3,item) or re.match(regex4,item)):
                    pass
                else:
                    BagOfWords.append(item)
            else:
                pass
        else:
            pass
BigBag=BagOfWords+BagOfHashes
stop_words = set(stopwords.words('english')) 
rawWord = [w for w in BigBag if w.lower() not in stop_words]
IgnoreThese=["yr-old", "here's", "year-old", "thi", "let's"]
rawWord = [w for w in rawWord if w.lower() not in IgnoreThese]
text = ' '.join(rawWord)
    
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
##install wordcloud
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#%%
mask = np.array(Image.open("MD.png"))
# random_state=7
wordcloud = WordCloud(background_color="white", mask = mask, collocations=False, 
                      stopwords=STOPWORDS, max_font_size=65).generate_from_text(text)
image_colors = ImageColorGenerator(mask)
# Open a plot of the generated image.
plt.figure(figsize = (12,24))
image = wordcloud.recolor(color_func=image_colors)
plt.imshow(image, interpolation="bilinear")
plt.title('WordCloud - Python')
plt.axis("off")
plt.show()
plt.imsave('WordCloud.png', image)