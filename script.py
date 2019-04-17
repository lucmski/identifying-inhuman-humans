import pandas as pd
import tweepy
import json
import pprint
import time

data = pd.read_csv('./new_isis_tweets.csv')

# sagar's keys
# consumer_key = 'KlIvRIuDPRq6NQTdFPXpVh96v'
# consumer_secret = 'I92dpWQo89ULGCNmpGtwo01t5fVRvWyhPPJyXRTr3cN6KBwtCV'
# access_token = '866792900-KS0Y8s2nl4haGSyGax2E1PPAGoxejfCeSh18weU8'
# access_token_secret = 'SgtPu7DH7mCjbbXVETSSdGt07o8IBdkEJHI55sQKHdavT'
	


def create_csv():
	# kshitij's keys
	consumer_key = "yyeI5zSWvvLVGSol7hu0tJ9gE"
	consumer_secret = "3N4fjsuLTCV4tIXEMICf587lM6mC7i8kcF4Ju1FSnx6VdKKLaW"
	access_token = "187109182-3vx120Tp28CEDfKZXB3JaZd5SV04DIZkhuIPEWfG"
	access_token_secret = "OXA5aGEXXqibb1FKl31EyVdLVVBqZnDrzS22oLy6KzCuh"

	auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)


	names = data['Screen Name'].unique()
	with open('./gender_isis.csv', 'a') as f:
	    header = 'Screen Name' + ',' + 'User Name' + ',' + 'Text' + ',' + 'Description' + '\n'
	    f.write(header)
	    for name in names:
	        print('Name - ', name)
	        print('Writing to file...')
	        row = data[data['Screen Name'] == name].values
	        user_name = row[0][11]
	        text = row[0][19]
	        try:
	        	user = api.get_user(name)
	        	x = user._json
	        	description = x['description'].replace(',', ' ').replace('\n', ' ').replace('  ', ' ')
	        	to_write = str(name) + ',' + str(user_name) + ',' + str(text) + ',' + description + '\n'

	        	f.write(to_write)
        	except tweepy.TweepError as e:
        		if e.api_code == 50:
        			print('User Not Found')
        			continue
        		elif e.api_code == 88:
        			print('\n\t\tLimit Reached\n')
        			time.sleep(600)
        			status = api.rate_limit_status()
        			while status['resources']['users']['/users/show/:id']['remaining'] <= 10:
		        		print('Limit Reached')
		        		time.sleep(600)
		        		print('Again Checking...')
        	# except:
        	# 	print('User Not Found')
        	# 	continue

	        

create_csv()