import datetime
import time
import urllib2
import json
import pickle
import parsedatetime
import dateutil.parser
from time import mktime
from bs4 import BeautifulSoup


CACHE_FILE = "data.json"
URL_LONG_IDEAS = "http://seekingalpha.com/analysis/investing-ideas/long-ideas/%s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _json_load(obj):
	try:
		data = json.loads(obj)
	except (EOFError, ValueError):
		data = {}
	for key in data:
		data[key] = (data[key][0], datetime.datetime.strptime(data[key][1], DATE_FORMAT))
	return data

def _json_dump(data):
	for key in data:
		data[key] = (data[key][0], data[key][1].strftime(DATE_FORMAT))
	return json.dumps(data, sort_keys=True, indent=2, separators=(',', ': '))

def _parse(html_doc):
	soup = BeautifulSoup(html_doc, 'html.parser')

	articles = soup.find_all('li')

	data = {}

	for article in articles:
		article_id = article['article_id']
		
		ticker = None
		for d in article.find_all('span'):
			if d.a:
				ticker = d.a.text
		if not ticker: continue

		pub_date = None
		for d in article.div.div.contents:
			if '\n\n        ' in d:
				pub_date = d
		if not pub_date: continue

		if 'Today' in pub_date or 'Yesterday' in pub_date:
			cal = parsedatetime.Calendar()
			time_struct, parse_status = cal.parse(pub_date)
			pub_date = datetime.datetime.fromtimestamp(mktime(time_struct))
		else:
			pub_date = dateutil.parser.parse(pub_date)

		print "%s: %s - %s" % (article_id, ticker, pub_date)
		data[article_id] = (ticker, pub_date)

	return data

def _write(data):
	orig_data = _read()
	if not orig_data: orig_data = {}
	orig_data.update(data)
	f = open(CACHE_FILE, 'w')
	f.write(_json_dump(orig_data))
	f.close()

def _read():
	try:
		f = open(CACHE_FILE, 'r')
	except IOError:
		return {}
	data = _json_load(f.read())
	f.close()
	return data
	
def update():
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }

	data = _read()
	if data:
		now = None
		for key in data:
			if not now: now = data[key][1]
			if data[key][1] < now: now = data[key][1]
	else:
		now = datetime.datetime.now()
	now = time.mktime(now.timetuple())
	now = "%0.d" % now

	while True:

		print "Capturing Date: %s" % time.strftime(DATE_FORMAT, time.localtime(float(now)))
		
		url = URL_LONG_IDEAS % now
	
		req = urllib2.Request(url, headers=headers)
		response = urllib2.urlopen(req)
		the_page = response.read()

		data = json.loads(the_page)

		now = data['last_ts']
		html_doc = data['html']
		data = _parse(html_doc)
		_write(data)

def get():
	return _read()
