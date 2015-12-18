import seeking_alpha
from yahoo import backtest

import dateutil.parser

#update()

print "Welcome to the Ubiquitous Computing Machine."
print "Please enter a date you'd like to test stocks from,"
print "or leave it blank for today."
date = raw_input("Date: ")

date = dateutil.parser.parse(date)

print "You chose to test stocks from: %s" % date.strftime("%b. %d, %Y")

stocks = seeking_alpha.get_stocks(date)