from yahoo_finance import Share
from operator import itemgetter

def backtest(ticker = "HD", start = "2006-10-01", end = "2015-10-01", duration = 50):
    ticker = Share(ticker)

    try:
        historical = sorted(ticker.get_historical(start, end), key=itemgetter("Date"))
    except ValueError as e:
        raise e

    moving_sum = []
    holding = None
    gainloss = 0
    initial_price = None
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

def indextest(startdates, enddates, durations, file):
    index_etfs = ['SPY', 'DIA', 'QQQ']
    data = []
    best = None
    worst = None
    avg_duration = None
    avg_period = None

    for i, start in enumerate(startdates):
        end = enddates[i]
        for duration in durations:
            for ticker in index_etfs:
                try:
                    data += [(ticker, start, end, duration, backtest(ticker, start, end, duration))]
                except ValueError:
                    pass
    
    for (ticker, start, end, duration, result) in data:
        if not best or best[4] < result:
            best = (ticker, start, end, duration, result)
        if not worst or worst[4] > result:
            worst = (ticker, start, end, duration, result)

    for duration1 in durations:
        a_sum = 0
        a_len = 0
        for (ticker, start, end, duration2, result) in data:
            if duration1 == duration2:
                a_sum += result
                a_len += 1
        if not avg_duration or (a_len <> 0 and avg_duration[4] < (a_sum / a_len)):
            avg_duration = (ticker, start, end, duration, (a_sum / a_len))

    for i, start1 in enumerate(startdates):
        end1 = enddates[i]
        a_sum = 0
        a_len = 0
        for (ticker, start2, end2, duration, result) in data:
            if (start1, end1) == (start2, end2):
                a_sum += result
                a_len += 1
        if not avg_period or (a_len <> 0 and avg_period[4] < (a_sum / a_len)):
            avg_period = (ticker, start, end, duration, (a_sum / a_len))

    with open(file, 'w') as f:
        f.write("best %s %s %s %s %s\n" % tuple(best))
        f.write("worst %s %s %s %s %s\n" % tuple(worst))
        f.write("avg-period %s %s %s\n" % (avg_period[1], avg_period[2], avg_period[4]))
        f.write("avg-duration %s %s" % (avg_duration[3], avg_duration[4]))
