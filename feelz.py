import os, sys, random, time, json
import pandas as pd
import pickle as pickle 
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from textblob import TextBlob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from flask import Flask, render_template, request, redirect, Response, jsonify

import logging
logging.getLogger().setLevel(logging.INFO)
def logit(logmsg):
	logging.info(logmsg) 
logit('initializing') 

pd.set_option('display.max_colwidth', -1)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu') 
options.add_argument('--disable-extensions')
options.add_argument('--no-sandbox')
browser = webdriver.Chrome('./chromedriver', chrome_options=options)

app = Flask(__name__)

@app.route('/')
def output():
	return render_template('index.html', name='Twitter Feelz')

@app.route('/appdata', methods = ['POST'])
def appdata():
	data = []
	data = request.get_json()
	sentiTweet(data)	
	return('sentiment')

def sentiTweet(data):
	tweets = []
	tweets = getUsers(data)
	lines = []
	lines = createList(tweets)
	data = []
	data = getPickl(lines)
	sentiment = []
	sentiment = getSent(data)
	return 'okok'

def getUsers(data):
	base_url = u'https://twitter.com/search?q='
	user1 = data['user1']
	user2 = data['user2']
	tweets = []
	global name1 
	name1 = '@' + user1.lstrip('@')
	url = base_url + name1
	# browser = webdriver.Chrome()
	browser.get(url)
	n = 1 
	tweets = browser.find_elements_by_class_name('TweetTextSize')
	with open('newtw'+ str(n) +'.txt', 'w') as file:
		for tweet in tweets:
			file.write("%s\n" % tweet.text)
			#pickle.dump(tweet.text, file)
	# why return?
	return tweets

# createList doesn't require an argument
def createList(tweets):
	# create comma deliniated list of tweets from file
	# coding isn't hard, so don't hardcode! 
	lines = []
	lines = open('newtw1.txt').read().splitlines()
	os.remove('newtw1.txt')
	print(len(lines))
	return lines 

def getPickl(lines):
	# df1 = pd.read_pickle()
	data = []
	data= pd.DataFrame({'lines': lines})
	for d in data:
		logit(d)
	return data

def getSent(data):
	pol = lambda x: TextBlob(x).sentiment.polarity
	sub = lambda x: TextBlob(x).sentiment.subjectivity
	logit('lets apply') 
	data['polarity'] = data['lines'].apply(pol)
	data['subjectivity'] = data['lines'].apply(sub)
	data = data[data.polarity != 0]
	data = data.reset_index(drop=True)
	user_polarity = str(data['polarity'].mean())
	user_subjective = str(data['subjectivity'].mean())
	logit('polarity is ' + user_polarity)
	logit('subjectivity is ' + user_subjective)
	plt.rcParams['figure.figsize'] = [10, 8]
	for index, tweet in enumerate(data.index):
	    logit(data['lines'][index])
	    y = data.polarity.loc[tweet]
	    x = data.subjectivity.loc[tweet]
	    plt.scatter(x, y, color='blue')
	    plt.text(x+.001, y+.001, data['lines'][index], fontsize=10)
	    plt.xlim(-.01, 2.0) 
	plt.title('Tweet Sentiment Analysis', fontsize=20)
	plt.ylabel('<-- Negative --- ATTITUDE ---- Positive -->', fontsize=15)
	plt.xlabel('<-- Facts --- BIAS ---- Opinions -->', fontsize=15)
	name = name1.lstrip('@') 
	logit(name)
	plt.savefig('static/' + name + '.png')
	plt.clf()
	logit("DONE")

# @TODO check local hostname to run on localhost
if __name__ == '__main__':
	# sys output not working? 
	sys.stdout = open('file.log', 'w')
	app.run(host='0.0.0.0')

sys.exit()
