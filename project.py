import datetime
import time
import urllib2
import json
from bs4 import BeautifulSoup

f = open("cache.html", 'w')

now = datetime.datetime.now()
now = time.mktime(now.timetuple())
now = "%0.d" % now

for x in range(0,1000):

	print "Capturing Date: %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(now)))

	url = 'http://seekingalpha.com/analysis/investing-ideas/long-ideas/%s' % now
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }

	req = urllib2.Request(url, headers=headers)
	response = urllib2.urlopen(req)
	the_page = response.read()

	data = json.loads(the_page)

	now = data['last_ts']
	html_doc = data['html']
	try:
		f.write(html_doc)
	except UnicodeEncodeError:
		pass
	f.flush()

#soup = BeautifulSoup(html_doc, 'html.parser')

f.close()