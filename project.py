import seeking_alpha
from yahoo import moving_avg, buy_and_hold
from utils import randomDate

import dateutil.parser
import dateutil.relativedelta
import datetime

DATE_FORMAT = "%b. %d, %Y"
YAHOO_DATE_FORMAT = "%Y-%m-%d"
INDEX_ETFS = ('SPY', 'DIA', 'QQQ')

print "Welcome to the Ubiquitous Computing Machine (UCM)."
print ""
print "This platform will decide which stocks you will invest in today."
print ""
print "The criteria is as follows:"
print "- You must hold the stock for one year, using either the 50-day MA or buy-and-hold method"
print "- The UCM determines stocks you invest in by checking for ideas on seekingalpha.com"
print "- The UCM then performs a backtest to get the historical 1-yr return with the chosen method"
print "- The UCM then compares that to the backtest of 3 index ETFs for the S&P, Dow, and Nasdaq"
print "- A stock is a recommended buy if it beats all three indexes"

print ""
print "Please enter the method you'd like to use:"
print "1) for 50-Day Moving Average"
print "2) for buy-and-hold"
method = raw_input("Method: ")
if method == "1":
	method = moving_avg
elif method == "2":
	method = buy_and_hold
else:
	print "You must select either 1 or 2"
	exit()

print ""
print "Please enter 'validate' if you'd like to see how the stocks that UCM picks"
print "performs over the course of the next year. If you select this option, UCM"
print "will randomly select 10 dates between 1 year ago and 2 years ago to run the prediction"
print "alorithm on, and then backtest it for the next year to see what the actual performance"
print "would have been."
validate = raw_input("Validate: ")

if not validate:
	print ""
	print "Please enter a date you'd like to test stocks from,"
	print "or leave it blank for yesterday."
	print ""
	date = raw_input("Date: ")

	date = dateutil.parser.parse(date) if date else datetime.datetime.now() - datetime.timedelta(days=1)
	if date >= datetime.datetime.now() - datetime.timedelta(days=1):
		print "You have to choose a date yesterday or before."
		exit()

	print ""
	print "You chose to test stocks from: %s" % date.strftime(DATE_FORMAT)
	print ""
	print "Searching for investing ideas on Seeking Alpha..."

	stocks = seeking_alpha.get(date)
	start_date = date - dateutil.relativedelta.relativedelta(years=1)
	end_date = date
	start = start_date.strftime(YAHOO_DATE_FORMAT)
	end = end_date.strftime(YAHOO_DATE_FORMAT)

	print ""
	print "The UCM identified %s stocks to backtest." % len(stocks)
	print ""
	print "Benchmarking the index funds' performance now..."

	max_return = -1
	for ticker in INDEX_ETFS:
		result = method(ticker=ticker, start=start, end=end)
		print "INDEX %s: %s return" % (ticker, result)
		if max_return < result: max_return = result

	print ""
	print "The benchmark to beat is: %s" % max_return

	print ""
	print "Performing backtest between %s and %s..." % (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

	selected = []
	for ticker in stocks:
		result = method(ticker=ticker, start=start, end=end)
		if result > max_return:
			print "SELECTED Ticker %s: %s return" % (ticker, result)
			selected += [ticker]
		else:
			print "Ticker %s: %s return" % (ticker, result)

	print ""
	print "The UCM selected %s stocks:" % len(selected)
	print "\n".join(selected)

	exit()

else:
	print ""
	print "You have chosen to validate stocks that UCM picks. The scoring system will be as follows:"
	print "- +1 point for every index that the stock outperforms"
	print ""
	print "++++++++++++++++++++++++++++++%s++++++++++++++++++++++++++++++" % method.__name__

	total_score = 0
	possible_score = 0
	for n in range(0, 10):
		print ""
		print "++++++++++++++++++++++++++++++ITERATION %s++++++++++++++++++++++++++++++" % n

		now = datetime.datetime.now()
		start = now - datetime.timedelta(days=1) - dateutil.relativedelta.relativedelta(years=2)
		end = now - datetime.timedelta(days=1) - dateutil.relativedelta.relativedelta(years=1)
		date = randomDate(start, end)

		print "Selecting Stocks from Date: %s" % date.strftime(DATE_FORMAT)
		print "Searching for investing ideas on Seeking Alpha..."

		stocks = seeking_alpha.get(date)
		start_date = date - dateutil.relativedelta.relativedelta(years=1)
		end_date = date
		start = start_date.strftime(YAHOO_DATE_FORMAT)
		end = end_date.strftime(YAHOO_DATE_FORMAT)

		print "The UCM identified %s stocks to backtest." % len(stocks)
		print "Performing index backtest benchmark between %s and %s..." % (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

		max_return = -1
		for ticker in INDEX_ETFS:
			result = method(ticker=ticker, start=start, end=end)
			print "INDEX %s: %s return" % (ticker, result)
			if max_return < result: max_return = result

		print "The benchmark to beat is: %s" % max_return
		print "Performing backtest between %s and %s..." % (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

		selected = []
		for ticker in stocks:
			result = method(ticker=ticker, start=start, end=end)
			if result > max_return:
				print "SELECTED Ticker %s: %s return" % (ticker, result)
				selected += [ticker]
			else:
				print "Ticker %s: %s return" % (ticker, result)

		print "The UCM selected %s stocks:" % len(selected)
		print "\n".join(selected)

		date = date + dateutil.relativedelta.relativedelta(years=1)
		start_date = date - dateutil.relativedelta.relativedelta(years=1)
		end_date = date
		start = start_date.strftime(YAHOO_DATE_FORMAT)
		end = end_date.strftime(YAHOO_DATE_FORMAT)

		print "Performing validation index backtest benchmark between %s and %s..." % (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

		max_return = {}
		for ticker in INDEX_ETFS:
			result = method(ticker=ticker, start=start, end=end)
			print "INDEX %s: %s return" % (ticker, result)
			max_return[ticker] = result

		print "The benchmarks to beat are: %s" % max_return
		print "Performing validation backtest between %s and %s..." % (start_date.strftime(DATE_FORMAT), end_date.strftime(DATE_FORMAT))

		score = 0
		possible = 0
		for ticker in selected:
			result = method(ticker=ticker, start=start, end=end)
			for index in max_return:
				possible += 1
				if result > max_return[index]:
					print "BEAT %s Ticker %s: %s return" % (index, ticker, result)
					score += 1
				else:
					print "MISSED %s Ticker %s: %s return" % (index, ticker, result)

		print "Final Score: %s / %s" % (score, possible)

		total_score += score
		possible_score += possible

	print ""
	print "++++++++++++++++++++++++++++++COMPLETE++++++++++++++++++++++++++++++"
	print ""
	print "Final Validation Score: %s / %s" % (total_score, possible_score)
