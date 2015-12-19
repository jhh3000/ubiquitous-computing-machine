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
URL_SHORT_IDEAS = "http://seekingalpha.com/analysis/investing-ideas/short-ideas/%s"
DATE_FORMAT = "%Y-%m-%d"


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

def _parse(raw, data={}):
	html_doc = raw['html']
	now = raw['last_ts']
	soup = BeautifulSoup(html_doc, 'html.parser')

	articles = soup.find_all('li')

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
			pub_date = datetime.datetime.fromtimestamp(mktime(time_struct)).date()
		else:
			pub_date = dateutil.parser.parse(pub_date).date()

		print "%s: %s - %s" % (article_id, ticker, pub_date)
		if pub_date not in data:
			data[pub_date] = [ticker]
		elif ticker not in data[pub_date]:
			data[pub_date] += [ticker]

	return now, data

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
	
def pull(date = None):
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }

	if date:
		now = date
	else:
		now = datetime.datetime.now()

	start = now.date()

	now += datetime.timedelta(days=1)
	now = time.mktime(now.timetuple())

	data = {}

	while len(data) <= 2:
		
		url = URL_LONG_IDEAS % "%0.d" % now
	
		req = urllib2.Request(url, headers=headers)
		response = urllib2.urlopen(req)
		the_page = response.read()

		raw = json.loads(the_page)
		now, data = _parse(raw, data)

	return data[start]

def get(date):
	return pull(date)
	#return _read()
