import random
import time
import datetime


def randomDate(start, end):
	stime = time.mktime(start.timetuple())
	etime = time.mktime(end.timetuple())

	ptime = stime + random.random() * (etime - stime)

	return datetime.datetime.fromtimestamp(ptime)
