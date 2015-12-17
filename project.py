from cache import update
from yahoo import backtest


#update()

data = get()

print backtest(data[max(data)][0])