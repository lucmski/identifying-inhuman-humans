import pandas as pd
from textblob import TextBlob
import pickle as pkl
import operator
import re

data = pd.read_csv('./static/new_isis_tweets.csv')

def get_sentiment_analysis(data):
	unique_ids = data['User Id'].unique()
	sentiment_pos = {}
	sentiment_neg = {}

	for i in unique_ids:
		try:
			su = 0
			count = 0
			tweet = data[data['User Id'] == i]['Full Tweet']
			for j in tweet:
				j = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", j).split())
				analysis = TextBlob(j)
				s, b = analysis.sentiment
				su += s
				count += 1
			su = float(su)/count

			name = data[data['User Id'] == i]['Screen Name'].unique()[0]
			tweet_count = data[data['User Id'] == i]['Tweet Count'].unique()[0]

			sentiment_neg[name] = [su, tweet_count]
		except:
			continue

	for key, value in sorted(sentiment_neg.items(), key = operator.itemgetter(1), reverse=True):
		sentiment_pos[key] = [value[0], value[1]]

	return sentiment_pos, sentiment_neg


sent_pos, sent_neg = get_sentiment_analysis(data)

sort_pos = sorted(sent_pos.items(), key = operator.itemgetter(1), reverse = True)
sort_neg = sorted(sent_neg.items(), key = operator.itemgetter(1))

with open('sentiment_pos.pkl', 'wb') as f:
	pkl.dump(sort_pos, f)

with open('sentiment_neg.pkl', 'wb') as f:
	pkl.dump(sort_neg, f)