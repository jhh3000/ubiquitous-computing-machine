from yahoo_finance import Share
from operator import itemgetter

def moving_avg(ticker = "HD", start = "2006-10-01", end = "2015-10-01", duration = 50):
    ticker = Share(ticker)

    try:
        historical = sorted(ticker.get_historical(start, end), key=itemgetter("Date"))
    except ValueError as e:
        raise e

    moving_sum = []
    holding = None
    gainloss = 0
    initial_price = None
    if len(historical) == 0:
        return -1

    del historical[-1]
    
    for i, day in enumerate(historical):
        closing_price = float(day['Adj_Close'])

        moving_sum += [closing_price]
        if len(moving_sum) > duration:
            del moving_sum[0]
        if i+1 > duration:
            moving_avg = sum(moving_sum) / float(duration)
            if not holding and closing_price > moving_avg:
                holding = closing_price
                if not initial_price: initial_price = closing_price
            if holding and closing_price < moving_avg:
                gainloss += closing_price - holding
                holding = None
            #print str(i) + " " + day['Date'] + " " + day['Adj_Close'] + " " + str(moving_avg)

    out = gainloss / initial_price if initial_price else 0
    return out

def buy_and_hold(ticker = "HD", start = "2006-10-01", end = "2015-10-01"):
    ticker = Share(ticker)

    try:
        historical = sorted(ticker.get_historical(start, end), key=itemgetter("Date"))
    except ValueError as e:
        raise e

    if len(historical) <= 1:
        return -1

    initial_price = float(min(historical, key=itemgetter("Date"))['Adj_Close'])
    final_price = float(max(historical, key=itemgetter("Date"))['Adj_Close'])

    out = (final_price - initial_price) / initial_price
    return out
