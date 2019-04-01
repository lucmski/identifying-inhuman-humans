import pandas as pd
import os
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


@app.route('/index')
@app.route('/home')
@app.route('/')
def index():
	k = 0
	data = pd.read_csv('./app/static/new_isis_tweets.csv')
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

	return render_template('home.html', cols=data_cols, rows=data_rows, lang=lang_data)
