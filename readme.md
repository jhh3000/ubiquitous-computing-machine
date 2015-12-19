
#This automated decision system recommends stocks to invest in on a given date based on only one signal:
1. The stock has to appear on that date on the 'Investing Ideas - Long Ideas' list on seekingalpha.com
2. The stock has to have appeared within 3 days on the same list

#The signal above is conisidered the "buy" signal, and must be generated on today's date. For the sell signal, there are three strategies that the automated decision system will use to invest your money over the course of a year. These strategies provide the exit points (or in the case of the first strategy, the exit and re-entry points):
1. *50 day moving average*: If the stock price passes above its 50 day moving average price, then buy. If the stock price passes below its 50 day moving average price, then sell.
2. *Buy and hold for the entire year*: Really simple; buy on the signal day, sell one year later.
3. *Trailing stop (15%)*: Make the trailing stop price 15% below its current price. If the stock hits the trailing stop price, sell. If the stock price goes up and hits a new ceiling, then make the new trailing stop price 15% below the new ceiling price.

To calculate the efficacy of this decision system, 25 dates from the window between 1 and 2 years ago are tested against the backtest methods given above, in a similar fashion to the homework 2. The results are below, and the raw output is copied to the text files. The result of each iteration (shown in the text file) is an average of the returns of the chosen method that is above the average of the three index fund returns. The results reported below are the average of the 25 iterations diff to index returns.

Index Funds: SPY, DIA, QQQ

Method 1 (method1.txt): 0.033972759227
Method 2 (method2.txt): 0.179523344279
Method 3 (method3.txt): 0.046819576784

In conclusion, the signal does seem to generally outperform the market, but the best method of holding the stock is simply to hold it for an entire year.
