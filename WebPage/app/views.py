import pandas as pd
import pickle as pkl
import operator
import os
import re
from textblob import TextBlob
from flask import render_template
from app import app
from flask import url_for, redirect, request, make_response


def get_lang_analysis(data):
	lang_list = data['Language'].unique()
	lang_dict = {'others': 0}
	for lang in lang_list:
		numbers = len(data[data['Language'] == lang])
		if numbers > 100:
			lang_dict[lang] = numbers
		else:
			lang_dict['others'] = lang_dict['others'] + numbers
	return lang_dict


def get_day_analysis(data):
	data['Day'] = data['DateTime'].str.split(' ').str[0]
	day_list = data['Day'].unique()
	day_dict = {}
	for day in day_list:
		day_dict[day] = len(data[data['Day'] == day])
	return day_dict


def get_device_analysis(data):
	devices_used = data[data['Device'] != 'None']
	device_list = devices_used['Device'].unique()
	device_dict = {}

	for device in device_list:
		device_dict[device] = len(devices_used[devices_used['Device'] == device])

	return device_dict


def get_country_analysis(data):
	loc_data = data[data['Location'] != 'None']
	loc_list = loc_data['Location'].unique()
	loc_dict = {}
	final_dict = {'Others': 0}

	for loc in loc_list:
		loc_dict[loc] = len(loc_data[loc_data['Location'] == loc])

	loc_dict_sorted = sorted(loc_dict.items(), key = operator.itemgetter(1), reverse = True)
	
	for key in loc_dict_sorted:
		if key[1] < 300:
			final_dict['Others'] = final_dict['Others'] + key[1]
		else:
			final_dict[key[0]] = key[1]

	return final_dict


def get_sentiment_analysis():

	sent_pos = {}
	sent_neg = {}

	with open('./app/static/sentiment_pos.pkl', 'rb') as f:
		sentiment_pos = pkl.load(f)

	with open('./app/static/sentiment_neg.pkl', 'rb') as f:
		sentiment_neg = pkl.load(f)

	for i in range(10):
		sent_pos[sentiment_pos[i][0]] = [sentiment_pos[i][1][0], sentiment_pos[i][1][1]]
		sent_neg[sentiment_neg[i][0]] = [sentiment_neg[i][1][0], sentiment_neg[i][1][1]]

	return sent_pos, sent_neg


def get_user_activity(data):
	user_activity = {}
	most_active = {}
	least_active = {}
	for name in data['Screen Name']:
		if name not in user_activity.keys():
			user_activity[name] = 1
		else:
			user_activity[name] += 1
	i = 0
	for key, val in sorted(user_activity.items(), key = operator.itemgetter(1)):
		least_active[key] = val
		i += 1
		if i > 15:
			break
	i = 0
	for key, val in sorted(user_activity.items(), key = operator.itemgetter(1), reverse = True):
		most_active[key] = val
		i += 1
		if i > 15:
			break

	return most_active, least_active



@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
	k = 0
	data = pd.read_csv('./app/static/new_isis_tweets.csv')
	# age_data = pd.read_csv('./app/static/')
	data_rows = {}
	data_cols = {}
	for i in data.keys():
		data_cols[k] = i
		k += 1
	k = 0
	for i in range(10):
		data_rows[k] = list(data.iloc[i, 0:20])
		k += 1

	lang_data = get_lang_analysis(data)

	day_dict = get_day_analysis(data)

	devices_dict = get_device_analysis(data)

	country_dict = get_country_analysis(data)
	
	# sentiment_dict_pos, sentiment_dict_neg = get_sentiment_analysis()
	most_active, least_active = get_user_activity(data)



	return render_template('home.html', cols=data_cols, rows=data_rows, lang=lang_data, day=day_dict, \
		device=devices_dict, country=country_dict, most=most_active, least=least_active)
