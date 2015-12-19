import seeking_alpha
from yahoo import moving_avg, buy_and_hold, trailing_stop
from utils import randomDate

import dateutil.parser
import dateutil.relativedelta
import datetime


DATE_FORMAT = "%b. %d, %Y"
YAHOO_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_METHOD = buy_and_hold
INDEX_ETFS = ('SPY', 'DIA', 'QQQ')
SIGNAL_DAYS = 3
ITERATIONS = 25


print "Welcome to the Ubiquitous Computing Machine (UCM), an automated decision system for stock picking."
print ""
print "This automated decision system recommends stocks to invest in on a given date based on only one signal:"
print "1) The stock has to appear on that date on the 'Investing Ideas - Long Ideas' list on seekingalpha.com"
print "2) The stock has to have appeared within %s days on the same list" % SIGNAL_DAYS
print ""
print "Then, the UCM will invest your money based on a number of methods:"
print "1) 50 day moving average (same as hw2)"
print "2) Buy and hold for the entire year"
print "3) Trailing stop (15%)"
print ""
print "Please enter the method you'd like to use:"
print "1) for 50-Day Moving Average"
print "2) for buy-and-hold"
print "3) for trailing stop of 15%"
method = raw_input("Method: ")
if method == "1":
	method = moving_avg
elif method == "2":
	method = buy_and_hold
elif method == "3":
	method = trailing_stop
else:
	method = DEFAULT_METHOD

print ""
print "Please enter 'backtest' if you'd like to see how the stocks that UCM picks"
print "performs over the course of the next year. If you select this option, UCM"
print "will randomly select %s dates between 1 year ago and 2 years ago to invest," % ITERATIONS
print "and then backtest those stocks for the next year to see what the actual performance"
print "would have been for your chosen method. Leave this blank to see yesterday's recommendations."
backtest = raw_input("Backtest: ")

if not backtest:
	date = datetime.datetime.now() - datetime.timedelta(days=1)

	print ""
	print "You chose to see yesterday's recommendations, date: %s" % date.strftime(DATE_FORMAT)
	print ""
	print "Searching for investing ideas on Seeking Alpha..."

	stocks = seeking_alpha.get(date, SIGNAL_DAYS)

	print ""
	print "The UCM identified %s stocks to invest in today." % len(stocks)
	print "\n".join(stocks)

	exit()

else:
	print ""
	print "You have chosen to backtest stocks that UCM picks. We'll compare the average return of each"
	print "portfolio and subtract from that the average return of the index to identify how much you beat"
	print "the market by with the given method and signal over the course of a year"
	print ""
	print "++++++++++++++++++++++++++++++%s++++++++++++++++++++++++++++++" % method.__name__

	backtest_avg = []
	for n in range(0, ITERATIONS):
		print ""
		print "++++++++++++++++++++++++++++++ITERATION %s++++++++++++++++++++++++++++++" % n

		now = datetime.datetime.now()
		start = now - datetime.timedelta(days=1) - dateutil.relativedelta.relativedelta(years=2)
		end = now - datetime.timedelta(days=1) - dateutil.relativedelta.relativedelta(years=1)
		date = randomDate(start, end)

		print "Selecting Stocks from Date: %s" % date.strftime(DATE_FORMAT)
		print "Searching for investing ideas on Seeking Alpha..."

		stocks = seeking_alpha.get(date, SIGNAL_DAYS)
		
		print "The UCM identified %s stocks to backtest." % len(stocks)
		print "\n".join(stocks)

		if len(stocks) == 0: continue

		start_date = date - dateutil.relativedelta.relativedelta(years=1)
		end_date = date
		start = start_date.strftime(YAHOO_DATE_FORMAT)
		end = end_date.strftime(YAHOO_DATE_FORMAT)

		print "Performing index benchmark between %s and %s..." % (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

		benchmark_avg = []
		for ticker in INDEX_ETFS:
			result = method(ticker=ticker, start=start, end=end)
			print "INDEX %s: %s return" % (ticker, result)
			if result: benchmark_avg += [result]
		benchmark_avg = sum(benchmark_avg) / len(benchmark_avg)

		print "The benchmark to beat is: %s" % benchmark_avg
		print "Performing portflio backtest between %s and %s..." % (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

		actual_avg = []
		for ticker in stocks:
			result = method(ticker=ticker, start=start, end=end)
			if result > benchmark_avg:
				print "BEAT Ticker %s: %s return" % (ticker, result)
			elif result:
				print "MISSED Ticker %s: %s return" % (ticker, result)
			else:
				print "ERROR Ticker %s, NOT ENOUGH DATA TO BACKTEST" % ticker
			if result: actual_avg += [result]
		actual_avg = sum(actual_avg) / len(actual_avg)

		diff = actual_avg - benchmark_avg

		print "Final Average Diff to Index: %s" % diff

		backtest_avg += [diff]

	print ""
	print "++++++++++++++++++++++++++++++COMPLETE++++++++++++++++++++++++++++++"
	
	backtest_avg = sum(backtest_avg) / len(backtest_avg)

	print ""
	print "Final Backtest Average: %s" % backtest_avg
