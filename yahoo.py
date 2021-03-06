from yahoo_finance import Share, YQLQueryError
from operator import itemgetter

def moving_avg(ticker, start, end, duration = 50):
    ticker = Share(ticker)

    while True:
        try:
            historical = sorted(ticker.get_historical(start, end), key=itemgetter("Date"))
        except ValueError as e:
            raise e
        except YQLQueryError as e:
            continue
        break

    moving_sum = []
    holding = None
    gainloss = 0
    initial_price = None
    if len(historical) == 0:
        return None

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

def buy_and_hold(ticker, start, end):
    ticker = Share(ticker)

    while True:
        try:
            historical = sorted(ticker.get_historical(start, end), key=itemgetter("Date"))
        except ValueError as e:
            raise e
        except YQLQueryError as e:
            continue
        break

    if len(historical) <= 1:
        return None

    initial_price = float(min(historical, key=itemgetter("Date"))['Adj_Close'])
    final_price = float(max(historical, key=itemgetter("Date"))['Adj_Close'])

    out = (final_price - initial_price) / initial_price
    return out

def trailing_stop(ticker, start, end, percentage = 0.15):
    ticker = Share(ticker)

    while True:
        try:
            historical = sorted(ticker.get_historical(start, end), key=itemgetter("Date"))
        except ValueError as e:
            raise e
        except YQLQueryError as e:
            continue
        break

    if len(historical) <= 1:
        return None

    initial_price = float(historical[0]['Adj_Close'])
    curr_price = initial_price
    stop_price = initial_price*(1-percentage)
    historical = historical[1:]

    while len(historical) > 0 and stop_price < curr_price:
        curr_price = float(historical[0]['Adj_Close'])
        if curr_price > stop_price/(1-percentage): stop_price = curr_price*(1-percentage)
        historical = historical[1:]

    out = (curr_price - initial_price) / initial_price
    return out
