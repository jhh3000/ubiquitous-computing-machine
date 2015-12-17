from cache import Cache

from bs4 import BeautifulSoup
import parsedatetime
import dateutil.parser

from datetime import datetime
from time import mktime
import json
import pickle

cache = Cache()
html_doc = cache.get()

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
		pub_date = datetime.fromtimestamp(mktime(time_struct))
	else:
		pub_date = dateutil.parser.parse(pub_date)

	print "%s: %s - %s" % (article_id, ticker, pub_date)
	data[article_id] = (ticker, pub_date)

obj = pickle.dumps(data)

f = open("data.txt", 'w')
f.write(obj)
f.close()