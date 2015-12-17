import datetime
import time
import urllib2
import json


CACHE_FILE = "cache2.html"
URL_LONG_IDEAS = "http://seekingalpha.com/analysis/investing-ideas/long-ideas/%s"

class Cache(object):
	"""
	Handles retrieval and update of the Seeking Alpha lists
	"""

	def __init__(self):
		pass
		
	def update(self):
		f = open(CACHE_FILE, 'w')

		url = URL_LONG_IDEAS % now
		user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
		headers = { 'User-Agent' : user_agent }

		req = urllib2.Request(url, headers=headers)

		now = datetime.datetime.now()
		now = time.mktime(now.timetuple())
		now = "%0.d" % now

		for x in range(0,1000):

			print "Capturing Date: %s" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(now)))
			
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

		f.close()

	def get(self):
		f = open(CACHE_FILE, 'r')
		return f.read()
