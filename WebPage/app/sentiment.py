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

	name_sent_pos = {}
	name_count_pos = {}
	name_sent_neg = {}
	name_count_neg = {}

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


	for key in sentiment_pos.keys():
		name_count_pos[key] = sentiment_pos[key][1]
		name_sent_pos[key] = sentiment_pos[key][0]

	for key in sentiment_neg.keys():
		name_count_neg[key] = sentiment_neg[key][1]
		name_sent_neg[key] = sentiment_neg[key][0]


	return name_sent_pos, name_count_pos, name_sent_neg, name_count_neg


name_sent_pos, name_count_pos, name_sent_neg, name_count_neg = get_sentiment_analysis(data)

name_sent_pos_sort = sorted(name_sent_pos.items(), key = operator.itemgetter(1), reverse = True)
name_count_pos_sort = sorted(name_count_pos.items(), key = operator.itemgetter(1), reverse = True)
name_sent_neg_sort = sorted(name_sent_neg.items(), key = operator.itemgetter(1))
name_count_neg_sort = sorted(name_count_neg.items(), key = operator.itemgetter(1))

with open('name_sent_pos.pkl', 'wb') as f:
	pkl.dump(name_sent_pos_sort, f)

with open('name_count_pos.pkl', 'wb') as f:
	pkl.dump(name_count_pos_sort, f)

with open('name_sent_neg.pkl', 'wb') as f:
	pkl.dump(name_sent_neg_sort, f)

with open('name_count_neg.pkl', 'wb') as f:
	pkl.dump(name_count_neg_sort, f)